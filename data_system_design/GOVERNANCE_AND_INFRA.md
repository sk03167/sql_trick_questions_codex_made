# Governance and Infrastructure Automation

[Scenario index](../DATA_SYSTEM_DESIGN_INDEX.md)

Every scenario needs both an ownership policy and technical enforcement. Ownership answers who defines the product, responds to failures, authorizes access, and accepts retention or semantic changes. Enforcement happens where records can be read, written, copied, cached, indexed, or restored.

| Platform | Discovery and metadata | Enforcement | Infrastructure controls | Boundary |
| --- | --- | --- | --- | --- |
| Azure | Microsoft Purview discovery plus actual engine grants | Entra identities, Azure RBAC, storage ACLs and query roles | Private routing, managed identities, source-safe runtimes | Catalog visibility is not a universal storage deny policy. |
| AWS | Glue Catalog and Lake Formation where integrated | IAM, supported Lake Formation grants, warehouse or service roles | VPC endpoints, KMS, workload IAM roles | Test direct S3 access and each engine integration separately. |
| Google Cloud | Knowledge Catalog formerly Dataplex Universal Catalog | IAM, BigQuery policies, storage permissions, service-specific enforcement | Service accounts, approved regions, private connectivity | Metadata policy intent must be verified at the actual execution and export paths. |
| Databricks | Unity Catalog plus product ownership and lineage | Unity Catalog grants and workspace or storage identities | Separate environments, locations, compute policies and progress state | Cataloged access can still be undermined by ungoverned direct storage credentials. |
| Snowflake | Horizon catalog capabilities and versioned products | Roles, grants, policies and secure sharing contracts | Account location, integrations, workload sizing and resource budgets | Validate feature availability and distinguish native, shared, and open-table access paths. |
| Open source or hybrid | OpenMetadata or DataHub plus a table catalog | Engine RBAC, cloud IAM, and supported policy integrations | Vault or cloud secrets, TLS, private endpoints and operational backup | Discovery tools do not automatically enforce permissions in every connector or engine. |

## Lifecycle controls

| Lifecycle | Control | Automated evidence |
| --- | --- | --- |
| Collection | Approved purpose, source scope, stable schema and minimization | Contract validation and field classification checks |
| Storage | Restricted raw zones, encryption, keys, access grants and retention | Denied-access probes, configuration policies and object inventories |
| Processing | Workload identities, approved fields and protected checkpoints | Identity scope tests, state-location checks and lineage events |
| Serving | Tenant or row policies, metric ownership and consumer contracts | Golden queries, tenant-denial tests and API authorization probes |
| Copies and indexes | Propagate permissions, deletion and allowed downstream purpose | Cross-store erasure manifests and restricted-document retrieval tests |
| Backups and restore | Protected recovery copies and reapplication of current policy | Isolated restore drill and post-restore permission validation |
| Decommission | Stop writers, revoke credentials and dispose of retained copies by policy | Dependency audit, revoked-access test and deletion evidence |

## Infrastructure ownership

| Approach | Benefit | Implementation requirements | Boundary |
| --- | --- | --- | --- |
| Terraform | Broad provider ecosystem and declarative plans | Separate remote state by ownership and environment; secure and lock it; validate provider coverage. | Providers and resource APIs differ, so shared language does not mean identical modules. |
| OpenTofu | Open-source-oriented declarative infrastructure workflow | Use explicit versions, tested providers, isolated state and encryption where configured. | Review migration and provider compatibility rather than assuming state interchange is universally safe. |
| Pulumi | General-purpose language infrastructure definitions | Test programs, preview changes, protect state and secrets, and scope automation identities. | Language-level power needs disciplined reproducibility and resource ownership. |
| Native cloud IaC | Bicep/ARM on Azure, CDK/CloudFormation on AWS, provider-specific declarative tools elsewhere | Keep environment parameters and identity controls explicit; import or manage existing resources carefully. | Native templates stay within their platform contract; job code and table data need separate lifecycle management. |
| Configuration and GitOps | Ansible/Packer for hosts; Helm and Argo CD for supported Kubernetes workloads | Bake versioned images, apply least privilege, and keep cloud resources under a separately declared owner. | GitOps reconciliation of manifests is not an automatic warehouse schema or historical data migration. |

Separate root ownership for networking and identities, data resources and catalogs, and job/application deployments. Do not let Terraform, a cloud template, and a manual console change all manage the same resource without a declared ownership transition. Import existing resources deliberately. Lock and secure remote state; state and plans can contain sensitive configuration. [Terraform state](https://developer.hashicorp.com/terraform/language/state), [OpenTofu state](https://opentofu.org/docs/language/state/), [Pulumi infrastructure as code](https://www.pulumi.com/docs/iac/).

## Minimum environment contract

- Private-source connectivity and a trusted runtime or runner location.
- Approved region, data classification, and permitted replication destination.
- Distinct workload identity, service grants, and secrets references for each environment.
- Versioned object prefixes, table/catalog namespaces, stream groups, and checkpoint locations.
- Compute quotas, workload isolation, budgets, logs, audit trails, and consumer-level SLOs.
- Backup and replay retention, recovery manifests, and periodic restore evidence.

## Privacy deletion is an engineering workflow

Inventory every raw copy, current-state table, historical version, training dataset, cache, search/vector index, export, and recovery copy. Define where erasure versus restricted retention applies. Carry the request identity and record acknowledgments per store; test that a backfill or restore cannot reintroduce a prohibited entity. Encryption alone does not perform logical erasure of all derived copies.

## Governance permutations

A cloud-native catalog with engine grants can be combined with any eligible CI and IaC recipe. OpenMetadata or DataHub can replace the discovery layer while keeping actual engine/storage policies. Unity Catalog and Snowflake roles belong to their platform execution boundaries. Lake Formation applies through supported integrations and permissions. Knowledge Catalog and Purview provide metadata and governance capabilities whose enforcement scope must be verified for the concrete paths. A cross-cloud discovery layer does not magically unify every provider IAM policy.

Primary references: [Microsoft Purview governance](https://learn.microsoft.com/en-us/azure/purview/overview), [Knowledge Catalog formerly Dataplex Universal Catalog](https://docs.cloud.google.com/knowledge-catalog/docs), [Lake Formation permission boundaries](https://docs.aws.amazon.com/lake-formation/latest/dg/lf-permissions-overview.html), [Databricks Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/), [OpenMetadata documentation](https://docs.open-metadata.org/), [DataHub documentation](https://docs.datahub.com/docs/features/feature-guides/lineage).
