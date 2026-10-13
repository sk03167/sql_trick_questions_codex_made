# Databricks notebook source
# Lab entry point: all widget values are strings. Use an isolated UC catalog.
import re
from datetime import date
dbutils.widgets.text("catalog", "de_lab_dev")
dbutils.widgets.text("run_date", "2026-10-12")
catalog = dbutils.widgets.get("catalog")
if not re.fullmatch(r"de_lab_[a-z][a-z0-9_]*", catalog):
    raise ValueError("Use an approved de_lab_ catalog")
run_date = date.fromisoformat(dbutils.widgets.get("run_date")).isoformat()

# COMMAND ----------
from pyspark.sql import functions as F, Window
from delta.tables import DeltaTable
spark.conf.set("spark.sql.session.timeZone", "UTC")
raw = spark.table(f"{catalog}.bronze.order_events")
shape = (F.col("sequence").rlike(r"^[0-9]+$")
         & F.col("event_time").rlike(r"(Z|[+-][0-9]{2}:[0-9]{2})$")
         & ((F.col("op") == "D") | F.col("amount").rlike(r"^[0-9]{1,16}(\.[0-9]{1,2})?$")))
parsed = (raw.withColumn("_shape_valid", shape)
          .withColumn("sequence", F.expr("try_cast(sequence AS BIGINT)"))
          .withColumn("event_time", F.expr("try_to_timestamp(event_time)"))
          .withColumn("amount", F.expr("try_cast(amount AS DECIMAL(18,2))")))
valid = (F.col("_shape_valid") & F.col("event_id").isNotNull() & (F.length("event_id") > 0)
         & F.col("order_id").isNotNull() & (F.length("order_id") > 0)
         & F.col("sequence").isNotNull() & (F.col("sequence") >= 0)
         & F.col("op").isin("I", "U", "D") & F.col("event_time").isNotNull()
         & F.col("_rescued_data").isNull()
         & ((F.col("op") == "D") | (F.col("amount").isNotNull()
             & (F.col("amount") >= 0) & F.col("region").isNotNull()
             & (F.length("region") > 0))))
# Null predicates are invalid too. Quarantine is written before failing publication.
invalid = parsed.filter(~F.coalesce(valid, F.lit(False)))
invalid.write.format("delta").mode("overwrite").saveAsTable(f"{catalog}.silver.orders_quarantine")
if invalid.limit(1).count():
    raise ValueError("Invalid source events quarantined; repair before publication")
fields = ["event_id", "order_id", "sequence", "op", "event_time", "amount", "region"]
good = parsed.select(*fields)
# Normalize unused delete payloads so ordering/conflict semantics are consistent.
good = (good.withColumn("amount", F.when(F.col("op") == "D", F.lit(None).cast("decimal(18,2)")).otherwise(F.col("amount")))
        .withColumn("region", F.when(F.col("op") == "D", F.lit(None).cast("string")).otherwise(F.col("region"))))
payload = F.to_json(F.struct(*[F.col(c) for c in fields if c != "event_id"]))
good = good.withColumn("_payload", payload)
identity_conflict = good.groupBy("event_id").agg(F.countDistinct("_payload").alias("n")).filter("n > 1")
sequence_conflict = good.groupBy("order_id", "sequence").agg(F.countDistinct("_payload").alias("n")).filter("n > 1")
if identity_conflict.limit(1).count() or sequence_conflict.limit(1).count():
    raise ValueError("Conflicting event identity or per-order sequence")
# Educational full-bronze replay. Do not scale this unbounded scan blindly.
window = Window.partitionBy("order_id").orderBy(F.col("sequence").desc(), F.col("event_id").desc())
latest = (good.withColumn("rn", F.row_number().over(window)).filter("rn = 1")
          .drop("rn", "_payload").withColumn("is_deleted", F.col("op") == "D")
          .withColumn("order_date", F.to_date("event_time")))
target = f"{catalog}.silver.orders_state"
if not spark.catalog.tableExists(target):
    latest.limit(0).write.format("delta").saveAsTable(target)
assignments = {c: f"s.{c}" for c in latest.columns}
(DeltaTable.forName(spark, target).alias("t")
 .merge(latest.alias("s"), "t.order_id = s.order_id")
 .whenMatchedUpdate(condition="s.sequence > t.sequence", set=assignments)
 .whenNotMatchedInsert(values=assignments).execute())
# catalog was validated above; identifiers are constructed only from this contract.
spark.sql(f"""CREATE OR REPLACE VIEW {catalog}.silver.orders_current AS
SELECT event_id, order_id, sequence, event_time, order_date, amount, region
FROM {catalog}.silver.orders_state WHERE NOT is_deleted""")
dbutils.jobs.taskValues.set(key="current_rows", value=spark.table(f"{catalog}.silver.orders_current").count())
