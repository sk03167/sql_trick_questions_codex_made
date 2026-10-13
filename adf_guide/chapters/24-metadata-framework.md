# 24. Metadata-driven ingestion framework and configuration ownership

Scale reusable pipelines without giving a control table arbitrary execution power.

## Data design and control schema

| Field | Example | Rule |
|---|---|---|
| `entity` | `orders` | Stable allowlisted key |
| `enabled` | true | Boolean; audited change |
| `source_kind` | `sql_ledger` / `adls_files` | Supported Switch case |
| `source_object` | Approved table/procedure or prefix | Not arbitrary SQL |
| `sink_object` | Approved landing/table | Scope and schema contract |
| `boundary_kind` | version/window/complete_batch | Explicit semantics |
| `last_committed` | Published source boundary | Advance only on acceptance |
| `batch_id` | Stable logical identity | Reused across retries |
| `max_parallelism` | Source-approved number | Budget and IR capacity |
| `contract_version` | `orders_v1` | Schema/order/delete semantics |

```mermaid
flowchart LR
 M["Reviewed control metadata"] --> L["Lookup bounded enabled entities"]
 L --> F["ForEach direct immutable items"]
 F --> C["Child route per allowlisted source kind"]
 C --> S["Batch-isolated stage and commit"]
 S --> A["Audited status / committed boundary"]
```

## Exact activity chain

**Lookup** `LookupConfig`, First row only false, returns bounded enabled entity records. **ForEach** Items `@activity('LookupConfig').output.value`, Sequential false, batchCount a measured source-approved limit. **Execute Pipeline** child with parameters `p_entity=@item().entity`, `p_batch_id` from the caller, and explicit bounded object/path fields. **Wait on completion** true. The child uses Switch/If plus allowlist validation before source/sink actions.

When inventory exceeds Lookup limits, page it through a reviewed outer pipeline/control query. Do not silently accept a truncated entity list. Store per-entity/batch status in a durable control/audit database with attempt IDs and committed source/target boundaries. Avoid shared mutable parent variables collecting parallel results.

## Governance and infrastructure automation

Control metadata is executable configuration. Restrict who can change enabled flags, endpoints, sink keys, cleanup paths, credentials, and procedure names. A catalog entry is not permission to grant broader source credentials. Validate contract version and supported connector/runtime before launching work.

The platform provisions IR/private routing and connector identities. The metadata framework chooses among preapproved connections; it should not dynamically provision credentials on each run. Protect watermark/control data and concurrency locks independently of application code.

## Code push automation and maintenance

Version framework code and metadata schema; audit runtime configuration changes separately. Use canary entities and a disposable sink for release tests. Pin source/deletion contract changes and migrations; code and metadata rollback have different effects. Generated ARM parameterization is not the same as a control-table row update.

## Tests

Disabled/wrong type entity, missing contract fields, duplicate key, query injection attempt, invalid sink path, lookup truncation, unsupported source kind, parallel source limits, child failure, retry, and concurrent watermark commits. Reconcile expected versus attempted/accepted entities and keep failed entities visible for replay.

## Official references

- [Copy Data Tool Metadata Driven](https://learn.microsoft.com/en-us/azure/data-factory/copy-data-tool-metadata-driven)
- [Control Flow Lookup Activity](https://learn.microsoft.com/en-us/azure/data-factory/control-flow-lookup-activity)
- [Control Flow For Each Activity](https://learn.microsoft.com/en-us/azure/data-factory/control-flow-for-each-activity)
- [Control Flow Execute Pipeline Activity](https://learn.microsoft.com/en-us/azure/data-factory/control-flow-execute-pipeline-activity)

[Guide index](../../AZURE_DATA_FACTORY_GUIDE_INDEX.md)
