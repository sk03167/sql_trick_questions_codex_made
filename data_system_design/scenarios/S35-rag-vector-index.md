# S35 Build a governed retrieval and vector indexing pipeline

[Scenario index](../../DATA_SYSTEM_DESIGN_INDEX.md) · **Family:** ML and AI · **Mode:** vector

Maintain a retrieval index that respects document updates, source permissions, and deletions. Illustrative task: users cannot retrieve restricted chunks even through semantic similarity search.

## Requirements to clarify

Confirm source versions and access, daily and peak volume, read versus write freshness, consumer query patterns, error tolerance, budget, operating skills, residency, retention, and recovery objectives. The numeric targets in this scenario are exercise assumptions, not vendor guarantees.

**Data grain:** Versioned chunk embedding and authorized retrieval result.

**Identity and progress:** Document version chunk ID embedding model version and entitlement version.

## Data design

1. Ingest documents and their permission metadata using stable source versions.
2. Parse and chunk deterministically; compute embeddings under a versioned model and dimension contract.
3. Upsert index entries and remove obsolete versions and deleted documents.
4. Filter retrieval by authenticated entitlements and evaluate quality against curated questions.

### Correctness contract

- Changing embedding models can require rebuilding the whole index.
- Similarity search is not an authorization mechanism.
- Deletion includes source text, cached chunks, embeddings, and derived indexes.

### Complete technology paths

These are proposed reference architectures, not exported vendor-certified deployments. Each path names concrete stages; when a worker or sink adapter is named, its connector configuration and code must be implemented and tested. The diagrams describe the data plane; operational deployment appears below.

#### Azure AI Search retrieval

Data moves through Document version ingestion worker, retains recoverable input in Blob originals and ACL manifest, and publishes through Azure AI Search plus retrieval API after validation.

```mermaid
flowchart TD
    source["Enterprise documents and<br/>source permissions"]
    ingest["Document version ingestion<br/>worker"]
    archive["Blob originals and ACL<br/>manifest"]
    process["Parsing and embedding jobs"]
    gate["Validate the product contract"]
    serving["Azure AI Search plus retrieval<br/>API"]
    hold["Hold publication and investigate"]
    source -->|extract or publish| ingest
    ingest -->|archive through a configured writer| archive
    archive -->|bounded input or restore| process
    process -->|candidate output| gate
    gate -->|accepted release| serving
    gate -->|contract violated| hold
```

[Editable diagram source](../diagrams/S35-azure-vector.mmd)

**Why this path helps:** Managed hybrid search provides a retrieval surface with structured filtering.

**What must be designed and verified:** Validate permission enforcement, index quotas, embedding dimensions, and deletion propagation.

Technology references: [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search).

Additional assembled data variants for this path:

| Variant | Compute and serving bundle | Required migration or verification |
| --- | --- | --- |
| PostgreSQL with pgvector retrieval | Parsing and embedding jobs → PostgreSQL pgvector with authorized retrieval API | Provision supported extension and compute in the selected location; benchmark filtered recall, indexing, backups, and concurrent writes. |

#### AWS OpenSearch vector retrieval

Data moves through Document ingestion worker, retains recoverable input in S3 originals and ACL manifest, and publishes through OpenSearch plus retrieval API after validation.

```mermaid
flowchart TD
    source["Enterprise documents and<br/>source permissions"]
    ingest["Document ingestion worker"]
    archive["S3 originals and ACL manifest"]
    process["Container parsing and<br/>embedding"]
    gate["Validate the product contract"]
    serving["OpenSearch plus retrieval API"]
    hold["Hold publication and investigate"]
    source -->|extract or publish| ingest
    ingest -->|archive through a configured writer| archive
    archive -->|bounded input or restore| process
    process -->|candidate output| gate
    gate -->|accepted release| serving
    gate -->|contract violated| hold
```

[Editable diagram source](../diagrams/S35-aws-vector.mmd)

**Why this path helps:** Combines object storage with an index for text and vector search.

**What must be designed and verified:** Index and tenant filtering must enforce the source ACL contract, not merely relevance.

Technology references: [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html).

Additional assembled data variants for this path:

| Variant | Compute and serving bundle | Required migration or verification |
| --- | --- | --- |
| PostgreSQL with pgvector retrieval | Container parsing and embedding → PostgreSQL pgvector with authorized retrieval API | Provision supported extension and compute in the selected location; benchmark filtered recall, indexing, backups, and concurrent writes. |

#### Google Cloud hosted vector retrieval

Data moves through Cloud Run document worker, retains recoverable input in GCS originals and ACL manifest, and publishes through Qdrant plus retrieval API after validation.

```mermaid
flowchart TD
    source["Enterprise documents and<br/>source permissions"]
    ingest["Cloud Run document worker"]
    archive["GCS originals and ACL manifest"]
    process["Container parsing and<br/>embedding"]
    gate["Validate the product contract"]
    serving["Qdrant plus retrieval API"]
    hold["Hold publication and investigate"]
    source -->|extract or publish| ingest
    ingest -->|archive through a configured writer| archive
    archive -->|bounded input or restore| process
    process -->|candidate output| gate
    gate -->|accepted release| serving
    gate -->|contract violated| hold
```

[Editable diagram source](../diagrams/S35-gcp-vector.mmd)

**Why this path helps:** An explicit hosted index preserves portability of the retrieval application.

**What must be designed and verified:** This is a hosted software design, not a claim of native integration with every Google service.

Technology references: [Qdrant overview](https://qdrant.tech/documentation/overview/), [pgvector official repository](https://github.com/pgvector/pgvector).

Additional assembled data variants for this path:

| Variant | Compute and serving bundle | Required migration or verification |
| --- | --- | --- |
| PostgreSQL with pgvector retrieval | Container parsing and embedding → PostgreSQL pgvector with authorized retrieval API | Provision supported extension and compute in the selected location; benchmark filtered recall, indexing, backups, and concurrent writes. |

#### Databricks AI Search retrieval

Data moves through Document jobs and source metadata, retains recoverable input in Delta content and source versions, and publishes through Databricks AI Search plus API after validation.

```mermaid
flowchart TD
    source["Enterprise documents and<br/>source permissions"]
    ingest["Document jobs and source<br/>metadata"]
    archive["Delta content and source<br/>versions"]
    process["Databricks parsing and<br/>embeddings"]
    gate["Validate the product contract"]
    serving["Databricks AI Search plus API"]
    hold["Hold publication and investigate"]
    source -->|extract or publish| ingest
    ingest -->|archive through a configured writer| archive
    archive -->|bounded input or restore| process
    process -->|candidate output| gate
    gate -->|accepted release| serving
    gate -->|contract violated| hold
```

[Editable diagram source](../diagrams/S35-db-vector.mmd)

**Why this path helps:** Keeps indexable content and transformations in the lakehouse ecosystem.

**What must be designed and verified:** Formerly Vector Search; verify supported sync modes, permission model, and index behavior.

Technology references: [Databricks AI Search formerly Vector Search](https://docs.databricks.com/aws/en/ai-search/ai-search), [Databricks Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/).

Additional assembled data variants for this path:

| Variant | Compute and serving bundle | Required migration or verification |
| --- | --- | --- |
| PostgreSQL with pgvector retrieval | Databricks parsing and embeddings → PostgreSQL pgvector with authorized retrieval API | Provision supported extension and compute in the selected location; benchmark filtered recall, indexing, backups, and concurrent writes. |

#### Open source retrieval services

Data moves through Document connector worker, retains recoverable input in Object originals and ACL manifest, and publishes through Qdrant plus retrieval API after validation.

```mermaid
flowchart TD
    source["Enterprise documents and<br/>source permissions"]
    ingest["Document connector worker"]
    archive["Object originals and ACL<br/>manifest"]
    process["Python parsing and embedding<br/>jobs"]
    gate["Validate the product contract"]
    serving["Qdrant plus retrieval API"]
    hold["Hold publication and investigate"]
    source -->|extract or publish| ingest
    ingest -->|archive through a configured writer| archive
    archive -->|bounded input or restore| process
    process -->|candidate output| gate
    gate -->|accepted release| serving
    gate -->|contract violated| hold
```

[Editable diagram source](../diagrams/S35-oss-vector.mmd)

**Why this path helps:** Controls model selection and index deployment boundaries.

**What must be designed and verified:** Capacity, backup, dimension migrations, and authorization belong to the operator.

Technology references: [Qdrant overview](https://qdrant.tech/documentation/overview/), [pgvector official repository](https://github.com/pgvector/pgvector).

Additional assembled data variants for this path:

| Variant | Compute and serving bundle | Required migration or verification |
| --- | --- | --- |
| PostgreSQL with pgvector retrieval | Python parsing and embedding jobs → PostgreSQL pgvector with authorized retrieval API | Provision supported extension and compute in the selected location; benchmark filtered recall, indexing, backups, and concurrent writes. |

### Logical model or operation lifecycle

Document versions, chunks and embeddings retain explicit identity. Retrieval checks the current source entitlement contract, and re-embedding creates a controlled model/index version transition.

```mermaid
erDiagram
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
    }
```

[Editable diagram source](../diagrams/S35-model.mmd)

### Replace each component deliberately

| Component | Alternatives | Why change it | What changes | Test before switching |
| --- | --- | --- | --- | --- |
| Source engine | PostgreSQL, MySQL, SQL Server, Oracle, MongoDB, DynamoDB, Cosmos DB, Cassandra, Bigtable | Match the operational workload or an existing estate. | Rework snapshot consistency, keys, delete capture, source ordering, and schema contracts. | Run source-specific bootstrap, mutation, delete, and retention tests. |
| Ingestion implementation | ADF, Glue workers, Airbyte, Fivetran, Informatica, Matillion, custom Python or Java workers | Trade connector maintenance against managed service cost and control. | Confirm endpoint support, network placement, source load, pagination or CDC envelopes, and acknowledgment rules. | Inject authentication, quota, partial-read, and retry failures. |
| Object storage | S3, ADLS Gen2, GCS, OCI Object Storage, IBM Cloud Object Storage, supported S3-compatible stores | Change placement, cost structure, or existing cloud integration. | Adjust IAM, encryption, filesystem assumptions, request costs, lifecycle and egress; verify table-writer support. | Resume multipart transfers, deny unauthorized access, and test recovery from actual retained versions. |
| Compute and transformation | Warehouse SQL with dbt, Spark, Flink, Beam on Dataflow, bounded Python with Polars or DuckDB | Fit relational, distributed, streaming, or bounded processing needs. | Rewrite runtime interfaces, date/type semantics, state handling, connector dependencies, and deployment artifacts. | Compare golden outputs plus load and restart behavior. |
| Orchestration | ADF or Fabric pipelines, Airflow, Dagster, Prefect, Lakeflow Jobs, cloud-native workflow services | Choose dependency handling, asset visibility, existing skills, and operations ownership. | Keep stable progress identities, timezones, backfill boundaries, concurrency controls, and external job submission. | Parse definitions, fail upstream work, and verify safe retries and recovery. |
| Serving | Snowflake, BigQuery, Redshift, Synapse, Fabric, Databricks SQL, Trino, ClickHouse, Pinot, Druid, purpose-built databases | Match consumer query shapes, freshness, concurrency, and operational read requirements. | Rework physical layout, query APIs, load adapters, tenant policies, mutations, and consumption models. | Benchmark actual consumer queries and reconcile output grain and precision. |
| BI and metric interface | Power BI, Tableau, Looker, Superset, Metabase, Cube, dbt Semantic Layer | Fit analyst workflow, semantic reuse, and existing licensing. | Translate semantic definitions, caching, refresh mode, identity propagation, and certified metrics. | Compare metric parity and denied-user behavior across interfaces. |
| Retrieval index | Azure AI Search, OpenSearch, Qdrant, pgvector, Databricks AI Search | Fit hybrid retrieval, filtering, operational boundaries, and existing data platforms. | Translate embedding dimensions, filter behavior, source ACLs, update/delete APIs, and index rebuild procedures. | Evaluate filtered relevance and verify denied and deleted chunks never appear. |

A substitution is accepted only after the source protocol, input/output types, table format, catalog, region, identity, mutations, replay, and consumer API still meet the stated contract. Moving to a new cloud may also move network placement, keys, quotas, and cost ownership. A list of names alone is not a valid architecture.

## Governance and infrastructure automation

### Scenario governance rules

- Propagate source ACLs and test denied retrieval before generating answers.
- Protect retrieval logs and avoid exposing confidential chunks to unauthorized evaluation users.
- Record document provenance, model version, licensing, and retention.

Ownership and metadata describe the intended controls. Infrastructure automation deploys resources, and engine/storage permission tests prove enforcement at real access paths.

```mermaid
flowchart TD
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
    metadata -. expected controls .-> audit
```

[Editable diagram source](../diagrams/S35-governance.mmd)

### Governance technology alternatives

| Platform | Catalog and ownership | Enforcement | Infrastructure controls | Boundary to test |
| --- | --- | --- | --- | --- |
| Azure | Microsoft Purview discovery plus actual engine grants | Entra identities, Azure RBAC, storage ACLs and query roles | Private routing, managed identities, source-safe runtimes | Catalog visibility is not a universal storage deny policy. |
| AWS | Glue Catalog and Lake Formation where integrated | IAM, supported Lake Formation grants, warehouse or service roles | VPC endpoints, KMS, workload IAM roles | Test direct S3 access and each engine integration separately. |
| Google Cloud | Knowledge Catalog formerly Dataplex Universal Catalog | IAM, BigQuery policies, storage permissions, service-specific enforcement | Service accounts, approved regions, private connectivity | Metadata policy intent must be verified at the actual execution and export paths. |
| Databricks | Unity Catalog plus product ownership and lineage | Unity Catalog grants and workspace or storage identities | Separate environments, locations, compute policies and progress state | Cataloged access can still be undermined by ungoverned direct storage credentials. |
| Snowflake | Horizon catalog capabilities and versioned products | Roles, grants, policies and secure sharing contracts | Account location, integrations, workload sizing and resource budgets | Validate feature availability and distinguish native, shared, and open-table access paths. |
| Open source or hybrid | OpenMetadata or DataHub plus a table catalog | Engine RBAC, cloud IAM, and supported policy integrations | Vault or cloud secrets, TLS, private endpoints and operational backup | Discovery tools do not automatically enforce permissions in every connector or engine. |

Discovery can be replaced with OpenMetadata or DataHub while keeping the same engine and storage enforcement. Source systems, object stores, query engines, exported copies, and caches are separate authorization surfaces. Instrument OpenLineage or native lineage where compatible; verify gaps instead of treating a catalog scan as complete operational lineage.

### Infrastructure automation alternatives

| Approach | Benefit | Implementation requirements | Important boundary |
| --- | --- | --- | --- |
| Terraform | Broad provider ecosystem and declarative plans | Separate remote state by ownership and environment; secure and lock it; validate provider coverage. | Providers and resource APIs differ, so shared language does not mean identical modules. |
| OpenTofu | Open-source-oriented declarative infrastructure workflow | Use explicit versions, tested providers, isolated state and encryption where configured. | Review migration and provider compatibility rather than assuming state interchange is universally safe. |
| Pulumi | General-purpose language infrastructure definitions | Test programs, preview changes, protect state and secrets, and scope automation identities. | Language-level power needs disciplined reproducibility and resource ownership. |
| Native cloud IaC | Bicep/ARM on Azure, CDK/CloudFormation on AWS, provider-specific declarative tools elsewhere | Keep environment parameters and identity controls explicit; import or manage existing resources carefully. | Native templates stay within their platform contract; job code and table data need separate lifecycle management. |
| Configuration and GitOps | Ansible/Packer for hosts; Helm and Argo CD for supported Kubernetes workloads | Bake versioned images, apply least privilege, and keep cloud resources under a separately declared owner. | GitOps reconciliation of manifests is not an automatic warehouse schema or historical data migration. |

Provision network paths, storage, catalogs, workload identities, secrets references, logging, backup, compute limits, and budgets before deploying jobs. Separate environments and remote state; do not commit state or credentials. Use explicit providers and versions, prevent two tools from owning the same resource, and test an isolated rebuild. For private sources, place a trusted runner or ingestion runtime on the reachable network; a CI runner location is a real architectural dependency.

## Code delivery and runtime automation

CI builds and tests a release. CD deploys the same artifact, runtime orchestration controls execution, and consumer-level checks detect regressions after promotion.

```mermaid
flowchart TD
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
    verify -->|regression or failure| recovery
```

[Editable diagram source](../diagrams/S35-delivery.mmd)

### Delivery alternatives and compatible scope

| Delivery choice | Benefit | Scope for this scenario | Deployment and identity implications |
| --- | --- | --- | --- |
| GitHub Actions | Hosted or private runners with PR checks and environment-specific release jobs. | Azure AI Search retrieval, AWS OpenSearch vector retrieval, Google Cloud hosted vector retrieval, Databricks AI Search retrieval, Open source retrieval services | Provider CLI or API deploys the reviewed immutable job artifact; production gate records the artifact digest. Use environment-bound short-lived cloud identity where supported; restrict token claims and trusted branches. |
| Jenkins | Private-network runners and shared libraries suit existing enterprise delivery estates. | Azure AI Search retrieval, AWS OpenSearch vector retrieval, Google Cloud hosted vector retrieval, Databricks AI Search retrieval, Open source retrieval services | A Jenkinsfile builds and tests once; a shared deploy library applies the reviewed artifact and records evidence. Isolate agents, pin plugins and dependencies, and scope credentials to a job and environment. |
| GitLab CI | Merge-request tests, protected environments, and configurable runners keep delivery close to source control. | Azure AI Search retrieval, AWS OpenSearch vector retrieval, Google Cloud hosted vector retrieval, Databricks AI Search retrieval, Open source retrieval services | Stage-specific jobs publish an immutable artifact and invoke the chosen platform deployment adapter. Use protected runners and environment permissions; identity federation depends on the target provider. |
| Azure DevOps Pipelines | Native Azure delivery and enterprise service connections suit Azure-centered teams. | Azure AI Search retrieval, Databricks AI Search retrieval | For ADF use validated factory artifacts and environment parameterization; for Databricks use bundles or the supported API. ADF factory resource deployment and pipeline definition publishing are separate lifecycle steps. |
| AWS CodePipeline and CodeBuild | Native AWS build roles and pipeline stages reduce cross-service identity plumbing. | AWS OpenSearch vector retrieval | Publish job artifacts and apply the chosen AWS or warehouse deployment adapter; CDK synthesizes CloudFormation. Build VPC access, source connection, artifact encryption, and least-privilege deploy roles must be provisioned. |
| Google Cloud Build | Containerized build steps integrate with Google service accounts and artifact storage. | Google Cloud hosted vector retrieval | Build a job image or template and deploy through Dataflow, Composer, Cloud Run, or warehouse-specific interfaces. Cloud Deploy has supported workload targets; data jobs require their actual job APIs rather than assumed generic support. |
| GitHub or GitLab build with Argo CD | A reconciler promotes declared Kubernetes manifests and makes drift visible. | Open source retrieval services | CI updates the reviewed image digest or Helm values in Git; Argo CD reconciles the selected namespace. Argo CD reconciles Kubernetes resources; cloud infrastructure and managed warehouse DDL remain separately owned. |
| Tekton pipelines on Kubernetes | Kubernetes-native task execution can fit a self-managed platform engineering estate. | Open source retrieval services | Pipeline tasks execute tests and platform-specific deploy steps; cloud resource state stays in the chosen IaC backend. Operators must manage cluster availability, runner permissions, artifact provenance, and secrets. |

### Runtime and platform deployment differences

SQL/dbt releases deploy model code plus controlled DDL and grants. Spark releases publish a tested wheel, JAR, container, or job definition. Flink releases must coordinate compatible state or savepoints before changing a job. ADF releases publish validated factory definitions with environment parameters and deliberate trigger handling. Databricks uses Declarative Automation Bundles or supported APIs; Fabric requires supported Git and deployment behavior per item. Kubernetes services use versioned manifests and image digests. The same CI tool can call these interfaces, but the interfaces are not interchangeable.

Runtime choices: Platform-native bounded schedule, Apache Airflow, Dagster, Prefect. For a continuous stream, an orchestrator manages lifecycle and repair; it should not start a fresh consumer for every arriving message.

### Safe promotion and rollback

Build once, record the code and dependency versions, test an isolated deployment with realistic interfaces, then promote the same artifact. Use expand-and-contract schema changes and avoid coupling destructive data changes to an ordinary code rollback. A failed publication retains the last accepted product version and clearly exposes stale or partial status. RAG quality tests and access-control tests are different release gates.

## Tests to run and automate

| Test | Automation and cadence | Evidence and failure action |
| --- | --- | --- |
| Attempt semantic retrieval of a restricted document as a denied user. | Deterministic fixture in CI; expensive restore or full-load variants before cutover | Persist inputs, artifact version, expected result and actual result. Block publication or promotion when the declared contract fails. |
| Remove a source document and assert its chunk IDs disappear from the index. | Isolated integration test before promotion and on connector upgrades | Persist inputs, artifact version, expected result and actual result. Block publication or promotion when the declared contract fails. |
| Benchmark recall, relevance, and latency on labeled representative queries. | Failure or replay drill in an isolated environment on a scheduled cadence | Persist inputs, artifact version, expected result and actual result. Block publication or promotion when the declared contract fails. |
| Rebuild embeddings with a changed dimension and verify controlled index cutover. | End-to-end or representative workload exercise before major releases | Persist inputs, artifact version, expected result and actual result. Block publication or promotion when the declared contract fails. |
| Permissions and tenant boundary | Automate authorized and denied reads on staging; rerun after policy changes | Test engine query, direct object access, exports and caches. A metadata-only permissions check is insufficient. |
| Infrastructure and supply chain | Automate syntax, plan, policy, secret scanning and dependency checks on each PR | Reject unapproved region, broad IAM, exposed storage, overlapping ownership, or unexpected destructive changes. |
| Data freshness and completeness | Continuously measure at the consumer boundary; compare periodic source manifests | Alert the owner and show stale or partial status. Job exit status is not the SLO. |
| Recovery and business acceptance | Automate restore/replay evidence; schedule a supervised drill and business review | Record actual RPO/RTO, reconciled business totals and remaining exceptions. Full production drills need the operational change process. |

### What needs human judgment

Automate repeatable fixtures, contracts, type/schema compatibility, data reconciliation, permission denial, infrastructure policy, load probes, and recovery evidence. Business owners still approve changed metric meaning, reconciliation tolerances, retention exceptions, and consumer acceptance. Security and operations review the intended policy and the consequences of a cutover; scripts produce evidence rather than defining policy by themselves.

## Failure recovery and tradeoffs

- Qdrant, pgvector, Azure AI Search, OpenSearch, and managed vector services differ in filters and index update semantics.
- A vector index complements original content storage rather than replacing it.
- RAG quality tests and access-control tests are different release gates.

Preserve the exact input and output release manifests, progress positions, job versions, and validation evidence. Recovery starts from the last durable accepted boundary and uses a compatible source and sink. Coordinate live and repair writers; if a sink has changed after the saved checkpoint, reconcile or rebuild rather than assuming connection switching restores correctness.

## Explore the documented combinations

```sh
python3 data_system_design/tools/enumerate_designs.py --scenario S35 --count
python3 data_system_design/tools/enumerate_designs.py --scenario S35 --limit 12
```

The enumerator expands the documented data bundles, runtime orchestration, metadata alternatives, eligible delivery systems, and their infrastructure tools. It rejects native-cloud delivery outside its cloud and Kubernetes delivery without a Kubernetes runtime. These are design candidates requiring the stated integration checks, not generated deployable infrastructure or proof that arbitrary products interoperate.

## Source references

- [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search)
- [Qdrant overview](https://qdrant.tech/documentation/overview/)
- [pgvector official repository](https://github.com/pgvector/pgvector)
- [Databricks AI Search formerly Vector Search](https://docs.databricks.com/aws/en/ai-search/ai-search)
- [GitHub Actions OIDC](https://docs.github.com/en/actions/concepts/security/openid-connect)
- [Terraform state](https://developer.hashicorp.com/terraform/language/state)
- [dbt data tests](https://docs.getdbt.com/docs/build/data-tests)

[Technology roles](../TECHNOLOGY_CHOICES.md) · [Automation recipes](../AUTOMATION_PLAYBOOK.md) · [Test patterns](../TESTING_PLAYBOOK.md) · [Compatibility rules](../COMPATIBILITY.md)
