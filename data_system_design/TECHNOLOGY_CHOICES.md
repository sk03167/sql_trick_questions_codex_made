# Data Technology Choices and Benefits

[Scenario index](../DATA_SYSTEM_DESIGN_INDEX.md)

Choose a component because it satisfies a measurable contract. A cloud name is a placement decision; a broker transports events; an object store retains bytes; a table format supplies table semantics; compute transforms records; a serving engine answers consumer queries. These roles should remain distinct even when one platform provides several.

| Role | Technologies | Need | Benefit | Tradeoff or boundary | Reference |
| --- | --- | --- | --- | --- | --- |
| Ingestion | ADF and Fabric pipelines | Bounded movement and orchestration | Repeatable connectors and dependency control | Pipeline runs are not a generic continuously running Kafka consumer. | [Azure Data Factory connectors](https://learn.microsoft.com/en-us/azure/data-factory/connector-overview) |
| Ingestion | AWS DMS and Google Datastream | Supported database change capture | Reduce custom snapshot and log-reader work | Check exact source, target, schema, log retention, and delete contracts. | [AWS DMS ongoing replication](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Task.CDC.html) |
| Ingestion | Debezium and Kafka Connect | Source-specific log or change-stream capture | Stable envelopes and replayable integration | Connector and source configuration define images, ordering, and resume behavior. | [Debezium PostgreSQL connector](https://debezium.io/documentation/reference/connectors/postgresql.html) |
| Ingestion | Airbyte and Fivetran | Supported source extraction | Reduce connector implementation and maintenance | Per-connector fidelity and delivery mode require verification. | [Airbyte connector documentation](https://docs.airbyte.com/) |
| Transport | Kafka MSK and Confluent | Partitioned retained event transport | Independent consumers and replay | Partition ordering is not global ordering or arbitrary-sink exactly-once. | [Apache Kafka documentation](https://kafka.apache.org/documentation/) |
| Transport | Kinesis Event Hubs and Pub Sub | Cloud-managed event transport | Provider integration and reduced broker administration | Clients, partition behavior, retention and APIs differ. | [AWS analytics reference architecture](https://docs.aws.amazon.com/wellarchitected/latest/analytics-lens/reference-architecture-2.html) |
| Device handoff | MQTT and RabbitMQ | Device messaging or task delivery | Fit connectivity or acknowledgment workflows | Do not assume long-term analytical replay without separate retention design. | [AWS IoT Core](https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html) |
| Storage | S3 ADLS GCS OCI and IBM object storage | Durable bytes and versioned archives | Independent storage and compute plus replay | Not a relational warehouse or table transaction manager. | [AWS analytics reference architecture](https://docs.aws.amazon.com/wellarchitected/latest/analytics-lens/reference-architecture-2.html) |
| Table format | Iceberg Delta Lake and Hudi | Table metadata snapshots and mutations | Transactional or incremental table behavior over files | Coordinate catalog, protocol, feature versions and readers/writers. | [Apache Iceberg reliability](https://iceberg.apache.org/docs/latest/reliability/) |
| Compute | Spark and Databricks | Distributed transformation and supported streaming | Large joins, complex processing and lakehouse integration | Checkpoint and sink behavior determine delivery guarantees. | [Spark Structured Streaming](https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html) |
| Compute | Flink | Stateful event-time stream computation | Fine-grained windows, state, and replay-aware processing | External end-to-end guarantees require compatible sinks and protocols. | [Apache Flink fault tolerance](https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/fault_tolerance/) |
| Compute | Beam on Dataflow | Batch and stream pipeline model on a managed runner | Runner-managed scaling and supported event-time processing | Runner and connector capabilities must be validated. | [Google Dataflow overview](https://docs.cloud.google.com/dataflow/docs/overview) |
| Compute | Warehouse SQL with dbt | Relational ELT and model testing | Versioned transformations and dependency-aware models | dbt is not a universal extraction connector or transactional CDC reader. | [dbt introduction and platform roles](https://docs.getdbt.com/docs/introduction) |
| Compute | DuckDB and Polars | Bounded analytical processing | Efficient local or single-node jobs | Memory, disk, publication and concurrency boundaries remain explicit. | [DuckDB documentation](https://duckdb.org/docs/stable/) |
| Warehouse | Snowflake BigQuery Redshift Synapse and Fabric Warehouse | Managed analytical SQL serving | Query-oriented physical execution and concurrency controls | They differ in DDL, SQL, loading, costs and authorization. | [Snowflake data loading](https://docs.snowflake.com/en/user-guide/data-load-overview) |
| Lake query | Databricks SQL Trino Athena and Spark SQL | Query compatible lake tables | Read shared table products without all consumers sharing a compute runtime | Use a supported catalog, table protocol and query endpoint. | [Trino documentation](https://trino.io/docs/current/) |
| Realtime OLAP | ClickHouse Pinot Druid and KQL engines | Fast fresh aggregates and filtering | Specialized serving for analytical query shapes | Mutation, indexing, retention and approximation contracts differ. | [ClickHouse overview](https://clickhouse.com/docs/get-started/about/intro) |
| NoSQL serving | MongoDB DynamoDB Cosmos DB Cassandra Bigtable and Redis | Query-oriented application projections | Fit documents, partitioned lookup, wide columns or cache access | Access patterns, consistency, TTL and reconstruction are workload-specific. | [MongoDB change streams](https://www.mongodb.com/docs/manual/changestreams/) |
| Search | Elasticsearch and OpenSearch | Derived document or log indexes | Full text and operational exploration | Keep a recovery archive and validate mappings, plugins and authorized access. | [Elastic search documentation](https://www.elastic.co/docs/solutions/search) |
| Graph | Neo4j and Neptune | Relationship traversal | Fit path and neighborhood queries | Models, query languages, licenses and auth differ. | [Amazon Neptune](https://docs.aws.amazon.com/neptune/latest/userguide/intro.html) |
| Spatial and time | PostGIS TimescaleDB and InfluxDB | Specialized spatial or temporal predicates | Indexes, time-oriented layout and explicit domain semantics | Check units, coordinate models, corrections and selected hosted features. | [PostGIS manual](https://postgis.net/docs/) |
| Feature definitions | Feast | Offline and online feature access contracts | Reusable feature views and point-in-time retrieval | It is not a general DAG orchestrator or a substitute for upstream feature computation. | [Feast feature store roles and limitations](https://docs.feast.dev/) |
| ML provenance | MLflow | Experiment and model lifecycle metadata | Link artifacts, evaluations and releases | Data snapshots and label definitions need their own reproducible manifests. | [MLflow documentation](https://mlflow.org/docs/latest/index.html) |
| Retrieval | Azure AI Search Qdrant pgvector and Databricks AI Search | Text/vector retrieval over authorized content | Support semantic or hybrid retrieval | Embedding version, filters, deletes and permission propagation remain mandatory. | [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search) |
| Orchestration | Airflow Dagster Prefect and Lakeflow Jobs | Dependencies, job lifecycle and execution control | Repeatable schedules, retries, operational visibility | Orchestration progress is not proof of business data correctness. | [Apache Airflow architecture](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html) |
| Governance | Purview Knowledge Catalog Unity Catalog Horizon OpenMetadata and DataHub | Discovery, ownership, lineage and product metadata | Make policy and provenance inspectable | Enforcement also needs actual engine and storage controls. | [Microsoft Purview governance](https://learn.microsoft.com/en-us/azure/purview/overview) |
| Delivery | GitHub Actions Jenkins GitLab Azure DevOps CodePipeline Cloud Build Argo CD and Tekton | Build test and release automation | Repeatable releases and environment evidence | Select identity and target-specific deployment adapters. | [GitHub Actions OIDC](https://docs.github.com/en/actions/concepts/security/openid-connect) |
| Infrastructure | Terraform OpenTofu Pulumi and native IaC | Provision and track resource intent | Reviewable reproducible environments | Protect state, avoid overlapping owners, and test restore separately. | [Terraform state](https://developer.hashicorp.com/terraform/language/state) |
| Quality | dbt tests Great Expectations and custom invariants | Assert data contracts and product correctness | Detect invalid or stale products before publication | Tool success does not replace business reconciliation or denied-access tests. | [dbt data tests](https://docs.getdbt.com/docs/build/data-tests) |
| Semantics | Power BI models LookML Cube and dbt Semantic Layer | Governed metric interpretation | Reuse business definitions across consumers | Validate nonadditive measures, cache policy, identity and version changes. | [Cube semantic layer documentation](https://cube.dev/docs/) |
| Reverse ETL | Hightouch or a custom destination worker | Controlled operational activation of curated data | Reduce API syncing work or gain precise delivery control | Define field authority, consent, deletes, idempotency and feedback-loop prevention. | [Hightouch reverse ETL documentation](https://hightouch.com/docs/) |

## Cloud translations

| Role | AWS | Azure | Google Cloud | Independent or self managed |
| --- | --- | --- | --- | --- |
| Durable bytes | S3 | ADLS Gen2 or Blob | Cloud Storage | Supported S3-compatible storage or other approved object store |
| Retained event transport | Kinesis or MSK | Event Hubs | Pub/Sub | Kafka or Confluent with appropriate hosting |
| Database CDC | DMS for supported pairs | Source-specific Debezium or supported ADF CDC path | Datastream for supported sources | Debezium or verified engine-specific tooling |
| Batch orchestration | MWAA/Airflow or Step Functions with actual job APIs | ADF/Fabric pipelines or Lakeflow Jobs | Cloud Composer/Airflow or Workflows with actual job APIs | Airflow Dagster or Prefect |
| Distributed compute | EMR or Glue Spark; Managed Flink | Databricks Spark; Flink on appropriate hosting | Dataproc Spark; Beam/Dataflow | Spark Flink or supported Python runtimes |
| Analytical SQL | Redshift Athena or supported lake query layer | Synapse Fabric or Databricks SQL | BigQuery or supported lake query layer | Snowflake on supported clouds; Trino ClickHouse PostgreSQL |
| Metadata and discovery | Glue Catalog and integrated Lake Formation | Purview plus platform catalogs | Knowledge Catalog | Unity Catalog Horizon OpenMetadata DataHub and format catalogs |
| Infrastructure | Terraform/OpenTofu/Pulumi or CDK/CloudFormation | Terraform/OpenTofu/Pulumi or Bicep/ARM | Terraform/OpenTofu/Pulumi and supported provider tools | Chosen providers, Helm/Argo CD for Kubernetes, Ansible/Packer for hosts |

## Component selection questions

1. What source contract and consumer latency are required? Distinguish event-time processing from periodic refresh.
2. Is the state append-only, mutable, historical, or query-oriented? What does a delete mean?
3. Who owns connectors, runtimes, table catalogs, credentials, retention, and outages?
4. What must be replayable or restorable? How long do source logs and snapshots survive?
5. Which interfaces and table features are supported by the exact chosen engines?
6. How will correctness, security, cost, and recovery be measured before and after a substitution?

## Format and deployment are separate choices

CSV/JSON/Avro/Protobuf describe serialization or record formats. Parquet/ORC describe columnar files. Delta Lake/Iceberg/Hudi describe table metadata and mutation protocols over files. S3/ADLS/GCS are storage systems. Native warehouse tables have their own managed storage and execution contracts. A compatible reader for one combination is not proof that every writer, delete mode, schema feature, catalog, or security control also works.

A managed connector shifts operational work; it does not remove the need to test its exact source, target, snapshot, delete and schema behavior. A self-managed stack gives more placement control while retaining operations, patching and restore responsibility. Costs include compute, storage, requests, egress, licensing, and engineering time.
