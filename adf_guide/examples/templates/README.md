# Templates to adapt before use

These are opt-in examples, not active Azure deployments. Real identities, endpoints, resource IDs, network/source rights, protected environment setup and approved runner dependencies are prerequisites.

| File | Purpose | Scope |
|---|---|---|
| [run-copy.parameters.json](run-copy.parameters.json) | Live file-copy runtime values | Stable business batch, actual storage setup required |
| [run-parent.parameters.json](run-parent.parameters.json) | Safe parameter demo inputs | Real factory required, no external data source |
| [run-child-invalid.parameters.json](run-child-invalid.parameters.json) | Expected Fail input | Child INVALID_INPUT regression |
| [test.parameters.example.json](test.parameters.example.json) | Exact generated ARM keys | Replace target factory/endpoints |
| [factory-bootstrap.bicep](factory-bootstrap.bicep) | Factory identity bootstrap | No broad source grants/private endpoints |
| [factory-bootstrap.compiled.json](factory-bootstrap.compiled.json) | Verified compiler output | Bicep 0.48.1, not deployed |
| [github-deploy.example.yml](github-deploy.example.yml) | OIDC protected release lifecycle | Managed Node22/Azure CLI/datafactory/pwsh/Az agent |
| [azure-pipelines-build.example.yml](azure-pipelines-build.example.yml) | Build/export artifact | Add protected test/prod release stages |
| [Jenkinsfile.example](Jenkinsfile.example) | Build/export on approved agent | Add protected release consuming same artifact |
| [gitlab-ci-build.example.yml](gitlab-ci-build.example.yml) | Build/export artifact | Add protected serialized Azure release |

From repository root, generate the three verified overrides:

```sh
python3 adf_guide/tools/make_parameters.py \
  --template adf_guide/examples/generated_arm/ARMTemplateForFactory.json \
  --factory '<actual-test-factory>' \
  --storage-url 'https://<test-account>.dfs.core.windows.net' \
  --rest-url 'https://<approved-vendor-host>/' \
  --output /tmp/adf-test.parameters.json
```

Azure CLI published-run example after actual authentication/deployment:

```sh
az datafactory pipeline create-run --resource-group '<test-rg>' \
  --factory-name '<test-factory>' --name pl_parallel_parent \
  --parameters @adf_guide/examples/templates/run-parent.parameters.json
```

A create-run response is submission, not success. The opt-in live_smoke.py polls the actual terminal outcome with a deadline. It tests only parameter/control execution, not Copy or content/permissions/performance.

The GitHub example uses current exported pre/post trigger handling; inspect it and intended trigger states/cleanup before activation. It deliberately doesn't unconditionally restart processing after a failed deploy/smoke. Add real connector/data acceptance gates before production. Runner/identity examples for GitHub aren't automatically reusable as GitLab/Jenkins federation configuration.
