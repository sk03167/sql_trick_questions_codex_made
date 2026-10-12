# Data System Design Scenario Index

A scenario-based study and architecture library containing **43 scenarios**, **274 complete reference paths**, and **377 diagrams**. The documented choices expand into **62,181 assembled design candidates** with the included explorer.

Each scenario explains the data grain, correctness contract, complete technology paths, per-component replacements, governance, infrastructure automation, code delivery, runtime orchestration, recovery, and tests to automate. Diagrams are schematic proposed designs, not deployed systems or vendor-certified integrations. All numerical workload targets are illustrative interview assumptions.

## Read a scenario in this order

1. Clarify the business purpose, consumer, source contract, and measurable service objectives.
2. Read the data grain and correctness rules before choosing technologies.
3. Compare the complete paths, then use component replacements to reason about alternatives.
4. Choose governance enforcement and infrastructure automation separately from processing.
5. Choose code delivery and runtime orchestration, then define test and recovery evidence.

GitHub renders the embedded Mermaid diagrams. Each diagram also has editable source in [data_system_design/diagrams](data_system_design/diagrams). For narrow screens, each view uses a vertical reading path and the surrounding text states its meaning. [Rendered examples](data_system_design/DIAGRAM_GALLERY.md) provide a static fallback.

## Scenario documents

| ID | Scenario | Family | What the document adds | Reference paths | Diagrams |
| --- | --- | --- | --- | --- | --- |
| S01 | [Move an on premises warehouse to cloud virtual machines](data_system_design/scenarios/S01-onprem-lift-and-shift.md) | Migration | Existing facts and dimensions retain their original grain; Exactly one authoritative ingestion writer exists at cutover. | 4 | 7 |
| S02 | [Replatform a legacy warehouse onto a managed cloud warehouse](data_system_design/scenarios/S02-warehouse-replatform.md) | Migration | Fact tables at their documented business grain and conformed dimensions; The same business definition must produce the same answer after translation. | 8 | 11 |
| S03 | [Build a lakehouse for batch and incremental analytics](data_system_design/scenarios/S03-lakehouse-platform.md) | Platform | Raw records preserve source identity; curated tables follow domain grain; Parquet files alone do not provide table-level transactions or snapshot management. | 9 | 11 |
| S04 | [Modernize SSIS Informatica or custom ETL workflows](data_system_design/scenarios/S04-legacy-etl-modernization.md) | Migration | One domain transformation output per documented business grain; A successful job exit is not proof of complete or correct data. | 6 | 8 |
| S05 | [Move Hadoop and HDFS analytics to object storage](data_system_design/scenarios/S05-hadoop-modernization.md) | Migration | Existing partitions plus a manifest identifying table files and schema; Object storage does not share all HDFS rename and filesystem semantics. | 7 | 9 |
| S06 | [Bootstrap historical data and catch up with live changes](data_system_design/scenarios/S06-snapshot-plus-cdc.md) | Ingestion | Raw change event and current-state row are separate grains; Snapshot and CDC must cover the same continuity boundary without omissions. | 6 | 9 |
| S07 | [Maintain CDC replicas through deletes and schema changes](data_system_design/scenarios/S07-cdc-deletes-and-evolution.md) | Ingestion | One change envelope per source operation and one surviving row per entity; A delete followed by replay of an older insert must not resurrect the entity. | 6 | 9 |
| S08 | [Ingest SaaS and REST APIs with limits and changing pages](data_system_design/scenarios/S08-saas-api-ingestion.md) | Ingestion | Raw request page and deduplicated business entity; Progress advances only after every page in the declared window is durable. | 6 | 8 |
| S09 | [Ingest files from SFTP object stores and partner drops](data_system_design/scenarios/S09-file-and-sftp-ingestion.md) | Ingestion | One delivered file version and parsed record; File-arrival notifications can be repeated or reordered. | 6 | 8 |
| S10 | [Build reusable ingestion for hundreds of sources](data_system_design/scenarios/S10-metadata-driven-ingestion.md) | Ingestion | One source specification and one extraction interval per run; A configuration change must not reset another source watermark or checkpoint. | 6 | 8 |
| S11 | [Build daily reporting with ETL or warehouse ELT](data_system_design/scenarios/S11-batch-analytics-and-elt.md) | Analytics | Order line and payment transaction facts with conformed customer and product dimensions; Joining independent one-to-many sources must not multiply monetary facts. | 8 | 10 |
| S12 | [Build event time clickstream and product analytics](data_system_design/scenarios/S12-clickstream-event-time.md) | Streaming | One immutable user event and one aggregate per event-time window; Arrival order is not event-time order. | 6 | 9 |
| S13 | [Enrich streaming facts with changing reference data](data_system_design/scenarios/S13-stream-enrichment.md) | Streaming | One fact event with the dimension version effective at that event time; An attribute effective tomorrow must not rewrite yesterday facts unless the reporting policy says so. | 6 | 9 |
| S14 | [Detect IoT anomalies and generate reliable alerts](data_system_design/scenarios/S14-iot-alerting.md) | Streaming | Sensor observation and separately managed incident state; Repeated observations must not send repeated business notifications. | 6 | 9 |
| S15 | [Serve real time analytical dashboards](data_system_design/scenarios/S15-realtime-olap.md) | Streaming | Raw event plus serving aggregate at a declared dimensional grain; Serving-engine upsert or dedup semantics must match business event identity. | 6 | 9 |
| S16 | [Build log analytics and search ingestion](data_system_design/scenarios/S16-logs-and-search.md) | Serving | Log entry or indexed document version; An index is a derived serving view, not the only recovery copy. | 4 | 6 |
| S17 | [Build analytics from MongoDB documents and change streams](data_system_design/scenarios/S17-mongodb-analytics.md) | NoSQL | Raw document or change event; child arrays become separate analytical rows; Flattening two independent arrays can create a Cartesian product. | 6 | 8 |
| S18 | [Analyze DynamoDB Cosmos DB Cassandra and Bigtable data](data_system_design/scenarios/S18-keyvalue-widecolumn-analytics.md) | NoSQL | Source item or cell mutation and a curated entity view; DynamoDB Streams, Cosmos change feed, Cassandra CDC, and Bigtable change streams have different contracts. | 6 | 8 |
| S19 | [Build a NoSQL read model from authoritative events](data_system_design/scenarios/S19-nosql-read-model.md) | NoSQL | One query-oriented projection per application lookup key; The projection is rebuildable and does not become an accidental second source of truth. | 6 | 9 |
| S20 | [Design facts dimensions and slowly changing history](data_system_design/scenarios/S20-dimensional-modeling.md) | Modeling | One row per declared fact event and one dimension row per effective version; Dimension intervals for a business key must not overlap. | 8 | 11 |
| S21 | [Track business validity and when the platform learned it](data_system_design/scenarios/S21-bitemporal-history.md) | Modeling | One entity version over business-valid and system-recorded intervals; Event time, ingestion time, and report publication time are different concepts. | 6 | 9 |
| S22 | [Design multi region analytics with residency boundaries](data_system_design/scenarios/S22-multi-region-residency.md) | Resilience | Regional raw entity and separately approved cross-region aggregate; Replication destinations must be approved for the actual data category. | 7 | 9 |
| S23 | [Recover a data platform after a regional or destructive failure](data_system_design/scenarios/S23-disaster-recovery.md) | Resilience | A recoverable platform generation with consistent data and metadata positions; Replication of a destructive change is not an independent backup. | 7 | 9 |
| S24 | [Keep restricted data on premises while using cloud analytics](data_system_design/scenarios/S24-hybrid-sensitive-data.md) | Hybrid | Local restricted records and approved exported aggregates; A query executed remotely can still transfer sensitive intermediate results. | 7 | 9 |
| S25 | [Move or federate analytics across cloud providers](data_system_design/scenarios/S25-cross-cloud-platform.md) | Hybrid | Versioned data product with source and destination completeness markers; Open table format does not imply free transfer or identical write semantics across engines. | 9 | 11 |
| S26 | [Publish domain owned data products with contracts](data_system_design/scenarios/S26-data-mesh-products.md) | Governance | One published product version at a documented consumer grain; A folder named data product is not an ownership or support contract. | 7 | 9 |
| S27 | [Share data securely across tenants and organizations](data_system_design/scenarios/S27-governed-data-sharing.md) | Governance | One authorized product slice or shared version per consumer contract; Tenant isolation holds at every storage, cache, export, and query path. | 7 | 9 |
| S28 | [Send curated data back into operational SaaS applications](data_system_design/scenarios/S28-reverse-etl.md) | Serving | One intended destination entity mutation; A successful HTTP response is not always proof the final destination state matches. | 6 | 9 |
| S29 | [Build reproducible training data and batch ML features](data_system_design/scenarios/S29-batch-ml-features.md) | ML and AI | One labeled entity at a prediction timestamp and one feature definition version; Features must use only information available by the prediction timestamp. | 7 | 9 |
| S30 | [Maintain online features with offline consistency](data_system_design/scenarios/S30-online-ml-features.md) | ML and AI | One versioned feature value per entity and feature timestamp; Older events cannot replace a newer online value. | 6 | 9 |
| S31 | [Publish consistent metrics and a semantic serving layer](data_system_design/scenarios/S31-semantic-metrics.md) | Analytics | Metric definition at a declared aggregation grain and filter context; Distinct users, averages, and ratios are not generally additive across groups. | 6 | 8 |
| S32 | [Build auditable financial reconciliation pipelines](data_system_design/scenarios/S32-financial-reconciliation.md) | Domain | Ledger posting settlement line and reconciliation decision are separate grains; No transaction disappears simply because it could not be matched. | 6 | 9 |
| S33 | [Synchronize disconnected edge devices and sites](data_system_design/scenarios/S33-edge-offline-ingestion.md) | Domain | Locally generated immutable event and centrally acknowledged event; Clock time alone cannot establish uniqueness across restarts and sites. | 6 | 8 |
| S34 | [Process documents images and other unstructured data](data_system_design/scenarios/S34-unstructured-data.md) | ML and AI | Source object version extracted page or chunk and derived feature; Original document identity must survive extraction and chunking. | 7 | 9 |
| S35 | [Build a governed retrieval and vector indexing pipeline](data_system_design/scenarios/S35-rag-vector-index.md) | ML and AI | Versioned chunk embedding and authorized retrieval result; Changing embedding models can require rebuilding the whole index. | 5 | 8 |
| S36 | [Build graph analytics and relationship serving](data_system_design/scenarios/S36-graph-analytics.md) | Serving | Entity node and directed relationship with validity and provenance; A repeated relationship event is not necessarily a new distinct edge. | 4 | 6 |
| S37 | [Design geospatial and time series analytics](data_system_design/scenarios/S37-geospatial-timeseries.md) | Domain | One measurement or position per device and event time; Latitude and longitude cannot be treated as generic Cartesian coordinates for distance. | 4 | 6 |
| S38 | [Build a small reliable platform without unnecessary distributed systems](data_system_design/scenarios/S38-small-platform.md) | Platform | Documented analytical table and versioned input batch; Simple systems still require durable inputs, safe retries, backups, and ownership. | 4 | 6 |
| S39 | [Backfill and replay history alongside live processing](data_system_design/scenarios/S39-backfill-and-replay.md) | Operations | One deterministic output partition or entity state for a bounded source range; Live and replay writers must not overwrite each other without a coordination rule. | 7 | 9 |
| S40 | [Recover from bad data and breaking schema incidents](data_system_design/scenarios/S40-quality-incident.md) | Operations | Validated or quarantined source batch and impacted product release; A failed quality check has a declared warn, quarantine, or block action. | 7 | 9 |
| S41 | [Tune a growing platform while controlling cost](data_system_design/scenarios/S41-cost-and-performance.md) | Operations | Cost and latency measurement per product job and query class; A cheaper partial result is not a successful optimization. | 9 | 11 |
| S42 | [Design end to end delivery guarantees and side effects](data_system_design/scenarios/S42-end-to-end-delivery.md) | Operations | Transport event business operation and sink commit are separate grains; Processor checkpointing alone does not make an arbitrary HTTP side effect exactly once. | 6 | 10 |
| S43 | [Consolidate acquired companies and conflicting business systems](data_system_design/scenarios/S43-acquisition-consolidation.md) | Domain | Source-qualified entity and separately managed mastered entity; The same local customer ID in two systems does not prove the same person. | 8 | 10 |

## Technology and operating guides

| Document | Contents |
| --- | --- |
| [Technology choices](data_system_design/TECHNOLOGY_CHOICES.md) | Roles, why each technology family is needed, benefits, tradeoffs, cloud translations and decision questions. |
| [Compatibility and combinations](data_system_design/COMPATIBILITY.md) | Bounded enumeration model, component contracts, valid bundles, conditional alternatives and rejected combinations. |
| [Governance and infrastructure](data_system_design/GOVERNANCE_AND_INFRA.md) | Catalogs versus enforcement, IAM, network, encryption, data lifecycle, IaC state and deployment ownership. |
| [Automation playbook](data_system_design/AUTOMATION_PLAYBOOK.md) | GitHub Actions, Jenkins, GitLab, Azure DevOps, AWS CodePipeline, Cloud Build, Argo CD and Tekton recipes. |
| [Testing playbook](data_system_design/TESTING_PLAYBOOK.md) | Tests by lifecycle, unit and integration fixtures, reconciliation, fault injection, performance, access and recovery drills. |
| [Diagram gallery](data_system_design/DIAGRAM_GALLERY.md) | Rendered samples, source locations, and regeneration commands. |
| [Sources](data_system_design/SOURCES.md) | Primary vendor, cloud and open-source documentation. |
| [Validation](data_system_design/VALIDATION.md) | Actual document, link, compatibility and diagram checks performed; proposed deployment tests are separate. |

## Cloud and platform coverage

The principal examples cover AWS, Azure, Google Cloud, Snowflake on AWS, Databricks on Azure, and open-source/self-managed designs. Selected scenarios add Microsoft Fabric, Oracle Cloud, and IBM watsonx.data. Snowflake and Databricks are platforms deployed within supported cloud locations, not additional cloud providers. Their examples can move to another supported cloud only after storage, networking, identity, region, connector, and feature checks.

## How to explore combinations

```sh
python3 data_system_design/tools/enumerate_designs.py --count
python3 data_system_design/tools/enumerate_designs.py --scenario S12 --cloud aws --limit 12
python3 data_system_design/tools/enumerate_designs.py --scenario S03 --all --output /tmp/S03-designs.jsonl
python3 data_system_design/tools/validate_design_docs.py
```

There is no finite exhaustive list of every possible workload, vendor release, deployment topology, or product combination. This library makes the covered scenarios and dimensions explicit, explains additional substitutions, and exhaustively expands its documented choices. It does not describe an arbitrary Cartesian product as a compatible deployment. Use pairwise integration checks and workload proofs for the chosen complete architecture.

## Suggested study routes

- Migration: S01 → S02 → S05 → S06 → S23 → S39.
- Batch and modeling: S08 → S09 → S10 → S11 → S20 → S21 → S31.
- Streaming: S07 → S12 → S13 → S14 → S15 → S30 → S42.
- NoSQL and specialized serving: S17 → S18 → S19 → S16 → S35 → S36 → S37.
- Governance and platform operations: S22 → S24 → S25 → S26 → S27 → S40 → S41.
- Business and ML: S28 → S29 → S30 → S32 → S33 → S34 → S43.

Research date: October 12, 2026. Keep product versions, supported connectors, regional availability, editions, limits, and prices current before implementation. Former names are noted where useful; Google Knowledge Catalog was formerly Dataplex Universal Catalog, and Databricks Declarative Automation Bundles were formerly Asset Bundles.
