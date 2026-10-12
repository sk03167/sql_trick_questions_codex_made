"""Coherent reference stacks, not certifications of every connector or service tier."""
def p(id,label,cloud,ingest,storage,compute,serve,benefit,caution,refs,k8s=False):
    return dict(id=id,label=label,cloud=cloud,ingest=ingest,storage=storage,compute=compute,serve=serve,
                benefit=benefit,caution=caution,refs=refs,k8s=k8s)

def profiles(s):
    mode=s['mode']; sid=s['id']
    if mode=='vm':
        return [p('azure-vm','Azure virtual machine lift and shift','azure','Database backup and log transport','Azure Blob backup archive','Restore SQL Server on Azure VM','Existing BI against SQL Server',
          'Keeps the engine and much of the existing package behavior while moving hosting.','Validate licenses, guest operating system, network identities, and unsupported external dependencies.',['azure-migrate']),
        p('aws-vm','AWS EC2 lift and shift','aws','Database backup and log transport','S3 backup archive','Restore SQL Server on EC2','Existing BI against SQL Server',
          'Preserves SQL Server semantics and lets infrastructure be reproduced.','AWS DMS is a separate replication option, not a replacement for engine and job restoration.',['aws-dms']),
        p('gcp-vm','Google Compute Engine lift and shift','gcp','Database backup and log transport','GCS backup archive','Restore SQL Server on GCE','Existing BI against SQL Server',
          'Separates the hosting move from a later logical warehouse redesign.','Confirm SQL Server licensing, operating-system support, domain connectivity, and restore bandwidth.',['gcp-migrate']),
        p('oci-vm','OCI Compute hosting alternative','oci','Engine-compatible backup transport','OCI Object Storage backups','Licensed matching engine on VM','Existing BI endpoint',
          'Can retain a matching engine when the organization already runs OCI.','Verify exact engine, VM image, support, licensing, and restore path; Oracle GoldenGate is not a generic VM mover.',['oci'])]
    if mode=='small':
        return [p('postgres','PostgreSQL with scheduled Python','oss','Python or Airbyte batch extractor','Versioned object files','SQL transformations in PostgreSQL','PostgreSQL analytical views',
          'A small number of components supports reproducible workloads and shared SQL access.','Separate operational and analytical capacity and test restore, concurrency, and disk growth.',['postgres','airbyte']),
        p('duckdb','DuckDB with object files','oss','Python HTTP and file extraction','Parquet object archive','DuckDB analytical job','Published tables or query service',
          'Efficient embedded analytics fits bounded workloads without a cluster.','Provide an explicit service and publication boundary; the embedded engine alone is not shared warehouse hosting.',['duckdb']),
        p('polars','Polars transforms with PostgreSQL serving','oss','Python extraction worker','Parquet object archive','Polars batch transformation','PostgreSQL or versioned Parquet',
          'Python-oriented transformations can run efficiently on one machine.','Benchmark memory and larger-than-memory behavior; reader and writer concurrency depend on the serving choice.',['polars','postgres']),
        p('bigquery-small','Managed warehouse for a small team','gcp','Cloud Run scheduled extractor','GCS immutable landing','BigQuery load and SQL','BigQuery curated datasets',
          'Managed query infrastructure reduces database administration for the team.','Control scans, concurrency, loading cost, credentials, and data-location settings.',['gcp-pipelines'])]
    if mode=='graph':
        return [p('aws-neptune','AWS Neptune graph serving','aws','CDC or file connector worker','S3 relationship archive','Spark identity and edge preparation','Neptune plus constrained query API',
          'Managed graph serving fits traversals over relationship data.','Choose and validate graph model, query language, load format, deletion semantics, and query limits.',['neptune']),
        p('azure-neo4j','Neo4j on Azure','azure','ADF files or CDC worker','ADLS raw relationships','Spark graph preparation','Neo4j service and query API',
          'Keeps graph-specific modeling separate from the analytical archive.','Choose licensed hosting or self-managed deployment and validate operational ownership.',['neo4j','adf']),
        p('gcp-neo4j','Neo4j on Google Cloud','gcp','Cloud Run or Dataflow ingestion','GCS raw relationships','Spark graph preparation','Neo4j service and query API',
          'Allows graph serving while retaining cloud storage and batch analytics.','Deployment, licensing, availability, and query authorization are independently designed.',['neo4j','dataflow']),
        p('oss-neo4j','Open source oriented graph platform','oss','Kafka Connect or batch workers','S3 compatible relationship archive','Spark entity matching','Neo4j plus constrained API',
          'Offers control of placement and connector behavior.','Neo4j feature availability depends on edition; self-hosting requires backups and operations.',['neo4j','kafka'],True)]
    if mode=='timeseries':
        return [p('aws-time','AWS hosted spatial and time analytics','aws','Kinesis with ingest worker','S3 telemetry archive','Flink normalization and aggregation','PostgreSQL with PostGIS or time engine',
          'A spatial database serves precise queries while cold history stays in object storage.','Confirm the selected hosted PostgreSQL extensions and time-engine features.',['postgis','flink']),
        p('azure-time','Azure spatial and telemetry analytics','azure','Event Hubs telemetry','ADLS telemetry archive','Spark normalization','PostgreSQL with PostGIS plus BI',
          'Uses durable event ingestion and a spatial query surface.','Keep event ordering, late corrections, and available extensions explicit.',['postgis','spark']),
        p('gcp-time','Google Cloud spatial analytics','gcp','Pub Sub with Dataflow','GCS telemetry archive','Dataflow validation and windows','BigQuery spatial SQL or PostGIS',
          'Managed stream processing and a SQL analytical endpoint support broad exploration.','Spatial functions and coordinate models must be reconciled with domain accuracy requirements.',['dataflow','postgis']),
        p('oss-time','Self hosted specialized time series','oss','Kafka telemetry','Parquet telemetry archive','Flink normalization','TimescaleDB or InfluxDB query API',
          'Specialized retention and time-oriented queries can fit telemetry workloads.','These engines are alternatives with different SQL, update, and spatial capabilities.',['timescale','influx','flink'],True)]
    if mode=='vector':
        return [p('azure-vector','Azure AI Search retrieval','azure','Document version ingestion worker','Blob originals and ACL manifest','Parsing and embedding jobs','Azure AI Search plus retrieval API',
          'Managed hybrid search provides a retrieval surface with structured filtering.','Validate permission enforcement, index quotas, embedding dimensions, and deletion propagation.',['azure-search']),
        p('aws-vector','AWS OpenSearch vector retrieval','aws','Document ingestion worker','S3 originals and ACL manifest','Container parsing and embedding','OpenSearch plus retrieval API',
          'Combines object storage with an index for text and vector search.','Index and tenant filtering must enforce the source ACL contract, not merely relevance.',['opensearch']),
        p('gcp-vector','Google Cloud hosted vector retrieval','gcp','Cloud Run document worker','GCS originals and ACL manifest','Container parsing and embedding','Qdrant or pgvector plus retrieval API',
          'An explicit hosted index preserves portability of the retrieval application.','This is a hosted software design, not a claim of native integration with every Google service.',['qdrant','pgvector']),
        p('db-vector','Databricks AI Search retrieval','azure','Document jobs and source metadata','Delta content and source versions','Databricks parsing and embeddings','Databricks AI Search plus API',
          'Keeps indexable content and transformations in the lakehouse ecosystem.','Formerly Vector Search; verify supported sync modes, permission model, and index behavior.',['databricks-vector','databricks-uc']),
        p('oss-vector','Open source retrieval services','oss','Document connector worker','Object originals and ACL manifest','Python parsing and embedding jobs','Qdrant or PostgreSQL pgvector',
          'Controls model selection and index deployment boundaries.','Capacity, backup, dimension migrations, and authorization belong to the operator.',['qdrant','pgvector'],True)]
    if mode=='search':
        return [p('aws-search','AWS OpenSearch log serving','aws','Kinesis or supported ingest agent','S3 permitted raw archive','Redaction and mapping worker','OpenSearch Dashboards and APIs',
          'Managed search infrastructure supports interactive operational investigation.','Choose mappings and supported ingest integrations explicitly; keep raw evidence elsewhere.',['opensearch']),
        p('azure-search','Azure log analytics serving','azure','Event Hubs or log collection','ADLS permitted raw archive','KQL ingestion or normalization','Azure Data Explorer or Fabric Eventhouse',
          'KQL-oriented serving fits operational logs and time-based exploration.','Choose Azure Data Explorer or Fabric capacity and deployment model deliberately.',['fabric-rti']),
        p('gcp-search','Elastic on Google Cloud','gcp','Pub Sub plus ingest worker','GCS permitted raw archive','Redaction and index transformation','Elasticsearch plus search APIs',
          'Separates durable history from a searchable derived index.','Verify the exact hosted Elastic offering, subscription features, and supported connectors.',['elastic']),
        p('oss-search','Self hosted OpenSearch or Elastic','oss','Fluent Bit or Kafka ingest','Object archive','Redaction and schema worker','Selected search engine APIs',
          'Allows deployment and plugin control where managed service limits do not fit.','Select one engine and compatible plugins; the alternatives are not protocol-identical.',['elastic','opensearch'],True)]
    base_mode=mode
    lake_modes={'lake','regional','recovery','hybrid','crosscloud','sharing','ml','unstructured'}
    streaming={'stream','olap','operational','features','edge'}
    is_lake=mode in lake_modes
    is_stream=mode in streaming
    data=[
      p('aws','AWS managed and native services','aws','Glue bounded extract','S3 replayable landing','Redshift loading and SQL dbt','Redshift governed marts',
        'Keeps extraction, storage, and warehouse operations in the AWS ecosystem.','Configure source support, warehouse type mapping, distribution, IAM, and realistic capacity.',['aws-analytics','dbt']),
      p('azure','Azure data services','azure','ADF Copy Activity','ADLS replayable landing','Synapse loading and SQL dbt','Synapse dedicated SQL marts',
        'ADF handles bounded movement while a SQL warehouse owns relational transformation.','Synapse dedicated SQL, serverless SQL, Databricks, and Fabric are distinct execution surfaces.',['adf','azure-analytics']),
      p('gcp','Google Cloud data services','gcp','Cloud Run bounded extractor','GCS replayable landing','BigQuery loading and SQL dbt','BigQuery governed marts',
        'Managed storage and SQL analytics fit scalable relational reporting.','Cloud Run extraction is an explicitly implemented worker; BigQuery load and streaming APIs differ.',['gcp-pipelines','dbt']),
      p('snowflake','Snowflake on AWS example','aws','Supported connector or extraction worker','S3 landing and source manifests','COPY into Snowflake plus SQL dbt','Snowflake governed marts',
        'A managed warehouse separates analytical compute from many source-specific extraction details.','Confirm source connector and account location; native Snowflake tables differ from external or managed Iceberg tables.',['snowflake-load','dbt']),
      p('databricks','Databricks on Azure example','azure','ADF files or bounded connector job','ADLS raw payload archive','Spark writes Delta Lake tables','Databricks SQL curated products',
        'One lakehouse compute ecosystem can process larger or less relational workloads.','Lakeflow Jobs orchestrates work; table-format, catalog, and runtime compatibility still require tests.',['databricks-jobs','delta','databricks-uc']),
      p('oss','Open source and self managed','oss','Airbyte or Python connector worker','S3 compatible raw storage','Spark writes Iceberg tables','Trino query API and BI',
        'Open interfaces provide placement flexibility and independent compute choices.','Operate catalogs, object storage, compute, credentials, and recovery; verify S3 API compatibility.',['airbyte','iceberg','trino'],True)
    ]
    if is_lake:
        data[0].update(compute='Glue or EMR Spark writes Iceberg',serve='Athena or Trino reads Iceberg',refs=['iceberg','aws-analytics'])
        data[1].update(compute='Databricks Spark writes Delta',serve='Databricks SQL reads Delta',refs=['delta','databricks-uc'])
        data[2].update(compute='Dataproc Spark writes Iceberg',serve='Trino reads GCS Iceberg tables',refs=['iceberg','trino','gcp-pipelines'])
        data[3].update(compute='COPY into native Snowflake tables',serve='Snowflake SQL with governed products',caution='This managed-warehouse alternative changes the storage and engine contract; evaluate Snowflake-managed Iceberg separately.',refs=['snowflake-load'])
        data.append(p('fabric','Microsoft Fabric platform alternative','azure','Fabric Data Factory pipelines','OneLake raw landing','Fabric Spark lakehouse tables','Fabric SQL endpoint and Power BI',
          'Integrated analytical workloads can simplify workspace-level operations.','Validate item Git support, deployment APIs, capacity, OneLake permissions, and lakehouse versus warehouse behavior.',['azure-analytics','fabric-rti']))
    if mode=='cdc':
        for x in data:
            x['ingest']={'aws':'AWS DMS source-specific CDC','azure':'Debezium worker and Kafka','gcp':'Datastream source-specific CDC','snowflake':'Verified CDC connector','databricks':'Debezium to Event Hubs Kafka API','oss':'Debezium with Kafka Connect'}[x['id']]
            x['compute']={'aws':'Spark applies sequenced changes','azure':'Spark applies sequenced changes','gcp':'CDC apply into BigQuery or Spark','snowflake':'Snowflake sequenced MERGE apply','databricks':'Spark sequenced Delta MERGE','oss':'Spark sequenced Iceberg MERGE'}[x['id']]
            x['caution']+=' Verify snapshot boundary, delete events, sequence ordering, source retention, and destination apply semantics.'
        # Data routes differ: durable change archive, then controlled application to a current-state sink.
        data[0]['serve']='Redshift via validated bulk or merge adapter'
        data[1]['serve']='Synapse via validated staging and apply adapter'
        data[2]['refs']+=['datastream'];data[0]['refs']+=['aws-dms'];data[1]['refs']+=['debezium']
    if mode in {'api','files','nosql-source','reverse'}:
        for x in data:
            if mode=='api':x['ingest']='ADF REST or custom API worker' if x['id']=='azure' else 'Quota-aware API connector worker'
            elif mode=='files':x['ingest']={'aws':'Transfer Family or file worker','azure':'ADF SFTP or file connector','gcp':'Storage Transfer or file worker'}.get(x['id'],'Versioned file connector worker')
            elif mode=='nosql-source':x['ingest']='Source-specific export and change worker'
            else:x.update(ingest='Versioned curated model extraction',compute='Desired-state diff and delivery worker',serve='Operational SaaS destination API')
            x['caution']+=' Source and destination capabilities are verified individually; the diagram implies no universal native connector.'
    if is_stream:
        for x in data:
            x['ingest']={'aws':'Kinesis Data Streams','azure':'Azure Event Hubs','gcp':'Google Pub Sub','snowflake':'Kafka durable event transport','databricks':'Event Hubs Kafka-compatible endpoint','oss':'Apache Kafka'}[x['id']]
            x['compute']={'aws':'Managed Apache Flink processing','azure':'Flink on AKS or Spark on Databricks','gcp':'Dataflow Apache Beam processing','snowflake':'External Flink plus sink adapter','databricks':'Spark Structured Streaming','oss':'Apache Flink processing'}[x['id']]
            x['serve']={'aws':'Curated events via sink adapter','azure':'Curated Delta or serving sink','gcp':'BigQuery via supported write adapter','snowflake':'Snowpipe Streaming and SQL marts','databricks':'Delta tables and Databricks SQL','oss':'Iceberg via compatible sink'}[x['id']]
            x['caution']+=' Bound state and define event-time and sink guarantees; checkpointing is not universal external exactly-once.'
            if x['id']=='azure':x['k8s']=True
            if x['id']=='aws':x['refs']+=['flink']
            if x['id']=='gcp':x['refs']+=['dataflow']
            if x['id']=='snowflake':x['refs']+=['snowflake-stream','flink']
    if mode=='olap':
        for x in data:
            x['serve']={'aws':'ClickHouse or Pinot query layer','azure':'Azure Data Explorer or Eventhouse','gcp':'BigQuery or hosted ClickHouse','snowflake':'Snowflake analytical query layer','databricks':'Databricks SQL or ClickHouse adapter','oss':'Pinot Druid or ClickHouse'}[x['id']]
            x['caution']+=' Each serving alternative needs a compatible write adapter and its own mutation and query contract.'
    if mode in {'operational','features'}:
        for x in data:
            x['serve']={'aws':'DynamoDB projection or features','azure':'Cosmos DB projection or Redis cache','gcp':'Bigtable projection or features','snowflake':'External Redis with outbound worker','databricks':'External online store via worker','oss':'Cassandra MongoDB or Redis'}[x['id']]
            if x['id']=='snowflake':x.update(ingest='Warehouse change or query polling',compute='Outbound projection worker',caution='Warehouse-centered alternative has additional refresh latency; do not claim it meets sub-second stream processing. Online serving remains external.')
            x['caution']+=' Select one serving database and validate partition keys, consistency, TTL, and conditional updates.'
    if mode=='hybrid':
        for x in data:
            x['ingest']='On premises approved aggregate worker'
            x['storage']=x['storage'].replace('raw','approved')+' only'
    if mode=='recovery':
        for x in data:
            x.update(ingest='Protected backup and replay manifest',compute='Restore data catalog grants and jobs',serve='Validated recovered consumer endpoint')
    if mode=='sharing':
        for x in data:
            x.update(ingest='Producer curated product release',compute='Policy-filtered share or export builder',serve='Authorized consumer query or copy')
            if x['id']=='snowflake':x['serve']='Snowflake Secure Data Sharing'
            if x['id']=='databricks':x['serve']='Delta Sharing authorized clients'
    if mode=='ml':
        for x in data:
            x['compute']+=' with point-in-time feature joins';x['serve']='Versioned offline features and training manifests'
    if mode=='unstructured':
        for x in data:
            x.update(ingest='Versioned document upload worker',compute='Container parsing OCR and extraction',serve='Structured metadata and derived features')
    if mode=='edge':
        for x in data:
            x['ingest']='Site-local durable spool and upload worker';x['caution']+=' Device acknowledgment and local buffer limits must be validated.'
    if sid in {'S02','S03','S11','S20','S25','S41','S43'}:
        data.append(p('oci','Oracle Cloud analytical alternative','oci','Verified file or GoldenGate adapter','OCI Object Storage landing','OCI Data Flow Spark or warehouse SQL','Autonomous Database warehouse workload',
          'Fits organizations with Oracle operational expertise and supported replication paths.','Confirm GoldenGate source/target support and distinguish Data Flow Spark from warehouse SQL execution.',['oci']))
        data.append(p('ibm','IBM hybrid lakehouse alternative','ibm','DataStage or custom connector','IBM Cloud Object Storage landing','Supported Spark or Presto transformation','watsonx.data analytical query layer',
          'Provides an alternative for IBM-centered or hybrid estates using supported open-table analytics.','Verify deployment edition, engine support, catalog, storage, and connector feature matrix.',['ibm']))
    return data

AUTOMATION=[
 dict(id='github',name='GitHub Actions',clouds=['*'],runtime='any',infra=['OpenTofu','Terraform','Pulumi'],benefit='Hosted or private runners with PR checks and environment-specific release jobs.',constraint='Use environment-bound short-lived cloud identity where supported; restrict token claims and trusted branches.',delivery='Provider CLI or API deploys the reviewed immutable job artifact; production gate records the artifact digest.'),
 dict(id='jenkins',name='Jenkins',clouds=['*'],runtime='any',infra=['Terraform','OpenTofu','Pulumi'],benefit='Private-network runners and shared libraries suit existing enterprise delivery estates.',constraint='Isolate agents, pin plugins and dependencies, and scope credentials to a job and environment.',delivery='A Jenkinsfile builds and tests once; a shared deploy library applies the reviewed artifact and records evidence.'),
 dict(id='gitlab',name='GitLab CI',clouds=['*'],runtime='any',infra=['Terraform','OpenTofu','Pulumi'],benefit='Merge-request tests, protected environments, and configurable runners keep delivery close to source control.',constraint='Use protected runners and environment permissions; identity federation depends on the target provider.',delivery='Stage-specific jobs publish an immutable artifact and invoke the chosen platform deployment adapter.'),
 dict(id='azure',name='Azure DevOps Pipelines',clouds=['azure'],runtime='any',infra=['Bicep','Terraform','Pulumi'],benefit='Native Azure delivery and enterprise service connections suit Azure-centered teams.',constraint='ADF factory resource deployment and pipeline definition publishing are separate lifecycle steps.',delivery='For ADF use validated factory artifacts and environment parameterization; for Databricks use bundles or the supported API.'),
 dict(id='aws',name='AWS CodePipeline and CodeBuild',clouds=['aws'],runtime='any',infra=['AWS CDK','Terraform','Pulumi'],benefit='Native AWS build roles and pipeline stages reduce cross-service identity plumbing.',constraint='Build VPC access, source connection, artifact encryption, and least-privilege deploy roles must be provisioned.',delivery='Publish job artifacts and apply the chosen AWS or warehouse deployment adapter; CDK synthesizes CloudFormation.'),
 dict(id='gcp',name='Google Cloud Build',clouds=['gcp'],runtime='any',infra=['Terraform','Pulumi','OpenTofu'],benefit='Containerized build steps integrate with Google service accounts and artifact storage.',constraint='Cloud Deploy has supported workload targets; data jobs require their actual job APIs rather than assumed generic support.',delivery='Build a job image or template and deploy through Dataflow, Composer, Cloud Run, or warehouse-specific interfaces.'),
 dict(id='argo',name='GitHub or GitLab build with Argo CD',clouds=['*'],runtime='k8s',infra=['OpenTofu','Terraform','Pulumi'],benefit='A reconciler promotes declared Kubernetes manifests and makes drift visible.',constraint='Argo CD reconciles Kubernetes resources; cloud infrastructure and managed warehouse DDL remain separately owned.',delivery='CI updates the reviewed image digest or Helm values in Git; Argo CD reconciles the selected namespace.'),
 dict(id='tekton',name='Tekton pipelines on Kubernetes',clouds=['*'],runtime='k8s',infra=['OpenTofu','Terraform','Pulumi'],benefit='Kubernetes-native task execution can fit a self-managed platform engineering estate.',constraint='Operators must manage cluster availability, runner permissions, artifact provenance, and secrets.',delivery='Pipeline tasks execute tests and platform-specific deploy steps; cloud resource state stays in the chosen IaC backend.')
]

def automation_options(profile):
    return [a for a in AUTOMATION if ('*' in a['clouds'] or profile['cloud'] in a['clouds']) and (a['runtime']=='any' or profile['k8s'])]

# Resolve every schematic reference path to one concrete technology per stage.
_original_profiles=profiles
def profiles(s):
    data=_original_profiles(s)
    replacements={
      'Glue or EMR Spark writes Iceberg':'EMR Spark writes Iceberg',
      'Athena or Trino reads Iceberg':'Athena reads Iceberg',
      'Airbyte or Python connector worker':'Airbyte connector worker',
      'ADF files or bounded connector job':'ADF bounded file ingestion',
      'ADF files or CDC worker':'Verified ingestion worker',
      'Cloud Run or Dataflow ingestion':'Cloud Run ingestion worker',
      'Kafka Connect or batch workers':'Kafka Connect ingestion worker',
      'PostgreSQL with PostGIS or time engine':'PostgreSQL with PostGIS',
      'BigQuery spatial SQL or PostGIS':'BigQuery spatial SQL',
      'TimescaleDB or InfluxDB query API':'TimescaleDB query API',
      'Qdrant or pgvector plus retrieval API':'Qdrant plus retrieval API',
      'Qdrant or PostgreSQL pgvector':'Qdrant plus retrieval API',
      'Cloud Run scheduled extractor':'Cloud Run scheduled extractor',
      'PostgreSQL or versioned Parquet':'PostgreSQL analytical views',
      'Kinesis or supported ingest agent':'Kinesis plus ingest worker',
      'Event Hubs or log collection':'Event Hubs ingestion',
      'KQL ingestion or normalization':'KQL ingestion normalization',
      'Azure Data Explorer or Fabric Eventhouse':'Azure Data Explorer query API',
      'Fluent Bit or Kafka ingest':'Fluent Bit with Kafka',
      'Selected search engine APIs':'OpenSearch query API',
      'Source-specific export and change worker':'Source-specific snapshot and change worker',
      'ADF REST or custom API worker':'ADF REST Copy with configured pagination',
      'ADF SFTP or file connector':'ADF SFTP Copy Activity',
      'Transfer Family or file worker':'AWS Transfer Family landing worker',
      'Storage Transfer or file worker':'Verified file transfer worker',
      'Flink on AKS or Spark on Databricks':'Apache Flink on AKS',
      'CDC apply into BigQuery or Spark':'Source-specific BigQuery CDC apply',
      'ClickHouse or Pinot query layer':'ClickHouse query API',
      'BigQuery or hosted ClickHouse':'BigQuery analytical query layer',
      'Databricks SQL or ClickHouse adapter':'Databricks SQL query endpoint',
      'Pinot Druid or ClickHouse':'Apache Pinot query API',
      'Cosmos DB projection or Redis cache':'Cosmos DB query projection',
      'Cassandra MongoDB or Redis':'Cassandra query projection',
      'OCI Data Flow Spark or warehouse SQL':'OCI Data Flow Spark and target load',
      'DataStage or custom connector':'Verified DataStage extraction',
      'Supported Spark or Presto transformation':'Supported Spark writes Iceberg',
      'Curated events via sink adapter':'Redshift via validated sink adapter',
      'Curated Delta or serving sink':'Azure Data Explorer via tested sink',
    }
    for x in data:
        for field in ('ingest','storage','compute','serve'):
            x[field]=replacements.get(x[field],x[field])
        if s['mode']=='features':
            if x['id']=='azure':x['serve']='Redis online feature store'
            if x['id']=='oss':x['serve']='Redis online feature store'
    return data

def data_variants(s,base):
    out=[dict(id='reference',name='Reference path',ingest=base['ingest'],storage=base['storage'],compute=base['compute'],serve=base['serve'],qualification=base['caution'])]
    mode=s['mode']
    # A compute+sink bundle prevents invalid independent format and engine mixing.
    if mode in {'warehouse','batch'}:
        out.append(dict(id='spark-load',name='External Spark with warehouse loading',ingest=base['ingest'],storage=base['storage'],compute='Spark transformation plus target-specific bulk loader',serve=base['serve'],qualification='Requires a runtime in the selected location, type mapping, a tested load adapter, and parity tests; changes compute cost and deployment artifacts.'))
    elif mode=='lake' and base['id'] not in {'snowflake','fabric','oci','ibm'}:
        out.append(dict(id='iceberg-trino',name='Iceberg with Spark and Trino',ingest=base['ingest'],storage=base['storage'],compute='Spark writes Iceberg with selected REST catalog',serve='Trino reads compatible Iceberg snapshots',qualification='Provision the engines and catalog explicitly; verify feature versions, credentials, delete handling, and concurrent writers.'))
        out.append(dict(id='delta-spark',name='Delta Lake with Spark query serving',ingest=base['ingest'],storage=base['storage'],compute='Spark writes Delta Lake tables',serve='Spark SQL through an explicit query service',qualification='This self-managed bundle needs an actual query endpoint; validate Delta protocol versions and supported object storage.'))
    elif mode in {'api','files'}:
        out.append(dict(id='custom-ingest',name='Custom bounded ingestion worker',ingest='Python API or file worker with durable manifest',storage=base['storage'],compute=base['compute'],serve=base['serve'],qualification='Implement authentication, paging or file completion, retries, checkpoints, and deletion semantics; retain the original output contract.'))
    elif mode in {'stream','olap'} and base['id'] in {'azure','databricks','oss','snowflake'}:
        out.append(dict(id='flink-kafka',name='Kafka protocol with Flink processing',ingest='Kafka or verified Kafka-compatible endpoint',storage=base['storage'],compute='Flink event-time processing plus sink adapter',serve=base['serve'],qualification='Verify endpoint protocol limitations, connector versions, watermark policy, checkpoint storage, and sink transaction semantics.'))
    elif mode=='vector':
        out.append(dict(id='pgvector',name='PostgreSQL with pgvector retrieval',ingest=base['ingest'],storage=base['storage'],compute=base['compute'],serve='PostgreSQL pgvector with authorized retrieval API',qualification='Provision supported extension and compute in the selected location; benchmark filtered recall, indexing, backups, and concurrent writes.'))
    return out

# Scenario-specific interfaces and benefits override generic platform examples.
_normalized_profiles=profiles
def profiles(s):
    data=_normalized_profiles(s)
    for x in data:
        mode=s['mode'];sid=s['id'];cloud=x['cloud'];pid=x['id']
        if mode in {'stream','olap','features','operational'}:
            x['benefit']={
              'aws':'Kinesis decouples producers and consumers, while managed Flink supplies recoverable stateful computation; the serving adapter exposes the selected consumer contract.',
              'azure':'Event Hubs buffers producer traffic and a Flink deployment on AKS controls event-time state and its serving adapter.',
              'gcp':'Pub/Sub decouples collection from Beam/Dataflow processing, with a supported write interface into the chosen serving store.',
              'snowflake':'An external event processor or outbound worker keeps source-specific logic separate from warehouse modeling and external serving.',
              'databricks':'Spark Structured Streaming and Delta tables align event processing with the lakehouse query ecosystem.',
              'oss':'Kafka retention and a Flink runtime provide explicit control over replay and state before publishing to a selected serving engine.'}[pid]
            x['caution']='Validate client protocol, partition ordering, event-time policy, checkpoint compatibility, archive completeness, sink acknowledgment and actual visible freshness. '+('The native data warehouse is not a point-lookup store or notification service; the external adapter remains required. ' if pid=='snowflake' else '')
            x['refs']=list(dict.fromkeys(x['refs']+[{'aws':'kinesis','azure':'eventhubs','gcp':'pubsub','snowflake':'snowflake-stream','databricks':'spark','oss':'kafka'}[pid],'flink' if pid not in {'gcp','databricks'} else ('dataflow' if pid=='gcp' else 'spark')]))
            x['archive_writer']={'aws':'Data Firehose delivery to S3','azure':'Event Hubs Capture to ADLS','gcp':'Dataflow archival branch to GCS','snowflake':'Kafka Connect object sink','databricks':'Event Hubs Capture to ADLS','oss':'Kafka Connect object sink'}[pid]
            if pid=='snowflake' and mode in {'features','operational'}:x['archive_writer']='Warehouse export worker with manifests'
        else:x['archive_writer']='Configured durable landing writer'
        if mode=='lake':
            x['benefit']='Durable objects retain replayable input; '+x['compute']+' creates a declared table contract and '+x['serve']+' provides the supported analytical query surface.'
        if mode=='cdc':
            x['benefit']=x['ingest']+' captures supported database changes while sequenced application and a raw archive separate recovery from current-state serving.'
            x['refs']=list(dict.fromkeys(x['refs']+['debezium']))
        if sid=='S05':
            x['ingest']='HDFS export with compatible Hadoop cloud connector'
            x['benefit']='Partition manifests and resumable HDFS export preserve provenance while the selected table and compute path removes dependence on local HDFS hosting.'
        if sid=='S17':
            x['source_override']='MongoDB replica set or sharded collections'
            x['ingest']='Debezium MongoDB with Kafka' if pid!='snowflake' else 'MongoDB change-stream extraction worker'
            x['compute']='Spark document normalization plus target loading' if pid not in {'snowflake','databricks','oss'} else ('Snowflake staged JSON normalization' if pid=='snowflake' else ('Spark document normalization to Delta' if pid=='databricks' else 'Spark document normalization to Iceberg'))
            x['benefit']='MongoDB change events retain document identity; explicit normalization creates analytical grains without flattening independent arrays into accidental cross products.'
            x['refs']=list(dict.fromkeys(x['refs']+['mongo','debezium-mongo']))
        if sid=='S18':
            if pid=='aws':x.update(source_override='DynamoDB items and export snapshot',ingest='DynamoDB export and Streams worker')
            elif pid=='azure':x.update(source_override='Cosmos DB items and selected feed mode',ingest='Cosmos snapshot and change-feed worker')
            elif pid=='gcp':x.update(source_override='Bigtable cells and change streams',ingest='Bigtable Dataflow change-stream pipeline')
            elif pid=='oss':x.update(source_override='Cassandra tables and CDC segments',ingest='Verified Cassandra CDC log reader')
            else:x.update(ingest='Selected NoSQL source-specific feed worker')
            x['compute']='Sequenced normalization plus target-specific apply'
            x['benefit']='The source-native snapshot and change interface controls operational read pressure; explicit normalization and sequence-aware apply create a reproducible analytical product.'
            x['refs']=list(dict.fromkeys(x['refs']+['dynamo','cosmos','bigtable','cassandra']))
        if sid in {'S14','S42'}:
            x['serve']={'aws':'DynamoDB operation ledger and delivery worker','azure':'Cosmos DB operation ledger and delivery worker','gcp':'PostgreSQL operation ledger and delivery worker','snowflake':'External operation ledger and delivery worker','databricks':'External operation ledger and delivery worker','oss':'PostgreSQL operation ledger and delivery worker'}[pid]
            x['benefit']+=' A durable operation ledger separates incident or action identity from retries of external notification delivery.'
        if mode=='edge':
            x['compute']='Spark deduplication of uploaded batches' if pid not in {'snowflake'} else 'Snowflake SQL deduplication of uploaded batches'
            x['benefit']='A durable site spool and central upload manifest preserve records across disconnection; batch deduplication controls reconnect bursts and repeated acknowledgments.'
        if mode=='hybrid':x['benefit']='Approved local aggregation reduces sensitive-data transfer, while cloud storage and query compute serve only the released products.'
        if mode=='recovery':x['benefit']='Recoverable manifests connect backups, metadata, identities, artifacts and progress state so the chosen platform can be reconstructed coherently.'
        if mode=='sharing':x['benefit']='A versioned producer product and explicit entitlement boundary give consumers an authorized query or delivered-copy contract.'
        if mode=='reverse':x['benefit']='A versioned desired-state diff and acknowledgment ledger make operational SaaS updates auditable and retryable.'
    for x in data:
        x['benefit']=x['benefit'].strip()
        x['caution']=x['caution'].strip()
    return data
