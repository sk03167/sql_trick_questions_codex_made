# Verification and execution limits

Researched/validated on 2026-10-13. UI recipes follow official Microsoft documentation, not recorded live clicks. All 82 official source links resolve; source_validation.json records titles/redirects.

## Completed checks

- 21 local unittest cases pass, including 150 deterministic reordered-event runs, duplicate/conflicting versions, late deletes, stale watermarks, atomic candidate-state rejection, file set/hash/schema/decimal reconciliation, missing/extra/corrupt files and path validation.
- Eleven sample source objects have coherent names/references, parameter scopes, child graph, stopped trigger and generated ARM override contracts.
- Microsoft's official utilities 1.0.3 validate/export the definitions successfully with Node 22.23.3. Ten deployable application resources and the three actual ARM parameter names are recorded. The tool fetches Microsoft's current validation bundle; its authoring SHA256 is recorded with generated metadata.
- Factory-bootstrap Bicep compiles successfully with Bicep 0.48.1 through an isolated temporary Azure CLI configuration. No Azure authentication/plan/deployment occurred.
- Owned Python/JSON syntax, Markdown references/index/structure and diagram manifest/hash coherence are checked.
- 58 Mermaid diagrams parse/render successfully in isolated Chromium; nonempty geometry, flowchart node overlap and label bounds checks pass. Ten SVG/PNG samples are visually reviewed/exported.

## Reproduce local checks

```sh
python3 -m unittest discover -s adf_guide/examples/tests -v
python3 adf_guide/tools/validate_factory.py
python3 adf_guide/tools/validate_guide.py
npm ci --prefix adf_guide/tools --ignore-scripts --no-audit --no-fund
cd adf_guide/tools
npm run build -- export ../examples/factory \
  '/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-adf-guide/providers/Microsoft.DataFactory/factories/adf-guide-dev' arm-output
npm exec -- playwright install chromium
node render_diagrams.cjs
```

Linux may need playwright install --with-deps chromium. The active GitHub workflow runs local checks, Microsoft export and diagram validation with no Azure credentials.

## Not executed

No real Azure factory, identity, linked-service connection, SHIR installation/registration, private endpoint, data source, Copy, Mapping Data Flow/CDC, SQL procedure, Databricks notebook, schedule/window/event trigger, live API or cloud release template was authenticated/provisioned/executed. Definition export is not a credential or data test. Local reference rules are not an ADF/SQL expression/runtime emulator. The SQL companion needs real database testing and production adaptation.

## Required live acceptance

Use the worked lab and chapter 28 test matrix: actual identities/IR/network, correctly resolved parameters, retry/failure propagation, source completion/delete/ordering/retention, data reconciliation, allowed/denied access, performance/source load, trigger release handling and recovery. The Copy lab's nonempty-file gate is intentionally only one guardrail. Use additional content checks and stable downstream batch/key idempotency before production publication.
