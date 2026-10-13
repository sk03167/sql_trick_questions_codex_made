# Reviewed templates to adapt

These files are examples and are **not activated cloud deployments**. Supply real identifiers, protected identity configuration, supported runtime settings, network access, and UC grants before using them.

| File | Contents | Prerequisites / scope |
|---|---|---|
| [classic-job.example.yml](classic-job.example.yml) | Classic job compute with runtime/node/policy variables | Standalone illustrative bundle; only ingestion task |
| [for-each.example.yml](for-each.example.yml) | JSON job parameter → loop → notebook widget | Plumbing demo, not metadata-driven extraction |
| [run-now.example.json](run-now.example.json) | Job runtime parameters and request idempotency token | Use with actual job ID; request token does not make table writes idempotent |
| [api_extract.py](api_extract.py) | Bounded HTTP retry and page/manifest contract | Adapt vendor contract/allowlist; use staging outside watched landing |
| [github-deploy.example.yml](github-deploy.example.yml) | Protected environment + GitHub OIDC | Managed runner with pinned CLI; federation policy |
| [azure-pipelines.example.yml](azure-pipelines.example.yml) | Azure DevOps protected OAuth variable group | Managed agent, CLI, protected variables |
| [Jenkinsfile.example](Jenkinsfile.example) | Credential binding and serialized deployment | Approved Jenkins agent/credential binding plugin |
| [gitlab-ci.example.yml](gitlab-ci.example.yml) | Manual protected deployment and resource group | CLI-equipped tagged runner, protected variables |
| [uc_bootstrap.tf](uc_bootstrap.tf) | Minimal catalog/schema IaC | Approved storage root, provider 1.137.0, reviewed backend/auth; not full bootstrap |

For the request JSON:

```sh
databricks jobs run-now <actual-job-id> --json @run-now.example.json --profile de-lab
```

Use one approved CLI version across development and runner images. The deployment templates assume it is already installed. Complete local tests and authenticated bundle validation, then run workspace fixtures before promotion. OAuth M2M fallbacks are not federation. GitHub environment subject, workspace assignment, source-code rights, run-as privileges, and UC grants must match.

The active repository CI only runs local documentation/configuration/tests/diagram checks. Copy a deployment template into your application workflow folder only after completing the environment setup.

Terraform syntax/provider-schema validation passed with Terraform 1.16.4 and Databricks provider 1.137.0, without plan/apply. Copy [the sample lock](terraform.lock.example.hcl) to `.terraform.lock.hcl` in the standalone Terraform project or generate an approved lock for your platforms; never copy provider binaries/state into Git.
