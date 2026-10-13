# Databricks practical guide

A Databricks-specific data engineering handbook: **34 detailed chapters**, **12 scenario walkthroughs**, parameter tables, UI instructions, Mermaid diagrams, notebooks/SQL, bundle/CI templates, fixtures, and verification tools. Azure Databricks is the main walkthrough; AWS/GCP differences are explicit.

Branch: `databricks-practical-guide`, created from `main` independently of `data-system-design-questions`. Researched 2026-10-13 against official documentation.

## Start here

1. Read platform/prerequisites/storage/UC setup (01–04).
2. Learn parameter mechanisms (05–07).
3. Run the orders lab (28), using ingestion/transformation/serving recipes (08–17).
4. Add identity, governance, deployment, testing, and operations (18–27).
5. Use focused CDF/document/federation/troubleshooting recipes (31–34) and the scenario table below.

The examples contain placeholders and require your workspace/cloud configuration. This is a broad practical catalogue, not a claim to enumerate every Databricks feature or valid technology combination. SQL/AI/ML adjacent systems should be selected for a specific requirement; the implementation focus here is data engineering.

## Chapters and contents

| Chapter | Contents |
|---|---|
| [01. Platform map and the shared lab](databricks_guide/chapters/01-platform-and-lab.md) | Know what runs where, and use one consistent set of names throughout the guide. |
| [02. Workspace prerequisites and compute choices](databricks_guide/chapters/02-workspace-compute.md) | Choose a runtime, identity, and execution surface before copying connector code. |
| [03. Azure storage identity and external locations](databricks_guide/chapters/03-azure-storage-identity.md) | Connect ADLS Gen2 with an Access Connector, then expose storage through Unity Catalog. |
| [04. Catalogs, schemas, volumes, and minimum grants](databricks_guide/chapters/04-catalogs-volumes-grants.md) | Create the lab namespace and make its file paths usable by the workload. |
| [05. Parameters: which syntax belongs where](databricks_guide/chapters/05-parameter-cheatsheet.md) | A concrete map of deployment values, runtime values, and notebook inputs. |
| [06. Notebook widgets and safe SQL parameter binding](databricks_guide/chapters/06-widgets-and-sql.md) | Create inputs through buttons or code and use identifiers safely. |
| [07. Lakeflow Jobs, dependencies, task values, and loops](databricks_guide/chapters/07-jobs-task-values.md) | Configure a job through the UI and connect the parameter flow to a reviewed bundle. |
| [08. Batch files with COPY INTO](databricks_guide/chapters/08-batch-copy-into.md) | Load a bounded delivery with file-level replay tracking and a defined schema. |
| [09. Auto Loader: schema, checkpoints, triggers, and replay](databricks_guide/chapters/09-auto-loader.md) | Incrementally ingest JSON files with a stable checkpoint and a deliberate schema policy. |
| [10. Database snapshots, JDBC, and incremental extraction](databricks_guide/chapters/10-jdbc-and-incremental.md) | Understand source load, watermark correctness, and how deletes are represented. |
| [11. Lakeflow Connect: managed SQL Server CDC](databricks_guide/chapters/11-managed-cdc.md) | Set up a managed ingestion gateway and pipeline, with log-retention tests. |
| [12. APIs and SaaS: pagination, limits, and durable landing](databricks_guide/chapters/12-apis-saas.md) | Extract outside Spark tasks when appropriate, then use the same governed file ingestion. |
| [13. Kafka and Event Hubs: offsets, authentication, and sinks](databricks_guide/chapters/13-kafka-event-hubs.md) | Persist raw messages and use event-time logic without confusing it with ingestion time. |
| [14. Lakeflow declarative pipelines: Python, SQL, and configuration](databricks_guide/chapters/14-declarative-pipelines.md) | Build a managed DAG, with a deliberate choice of parameter mechanism. |
| [15. Ordered CDC, MERGE, hard deletes, and SCD history](databricks_guide/chapters/15-cdc-scd-merge.md) | Prevent retries and late updates from corrupting current state. |
| [16. Watermarks, state, streaming joins, and external sink delivery](databricks_guide/chapters/16-stream-state-and-external-sinks.md) | Make late-data and retry behavior explicit instead of relying on an exactly-once label. |
| [17. Gold tables, SQL warehouses, dbt, and exports](databricks_guide/chapters/17-gold-and-sql-serving.md) | Publish reconciled results with a clear refresh and serving contract. |
| [18. Secrets, service principals, Run as, and authentication](databricks_guide/chapters/18-secrets-and-service-principals.md) | Separate deployment identity, execution identity, and source-system credentials. |
| [19. Governance: row filters, masking, lineage, tags, and ABAC](databricks_guide/chapters/19-fine-grained-governance.md) | Implement a small explicit policy before scaling policy administration. |
| [20. Bundles: variables, targets, resources, and deployment commands](databricks_guide/chapters/20-bundles.md) | Deploy the same reviewed job to separate environments with explicit runtime inputs. |
| [21. GitHub Actions deployment with workload identity federation](databricks_guide/chapters/21-github-actions.md) | Configure exact trust fields and runner variables; keep deployment opt-in. |
| [22. Azure DevOps, Jenkins, GitLab, and orchestration alternatives](databricks_guide/chapters/22-other-ci-systems.md) | Use equivalent validation and deployment stages with different runners and identity adapters. |
| [23. Terraform, policies, cloud networking, and resource ownership](databricks_guide/chapters/23-terraform-and-network.md) | Automate the platform before deploying the data application. |
| [24. Git folders, code structure, packages, and runtime upgrades](databricks_guide/chapters/24-git-and-maintenance.md) | Make notebook changes reviewable and avoid mutable personal production code. |
| [25. Tests: local, Spark, workspace, contracts, and production gates](databricks_guide/chapters/25-test-strategy.md) | Choose assertions that detect business corruption as well as platform failures. |
| [26. Monitoring, audit, freshness, and cost](databricks_guide/chapters/26-observability-cost.md) | Track correctness and lag alongside run status and compute consumption. |
| [27. Performance, liquid clustering, file sizes, and table maintenance](databricks_guide/chapters/27-performance-delta.md) | Tune after proving correctness and use measurements tied to a workload. |
| [28. Worked orders lab: from fixture upload to published revenue](databricks_guide/chapters/28-worked-orders-lab.md) | Run the connected examples, verify exact outputs, and exercise a late-delete retry. |
| [29. ADF integration: linked service, Base Parameters, and return values](databricks_guide/chapters/29-adf-integration.md) | Pass ADF variables to Databricks without confusing its expression language with job syntax. |
| [30. Cloud substitutions, federation, sharing, and recovery](databricks_guide/chapters/30-clouds-and-recovery.md) | Change one technology deliberately, and know which state you must restore. |
| [31. Delta change data feed and version-bound recovery](databricks_guide/chapters/31-change-data-feed.md) | Read inserts, updates, and deletes downstream without treating CDF as a permanent audit log. |
| [32. NoSQL, nested JSON, schema drift, and grain changes](databricks_guide/chapters/32-nosql-json.md) | Ingest document changes and transform nested records without multiplying amounts accidentally. |
| [33. Federation connections, foreign catalogs, and governed sharing](databricks_guide/chapters/33-federation-sharing.md) | Read remote PostgreSQL without ingestion, and distribute approved tables to recipients. |
| [34. Troubleshooting by symptom, field, and evidence](databricks_guide/chapters/34-troubleshooting.md) | Use a concrete diagnostic order before changing permissions or resetting state. |

## Scenario walkthroughs

| Scenario | What it covers |
|---|---|
| [On-prem warehouse migration with parallel reconciliation](databricks_guide/scenarios/01-on-prem-migration.md) | Replace a legacy warehouse while controlling write cutover, reconciliation, and recovery. |
| [Daily files: 100 million orders ready by 6 a.m.](databricks_guide/scenarios/02-daily-files-sla.md) | Design a bounded ingest-and-transform workload against a deadline and a measurable capacity model. |
| [CDC with hard deletes and customer history](databricks_guide/scenarios/03-cdc-and-scd2.md) | Choose current state versus type-2 history and explicitly handle out-of-order changes. |
| [Kafka/Event Hubs events and near-real-time aggregates](databricks_guide/scenarios/04-streaming-events.md) | Build streaming analytics with bounded state, raw replay, and a stated freshness target. |
| [SaaS REST ingestion with pagination and rate limits](databricks_guide/scenarios/05-saas-api.md) | Ingest a vendor API while preserving raw response evidence and completion boundaries. |
| [Document/NoSQL source to header and line facts](databricks_guide/scenarios/06-document-nosql.md) | Flatten nested records without losing deletes, schema changes, or business grain. |
| [Multi-tenant PII platform with row and column controls](databricks_guide/scenarios/07-tenant-governance.md) | Let teams query shared curated tables under explicit policy and workspace isolation. |
| [Same file/Kafka lakehouse across Azure, AWS, and GCP](databricks_guide/scenarios/08-cloud-substitutions.md) | Reuse the logical design while replacing cloud-specific identity, network, and service settings. |
| [Warehouse modernization: SQL/dbt marts and concurrent BI](databricks_guide/scenarios/09-warehouse-bi.md) | Serve governed metrics while migrating legacy SQL and controlling query performance. |
| [Backfill, lost checkpoints, and region recovery](databricks_guide/scenarios/10-replay-disaster-recovery.md) | Recover data state without silently skipping retained changes or duplicating external effects. |
| [Federated migration discovery and partner data sharing](databricks_guide/scenarios/11-federation-and-sharing.md) | Read external data with foreign catalogs, then disclose only approved assets to recipients. |
| [Dev/test/prod CI/CD, schema evolution, and runtime upgrades](databricks_guide/scenarios/12-promotion-and-upgrades.md) | Promote a tested application and distinguish code, schema, policy, and state changes. |

## Executable and reviewable companions

- [Examples README](databricks_guide/examples/README.md): prerequisites and exact commands.
- [Orders Jobs bundle](databricks_guide/examples/databricks.yml) and [task definitions](databricks_guide/examples/resources/orders.job.yml).
- [Alternative Lakeflow bundle](databricks_guide/examples/lakeflow_bundle/databricks.yml).
- [Templates](databricks_guide/examples/templates/README.md): classic compute, loops, run request, four CI vendors, API extraction, and Terraform.
- [Verification](databricks_guide/VERIFICATION.md): checks performed and cloud checks remaining.
- [Source register](databricks_guide/SOURCES.md): official references.
- [Diagram gallery](databricks_guide/DIAGRAMS.md): rendered samples plus the complete Mermaid manifest.

## What is verified

Local fixture/reference rules, API failure handling, Python syntax, bundle configuration shape, file/reference completeness, and diagram parse/render checks are locally verifiable. Workspace authentication, live UI, UC/cloud permissions, Spark/Delta/Connect execution, connector behavior, performance, Terraform apply, and cloud deployment require your environment and were not executed during authoring. Local CI deliberately has no Databricks credentials.
