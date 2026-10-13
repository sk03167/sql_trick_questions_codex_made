# ADF example factory and local acceptance oracle

Start with [the worked lab](../chapters/30-worked-lab.md), [parameters](../chapters/06-parameter-map.md) and [deployment](../chapters/26-azure-devops-ci.md). The source root `factory/` contains four pipelines, three datasets, two linked services, one stopped trigger, development-factory metadata and custom publish/ARM configuration. No live Azure factory was connected during authoring.

## Definitions and intended execution

| Asset | What it demonstrates | Dependencies |
|---|---|---|
| pl_parallel_parent / pl_parameter_child | Immutable inputs, isolated per-child variable, explicit invalid-input Fail | A real ADF factory; Wait/Set Variable only |
| pl_copy_files | Parameterized Binary Copy, stable batch folder, nonempty-file gate | Actual ADLS endpoint, identity permissions/runtime networking |
| pl_rest_orders_example | REST source paging and collection mapping | Adapt vendor endpoint/auth/response contract; example.invalid isn't live |
| tr_daily_files_stopped | Previous completed India-local day at 04:00 | Deliberately stopped; source/date/trigger readiness tests |

`ls_adls` uses a parameterized account URL and the documented system-assigned managed identity path. Bootstrap storage source/sink rights and connectivity; ADF management Contributor alone is insufficient. Factory/account names/resource IDs are illustrative.

## Validate locally and export with Microsoft utilities

Use supported Node 20/22; authoring validation/export used Node 22.23.3 and utilities 1.0.3. From repository root:

```sh
python3 -m unittest discover -s adf_guide/examples/tests -v
python3 adf_guide/tools/validate_factory.py
python3 adf_guide/tools/validate_guide.py
cd adf_guide/tools
npm ci --ignore-scripts --no-audit --no-fund
npm run build -- validate ../examples/factory \
  '/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-adf-guide/providers/Microsoft.DataFactory/factories/adf-guide-dev'
npm run build -- export ../examples/factory \
  '/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-adf-guide/providers/Microsoft.DataFactory/factories/adf-guide-dev' arm-output
```

The utility downloads Microsoft's current validation bundle. The zero subscription UUID and source factory name are illustrative and do not identify an authenticated factory. Definition validation/export deploys nothing; connector credentials/network/runtime behavior remain untested. Output directory is relative to `tools/`. A generated snapshot and metadata are provided under `generated_arm/`; deploy only reviewed output with real environment overrides.

## Live parameter demo

In an approved development factory import/connect source definitions with the real factory settings. Publish/deploy reviewed definitions, then Debug or Trigger now the parent with `p_entities=["orders","customers"]`, `p_batch_id=demo-001`. Inspect child inputs/output and labels. Invalid entity `unapproved` should produce INVALID_INPUT. The opt-in `tools/live_smoke.py` runs this parameter-only published pipeline through Azure CLI and awaits terminal status; it isn't called by local CI.

## Live file lab

Upload exactly two CSV fixtures into `lab/incoming/orders/2026-10-12`. Keep the example manifest outside the two-file source. Bind the real account URL. Run Copy with the supplied run-copy.parameters.json values. Destination is `lab/landing/orders/batch=orders-20261012-001`.

Expected names/bytes unchanged; three parsed rows and revenue IN 145.00 / US 50.00. Run unchanged with the same logical batch ID and verify the same accepted file set. Nonempty filesRead isn't row/revenue validation, and repeated overwrite isn't a guarantee that a downstream append consumer is idempotent.

## SQL and production scope

The ordered SQL commit companion is illustrative SQL Server/Azure SQL code, not used by the portable demo. It has not been SQL-executed; source boundary/count proof, retained-state auditing, accepted-batch ledger, schema/security/concurrency tests and a replay response contract are prerequisites before production. The local version/tombstone model is an independent oracle, not SQL or ADF execution.

Before production complete connector/IR access, deletion/ordering/completion contracts, target schema/commit semantics, monitoring, retention, source load, recovery and release trigger handling. Deployment templates are opt-in. Do not start the stopped trigger merely because the JSON or ARM validated.
