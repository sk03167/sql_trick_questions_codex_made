# Run only as a Lakeflow Spark Declarative Pipeline, not as a regular notebook.
from pyspark import pipelines as dp
from pyspark.sql import functions as F
RAW_SCHEMA = "event_id STRING, order_id STRING, sequence STRING, op STRING, event_time STRING, amount STRING, region STRING"
VALID = """_shape_valid AND event_id IS NOT NULL AND length(event_id) > 0
AND order_id IS NOT NULL AND length(order_id) > 0
AND sequence IS NOT NULL AND sequence >= 0
AND op IN ('I','U','D') AND event_time IS NOT NULL
AND _rescued_data IS NULL
AND (op = 'D' OR (amount IS NOT NULL AND amount >= 0 AND region IS NOT NULL AND length(region) > 0))"""
@dp.table(name="order_events_pipeline")
def raw_events():
    return (spark.readStream.format("cloudFiles").schema(RAW_SCHEMA)
            .option("cloudFiles.format", "json")
            .option("cloudFiles.schemaLocation", spark.conf.get("lab.schema_path"))
            .option("cloudFiles.schemaEvolutionMode", "rescue")
            .option("rescuedDataColumn", "_rescued_data")
            .load(spark.conf.get("lab.source_path")))
@dp.temporary_view(name="parsed_order_events")
def parsed_events():
    raw = spark.readStream.table("order_events_pipeline")
    shape = (F.col("sequence").rlike(r"^[0-9]+$")
             & F.col("event_time").rlike(r"(Z|[+-][0-9]{2}:[0-9]{2})$")
             & ((F.col("op") == "D") | F.col("amount").rlike(r"^[0-9]{1,16}(\.[0-9]{1,2})?$")))
    return (raw.withColumn("_shape_valid", shape)
            .withColumn("sequence", F.expr("try_cast(sequence AS BIGINT)"))
            .withColumn("event_time", F.expr("try_to_timestamp(event_time)"))
            .withColumn("amount", F.expr("try_cast(amount AS DECIMAL(18,2))")))
@dp.table(name="valid_order_events")
@dp.expect_or_drop("valid_contract", VALID)
def valid_events():
    return spark.readStream.table("parsed_order_events")
@dp.table(name="invalid_order_events")
def invalid_events():
    return spark.readStream.table("parsed_order_events").filter("NOT coalesce((" + VALID + "), false)")
dp.create_streaming_table("orders_current_pipeline")
dp.create_auto_cdc_flow(
    target="orders_current_pipeline", source="valid_order_events", keys=["order_id"],
    sequence_by="sequence", apply_as_deletes="op = 'D'",
    except_column_list=["op", "event_id", "_rescued_data", "_shape_valid"], stored_as_scd_type=1,
)
@dp.materialized_view(name="daily_revenue_pipeline")
def revenue():
    return (spark.read.table("orders_current_pipeline")
            .withColumn("order_date", F.to_date("event_time"))
            .groupBy("order_date", "region")
            .agg(F.count("order_id").alias("order_count"), F.sum("amount").alias("revenue")))
# AUTO CDC ordering relies on a valid unique source sequence contract.
# Add a source conflict gate before production; this illustrative pipeline
# quarantines/drops invalid rows while the Jobs lab fails publication for them.
