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
from decimal import Decimal
from pyspark.sql import functions as F
dbutils.widgets.text("min_current_rows", "2")
dbutils.widgets.text("validate_fixture", "true")
minimum = int(dbutils.widgets.get("min_current_rows"))
if minimum < 0:
    raise ValueError("min_current_rows must be nonnegative")
flag = dbutils.widgets.get("validate_fixture").lower()
if flag not in {"true", "false"}:
    raise ValueError("validate_fixture must be true or false")
current = spark.table(f"{catalog}.silver.orders_current")
gold = spark.table(f"{catalog}.gold.daily_revenue")
assert current.count() >= minimum, "Minimum row guardrail failed"
assert not current.groupBy("order_id").count().filter("count > 1").limit(1).count(), "Duplicate current key"
expected = current.groupBy("order_date", "region").agg(
    F.count("order_id").alias("order_count"), F.sum("amount").alias("revenue"))
columns = ["order_date", "region", "order_count", "revenue"]
assert not expected.select(*columns).exceptAll(gold.select(*columns)).limit(1).count(), "Gold missing/wrong groups"
assert not gold.select(*columns).exceptAll(expected.select(*columns)).limit(1).count(), "Gold unexpected groups"
if flag == "true":
    actual_orders = {(r.order_id, r.sequence, r.amount, r.region) for r in current.collect()}
    assert actual_orders == {("O100", 2, Decimal("120.00"), "IN"), ("O300", 1, Decimal("50.00"), "US")}, actual_orders
    actual_gold = {(str(r.order_date), r.region, r.order_count, r.revenue) for r in gold.collect()}
    assert actual_gold == {("2026-10-12", "IN", 1, Decimal("120.00")), ("2026-10-12", "US", 1, Decimal("50.00"))}, actual_gold
# Fixture collection is intentionally tiny; production assertions remain distributed.
print({"catalog": catalog, "business_date_label": run_date, "quality": "passed"})
