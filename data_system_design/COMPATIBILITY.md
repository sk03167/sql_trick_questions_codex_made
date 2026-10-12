# Compatibility and Combination Rules

[Scenario index](../DATA_SYSTEM_DESIGN_INDEX.md)

The combination explorer exhaustively assembles a finite, explicit design space. It does not discover every vendor connector or certify a generated architecture. Each result retains a source contract and a complete compute/serving bundle, plus its required integration checks.

## Enumerated dimensions

1. Scenario and coherent reference path.
2. Data bundle: reference, or one of the documented assembled replacements. A changed table format travels with a compatible proposed writer and query endpoint.
3. Runtime orchestration: bounded schedule or continuous-job lifecycle control as appropriate.
4. Governance metadata: platform metadata, OpenMetadata, or DataHub. Engine and storage enforcement remains required in every case.
5. Delivery engine: GitHub Actions, Jenkins, GitLab CI, eligible native-cloud CI, or eligible Kubernetes CI/GitOps.
6. Infrastructure tool supported by that documented delivery recipe.

Storage locations and formats inside a bundle are explicit rather than independently mixed with arbitrary consumers. Each scenario component-swap table describes further substitutions and the contract work required; those unmodeled substitutions are not included in the numeric count.

## Implemented exclusions

- Azure DevOps native recipe is listed for Azure reference paths; AWS CodePipeline native recipe for AWS paths; Cloud Build native recipe for Google paths. Other CI tools can target those clouds through configured identities and APIs.
- Argo CD and Tekton recipes require a path marked as a Kubernetes deployment. Adding Kubernetes to another path is a new explicit deployment decision, not a free substitution.
- Iceberg/Trino and Delta/Spark alternatives are bundled rather than allowing arbitrary native warehouse readers over unsupported table protocols.
- The VM migration scenario preserves its database engine. A warehouse redesign is a different scenario, S02.
- A bounded ADF pipeline is not modeled as a continuously running stream-processing engine.

These structural rules prevent obvious invalid combinations. They do not check service tiers, cloud regions, actual connector versions, quotas, licensing, every table feature, or all private-network routes.

## Compatibility review for each candidate

| Interface | Evidence required |
| --- | --- |
| Source to extraction | Snapshot boundary, types, stable keys, DDL behavior, delete images, logs/feeds and credentials |
| Producer to transport | Serialization, maximum record size, partition key, ordering scope, retention and retry acknowledgments |
| Transport to processor | Exact client protocol, connector versions, offset semantics and crash/rebalance recovery |
| Processor to table | Supported table features, catalog protocol, write commit, concurrency, schema evolution and delete application |
| Table to query engine | Reader version, authorization, partition pruning, nested types and all enabled delete/snapshot features |
| Processor to serving API | Idempotent keys, mutations, rate limits, acknowledgment and visibility/freshness behavior |
| CI to deployment API | Short-lived identity, trusted runner placement, environment scope and immutable artifact provenance |
| Restore to running job | Compatible job state, available source offsets, retained table snapshots and coordinated writer ownership |

## Alternatives that need redesign

Replacing Kafka with Pub/Sub or Kinesis changes clients and ordering contracts. Replacing Spark with Flink changes runtime state and computation semantics. Replacing Delta with Iceberg or Hudi changes metadata and protocol behavior. Replacing Snowflake with BigQuery or Redshift changes SQL, physical layout, loading and grants. Replacing PostgreSQL with DynamoDB or Cassandra changes key and query design. Replacing live sharing with downloaded files changes revocation and deletion obligations.

For interoperability, run the precise reader and writer versions against real table features. Do not use file-level compatibility as a proxy for table transactions or policy enforcement. Changing format may require a full rewrite or migration rather than editing a configuration string.

## Runtime meaning

The scheduler controls when bounded work runs or manages a continuous job lifecycle. It is not the event transport and should not submit a new consumer for every event. CI deploys code and resource intent; it does not automatically run all runtime data-quality or source-completeness checks. Metadata tools improve discovery; they do not universally authorize storage and engine reads.

## Explorer output

Every JSONL candidate records scenario, reference path, data bundle, selected stages, orchestration, metadata/enforcement choice, CI, IaC and outstanding qualification text. Use --count to inspect scope, --limit to sample, and --all --output to export every documented combination for the selected scenario. The numeric count describes architecture assemblies, not proven deployments or independent benchmark results.
