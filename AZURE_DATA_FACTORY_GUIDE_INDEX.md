# Azure Data Factory practical guide

A dedicated ADF v2 handbook with **34 chapters**, **12 scenario walkthroughs**, **58 editable diagrams**, exact UI fields and expression/parameter recipes, sample factory definitions, ARM exports, CI/IaC templates, fixtures and verification tools.

Branch `azure-data-factory-practical-guide`, independently based on `main`. Researched 2026-10-13 using official Microsoft documentation.

## Start here

1. Platform/factory/IR/linked-service/dataset setup: chapters 01–05.
2. Parameters, expressions and concurrency: 06–08 and 15–18.
3. Source ingestion and correctness: 09–14, transformations/loading: 19–22.
4. Governance, metadata frameworks, Git/CI and testing: 23–28.
5. Monitoring and the hands-on lab: 29–30; recovery, source substitutions and troubleshooting: 31–34.

This is a broad data-engineering guide, not a promise that every connector/cloud/compute combination is equivalent. Fabric Data Factory/Synapse have separate scope and migration caveats. All endpoints/resource IDs and environment names must be adapted. No real factory was connected or deployed during authoring.

## Chapter index

| Chapter | Contents |
|---|---|
| [01. ADF platform map and the shared lab](adf_guide/chapters/01-platform-map.md) | Understand control flow, data movement, transformation compute, and environment boundaries. |
| [02. Create the factory and navigate authoring, debug, and publish](adf_guide/chapters/02-create-and-author.md) | Set up the development surface and distinguish code validation from execution. |
| [03. Azure IR, self-hosted IR, Azure-SSIS IR, and execution location](adf_guide/chapters/03-integration-runtimes.md) | Choose the execution plane that can actually reach both ends of the activity. |
| [04. Linked services, managed identities, SQL credentials, and Key Vault](adf_guide/chapters/04-linked-services-identity.md) | Define connections without making runtime input a secret distribution channel. |
| [05. Datasets, formats, locations, and parameterized paths](adf_guide/chapters/05-datasets-and-paths.md) | Describe the selected source/sink data and keep transport separate from parsing. |
| [06. Parameter scopes and deployment versus runtime values](adf_guide/chapters/06-parameter-map.md) | Know exactly where to define, pass, and read each value. |
| [07. Expressions: types, interpolation, dates, escaping, and outputs](adf_guide/chapters/07-expressions.md) | Use ADF syntax deliberately instead of mixing pipeline, SQL, Data Flow, and notebook languages. |
| [08. Variables, counters, arrays, and parallel-loop races](adf_guide/chapters/08-variables-and-concurrency.md) | Keep iteration-local state inside isolated child pipeline runs. |
| [09. File ingestion: Binary/CSV, hierarchy, wildcards, and completion](adf_guide/chapters/09-file-copy.md) | Move a complete immutable delivery into a stable batch destination. |
| [10. SQL/Oracle/on-prem database ingestion and source load](adf_guide/chapters/10-database-copy.md) | Configure query/table reads, runtime routing, and a reproducible extraction boundary. |
| [11. Incremental watermarks, committed boundaries, and transactional advancement](adf_guide/chapters/11-watermarks.md) | Capture a stable interval and move its boundary only after target acceptance. |
| [12. CDC, hard deletes, soft deletes, and snapshot comparison](adf_guide/chapters/12-cdc-deletes.md) | Choose a change/deletion mechanism rather than expecting Copy to infer missing rows. |
| [13. REST Copy: linked service, dataset, pagination, and JSON mapping](adf_guide/chapters/13-rest-copy.md) | Copy API rows with the connector's native request and pagination fields. |
| [14. Web, HTTP Copy, Azure Functions, and custom paging](adf_guide/chapters/14-web-http-functions.md) | Choose a control request versus bulk transfer and make polling finite. |
| [15. Lookup, Get Metadata, and Filter: output shapes and limits](adf_guide/chapters/15-lookup-metadata-filter.md) | Use bounded control metadata without treating it as a bulk-data channel. |
| [16. ForEach, Execute Pipeline, and child return values](adf_guide/chapters/16-foreach-child-returns.md) | Pass immutable per-item inputs and wait for real child outcomes. |
| [17. If, Switch, Until, retries, and error-propagation graphs](adf_guide/chapters/17-conditions-errors-until.md) | Make failure visible even when logging and cleanup succeed. |
| [18. Schedule, tumbling windows, storage events, and batch identity](adf_guide/chapters/18-triggers-windows-events.md) | Use a trigger whose state and retry model match the source delivery contract. |
| [19. Mapping Data Flow transformations: schema, joins, aggregate, and sink](adf_guide/chapters/19-mapping-data-flows.md) | Build a managed Spark graph and retain the business grain through transformations. |
| [20. Data Flow parameters, expression mode, compute, and performance](adf_guide/chapters/20-data-flow-parameters.md) | Bind runtime inputs while keeping its expression language separate from pipeline syntax. |
| [21. Databricks, Synapse, SQL, functions, and streaming boundaries](adf_guide/chapters/21-external-compute.md) | Use ADF as the orchestrator while keeping compute-specific semantics explicit. |
| [22. Loading, SQL upsert, deletes, partitions, and idempotent publication](adf_guide/chapters/22-loading-idempotency.md) | Define what retrying a load changes before choosing append, overwrite, or upsert. |
| [23. Security, private endpoints, Purview, RBAC, and diagnostic access](adf_guide/chapters/23-security-network-governance.md) | Keep management permissions, data permissions, networking, and lineage distinct. |
| [24. Metadata-driven ingestion framework and configuration ownership](adf_guide/chapters/24-metadata-framework.md) | Scale reusable pipelines without giving a control table arbitrary execution power. |
| [25. Git branches, collaboration, Publish all, and exported ARM](adf_guide/chapters/25-git-publish.md) | Review source changes and understand what is actually live in a factory. |
| [26. Azure DevOps CI/CD: build artifacts, environment overrides, and trigger handling](adf_guide/chapters/26-azure-devops-ci.md) | Generate once, test the same artifact, and promote it with a controlled release. |
| [27. GitHub Actions, Jenkins, GitLab, Bicep, and Terraform alternatives](adf_guide/chapters/27-other-ci-and-infra.md) | Replace the runner without changing the ADF artifact or runtime data contract. |
| [28. Tests: source contracts, definition validation, integration, and release gates](adf_guide/chapters/28-test-strategy.md) | Check real data outcomes separately from ADF resource shape and run status. |
| [29. Monitoring, Log Analytics, Copy bottlenecks, and cost](adf_guide/chapters/29-monitor-cost-performance.md) | Diagnose the slow stage and watch freshness/completeness alongside run status. |
| [30. Worked lab: parameter isolation, file Copy, rerun, and reconciliation](adf_guide/chapters/30-worked-lab.md) | Use the validated sample factory and record exact expected results. |
| [31. Backfill, recovery, region migration, and rollback](adf_guide/chapters/31-backfill-recovery.md) | Restore boundaries, identities, triggers, and data—not only the pipeline JSON. |
| [32. NoSQL, SFTP, nested documents, and cross-cloud source substitutions](adf_guide/chapters/32-nosql-sftp-crosscloud.md) | Check each connector's operation/schema contract instead of replacing only a hostname. |
| [33. Troubleshooting by symptom, parameter, runtime, and graph](adf_guide/chapters/33-troubleshooting.md) | Find the failing layer before resetting state or broadening permissions. |
| [34. ADF versus Synapse pipelines and Fabric Data Factory](adf_guide/chapters/34-fabric-synapse-scope.md) | Use the requested ADF service and plan migrations by capability, not product-name substitution. |

## Scenario index

| Scenario | Focus |
|---|---|
| [On-prem warehouse migration to Azure](adf_guide/scenarios/01-on-prem-migration.md) | Use SHIR, snapshots, CDC, parallel validation and controlled cutover. |
| [Daily files: 100 million orders by 6 a.m.](adf_guide/scenarios/02-daily-files-deadline.md) | Use a completion contract, bounded Copy and measured processing capacity. |
| [Incremental database CDC with hard deletes](adf_guide/scenarios/03-database-cdc.md) | Choose native CDC or a complete ordered ledger, then commit state and boundary. |
| [Paginated SaaS REST API to durable landing](adf_guide/scenarios/04-rest-saas.md) | Configure native pagination or a custom extractor for unsupported contracts. |
| [SFTP files to ADLS with verified completion](adf_guide/scenarios/05-sftp-batch.md) | Preserve transport identity, host keys and a stable business batch. |
| [Many tables with metadata-driven parallel ingestion](adf_guide/scenarios/06-metadata-framework.md) | Use bounded Lookup, immutable loop inputs and isolated children/control state. |
| [ADF orchestration with Databricks or SQL transformations](adf_guide/scenarios/07-databricks-sql.md) | Move sources first and verify external computation outcomes before publication. |
| [Cosmos/MongoDB documents to header and line facts](adf_guide/scenarios/08-nosql-documents.md) | Preserve source versions/deletes and avoid row multiplication when flattening. |
| [Kafka/Event Hubs with ADF batch orchestration](adf_guide/scenarios/09-streaming-boundary.md) | Keep streaming offsets/state in the streaming engine and give ADF completed handoffs. |
| [Private source/sink access and governed enterprise pipelines](adf_guide/scenarios/10-private-governance.md) | Configure actual execution-plane routes and least-privilege source identities. |
| [Backfill, source retention gaps and region recovery](adf_guide/scenarios/11-replay-region-recovery.md) | Restore explicit boundaries, data, control state, identity and scheduler state. |
| [Dev/test/prod delivery and maintenance](adf_guide/scenarios/12-release-maintenance.md) | Promote the same reviewed ARM artifact with tested parameter and trigger contracts. |

## Practical companions

- [Examples and exact run instructions](adf_guide/examples/README.md).
- [Validated factory source root](adf_guide/examples/factory/) and [generated ARM/parameter contract](adf_guide/examples/generated_arm/README.md).
- [Deployment/infra templates](adf_guide/examples/templates/README.md), including GitHub/Azure DevOps/Jenkins/GitLab.
- [Verification and execution limits](adf_guide/VERIFICATION.md).
- [Diagram gallery](adf_guide/DIAGRAMS.md) and [official source register](adf_guide/SOURCES.md).

## What validation proves

Local fixture/reference checks, owned-definition/graph checks, Microsoft ADF validate/export, Python syntax, local links, generated ARM parameter coherence and diagram rendering are checked. These do not prove credentials/IR/network/live Copy/API/SQL/Data Flow/Databricks execution, throughput, data security or cloud deployment. The active GitHub workflow has no Azure credentials and deploys nothing.
