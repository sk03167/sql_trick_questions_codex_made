# Code Delivery and Runtime Automation Playbook

[Scenario index](../DATA_SYSTEM_DESIGN_INDEX.md)

Delivery automation builds, tests, and promotes code. Infrastructure automation provisions resources. Runtime orchestration controls jobs and dependencies. Data-quality automation measures actual products. Separate these responsibilities even if one platform hosts several.

| Delivery system | Benefit | Infrastructure alternatives | Target deployment | Required identity or runtime boundary |
| --- | --- | --- | --- | --- |
| GitHub Actions | Hosted or private runners with PR checks and environment-specific release jobs. | OpenTofu, Terraform, Pulumi | Provider CLI or API deploys the reviewed immutable job artifact; production gate records the artifact digest. | Use environment-bound short-lived cloud identity where supported; restrict token claims and trusted branches. |
| Jenkins | Private-network runners and shared libraries suit existing enterprise delivery estates. | Terraform, OpenTofu, Pulumi | A Jenkinsfile builds and tests once; a shared deploy library applies the reviewed artifact and records evidence. | Isolate agents, pin plugins and dependencies, and scope credentials to a job and environment. |
| GitLab CI | Merge-request tests, protected environments, and configurable runners keep delivery close to source control. | Terraform, OpenTofu, Pulumi | Stage-specific jobs publish an immutable artifact and invoke the chosen platform deployment adapter. | Use protected runners and environment permissions; identity federation depends on the target provider. |
| Azure DevOps Pipelines | Native Azure delivery and enterprise service connections suit Azure-centered teams. | Bicep, Terraform, Pulumi | For ADF use validated factory artifacts and environment parameterization; for Databricks use bundles or the supported API. | ADF factory resource deployment and pipeline definition publishing are separate lifecycle steps. |
| AWS CodePipeline and CodeBuild | Native AWS build roles and pipeline stages reduce cross-service identity plumbing. | AWS CDK, Terraform, Pulumi | Publish job artifacts and apply the chosen AWS or warehouse deployment adapter; CDK synthesizes CloudFormation. | Build VPC access, source connection, artifact encryption, and least-privilege deploy roles must be provisioned. |
| Google Cloud Build | Containerized build steps integrate with Google service accounts and artifact storage. | Terraform, Pulumi, OpenTofu | Build a job image or template and deploy through Dataflow, Composer, Cloud Run, or warehouse-specific interfaces. | Cloud Deploy has supported workload targets; data jobs require their actual job APIs rather than assumed generic support. |
| GitHub or GitLab build with Argo CD | A reconciler promotes declared Kubernetes manifests and makes drift visible. | OpenTofu, Terraform, Pulumi | CI updates the reviewed image digest or Helm values in Git; Argo CD reconciles the selected namespace. | Argo CD reconciles Kubernetes resources; cloud infrastructure and managed warehouse DDL remain separately owned. |
| Tekton pipelines on Kubernetes | Kubernetes-native task execution can fit a self-managed platform engineering estate. | OpenTofu, Terraform, Pulumi | Pipeline tasks execute tests and platform-specific deploy steps; cloud resource state stays in the chosen IaC backend. | Operators must manage cluster availability, runner permissions, artifact provenance, and secrets. |

## Release lifecycle

1. A PR changes source code, configuration, contracts, tests, diagrams, and IaC intent together.
2. Run fast deterministic unit and contract tests plus plan/policy and dependency checks.
3. Build a wheel, JAR, container, compiled SQL/dbt project, or platform artifact once and record its digest.
4. Deploy that artifact to isolated staging with environment-specific identities and parameters.
5. Run real-interface integration, permissions, replay, reconciliation, and representative workload probes.
6. Promote the same artifact using the organization release policy. Keep stateful job migration and destructive DDL separate.
7. Observe consumer freshness, completeness and business totals; stop or repair publication if the contract regresses.

## GitHub Actions example for this documentation repository

This runnable example validates the study documents only. It does not deploy cloud resources or process production data. A real platform pipeline adds the selected build, IaC-plan, staging, target-specific deploy and product-validation jobs. OIDC should scope any cloud role to the approved repository, workflow, branch and environment. [GitHub Actions OIDC](https://docs.github.com/en/actions/concepts/security/openid-connect).

```yaml
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


Pin trusted action releases to reviewed commit SHAs in a production workflow. Untrusted PR code must not obtain deployment credentials or run on a broadly privileged private runner.

## Jenkins example

This Jenkinsfile runs the same documentation gate on a configured Python agent. In a real platform add immutable artifact publication, selected IaC preview, staging tests, controlled deployment and post-release probes; use scoped agents and a reviewed shared library. [Jenkins Pipeline](https://www.jenkins.io/doc/book/pipeline/).

```groovy
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


## GitLab CI example

The agent or image must contain the chosen Python version. Add target-specific deployment stages separately and keep protected environment credentials out of untrusted merge-request jobs. [GitLab CI CD](https://docs.gitlab.com/ci/).

```yaml
stages: [test]
design_catalog:
  stage: test
  image: python:3.12-slim
  script:
    - python3 data_system_design/tools/validate_design_docs.py
```


## Native cloud and GitOps translations

| Target | Translation | Boundary |
| --- | --- | --- |
| Azure DevOps | Use script tasks for identical gates; deploy Bicep/ARM or selected Terraform/Pulumi; use supported ADF artifacts, Databricks bundles or Fabric item deployment. | Deploy identities and private agents deliberately; preserve checkpoints and trigger behavior. |
| AWS CodePipeline/CodeBuild | Use a buildspec to run gates, publish to the artifact store, and execute selected CDK/CloudFormation or provider deployment steps. | The build role, network paths and actual job APIs remain part of the architecture. |
| Google Cloud Build | Use container steps for gates, artifact builds and selected resource/job APIs. | Cloud Deploy is not assumed to deploy every data-platform item. |
| Argo CD | CI publishes a reviewed image digest and manifests; Argo CD reconciles Kubernetes resources. | Managed warehouses, cloud network state and historical data are separately managed. |
| Tekton | Represent build/test/deploy as Kubernetes tasks with scoped workload identities. | You own the cluster, pipeline controller, artifact store and recovery. |

## Platform artifact differences

| Platform artifact | Deploy mechanism | Additional release test |
| --- | --- | --- |
| SQL/dbt model | Supported warehouse adapter plus migration or grants workflow | SQL/type parity, downstream golden queries and expand-and-contract schema checks |
| Spark batch job | Wheel/JAR/container plus job definition | Runtime dependencies, partition correctness and idempotent retry |
| Flink stream job | JAR/container plus controlled state/savepoint transition | State serializer compatibility and crash-after-sink-commit replay |
| ADF factory | Supported publish/build artifact plus environment deployment | Linked service resolution, parameters, trigger handling and stable progress identities |
| Databricks assets | Declarative Automation Bundles and supported CLI/API | Validate/deploy/run in staging; verify permissions, source paths and checkpoint separation |
| Fabric assets | Supported item Git/deployment APIs and environment configuration | Verify per-item support, capacity, bindings, permissions and actual runtime execution |
| Kubernetes service | Helm or manifests with an immutable image digest | Readiness, rollback, workload identity and external service connectivity |

Databricks Declarative Automation Bundles were formerly called Databricks Asset Bundles. Bundle definitions and platform APIs have their own compatibility requirements. [Databricks Declarative Automation Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/). ADF CI/CD uses factory definitions and environment deployment artifacts; a Git push alone does not prove successful runtime execution. [ADF CI CD](https://learn.microsoft.com/en-us/azure/data-factory/continuous-integration-delivery).

## Pairwise automation selection

Choose one deployment owner per resource. CI can invoke Terraform, OpenTofu, Pulumi, or a supported native tool, and then call a platform-specific job deployment adapter. Governance tests remain mandatory regardless of the CI engine. For Kubernetes choose GitOps only for the resources it actually reconciles. Plan artifacts, logs and state must use an approved access and retention policy.

## Rollback data and code separately

Reverting a Git commit does not undo already-published tables, external API updates, erased data, incompatible stream state, or warehouse DDL. Retain recoverable release manifests and use a scenario-specific repair or replay path. For changes that cannot be safely reversed, prefer an explicit forward fix or shadow rebuild with verified consumer cutover.
