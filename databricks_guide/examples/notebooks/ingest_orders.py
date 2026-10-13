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
from pyspark.sql import functions as F
source_path = f"/Volumes/{catalog}/ops/landing/orders"
schema_path = f"/Volumes/{catalog}/ops/state/orders_schema_v1"
checkpoint_path = f"/Volumes/{catalog}/ops/state/orders_bronze_v1"
target_table = f"{catalog}.bronze.order_events"
raw_schema = "event_id STRING, order_id STRING, sequence STRING, op STRING, event_time STRING, amount STRING, region STRING"
raw = (spark.readStream.format("cloudFiles")
       .option("cloudFiles.format", "json")
       .option("cloudFiles.schemaLocation", schema_path)
       .option("cloudFiles.schemaEvolutionMode", "rescue")
       .option("rescuedDataColumn", "_rescued_data")
       .option("cloudFiles.maxFilesPerTrigger", "100")
       .schema(raw_schema).load(source_path)
       .select("*", F.col("_metadata.file_path").alias("source_file")))
query = (raw.writeStream.option("checkpointLocation", checkpoint_path)
         .trigger(availableNow=True).toTable(target_table))
query.awaitTermination()
# Total bronze rows, not new rows in this run. Task values must be small JSON.
dbutils.jobs.taskValues.set(key="bronze_rows", value=spark.table(target_table).count())
