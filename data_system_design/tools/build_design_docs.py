from pathlib import Path
import json,re,textwrap,itertools
from scenarios import SCENARIOS
from profiles import profiles, data_variants, AUTOMATION, automation_options
from references import REFERENCES
BASE=Path(__file__).resolve().parent
OUT=BASE.parents[1] if BASE.name=='tools' else BASE/'output'
DOC=OUT/'data_system_design'
DIAGRAMS=[]

def table(headers,rows):
    def esc(v):return str(v).replace('|','\\|').replace('\n',' ')
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join('---' for _ in headers)+' |']+['| '+' | '.join(esc(v) for v in r)+' |' for r in rows])
def bullets(items):return '\n'.join('- '+x for x in items)
def numbered(items):return '\n'.join(f'{i}. {x}' for i,x in enumerate(items,1))
def cite(key):
    label,url=REFERENCES[key];return f'[{label}]({url})'
def filename(s):return s['id']+'-'+s['slug']+'.md'
def label(text):
    lines=textwrap.wrap(text,width=30,break_long_words=False,break_on_hyphens=False)
    return '<br/>'.join(lines).replace('"','&quot;').replace('& ','&amp; ')
def diagram(s,name,source,summary):
    id=s['id']+'-'+name
    dest=DOC/'diagrams'/f'{id}.mmd';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(source+'\n')
    DIAGRAMS.append(dict(id=id,scenario=s['id'],name=name,source=source,summary=summary,path=f'diagrams/{id}.mmd'))
    return f'{summary}\n\n```mermaid\n{source}\n```\n\n[Editable diagram source](../diagrams/{id}.mmd)'

def data_diagram(s,x):
    stream=s['mode'] in {'stream','olap','features','operational'} and x['id']!='snowflake' or s['mode'] in {'stream','olap'}
    source=x.get('source_override',s['source'])
    src=f'''flowchart TD
    source["{label(source)}"]
    ingest["{label(x['ingest'])}"]
    archive["{label(x['storage'])}"]
    process["{label(x['compute'])}"]
    gate["Validate the product contract"]
    serving["{label(x['serve'])}"]
    hold["Hold publication and investigate"]
    source -->|extract or publish| ingest
    ingest -->|archive through a configured writer| archive'''
    if stream:
        src=src.replace('    ingest -->|archive through a configured writer| archive',f'    archive_writer[\"{label(x["archive_writer"])}\"]\n    ingest -->|independent archive path| archive_writer\n    archive_writer -->|durable original records| archive')
        src+='\n    ingest -->|consume live records| process\n    archive -. replay archived records .-> process'
    else:src+='\n    archive -->|bounded input or restore| process'
    src+='\n    process -->|candidate output| gate\n    gate -->|accepted release| serving\n    gate -->|contract violated| hold'
    if s['mode'] in {'stream','olap','features','operational','cdc'}:
        src+='\n    state["Separate checkpoints and progress"]\n    process -. persist recoverable state .-> state'
    return src

def control_diagram(s):
    return '''flowchart TD
    owner["Product owner and policy contract"]
    metadata["Catalog lineage and classification"]
    iam["Engine and storage authorization"]
    infra["Versioned infrastructure definitions"]
    plan["Plan policy and permission tests"]
    apply["Environment-specific resource rollout"]
    audit["Runtime audits and access reviews"]
    owner -->|register intent| metadata
    owner -->|authorize required access| iam
    infra -->|review changes| plan
    iam -->|test actual enforcement| plan
    plan -->|accepted configuration| apply
    apply -->|collect evidence| audit
    metadata -. expected controls .-> audit'''

def delivery_diagram(s):
    return '''flowchart TD
    pr["Pull request and versioned contracts"]
    checks["Unit schema IaC and diagram checks"]
    artifact["Immutable reviewed artifact"]
    staging["Deploy into isolated staging"]
    probe["Integration parity and access tests"]
    production["Promote the same artifact"]
    verify["Observe product SLOs and correctness"]
    recovery["Rollback code or repair data safely"]
    pr -->|run CI| checks
    checks -->|build once| artifact
    artifact -->|deploy candidate| staging
    staging -->|exercise real interfaces| probe
    probe -->|release gate passes| production
    production -->|validate consumer boundary| verify
    verify -->|regression or failure| recovery'''

def sequence_diagram(s):
    if s['mode'] in {'vm','cdc','warehouse'} and s['family']=='Migration' or s['id']=='S06':
        return '''sequenceDiagram
    participant O as Old authoritative system
    participant M as Migration coordinator
    participant N as New target
    participant C as Consumers
    M->>O: Capture consistent snapshot and position
    O->>N: Bulk snapshot with manifests
    O->>N: Apply retained ongoing changes
    M->>N: Reconcile at an agreed checkpoint
    M->>O: Fence old writer or pause final ingestion
    O->>N: Apply final accepted changes
    M->>C: Switch the consumer endpoint
    C->>N: Read validated products
    Note over O,N: After target writes begin rollback needs reconciliation'''
    if s['mode'] in {'cdc','stream','olap','operational','features'}:
        return '''sequenceDiagram
    participant B as Replayable source
    participant P as Processor
    participant S as Serving sink
    participant K as Progress store
    B->>P: Event with stable identity and sequence
    P->>S: Idempotent or transactional write
    S-->>P: Durable acknowledgment
    P->>K: Persist compatible progress
    Note over P,K: Crash here can cause a replay
    B->>P: Deliver the event again after restart
    P->>S: Reapply with the same business identity
    S-->>P: Same visible business result
    Note over P,S: Arbitrary side effects need their own deduplication contract'''
    return None

def model_diagram(s):
    if s['id']=='S20':
        return 'model', """erDiagram
    DIM_CUSTOMER ||--o{ FACT_ORDER : attributes
    DIM_PRODUCT ||--o{ FACT_ORDER : describes
    DIM_CUSTOMER {
        bigint customer_sk PK
        string customer_business_key
        timestamp valid_from
        timestamp valid_to
        string segment
    }
    DIM_PRODUCT {
        bigint product_sk PK
        string product_business_key
    }
    FACT_ORDER {
        string order_line_id PK
        bigint customer_sk FK
        bigint product_sk FK
        timestamp event_time
        decimal amount
        string currency
    }""", 'The star model preserves order-line grain. Each fact resolves to one customer history version and one product; non-overlapping validity intervals prevent duplicate enrichment.'
    if s['id']=='S21':
        return 'model', """erDiagram
    ENTITY ||--o{ TEMPORAL_VERSION : has
    ENTITY {
        string entity_id PK
    }
    TEMPORAL_VERSION {
        string version_id PK
        string entity_id FK
        timestamp valid_from
        timestamp valid_to
        timestamp recorded_from
        timestamp recorded_to
        string correction_id
    }""", 'Business validity and system-recorded validity are separate intervals. Queries choose the perspective before joining versions, and interval constraints live in tested application or database logic.'
    if s['id']=='S28':
        return 'operation-state', """stateDiagram-v2
    [*] --> DesiredState
    DesiredState --> PendingDelivery: Versioned diff
    PendingDelivery --> Acknowledged: Destination confirms durable result
    PendingDelivery --> Retryable: Quota or temporary failure
    Retryable --> PendingDelivery: Same operation identity
    PendingDelivery --> NeedsReview: Permanent conflict
    NeedsReview --> PendingDelivery: Corrected authorized operation
    Acknowledged --> [*]""", 'The delivery ledger distinguishes desired state, attempted delivery and acknowledged destination state. Retries preserve operation identity instead of creating a new business update.'
    if s['id']=='S32':
        return 'model', """erDiagram
    LEDGER_POSTING ||--o{ MATCH_DECISION : evidence
    SETTLEMENT_LINE ||--o{ MATCH_DECISION : evidence
    LEDGER_POSTING {
        string posting_id PK
        string transaction_ref
        decimal amount
        string currency
        string source_release
    }
    SETTLEMENT_LINE {
        string line_id PK
        string settlement_batch
        decimal amount
        string currency
    }
    MATCH_DECISION {
        string decision_id PK
        string posting_id FK
        string line_id FK
        decimal allocated_amount
        string status
        string rule_version
    }""", 'Financial amounts and reconciliation decisions have separate grains. A partial match records an allocation with rule provenance; unmatched records remain visible. Currency and decimal precision are required.'
    if s['id']=='S35':
        return 'model', """erDiagram
    SOURCE_DOCUMENT ||--o{ CHUNK : contains
    CHUNK ||--o{ EMBEDDING : represents
    SOURCE_DOCUMENT {
        string document_version_id PK
        string source_uri
        string entitlement_version
        string content_hash
    }
    CHUNK {
        string chunk_id PK
        string document_version_id FK
        string parser_version
    }
    EMBEDDING {
        string embedding_id PK
        string chunk_id FK
        string model_version
        int dimensions
        string index_release
    }""", 'Document versions, chunks and embeddings retain explicit identity. Retrieval checks the current source entitlement contract, and re-embedding creates a controlled model/index version transition.'
    if s['id']=='S42':
        return 'outbox', """sequenceDiagram
    participant A as Application
    participant D as Source database
    participant C as Outbox CDC reader
    participant B as Replayable broker
    participant P as Consumer
    participant L as Operation ledger
    participant E as External destination
    A->>D: Commit business change and outbox row in one transaction
    C->>D: Read committed outbox changes
    C->>B: Publish stable operation identity
    B->>P: Deliver or redeliver operation
    P->>L: Register or claim idempotent operation
    P->>E: Request action with supported idempotency key
    E-->>P: Durable result or retryable failure
    P->>L: Persist acknowledged destination state
    Note over P,E: If the destination lacks idempotency use reconciliation and a declared delivery contract""", 'The source transaction atomically creates business state and its outbox record. Downstream delivery still needs destination-specific deduplication or reconciliation; the outbox alone does not make an arbitrary external action exactly once.'
    return None

CATALOG_ROWS=[
('Azure','Microsoft Purview discovery plus actual engine grants','Entra identities, Azure RBAC, storage ACLs and query roles','Private routing, managed identities, source-safe runtimes','Catalog visibility is not a universal storage deny policy.'),
('AWS','Glue Catalog and Lake Formation where integrated','IAM, supported Lake Formation grants, warehouse or service roles','VPC endpoints, KMS, workload IAM roles','Test direct S3 access and each engine integration separately.'),
('Google Cloud','Knowledge Catalog formerly Dataplex Universal Catalog','IAM, BigQuery policies, storage permissions, service-specific enforcement','Service accounts, approved regions, private connectivity','Metadata policy intent must be verified at the actual execution and export paths.'),
('Databricks','Unity Catalog plus product ownership and lineage','Unity Catalog grants and workspace or storage identities','Separate environments, locations, compute policies and progress state','Cataloged access can still be undermined by ungoverned direct storage credentials.'),
('Snowflake','Horizon catalog capabilities and versioned products','Roles, grants, policies and secure sharing contracts','Account location, integrations, workload sizing and resource budgets','Validate feature availability and distinguish native, shared, and open-table access paths.'),
('Open source or hybrid','OpenMetadata or DataHub plus a table catalog','Engine RBAC, cloud IAM, and supported policy integrations','Vault or cloud secrets, TLS, private endpoints and operational backup','Discovery tools do not automatically enforce permissions in every connector or engine.')
]

def swaps(s):
    mode=s['mode']
    rows=[
      ('Source engine','PostgreSQL, MySQL, SQL Server, Oracle, MongoDB, DynamoDB, Cosmos DB, Cassandra, Bigtable','Match the operational workload or an existing estate.','Rework snapshot consistency, keys, delete capture, source ordering, and schema contracts.','Run source-specific bootstrap, mutation, delete, and retention tests.'),
      ('Ingestion implementation','ADF, Glue workers, Airbyte, Fivetran, Informatica, Matillion, custom Python or Java workers','Trade connector maintenance against managed service cost and control.','Confirm endpoint support, network placement, source load, pagination or CDC envelopes, and acknowledgment rules.','Inject authentication, quota, partial-read, and retry failures.'),
      ('Object storage','S3, ADLS Gen2, GCS, OCI Object Storage, IBM Cloud Object Storage, supported S3-compatible stores','Change placement, cost structure, or existing cloud integration.','Adjust IAM, encryption, filesystem assumptions, request costs, lifecycle and egress; verify table-writer support.','Resume multipart transfers, deny unauthorized access, and test recovery from actual retained versions.'),
      ('Compute and transformation','Warehouse SQL with dbt, Spark, Flink, Beam on Dataflow, bounded Python with Polars or DuckDB','Fit relational, distributed, streaming, or bounded processing needs.','Rewrite runtime interfaces, date/type semantics, state handling, connector dependencies, and deployment artifacts.','Compare golden outputs plus load and restart behavior.'),
      ('Orchestration','ADF or Fabric pipelines, Airflow, Dagster, Prefect, Lakeflow Jobs, cloud-native workflow services','Choose dependency handling, asset visibility, existing skills, and operations ownership.','Keep stable progress identities, timezones, backfill boundaries, concurrency controls, and external job submission.','Parse definitions, fail upstream work, and verify safe retries and recovery.'),
      ('Serving','Snowflake, BigQuery, Redshift, Synapse, Fabric, Databricks SQL, Trino, ClickHouse, Pinot, Druid, purpose-built databases','Match consumer query shapes, freshness, concurrency, and operational read requirements.','Rework physical layout, query APIs, load adapters, tenant policies, mutations, and consumption models.','Benchmark actual consumer queries and reconcile output grain and precision.'),
      ('BI and metric interface','Power BI, Tableau, Looker, Superset, Metabase, Cube, dbt Semantic Layer','Fit analyst workflow, semantic reuse, and existing licensing.','Translate semantic definitions, caching, refresh mode, identity propagation, and certified metrics.','Compare metric parity and denied-user behavior across interfaces.')
    ]
    if mode in {'stream','olap','features','operational','edge','cdc'}:
        rows.insert(2,('Transport','Kafka or MSK, Confluent, Event Hubs, Kinesis, Pub Sub; MQTT or RabbitMQ for appropriate device/task handoffs','Choose replay, partitioning, managed operations, or device delivery needs.','Kafka API compatibility is limited by the endpoint; Kinesis and Pub Sub use different clients and ordering. MQTT/RabbitMQ need an explicit archive if replay is required.','Test retention exhaustion, key ordering, rebalance, redelivery, and broker failure.'))
    if mode in {'lake','cdc','regional','crosscloud','recovery','ml'}:
        rows.insert(4,('Table format and catalog','Delta Lake, Apache Iceberg, Apache Hudi; native warehouse tables as a redesign alternative','Choose mutation, snapshot, and multi-engine needs.','Migrate metadata, reader/writer protocols, compaction, deletes, schema evolution, and catalog authorization together; plain Parquet is not the same table contract.','Verify concurrent writes, snapshot reads, schema changes, and every selected engine.'))
    if mode in {'operational','features'}:
        rows.append(('Online serving database','DynamoDB, Cosmos DB, Bigtable, Cassandra, MongoDB, Redis','Fit partitioned lookups, document reads, consistency, and latency.','Design the new key schema, access patterns, TTL, atomic writes, and rebuild behavior; these are not interchangeable tables.','Replay reordered mutations; load hot keys; test stale reads and tenant isolation.'))
    if mode=='vector':rows.append(('Retrieval index','Azure AI Search, OpenSearch, Qdrant, pgvector, Databricks AI Search','Fit hybrid retrieval, filtering, operational boundaries, and existing data platforms.','Translate embedding dimensions, filter behavior, source ACLs, update/delete APIs, and index rebuild procedures.','Evaluate filtered relevance and verify denied and deleted chunks never appear.'))
    if mode=='graph':rows.append(('Graph store','Neo4j, Neptune, relational recursive SQL for suitable bounded workloads','Fit traversal and relationship modeling rather than conventional aggregation.','Map property-graph or RDF semantics, query languages, identity, edge versioning, and authorization.','Compare known paths, cycles, deleted entities, and high-degree performance.'))
    if mode=='vm':
        rows=[('Host and cloud','Azure VM, AWS EC2, Google Compute Engine, OCI Compute','Change data-center hosting while preserving the engine.','Validate supported VM images, licenses, network identity, disks, backup transport, and monitoring.','Restore representative backups and run original jobs and reports.'),
          ('Migration transport','Engine backup/log replay, supported native replication, verified migration services','Balance transfer duration, final catch-up, and compatibility.','Preserve a consistent recovery position and source log retention; offline appliances still need delta catch-up.','Inject disconnects, restore logs, reconcile totals, and rehearse writer fencing.'),
          ('Migration strategy','Lift and shift; managed database replatform; analytical warehouse redesign','Reduce compatibility risk now or deliberately modernize the platform.','Changing the engine changes SQL, jobs, grants, schema, and physical design; see S02 for replatforming.','Run SQL parity, data reconciliation, workload testing, and an updated rollback rehearsal.')]
    return rows

INFRA_ROWS=[
('Terraform','Broad provider ecosystem and declarative plans','Separate remote state by ownership and environment; secure and lock it; validate provider coverage.','Providers and resource APIs differ, so shared language does not mean identical modules.'),
('OpenTofu','Open-source-oriented declarative infrastructure workflow','Use explicit versions, tested providers, isolated state and encryption where configured.','Review migration and provider compatibility rather than assuming state interchange is universally safe.'),
('Pulumi','General-purpose language infrastructure definitions','Test programs, preview changes, protect state and secrets, and scope automation identities.','Language-level power needs disciplined reproducibility and resource ownership.'),
('Native cloud IaC','Bicep/ARM on Azure, CDK/CloudFormation on AWS, provider-specific declarative tools elsewhere','Keep environment parameters and identity controls explicit; import or manage existing resources carefully.','Native templates stay within their platform contract; job code and table data need separate lifecycle management.'),
('Configuration and GitOps','Ansible/Packer for hosts; Helm and Argo CD for supported Kubernetes workloads','Bake versioned images, apply least privilege, and keep cloud resources under a separately declared owner.','GitOps reconciliation of manifests is not an automatic warehouse schema or historical data migration.')
]

TECHNOLOGIES=[
('Ingestion','ADF and Fabric pipelines','Bounded movement and orchestration','Repeatable connectors and dependency control','Pipeline runs are not a generic continuously running Kafka consumer.','adf'),
('Ingestion','AWS DMS and Google Datastream','Supported database change capture','Reduce custom snapshot and log-reader work','Check exact source, target, schema, log retention, and delete contracts.','aws-dms'),
('Ingestion','Debezium and Kafka Connect','Source-specific log or change-stream capture','Stable envelopes and replayable integration','Connector and source configuration define images, ordering, and resume behavior.','debezium'),
('Ingestion','Airbyte and Fivetran','Supported source extraction','Reduce connector implementation and maintenance','Per-connector fidelity and delivery mode require verification.','airbyte'),
('Transport','Kafka MSK and Confluent','Partitioned retained event transport','Independent consumers and replay','Partition ordering is not global ordering or arbitrary-sink exactly-once.','kafka'),
('Transport','Kinesis Event Hubs and Pub Sub','Cloud-managed event transport','Provider integration and reduced broker administration','Clients, partition behavior, retention and APIs differ.','aws-analytics'),
('Device handoff','MQTT and RabbitMQ','Device messaging or task delivery','Fit connectivity or acknowledgment workflows','Do not assume long-term analytical replay without separate retention design.','aws-iot'),
('Storage','S3 ADLS GCS OCI and IBM object storage','Durable bytes and versioned archives','Independent storage and compute plus replay','Not a relational warehouse or table transaction manager.','aws-analytics'),
('Table format','Iceberg Delta Lake and Hudi','Table metadata snapshots and mutations','Transactional or incremental table behavior over files','Coordinate catalog, protocol, feature versions and readers/writers.','iceberg'),
('Compute','Spark and Databricks','Distributed transformation and supported streaming','Large joins, complex processing and lakehouse integration','Checkpoint and sink behavior determine delivery guarantees.','spark'),
('Compute','Flink','Stateful event-time stream computation','Fine-grained windows, state, and replay-aware processing','External end-to-end guarantees require compatible sinks and protocols.','flink'),
('Compute','Beam on Dataflow','Batch and stream pipeline model on a managed runner','Runner-managed scaling and supported event-time processing','Runner and connector capabilities must be validated.','dataflow'),
('Compute','Warehouse SQL with dbt','Relational ELT and model testing','Versioned transformations and dependency-aware models','dbt is not a universal extraction connector or transactional CDC reader.','dbt'),
('Compute','DuckDB and Polars','Bounded analytical processing','Efficient local or single-node jobs','Memory, disk, publication and concurrency boundaries remain explicit.','duckdb'),
('Warehouse','Snowflake BigQuery Redshift Synapse and Fabric Warehouse','Managed analytical SQL serving','Query-oriented physical execution and concurrency controls','They differ in DDL, SQL, loading, costs and authorization.','snowflake-load'),
('Lake query','Databricks SQL Trino Athena and Spark SQL','Query compatible lake tables','Read shared table products without all consumers sharing a compute runtime','Use a supported catalog, table protocol and query endpoint.','trino'),
('Realtime OLAP','ClickHouse Pinot Druid and KQL engines','Fast fresh aggregates and filtering','Specialized serving for analytical query shapes','Mutation, indexing, retention and approximation contracts differ.','clickhouse'),
('NoSQL serving','MongoDB DynamoDB Cosmos DB Cassandra Bigtable and Redis','Query-oriented application projections','Fit documents, partitioned lookup, wide columns or cache access','Access patterns, consistency, TTL and reconstruction are workload-specific.','mongo'),
('Search','Elasticsearch and OpenSearch','Derived document or log indexes','Full text and operational exploration','Keep a recovery archive and validate mappings, plugins and authorized access.','elastic'),
('Graph','Neo4j and Neptune','Relationship traversal','Fit path and neighborhood queries','Models, query languages, licenses and auth differ.','neptune'),
('Spatial and time','PostGIS TimescaleDB and InfluxDB','Specialized spatial or temporal predicates','Indexes, time-oriented layout and explicit domain semantics','Check units, coordinate models, corrections and selected hosted features.','postgis'),
('Feature definitions','Feast','Offline and online feature access contracts','Reusable feature views and point-in-time retrieval','It is not a general DAG orchestrator or a substitute for upstream feature computation.','feast'),
('ML provenance','MLflow','Experiment and model lifecycle metadata','Link artifacts, evaluations and releases','Data snapshots and label definitions need their own reproducible manifests.','mlflow'),
('Retrieval','Azure AI Search Qdrant pgvector and Databricks AI Search','Text/vector retrieval over authorized content','Support semantic or hybrid retrieval','Embedding version, filters, deletes and permission propagation remain mandatory.','azure-search'),
('Orchestration','Airflow Dagster Prefect and Lakeflow Jobs','Dependencies, job lifecycle and execution control','Repeatable schedules, retries, operational visibility','Orchestration progress is not proof of business data correctness.','airflow'),
('Governance','Purview Knowledge Catalog Unity Catalog Horizon OpenMetadata and DataHub','Discovery, ownership, lineage and product metadata','Make policy and provenance inspectable','Enforcement also needs actual engine and storage controls.','purview'),
('Delivery','GitHub Actions Jenkins GitLab Azure DevOps CodePipeline Cloud Build Argo CD and Tekton','Build test and release automation','Repeatable releases and environment evidence','Select identity and target-specific deployment adapters.','github'),
('Infrastructure','Terraform OpenTofu Pulumi and native IaC','Provision and track resource intent','Reviewable reproducible environments','Protect state, avoid overlapping owners, and test restore separately.','terraform'),
('Quality','dbt tests Great Expectations and custom invariants','Assert data contracts and product correctness','Detect invalid or stale products before publication','Tool success does not replace business reconciliation or denied-access tests.','dbt-tests'),
('Semantics','Power BI models LookML Cube and dbt Semantic Layer','Governed metric interpretation','Reuse business definitions across consumers','Validate nonadditive measures, cache policy, identity and version changes.','cube'),
('Reverse ETL','Hightouch or a custom destination worker','Controlled operational activation of curated data','Reduce API syncing work or gain precise delivery control','Define field authority, consent, deletes, idempotency and feedback-loop prevention.','hightouch')
]

def schedulers(s,x):
    if s['mode'] in {'stream','olap','features','operational'}:
        return ['Platform job lifecycle controller','Airflow submits and monitors continuous job','Dagster controls deployments and repair jobs']
    if s['mode']=='vm':return ['Existing SQL Agent or SSIS schedule','Airflow with existing-engine adapter','Prefect with existing-engine adapter']
    return ['Platform-native bounded schedule','Apache Airflow','Dagster','Prefect']

def native_gov(x):
    if x['id'].startswith('databricks') or x['id']=='db-vector':return 'Unity Catalog plus storage and service policies'
    if x['id']=='snowflake':return 'Snowflake roles and supported catalog policies'
    return {'aws':'AWS catalogs plus IAM and supported engine grants','azure':'Purview metadata plus actual engine and storage grants','gcp':'Knowledge Catalog metadata plus actual IAM and query policies','oss':'Table catalog plus engine roles and storage identities','oci':'OCI metadata and database plus storage identities','ibm':'IBM catalog and engine plus storage identities'}[x['cloud']]

def candidate_count(catalog):
    return sum(len(item['data_variants'])*len(item['schedulers'])*3*sum(len(a['infra']) for a in item['automation']) for item in catalog)

def build():
    DOC.mkdir(parents=True,exist_ok=True);(DOC/'scenarios').mkdir(exist_ok=True)
    catalog=[]
    for s in SCENARIOS:
        stack=profiles(s); seq=sequence_diagram(s)
        parts=[f"# {s['id']} {s['title']}",f"[Scenario index](../../DATA_SYSTEM_DESIGN_INDEX.md) · **Family:** {s['family']} · **Mode:** {s['mode']}",
          s['goal'],
          '## Requirements to clarify',
          'Confirm source versions and access, daily and peak volume, read versus write freshness, consumer query patterns, error tolerance, budget, operating skills, residency, retention, and recovery objectives. The numeric targets in this scenario are exercise assumptions, not vendor guarantees.',
          f"**Data grain:** {s['grain']}.\n\n**Identity and progress:** {s['key']}.",
          '## Data design',numbered(s['steps']),
          '### Correctness contract',bullets(s['invariants']),
          '### Complete technology paths',
          'These are proposed reference architectures, not exported vendor-certified deployments. Each path names concrete stages; when a worker or sink adapter is named, its connector configuration and code must be implemented and tested. The diagrams describe the data plane; operational deployment appears below.']
        for x in stack:
            dv=data_variants(s,x); auto=automation_options(x)
            item=dict(scenario=s['id'],scenario_file=f'scenarios/{filename(s)}',reference=x,data_variants=dv,schedulers=schedulers(s,x),governance=[native_gov(x),'OpenMetadata discovery plus the same engine and storage enforcement','DataHub discovery plus the same engine and storage enforcement'],automation=auto)
            catalog.append(item)
            parts.extend([f"#### {x['label']}",diagram(s,x['id'],data_diagram(s,x),f"Data moves through {x['ingest']}, retains recoverable input in {x['storage']}, and publishes through {x['serve']} after validation."),
              f"**Why this path helps:** {x['benefit']}\n\n**What must be designed and verified:** {x['caution']}",
              'Technology references: '+', '.join(cite(k) for k in dict.fromkeys(x['refs']))+'.'])
            if len(dv)>1:
                parts.extend(['Additional assembled data variants for this path:',table(['Variant','Compute and serving bundle','Required migration or verification'],[[v['name'],v['compute']+' → '+v['serve'],v['qualification']] for v in dv[1:]])])
        model=model_diagram(s)
        if model:
            name,src,summary=model
            parts.extend(['### Logical model or operation lifecycle',diagram(s,name,src,summary)])
        if seq:parts.extend(['### Order of critical operations',diagram(s,'sequence',seq,'This sequence exposes the boundary at which a crash, catch-up, or endpoint switch affects correctness. It is schematic; implement the contract with the selected source and sink protocols.')])
        parts.extend(['### Replace each component deliberately',table(['Component','Alternatives','Why change it','What changes','Test before switching'],swaps(s)),
          'A substitution is accepted only after the source protocol, input/output types, table format, catalog, region, identity, mutations, replay, and consumer API still meet the stated contract. Moving to a new cloud may also move network placement, keys, quotas, and cost ownership. A list of names alone is not a valid architecture.',
          '## Governance and infrastructure automation',
          '### Scenario governance rules',bullets(s['governance']),
          diagram(s,'governance',control_diagram(s),'Ownership and metadata describe the intended controls. Infrastructure automation deploys resources, and engine/storage permission tests prove enforcement at real access paths.'),
          '### Governance technology alternatives',table(['Platform','Catalog and ownership','Enforcement','Infrastructure controls','Boundary to test'],CATALOG_ROWS),
          'Discovery can be replaced with OpenMetadata or DataHub while keeping the same engine and storage enforcement. Source systems, object stores, query engines, exported copies, and caches are separate authorization surfaces. Instrument OpenLineage or native lineage where compatible; verify gaps instead of treating a catalog scan as complete operational lineage.',
          '### Infrastructure automation alternatives',table(['Approach','Benefit','Implementation requirements','Important boundary'],INFRA_ROWS),
          'Provision network paths, storage, catalogs, workload identities, secrets references, logging, backup, compute limits, and budgets before deploying jobs. Separate environments and remote state; do not commit state or credentials. Use explicit providers and versions, prevent two tools from owning the same resource, and test an isolated rebuild. For private sources, place a trusted runner or ingestion runtime on the reachable network; a CI runner location is a real architectural dependency.',
          '## Code delivery and runtime automation',diagram(s,'delivery',delivery_diagram(s),'CI builds and tests a release. CD deploys the same artifact, runtime orchestration controls execution, and consumer-level checks detect regressions after promotion.'),
          '### Delivery alternatives and compatible scope',table(['Delivery choice','Benefit','Scope for this scenario','Deployment and identity implications'],[[a['name'],a['benefit'],', '.join(x['label'] for x in stack if a in automation_options(x)) or 'Conditional: add a supported Kubernetes or native-cloud target before choosing this option',a['delivery']+' '+a['constraint']] for a in AUTOMATION]),
          '### Runtime and platform deployment differences',
          'SQL/dbt releases deploy model code plus controlled DDL and grants. Spark releases publish a tested wheel, JAR, container, or job definition. Flink releases must coordinate compatible state or savepoints before changing a job. ADF releases publish validated factory definitions with environment parameters and deliberate trigger handling. Databricks uses Declarative Automation Bundles or supported APIs; Fabric requires supported Git and deployment behavior per item. Kubernetes services use versioned manifests and image digests. The same CI tool can call these interfaces, but the interfaces are not interchangeable.',
          'Runtime choices: '+', '.join(dict.fromkeys(o for item in catalog if item['scenario']==s['id'] for o in item['schedulers']))+'. For a continuous stream, an orchestrator manages lifecycle and repair; it should not start a fresh consumer for every arriving message.',
          '### Safe promotion and rollback',
          'Build once, record the code and dependency versions, test an isolated deployment with realistic interfaces, then promote the same artifact. Use expand-and-contract schema changes and avoid coupling destructive data changes to an ordinary code rollback. A failed publication retains the last accepted product version and clearly exposes stale or partial status. ' + s['risks'][-1],
          '## Tests to run and automate',
          table(['Test','Automation and cadence','Evidence and failure action'],[[test, ['Deterministic fixture in CI; expensive restore or full-load variants before cutover','Isolated integration test before promotion and on connector upgrades','Failure or replay drill in an isolated environment on a scheduled cadence','End-to-end or representative workload exercise before major releases'][i], 'Persist inputs, artifact version, expected result and actual result. Block publication or promotion when the declared contract fails.'] for i,test in enumerate(s['tests'])]+[
            ['Permissions and tenant boundary','Automate authorized and denied reads on staging; rerun after policy changes','Test engine query, direct object access, exports and caches. A metadata-only permissions check is insufficient.'],
            ['Infrastructure and supply chain','Automate syntax, plan, policy, secret scanning and dependency checks on each PR','Reject unapproved region, broad IAM, exposed storage, overlapping ownership, or unexpected destructive changes.'],
            ['Data freshness and completeness','Continuously measure at the consumer boundary; compare periodic source manifests','Alert the owner and show stale or partial status. Job exit status is not the SLO.'],
            ['Recovery and business acceptance','Automate restore/replay evidence; schedule a supervised drill and business review','Record actual RPO/RTO, reconciled business totals and remaining exceptions. Full production drills need the operational change process.']]),
          '### What needs human judgment',
          'Automate repeatable fixtures, contracts, type/schema compatibility, data reconciliation, permission denial, infrastructure policy, load probes, and recovery evidence. Business owners still approve changed metric meaning, reconciliation tolerances, retention exceptions, and consumer acceptance. Security and operations review the intended policy and the consequences of a cutover; scripts produce evidence rather than defining policy by themselves.',
          '## Failure recovery and tradeoffs',bullets(s['risks']),
          'Preserve the exact input and output release manifests, progress positions, job versions, and validation evidence. Recovery starts from the last durable accepted boundary and uses a compatible source and sink. Coordinate live and repair writers; if a sink has changed after the saved checkpoint, reconcile or rebuild rather than assuming connection switching restores correctness.',
          '## Explore the documented combinations',
          f"```sh\npython3 data_system_design/tools/enumerate_designs.py --scenario {s['id']} --count\npython3 data_system_design/tools/enumerate_designs.py --scenario {s['id']} --limit 12\n```",
          'The enumerator expands the documented data bundles, runtime orchestration, metadata alternatives, eligible delivery systems, and their infrastructure tools. It rejects native-cloud delivery outside its cloud and Kubernetes delivery without a Kubernetes runtime. These are design candidates requiring the stated integration checks, not generated deployable infrastructure or proof that arbitrary products interoperate.',
          '## Source references',bullets(cite(k) for k in dict.fromkeys(s['refs']+['github','terraform','dbt-tests'])),
          '[Technology roles](../TECHNOLOGY_CHOICES.md) · [Automation recipes](../AUTOMATION_PLAYBOOK.md) · [Test patterns](../TESTING_PLAYBOOK.md) · [Compatibility rules](../COMPATIBILITY.md)'])
        (DOC/'scenarios'/filename(s)).write_text('\n\n'.join(parts)+'\n')
    (DOC/'design_candidates.json').write_text(json.dumps(catalog,indent=2)+'\n')
    (DOC/'diagram_manifest.json').write_text(json.dumps(DIAGRAMS,indent=2)+'\n')
    write_reference_docs(catalog)
    print(f'Generated {len(SCENARIOS)} scenarios, {len(catalog)} reference paths, {len(DIAGRAMS)} diagrams, {candidate_count(catalog)} assembled candidates.')

def write_reference_docs(catalog):
    index=[
      '# Data System Design Scenario Index',
      f"A scenario-based study and architecture library containing **{len(SCENARIOS)} scenarios**, **{len(catalog)} complete reference paths**, and **{len(DIAGRAMS)} diagrams**. The documented choices expand into **{candidate_count(catalog):,} assembled design candidates** with the included explorer.",
      'Each scenario explains the data grain, correctness contract, complete technology paths, per-component replacements, governance, infrastructure automation, code delivery, runtime orchestration, recovery, and tests to automate. Diagrams are schematic proposed designs, not deployed systems or vendor-certified integrations. All numerical workload targets are illustrative interview assumptions.',
      '## Read a scenario in this order',
      numbered(['Clarify the business purpose, consumer, source contract, and measurable service objectives.','Read the data grain and correctness rules before choosing technologies.','Compare the complete paths, then use component replacements to reason about alternatives.','Choose governance enforcement and infrastructure automation separately from processing.','Choose code delivery and runtime orchestration, then define test and recovery evidence.']),
      'GitHub renders the embedded Mermaid diagrams. Each diagram also has editable source in [data_system_design/diagrams](data_system_design/diagrams). For narrow screens, each view uses a vertical reading path and the surrounding text states its meaning. [Rendered examples](data_system_design/DIAGRAM_GALLERY.md) provide a static fallback.',
      '## Scenario documents',
      table(['ID','Scenario','Family','What the document adds','Reference paths','Diagrams'],[[s['id'],f"[{s['title']}](data_system_design/scenarios/{filename(s)})",s['family'],s['grain']+'; '+s['invariants'][0],len(profiles(s)),len([d for d in DIAGRAMS if d['scenario']==s['id']])] for s in SCENARIOS]),
      '## Technology and operating guides',
      table(['Document','Contents'],[
        ['[Technology choices](data_system_design/TECHNOLOGY_CHOICES.md)','Roles, why each technology family is needed, benefits, tradeoffs, cloud translations and decision questions.'],
        ['[Compatibility and combinations](data_system_design/COMPATIBILITY.md)','Bounded enumeration model, component contracts, valid bundles, conditional alternatives and rejected combinations.'],
        ['[Governance and infrastructure](data_system_design/GOVERNANCE_AND_INFRA.md)','Catalogs versus enforcement, IAM, network, encryption, data lifecycle, IaC state and deployment ownership.'],
        ['[Automation playbook](data_system_design/AUTOMATION_PLAYBOOK.md)','GitHub Actions, Jenkins, GitLab, Azure DevOps, AWS CodePipeline, Cloud Build, Argo CD and Tekton recipes.'],
        ['[Testing playbook](data_system_design/TESTING_PLAYBOOK.md)','Tests by lifecycle, unit and integration fixtures, reconciliation, fault injection, performance, access and recovery drills.'],
        ['[Diagram gallery](data_system_design/DIAGRAM_GALLERY.md)','Rendered samples, source locations, and regeneration commands.'],
        ['[Sources](data_system_design/SOURCES.md)','Primary vendor, cloud and open-source documentation.'],
        ['[Validation](data_system_design/VALIDATION.md)','Actual document, link, compatibility and diagram checks performed; proposed deployment tests are separate.']]),
      '## Cloud and platform coverage',
      'The principal examples cover AWS, Azure, Google Cloud, Snowflake on AWS, Databricks on Azure, and open-source/self-managed designs. Selected scenarios add Microsoft Fabric, Oracle Cloud, and IBM watsonx.data. Snowflake and Databricks are platforms deployed within supported cloud locations, not additional cloud providers. Their examples can move to another supported cloud only after storage, networking, identity, region, connector, and feature checks.',
      '## How to explore combinations',
      '```sh\npython3 data_system_design/tools/enumerate_designs.py --count\npython3 data_system_design/tools/enumerate_designs.py --scenario S12 --cloud aws --limit 12\npython3 data_system_design/tools/enumerate_designs.py --scenario S03 --all --output /tmp/S03-designs.jsonl\npython3 data_system_design/tools/validate_design_docs.py\n```',
      'There is no finite exhaustive list of every possible workload, vendor release, deployment topology, or product combination. This library makes the covered scenarios and dimensions explicit, explains additional substitutions, and exhaustively expands its documented choices. It does not describe an arbitrary Cartesian product as a compatible deployment. Use pairwise integration checks and workload proofs for the chosen complete architecture.',
      '## Suggested study routes',
      '- Migration: S01 → S02 → S05 → S06 → S23 → S39.\n- Batch and modeling: S08 → S09 → S10 → S11 → S20 → S21 → S31.\n- Streaming: S07 → S12 → S13 → S14 → S15 → S30 → S42.\n- NoSQL and specialized serving: S17 → S18 → S19 → S16 → S35 → S36 → S37.\n- Governance and platform operations: S22 → S24 → S25 → S26 → S27 → S40 → S41.\n- Business and ML: S28 → S29 → S30 → S32 → S33 → S34 → S43.',
      'Research date: October 12, 2026. Keep product versions, supported connectors, regional availability, editions, limits, and prices current before implementation. Former names are noted where useful; Google Knowledge Catalog was formerly Dataplex Universal Catalog, and Databricks Declarative Automation Bundles were formerly Asset Bundles.']
    (OUT/'DATA_SYSTEM_DESIGN_INDEX.md').write_text('\n\n'.join(index)+'\n')
    tech=[ '# Data Technology Choices and Benefits',
      '[Scenario index](../DATA_SYSTEM_DESIGN_INDEX.md)',
      'Choose a component because it satisfies a measurable contract. A cloud name is a placement decision; a broker transports events; an object store retains bytes; a table format supplies table semantics; compute transforms records; a serving engine answers consumer queries. These roles should remain distinct even when one platform provides several.',
      table(['Role','Technologies','Need','Benefit','Tradeoff or boundary','Reference'],[[*r[:5],cite(r[5])] for r in TECHNOLOGIES]),
      '## Cloud translations',
      table(['Role','AWS','Azure','Google Cloud','Independent or self managed'],[
        ['Durable bytes','S3','ADLS Gen2 or Blob','Cloud Storage','Supported S3-compatible storage or other approved object store'],
        ['Retained event transport','Kinesis or MSK','Event Hubs','Pub/Sub','Kafka or Confluent with appropriate hosting'],
        ['Database CDC','DMS for supported pairs','Source-specific Debezium or supported ADF CDC path','Datastream for supported sources','Debezium or verified engine-specific tooling'],
        ['Batch orchestration','MWAA/Airflow or Step Functions with actual job APIs','ADF/Fabric pipelines or Lakeflow Jobs','Cloud Composer/Airflow or Workflows with actual job APIs','Airflow Dagster or Prefect'],
        ['Distributed compute','EMR or Glue Spark; Managed Flink','Databricks Spark; Flink on appropriate hosting','Dataproc Spark; Beam/Dataflow','Spark Flink or supported Python runtimes'],
        ['Analytical SQL','Redshift Athena or supported lake query layer','Synapse Fabric or Databricks SQL','BigQuery or supported lake query layer','Snowflake on supported clouds; Trino ClickHouse PostgreSQL'],
        ['Metadata and discovery','Glue Catalog and integrated Lake Formation','Purview plus platform catalogs','Knowledge Catalog','Unity Catalog Horizon OpenMetadata DataHub and format catalogs'],
        ['Infrastructure','Terraform/OpenTofu/Pulumi or CDK/CloudFormation','Terraform/OpenTofu/Pulumi or Bicep/ARM','Terraform/OpenTofu/Pulumi and supported provider tools','Chosen providers, Helm/Argo CD for Kubernetes, Ansible/Packer for hosts']]),
      '## Component selection questions',numbered(['What source contract and consumer latency are required? Distinguish event-time processing from periodic refresh.','Is the state append-only, mutable, historical, or query-oriented? What does a delete mean?','Who owns connectors, runtimes, table catalogs, credentials, retention, and outages?','What must be replayable or restorable? How long do source logs and snapshots survive?','Which interfaces and table features are supported by the exact chosen engines?','How will correctness, security, cost, and recovery be measured before and after a substitution?']),
      '## Format and deployment are separate choices',
      'CSV/JSON/Avro/Protobuf describe serialization or record formats. Parquet/ORC describe columnar files. Delta Lake/Iceberg/Hudi describe table metadata and mutation protocols over files. S3/ADLS/GCS are storage systems. Native warehouse tables have their own managed storage and execution contracts. A compatible reader for one combination is not proof that every writer, delete mode, schema feature, catalog, or security control also works.',
      'A managed connector shifts operational work; it does not remove the need to test its exact source, target, snapshot, delete and schema behavior. A self-managed stack gives more placement control while retaining operations, patching and restore responsibility. Costs include compute, storage, requests, egress, licensing, and engineering time.']
    (DOC/'TECHNOLOGY_CHOICES.md').write_text('\n\n'.join(tech)+'\n')
    compatibility='''# Compatibility and Combination Rules

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
'''
    (DOC/'COMPATIBILITY.md').write_text(compatibility)
    governance=['# Governance and Infrastructure Automation',
      '[Scenario index](../DATA_SYSTEM_DESIGN_INDEX.md)',
      'Every scenario needs both an ownership policy and technical enforcement. Ownership answers who defines the product, responds to failures, authorizes access, and accepts retention or semantic changes. Enforcement happens where records can be read, written, copied, cached, indexed, or restored.',
      table(['Platform','Discovery and metadata','Enforcement','Infrastructure controls','Boundary'],CATALOG_ROWS),
      '## Lifecycle controls',
      table(['Lifecycle','Control','Automated evidence'],[
       ['Collection','Approved purpose, source scope, stable schema and minimization','Contract validation and field classification checks'],
       ['Storage','Restricted raw zones, encryption, keys, access grants and retention','Denied-access probes, configuration policies and object inventories'],
       ['Processing','Workload identities, approved fields and protected checkpoints','Identity scope tests, state-location checks and lineage events'],
       ['Serving','Tenant or row policies, metric ownership and consumer contracts','Golden queries, tenant-denial tests and API authorization probes'],
       ['Copies and indexes','Propagate permissions, deletion and allowed downstream purpose','Cross-store erasure manifests and restricted-document retrieval tests'],
       ['Backups and restore','Protected recovery copies and reapplication of current policy','Isolated restore drill and post-restore permission validation'],
       ['Decommission','Stop writers, revoke credentials and dispose of retained copies by policy','Dependency audit, revoked-access test and deletion evidence']]),
      '## Infrastructure ownership',table(['Approach','Benefit','Implementation requirements','Boundary'],INFRA_ROWS),
      'Separate root ownership for networking and identities, data resources and catalogs, and job/application deployments. Do not let Terraform, a cloud template, and a manual console change all manage the same resource without a declared ownership transition. Import existing resources deliberately. Lock and secure remote state; state and plans can contain sensitive configuration. '+cite('terraform')+', '+cite('opentofu')+', '+cite('pulumi')+'.',
      '## Minimum environment contract',
      bullets(['Private-source connectivity and a trusted runtime or runner location.','Approved region, data classification, and permitted replication destination.','Distinct workload identity, service grants, and secrets references for each environment.','Versioned object prefixes, table/catalog namespaces, stream groups, and checkpoint locations.','Compute quotas, workload isolation, budgets, logs, audit trails, and consumer-level SLOs.','Backup and replay retention, recovery manifests, and periodic restore evidence.']),
      '## Privacy deletion is an engineering workflow',
      'Inventory every raw copy, current-state table, historical version, training dataset, cache, search/vector index, export, and recovery copy. Define where erasure versus restricted retention applies. Carry the request identity and record acknowledgments per store; test that a backfill or restore cannot reintroduce a prohibited entity. Encryption alone does not perform logical erasure of all derived copies.',
      '## Governance permutations',
      'A cloud-native catalog with engine grants can be combined with any eligible CI and IaC recipe. OpenMetadata or DataHub can replace the discovery layer while keeping actual engine/storage policies. Unity Catalog and Snowflake roles belong to their platform execution boundaries. Lake Formation applies through supported integrations and permissions. Knowledge Catalog and Purview provide metadata and governance capabilities whose enforcement scope must be verified for the concrete paths. A cross-cloud discovery layer does not magically unify every provider IAM policy.',
      'Primary references: '+', '.join(cite(k) for k in ['purview','gcp-catalog','lakeformation','databricks-uc','openmetadata','datahub'])+'.']
    (DOC/'GOVERNANCE_AND_INFRA.md').write_text('\n\n'.join(governance)+'\n')
    write_automation()
    write_testing()
    source_rows=[[key,label,url] for key,(label,url) in sorted(REFERENCES.items())]
    (DOC/'SOURCES.md').write_text('# Primary Documentation Sources\n\n[Scenario index](../DATA_SYSTEM_DESIGN_INDEX.md)\n\nResearch date: October 12, 2026. These links describe components and platform contracts. Scenario designs and combinations are original proposed applications of those contracts; references do not certify a whole generated architecture. Product versions, editions, availability and limits must be checked for a real deployment.\n\n'+table(['Key','Documentation','Link'],[[k,l,f'[{l}]({u})'] for k,l,u in source_rows])+'\n')
    if not (DOC/'DIAGRAM_GALLERY.md').exists():
        (DOC/'DIAGRAM_GALLERY.md').write_text('# Architecture Diagram Gallery\n\nRendering is pending. All editable Mermaid sources are in diagrams and embedded in the scenario documents.\n')
    if not (DOC/'VALIDATION.md').exists():
        (DOC/'VALIDATION.md').write_text('# Data Design Catalog Validation\n\nValidation is pending. Run the document and diagram validators.\n')

def write_automation():
    parts=['# Code Delivery and Runtime Automation Playbook',
      '[Scenario index](../DATA_SYSTEM_DESIGN_INDEX.md)',
      'Delivery automation builds, tests, and promotes code. Infrastructure automation provisions resources. Runtime orchestration controls jobs and dependencies. Data-quality automation measures actual products. Separate these responsibilities even if one platform hosts several.',
      table(['Delivery system','Benefit','Infrastructure alternatives','Target deployment','Required identity or runtime boundary'],[[a['name'],a['benefit'],', '.join(a['infra']),a['delivery'],a['constraint']] for a in AUTOMATION]),
      '## Release lifecycle',numbered(['A PR changes source code, configuration, contracts, tests, diagrams, and IaC intent together.','Run fast deterministic unit and contract tests plus plan/policy and dependency checks.','Build a wheel, JAR, container, compiled SQL/dbt project, or platform artifact once and record its digest.','Deploy that artifact to isolated staging with environment-specific identities and parameters.','Run real-interface integration, permissions, replay, reconciliation, and representative workload probes.','Promote the same artifact using the organization release policy. Keep stateful job migration and destructive DDL separate.','Observe consumer freshness, completeness and business totals; stop or repair publication if the contract regresses.']),
      '## GitHub Actions example for this documentation repository',
      'This runnable example validates the study documents only. It does not deploy cloud resources or process production data. A real platform pipeline adds the selected build, IaC-plan, staging, target-specific deploy and product-validation jobs. OIDC should scope any cloud role to the approved repository, workflow, branch and environment. '+cite('github')+'.',
      '''```yaml
name: Design documentation checks
on:
  pull_request:
    paths: ["data_system_design/**", "DATA_SYSTEM_DESIGN_INDEX.md"]
  push:
    branches: [data-system-design-questions]
    paths: ["data_system_design/**", "DATA_SYSTEM_DESIGN_INDEX.md"]
permissions:
  contents: read
jobs:
  documents:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate catalog and compatibility rules
        run: python3 data_system_design/tools/validate_design_docs.py
```
''',
      'Pin trusted action releases to reviewed commit SHAs in a production workflow. Untrusted PR code must not obtain deployment credentials or run on a broadly privileged private runner.',
      '## Jenkins example',
      'This Jenkinsfile runs the same documentation gate on a configured Python agent. In a real platform add immutable artifact publication, selected IaC preview, staging tests, controlled deployment and post-release probes; use scoped agents and a reviewed shared library. '+cite('jenkins')+'.',
      '''```groovy
pipeline {
  agent any
  options { disableConcurrentBuilds() }
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Document and compatibility checks') {
      steps { sh 'python3 data_system_design/tools/validate_design_docs.py' }
    }
  }
}
```
''',
      '## GitLab CI example',
      'The agent or image must contain the chosen Python version. Add target-specific deployment stages separately and keep protected environment credentials out of untrusted merge-request jobs. '+cite('gitlab')+'.',
      '''```yaml
stages: [test]
design_catalog:
  stage: test
  image: python:3.12-slim
  script:
    - python3 data_system_design/tools/validate_design_docs.py
```
''',
      '## Native cloud and GitOps translations',
      table(['Target','Translation','Boundary'],[
        ['Azure DevOps','Use script tasks for identical gates; deploy Bicep/ARM or selected Terraform/Pulumi; use supported ADF artifacts, Databricks bundles or Fabric item deployment.','Deploy identities and private agents deliberately; preserve checkpoints and trigger behavior.'],
        ['AWS CodePipeline/CodeBuild','Use a buildspec to run gates, publish to the artifact store, and execute selected CDK/CloudFormation or provider deployment steps.','The build role, network paths and actual job APIs remain part of the architecture.'],
        ['Google Cloud Build','Use container steps for gates, artifact builds and selected resource/job APIs.','Cloud Deploy is not assumed to deploy every data-platform item.'],
        ['Argo CD','CI publishes a reviewed image digest and manifests; Argo CD reconciles Kubernetes resources.','Managed warehouses, cloud network state and historical data are separately managed.'],
        ['Tekton','Represent build/test/deploy as Kubernetes tasks with scoped workload identities.','You own the cluster, pipeline controller, artifact store and recovery.']]),
      '## Platform artifact differences',
      table(['Platform artifact','Deploy mechanism','Additional release test'],[
        ['SQL/dbt model','Supported warehouse adapter plus migration or grants workflow','SQL/type parity, downstream golden queries and expand-and-contract schema checks'],
        ['Spark batch job','Wheel/JAR/container plus job definition','Runtime dependencies, partition correctness and idempotent retry'],
        ['Flink stream job','JAR/container plus controlled state/savepoint transition','State serializer compatibility and crash-after-sink-commit replay'],
        ['ADF factory','Supported publish/build artifact plus environment deployment','Linked service resolution, parameters, trigger handling and stable progress identities'],
        ['Databricks assets','Declarative Automation Bundles and supported CLI/API','Validate/deploy/run in staging; verify permissions, source paths and checkpoint separation'],
        ['Fabric assets','Supported item Git/deployment APIs and environment configuration','Verify per-item support, capacity, bindings, permissions and actual runtime execution'],
        ['Kubernetes service','Helm or manifests with an immutable image digest','Readiness, rollback, workload identity and external service connectivity']]),
      'Databricks Declarative Automation Bundles were formerly called Databricks Asset Bundles. Bundle definitions and platform APIs have their own compatibility requirements. '+cite('databricks-bundles')+'. ADF CI/CD uses factory definitions and environment deployment artifacts; a Git push alone does not prove successful runtime execution. '+cite('azure-ci')+'.',
      '## Pairwise automation selection',
      'Choose one deployment owner per resource. CI can invoke Terraform, OpenTofu, Pulumi, or a supported native tool, and then call a platform-specific job deployment adapter. Governance tests remain mandatory regardless of the CI engine. For Kubernetes choose GitOps only for the resources it actually reconciles. Plan artifacts, logs and state must use an approved access and retention policy.',
      '## Rollback data and code separately',
      'Reverting a Git commit does not undo already-published tables, external API updates, erased data, incompatible stream state, or warehouse DDL. Retain recoverable release manifests and use a scenario-specific repair or replay path. For changes that cannot be safely reversed, prefer an explicit forward fix or shadow rebuild with verified consumer cutover.']
    (DOC/'AUTOMATION_PLAYBOOK.md').write_text('\n\n'.join(parts)+'\n')

def write_testing():
    parts=['# Data Platform Testing Playbook',
      '[Scenario index](../DATA_SYSTEM_DESIGN_INDEX.md)',
      'Test the product contract and failure boundaries, not only whether a job ran. The scenario documents propose workload-specific tests. This guide shows where to automate them and what evidence to retain; these are proposed platform tests, not claims that cloud deployments were executed for this catalog.',
      table(['Stage','Tests','Cadence','Evidence'],[
        ['Local and PR','Pure transforms, keys, business arithmetic, schema compatibility, SQL fixtures, DAG parse, diagram syntax, IaC policies','Every change','Deterministic fixtures, expected rows, artifact commit and failing contract'],
        ['Staging integration','Actual connectors, loading, grants, source snapshots, deletes, API pagination, sink acknowledgments','Before promotion and on connector/runtime upgrades','Source/target checkpoints, input manifests, logs, row-level and business-level comparisons'],
        ['State and failure','Duplicate replay, out-of-order delivery, broker rebalance, crash before/after sink commit, checkpoint recovery','Targeted fixtures each release; isolated scheduled fault drills','Injected fault position and externally visible state before and after recovery'],
        ['Performance and cost','Skew, hot keys, expected concurrency, backlog catch-up, cold/warm cache, file sizes and egress','Major changes and periodic representative runs','Data volume, distribution, query classes, latency percentiles and cost per processed unit'],
        ['Security','Allowed/denied queries, tenant boundaries, direct-storage bypass, source ACL propagation, runner identity','PR policies plus staging/runtime probes','Identity, requested action, expected allow/deny, actual access decision'],
        ['Continuous product checks','Freshness, completeness, schema drift, key integrity, semantic invariants and volume anomalies','Every publish and continuously where appropriate','Consumer timestamp, source cutoff, completeness manifest and product release'],
        ['Recovery','Protected copy restore, catalog/grant restore, checkpoint/source retention compatibility, RPO/RTO','Isolated regular drill and supervised production exercise when approved','Recovered data point, elapsed time, job version, reconciled outputs and deviations']]),
      '## High value fixture patterns',
      table(['Pattern','Fixture','Required observation'],[
        ['Idempotency','Deliver the same stable event or file version twice','Business state and totals stay unchanged after the second application.'],
        ['Delete ordering','Apply delete sequence 20, then replay update sequence 19','The entity stays deleted.'],
        ['Snapshot continuity','Update and delete keys while a historical snapshot is loading','The converged state matches the source at the agreed checkpoint.'],
        ['Late event time','Deliver a record before and after the configured watermark threshold','Both outcomes follow the declared late-data policy and are visible in evidence.'],
        ['One-to-many joins','Two payments and three adjustments for one order','Totals use the intended grain without multiplying amounts.'],
        ['Schema drift','Rename or remove a field and introduce incompatible types','Breaking data is rejected, quarantined or deliberately migrated; no silent coercion.'],
        ['Tenant isolation','Run equivalent reads as permitted and denied tenant identities','Every query, export, cache and storage path enforces the intended boundary.'],
        ['Temporal truth','Change a dimension after a prediction or historical event time','The historical or point-in-time join does not use future information.'],
        ['Atomic publish','Crash between staging and release visibility','Consumers see one accepted release or clearly marked partial/stale state.'],
        ['Recovery','Restore data with a catalog and stream checkpoint from different times','The process detects inconsistency or performs a controlled reconstruction.']]),
      '## Reconciliation depth',
      'Compare schema and type interpretation, primary-key sets, duplicate counts, expected partition coverage, selected record-level values, and grouped business totals. Counts alone can agree while keys or amounts are wrong. Hashes require canonicalization of NULLs, decimals, timezones and field order. Compare against a declared source checkpoint so live source changes do not look like ingestion errors.',
      '## Automation technologies',
      'Use pytest/JUnit or appropriate language frameworks for deterministic transformations and client behavior; dbt data tests for warehouse assertions; Great Expectations or equivalent for data contracts; SQL and independent reference oracles for reconciliation; Testcontainers or isolated services for real interfaces; cloud policy checks and explicit denied-access probes for authorization. Fault and load tools must exercise the real contracts of the selected broker, compute and sink. '+cite('dbt-tests')+', '+cite('gx')+'.',
      '## What should not be a blind automated claim',
      'Do not treat SDK mocks as proof of real API quota, network, authentication or connector compatibility. Do not treat catalog scans as permission enforcement. Do not treat average load as proof of hot-key or peak behavior. Do not label arbitrary side effects exactly-once because the stream processor has checkpoints. Do not call a backup usable without a successful restore.',
      '## Human acceptance',
      'Business owners define semantic equivalence and reconciliation tolerance. Operators assess cutover and rollback consequences. Security and data owners assess purpose, retention, access, and location. Automation supplies repeatable evidence and blocks declared contract failures; it does not silently choose those organizational policies.',
      '## This repository verification',
      'The included validators check document completeness, source/diagram links, diagram identity, enumeration rules and candidate metadata. The diagram runner parses and renders Mermaid. Those tests do not connect to cloud services, test real workloads, or prove benchmark targets. See [actual validation results](VALIDATION.md).']
    (DOC/'TESTING_PLAYBOOK.md').write_text('\n\n'.join(parts)+'\n')

if __name__=='__main__':build()
