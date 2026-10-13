# Local verification tools

Run from repository root.

```sh
python3 -m unittest discover -s databricks_guide/examples/tests -v
python3 databricks_guide/tools/validate_guide.py
python3 -m pip install -r databricks_guide/tools/requirements.txt
python3 databricks_guide/tools/validate_config.py
npm ci --prefix databricks_guide/tools --ignore-scripts --no-audit --no-fund
npm exec --prefix databricks_guide/tools -- playwright install chromium
node databricks_guide/tools/render_diagrams.cjs
```

Linux runners may need `playwright install --with-deps chromium`. To use an existing isolated test Chromium, set DESIGN_CHROMIUM_PATH to its executable. DIAGRAM_RUNTIME_DIR can point at installed Mermaid/Playwright packages. Do not use a personal browser profile.

validate_guide.py checks chapter/scenario/index references, Python syntax, JSON fixtures, and diagram manifest/hash coherence. validate_config.py parses YAML and checks four bundle shapes against the official schema produced by `databricks bundle schema` with installed CLI 1.18.0. The Unicode pattern validator uses regex to preserve the official schema's Unicode rules. It does not omit schema checks or perform authenticated CLI validation.

The renderer parses/renders all diagrams and checks nonempty geometry, overlapping flowchart node bounds, and label clipping. Samples are exported to rendered/. These geometry checks do not prove every edge label is perfectly placed; sample visual inspection complements them.

The schema snapshot is a tool compatibility reference, not a workspace version guarantee. Refresh deliberately from a reviewed CLI, review diffs, and run authenticated bundle validation and workspace tests before deploying. The source_validation.json report records official URL resolution/title checks; it does not verify a live Databricks UI. Terraform formatting/provider-schema validation was run separately (Terraform 1.16.4, provider 1.137.0); Jenkins execution and cloud provisioning were not performed.
