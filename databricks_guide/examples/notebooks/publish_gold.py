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
current = spark.table(f"{catalog}.silver.orders_current")
gold = current.groupBy("order_date", "region").agg(
    F.count("order_id").alias("order_count"), F.sum("amount").alias("revenue"))
# Small lab: complete deterministic rebuild, including removal of empty old groups.
gold.write.format("delta").mode("overwrite").saveAsTable(f"{catalog}.gold.daily_revenue")
dbutils.jobs.taskValues.set(key="gold_groups", value=gold.count())
