# Verification and execution limits

Authoring date: 2026-10-13. The branch was authored against current official Databricks/Microsoft/Spark documentation; [source URL checks](source_validation.json) record all 81 references and redirects. UI recipes are documentation-based, not live workspace click recordings.

## Local checks completed

- 21 unittest cases pass, including 200 deterministic arrival-order shuffles plus retries, late deletes, conflict rejection, correction/removal of gold groups, decimal revenue, invalid fractional-cents/overflow rejection, UTC date boundaries, pagination loops, partial extraction and bounded 429/401 behavior.
- Terraform formatting and provider-schema validation pass with Terraform 1.16.4 and Databricks provider 1.137.0; no plan/apply or workspace call was made.
- Eight YAML files parse. Four standalone/assembled bundle examples validate against the official CLI 1.18.0 schema snapshot; main task paths, dependencies, and variable references are coherent.
- All owned Python files parse; JSON fixture lines parse; all local Markdown references and chapter/scenario index entries are checked.
- 58 Mermaid diagrams parse and render in an isolated Chromium browser. Nonempty geometry, flowchart node overlap, and label clipping checks pass. Ten PNG/SVG samples are included. Diagram hashes match the Markdown sources.
- Official source URLs resolve successfully; the link check validates resolution/titles, not every workspace-specific capability.

## Commands to reproduce

```sh
python3 -m unittest discover -s databricks_guide/examples/tests -v
python3 databricks_guide/tools/validate_guide.py
python3 -m pip install -r databricks_guide/tools/requirements.txt
python3 databricks_guide/tools/validate_config.py
npm ci --prefix databricks_guide/tools --ignore-scripts --no-audit --no-fund
npm exec --prefix databricks_guide/tools -- playwright install chromium
node databricks_guide/tools/render_diagrams.cjs
```

## Not executed without a configured workspace

No Databricks account/workspace was authenticated or provisioned. No live notebooks, Spark SQL, Auto Loader, Delta MERGE, Lakeflow/AUTO CDC/Connect, Databricks Connect, source connectors, UC/cloud IAM policies, private networking, SQL warehouse queries, sharing recipients, CI deployment templates, Jenkins pipeline, or Terraform apply were executed. Local reference tests are an independent oracle and do not substitute for engine execution. Bundle shape checks do not substitute for authenticated bundle validate.

The worked job includes a real assert_quality task and exact expected outputs for your workspace run. [The test strategy](chapters/25-test-strategy.md) and each scenario specify required integration, access, performance, retention and recovery tests. Templates have placeholders and are opt-in; the active GitHub workflow only performs local checks and has no Databricks credentials.

## Practical limits and next validation

The Jobs lab deliberately uses a complete bronze scan and full gold rebuild for small-fixture transparency. Production needs bounded incremental processing with durable contract/order checks, actual sizing, alerting and retention. The alternative Lakeflow lab drops/quarantines bad rows and assumes valid source sequence ordering; its contract differs from the Jobs lab's fail-on-invalid publication gate. Test those choices explicitly before promotion. Source API and cloud/runtime capabilities vary, and public previews/beta features are identified rather than assumed universally available.
