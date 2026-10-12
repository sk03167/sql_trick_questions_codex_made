# Primary Documentation Sources

[Scenario index](../DATA_SYSTEM_DESIGN_INDEX.md)

Research date: October 12, 2026. These links describe components and platform contracts. Scenario designs and combinations are original proposed applications of those contracts; references do not certify a whole generated architecture. Product versions, editions, availability and limits must be checked for a real deployment.

| Key | Documentation | Link |
| --- | --- | --- |
| adf | Azure Data Factory connectors | [Azure Data Factory connectors](https://learn.microsoft.com/en-us/azure/data-factory/connector-overview) |
| adf-cdc | ADF CDC and batch pipeline boundaries | [ADF CDC and batch pipeline boundaries](https://learn.microsoft.com/en-us/azure/data-factory/concepts-change-data-capture) |
| adf-rest | ADF REST connector | [ADF REST connector](https://learn.microsoft.com/en-us/azure/data-factory/connector-rest) |
| airbyte | Airbyte connector documentation | [Airbyte connector documentation](https://docs.airbyte.com/) |
| airflow | Apache Airflow architecture | [Apache Airflow architecture](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html) |
| argo | Argo CD Kubernetes GitOps | [Argo CD Kubernetes GitOps](https://argo-cd.readthedocs.io/en/stable/) |
| aws-analytics | AWS analytics reference architecture | [AWS analytics reference architecture](https://docs.aws.amazon.com/wellarchitected/latest/analytics-lens/reference-architecture-2.html) |
| aws-ci | AWS CodePipeline | [AWS CodePipeline](https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html) |
| aws-dms | AWS DMS ongoing replication | [AWS DMS ongoing replication](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Task.CDC.html) |
| aws-iot | AWS IoT Core | [AWS IoT Core](https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html) |
| azure-analytics | Microsoft modern warehouse architecture | [Microsoft modern warehouse architecture](https://learn.microsoft.com/azure/architecture/databases/architecture/dataops-mdw) |
| azure-ci | ADF CI CD | [ADF CI CD](https://learn.microsoft.com/en-us/azure/data-factory/continuous-integration-delivery) |
| azure-iot | Azure IoT Hub | [Azure IoT Hub](https://learn.microsoft.com/en-us/azure/iot-hub/iot-concepts-and-iot-hub) |
| azure-migrate | Azure Migrate overview | [Azure Migrate overview](https://learn.microsoft.com/en-us/azure/migrate/migrate-services-overview) |
| azure-search | Azure AI Search | [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search) |
| bigtable | Bigtable change streams | [Bigtable change streams](https://docs.cloud.google.com/bigtable/docs/change-streams-overview) |
| cassandra | Cassandra CDC operating guide | [Cassandra CDC operating guide](https://cassandra.apache.org/doc/latest/cassandra/managing/operating/cdc.html) |
| clickhouse | ClickHouse overview | [ClickHouse overview](https://clickhouse.com/docs/get-started/about/intro) |
| cosmos | Cosmos DB change feed modes | [Cosmos DB change feed modes](https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed) |
| cube | Cube semantic layer documentation | [Cube semantic layer documentation](https://cube.dev/docs/) |
| dagster | Dagster documentation | [Dagster documentation](https://dagster.io/docs) |
| databricks-bundles | Databricks Declarative Automation Bundles | [Databricks Declarative Automation Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/) |
| databricks-jobs | Databricks Lakeflow Jobs | [Databricks Lakeflow Jobs](https://docs.databricks.com/aws/en/jobs/) |
| databricks-uc | Databricks Unity Catalog | [Databricks Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/) |
| databricks-vector | Databricks AI Search formerly Vector Search | [Databricks AI Search formerly Vector Search](https://docs.databricks.com/aws/en/ai-search/ai-search) |
| dataflow | Google Dataflow overview | [Google Dataflow overview](https://docs.cloud.google.com/dataflow/docs/overview) |
| datahub | DataHub documentation | [DataHub documentation](https://docs.datahub.com/docs/features/feature-guides/lineage) |
| datastream | Google Datastream documentation | [Google Datastream documentation](https://docs.cloud.google.com/datastream/docs) |
| dbt | dbt introduction and platform roles | [dbt introduction and platform roles](https://docs.getdbt.com/docs/introduction) |
| dbt-tests | dbt data tests | [dbt data tests](https://docs.getdbt.com/docs/build/data-tests) |
| debezium | Debezium PostgreSQL connector | [Debezium PostgreSQL connector](https://debezium.io/documentation/reference/connectors/postgresql.html) |
| debezium-mongo | Debezium MongoDB connector | [Debezium MongoDB connector](https://debezium.io/documentation/reference/connectors/mongodb.html) |
| delta | Delta Lake documentation | [Delta Lake documentation](https://docs.delta.io/) |
| delta-share | Delta Sharing protocol and server | [Delta Sharing protocol and server](https://github.com/delta-io/delta-sharing) |
| druid | Apache Druid design | [Apache Druid design](https://druid.apache.org/docs/latest/design/) |
| duckdb | DuckDB documentation | [DuckDB documentation](https://duckdb.org/docs/stable/) |
| dynamo | DynamoDB Streams and item ordering | [DynamoDB Streams and item ordering](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html) |
| elastic | Elastic search documentation | [Elastic search documentation](https://www.elastic.co/docs/solutions/search) |
| eventhubs | Azure Event Hubs overview | [Azure Event Hubs overview](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-about) |
| fabric-rti | Fabric Real Time Intelligence | [Fabric Real Time Intelligence](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/overview) |
| feast | Feast feature store roles and limitations | [Feast feature store roles and limitations](https://docs.feast.dev/) |
| fivetran | Fivetran documentation | [Fivetran documentation](https://fivetran.com/docs/getting-started) |
| flink | Apache Flink fault tolerance | [Apache Flink fault tolerance](https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/fault_tolerance/) |
| gcp-catalog | Knowledge Catalog formerly Dataplex Universal Catalog | [Knowledge Catalog formerly Dataplex Universal Catalog](https://docs.cloud.google.com/knowledge-catalog/docs) |
| gcp-ci | Google Cloud Build | [Google Cloud Build](https://docs.cloud.google.com/build/docs/overview) |
| gcp-migrate | Google Cloud migration planning | [Google Cloud migration planning](https://docs.cloud.google.com/architecture/migration-to-gcp-getting-started) |
| gcp-pipelines | Google Cloud pipeline architecture | [Google Cloud pipeline architecture](https://cloud.google.com/blog/topics/developers-practitioners/what-data-pipeline-architecture-should-i-use/) |
| gcp-transfer | Google Storage Transfer Service | [Google Storage Transfer Service](https://docs.cloud.google.com/storage-transfer/docs/overview) |
| github | GitHub Actions OIDC | [GitHub Actions OIDC](https://docs.github.com/en/actions/concepts/security/openid-connect) |
| gitlab | GitLab CI CD | [GitLab CI CD](https://docs.gitlab.com/ci/) |
| gx | Great Expectations Core | [Great Expectations Core](https://docs.greatexpectations.io/docs/core/introduction/) |
| hightouch | Hightouch reverse ETL documentation | [Hightouch reverse ETL documentation](https://hightouch.com/docs/) |
| hudi | Apache Hudi overview | [Apache Hudi overview](https://hudi.apache.org/docs/overview/) |
| ibm | IBM watsonx data official architecture repository | [IBM watsonx data official architecture repository](https://github.com/IBM/watsonx-data) |
| iceberg | Apache Iceberg reliability | [Apache Iceberg reliability](https://iceberg.apache.org/docs/latest/reliability/) |
| influx | InfluxDB documentation | [InfluxDB documentation](https://docs.influxdata.com/) |
| jenkins | Jenkins Pipeline | [Jenkins Pipeline](https://www.jenkins.io/doc/book/pipeline/) |
| kafka | Apache Kafka documentation | [Apache Kafka documentation](https://kafka.apache.org/documentation/) |
| kinesis | Amazon Kinesis Data Streams | [Amazon Kinesis Data Streams](https://docs.aws.amazon.com/streams/latest/dev/introduction.html) |
| lakeformation | Lake Formation permission boundaries | [Lake Formation permission boundaries](https://docs.aws.amazon.com/lake-formation/latest/dg/lf-permissions-overview.html) |
| mermaid | Mermaid flowchart syntax | [Mermaid flowchart syntax](https://mermaid.js.org/syntax/flowchart.html) |
| mlflow | MLflow documentation | [MLflow documentation](https://mlflow.org/docs/latest/index.html) |
| mongo | MongoDB change streams | [MongoDB change streams](https://www.mongodb.com/docs/manual/changestreams/) |
| neo4j | Neo4j documentation | [Neo4j documentation](https://neo4j.com/docs/) |
| neptune | Amazon Neptune | [Amazon Neptune](https://docs.aws.amazon.com/neptune/latest/userguide/intro.html) |
| oci | OCI GoldenGate | [OCI GoldenGate](https://docs.oracle.com/en/cloud/paas/goldengate-service/index.html) |
| openmetadata | OpenMetadata documentation | [OpenMetadata documentation](https://docs.open-metadata.org/) |
| opensearch | Amazon OpenSearch Service | [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html) |
| opentofu | OpenTofu state | [OpenTofu state](https://opentofu.org/docs/language/state/) |
| pgvector | pgvector official repository | [pgvector official repository](https://github.com/pgvector/pgvector) |
| pinot | Apache Pinot architecture | [Apache Pinot architecture](https://docs.pinot.apache.org/architecture-and-concepts/concepts/architecture) |
| polars | Polars user guide | [Polars user guide](https://docs.pola.rs/) |
| postgis | PostGIS manual | [PostGIS manual](https://postgis.net/docs/) |
| postgres | PostgreSQL documentation | [PostgreSQL documentation](https://www.postgresql.org/docs/current/index.html) |
| prefect | Prefect flows | [Prefect flows](https://docs.prefect.io/v3/concepts/flows) |
| pubsub | Google Pub Sub overview | [Google Pub Sub overview](https://docs.cloud.google.com/pubsub/docs/overview) |
| pulumi | Pulumi infrastructure as code | [Pulumi infrastructure as code](https://www.pulumi.com/docs/iac/) |
| purview | Microsoft Purview governance | [Microsoft Purview governance](https://learn.microsoft.com/en-us/azure/purview/overview) |
| qdrant | Qdrant overview | [Qdrant overview](https://qdrant.tech/documentation/overview/) |
| redis | Redis data types | [Redis data types](https://redis.io/docs/latest/develop/data-types/) |
| snowflake-load | Snowflake data loading | [Snowflake data loading](https://docs.snowflake.com/en/user-guide/data-load-overview) |
| snowflake-share | Snowflake secure data sharing | [Snowflake secure data sharing](https://docs.snowflake.com/en/user-guide/data-sharing-intro) |
| snowflake-stream | Snowpipe Streaming | [Snowpipe Streaming](https://docs.snowflake.com/en/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview) |
| spark | Spark Structured Streaming | [Spark Structured Streaming](https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html) |
| tekton | Tekton Tasks and Pipelines | [Tekton Tasks and Pipelines](https://tekton.dev/docs/pipelines/) |
| terraform | Terraform state | [Terraform state](https://developer.hashicorp.com/terraform/language/state) |
| timescale | Timescale documentation | [Timescale documentation](https://www.tigerdata.com/docs/learn/hypertables/creating-and-configuring-hypertables) |
| trino | Trino documentation | [Trino documentation](https://trino.io/docs/current/) |
