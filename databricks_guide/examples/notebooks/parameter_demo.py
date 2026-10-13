# Databricks notebook source
# Parameter plumbing demo only; does not ingest each named entity.
dbutils.widgets.text("entity", "orders")
entity = dbutils.widgets.get("entity")
if entity not in {"orders", "customers"}:
    raise ValueError("Unknown entity")
print({"entity": entity})
