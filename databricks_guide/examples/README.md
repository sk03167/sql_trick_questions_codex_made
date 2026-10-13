# Orders reference project

Start with [worked lab](../chapters/28-worked-orders-lab.md), [UC setup](../chapters/04-catalogs-volumes-grants.md), and [bundles](../chapters/20-bundles.md). This project is an educational implementation with placeholders; no cloud deployment occurred during authoring.

## Prerequisites

- UC-enabled target workspace and compatible serverless notebook Jobs (or adapt the classic-compute template).
- Catalog de_lab_dev and schemas bronze/silver/gold/ops exist, with managed storage configured.
- Volumes ops.landing and ops.state exist; create landing/orders and upload only orders_001.json for the initial fixture.
- Execution identity has namespace USE, landing READ VOLUME, state READ/WRITE VOLUME, schema CREATE TABLE, existing-table SELECT/MODIFY, and source-code permissions. CREATE TABLE is also needed for the current view; migrations can need ownership.
- Databricks CLI is installed and authenticated to the intended workspace. Offline schema capture was made with CLI 1.18.0; use an approved compatible CLI and authenticated validation.

## Run local checks from the repository root

```sh
python3 -m unittest discover -s databricks_guide/examples/tests -v
python3 -m venv /tmp/databricks-guide-checks
/tmp/databricks-guide-checks/bin/pip install -r databricks_guide/tools/requirements.txt
/tmp/databricks-guide-checks/bin/python databricks_guide/tools/validate_config.py
python3 databricks_guide/tools/validate_guide.py
```

Local rules form an independent fixture oracle; they do not run Spark, Delta, Auto Loader, Lakeflow Connect, or Unity Catalog. Python syntax validation does not execute notebook code. The `assert_quality` task is the corresponding live workspace check.

## Deploy and run the Jobs implementation

```sh
cd databricks_guide/examples
databricks auth login --host 'https://<dev-workspace-host>' --profile de-lab
export BUNDLE_VAR_workspace_host='https://<dev-workspace-host>'
databricks bundle validate -t dev --profile de-lab
databricks bundle deploy -t dev --profile de-lab
databricks bundle run orders_daily -t dev --profile de-lab \
  --params 'catalog=de_lab_dev,run_date=2026-10-12,min_current_rows=2,validate_fixture=true'
```

Keep the same logical ingestion checkpoint between retries/runs. Run twice unchanged, then upload orders_002.json and run with validate_fixture=false,min_current_rows=1. First expected revenue: IN 120.00 and US 50.00; after correction IN 130.00 only. Full expected state is in the worked lab and tests. The business date input labels a run; this small implementation rebuilds current-state gold across all dates, not only that date.

The raw amount and sequence fields are strings; silver casts and validates. Sequence must be unsigned integer text fitting BIGINT; non-delete amounts must fit decimal(18,2) without rounding; event timestamps require an explicit timezone. Updates are full records. A duplicate event/ordering conflict stops publication. Quarantine is a full-bronze diagnostic snapshot. State preserves delete sequence/tombstones. This transparent full-history scan is deliberately a small lab; choose incremental state/contract enforcement and retention for production.

## Alternative Lakeflow implementation

The separate lakeflow_bundle/databricks.yml deploys the Python pipeline with `_pipeline` table names. It owns its output tables/checkpoints independently. It drops/quarantines invalid rows, whereas the Jobs project fails publication for invalid rows. AUTO CDC relies on a valid unique source ordering contract; add its source conflict gate and retention tests before production. Use one implementation per target. SQL pipeline parameter demo is a separate illustrative asset.

## Production promotion

Set the actual prod workspace_host and run_as_sp application ID, approve catalog/network/grants and target settings, configure run-specific business inputs, disable fixture-specific assertions for nonfixture data, and run workspace reconciliation/security/performance/recovery tests. The prod target is a deployment example, not automatic production readiness.

```sh
export BUNDLE_VAR_workspace_host='https://<prod-workspace-host>'
export BUNDLE_VAR_run_as_sp='<execution-application-id>'
databricks bundle validate -t prod
databricks bundle deploy -t prod
```

Never use bundle destroy as production rollback. Terraform/bootstrap, bundle resources, table/schema migration, code revision, and data replay have separate ownership/lifecycle.
