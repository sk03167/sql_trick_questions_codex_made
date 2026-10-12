# Data Design Catalog Validation

Validated on October 12, 2026. These checks verify the study library and its diagrams. The cloud deployments and workload tests proposed inside the scenarios were not executed.

| Check | Result |
| --- | --- |
| Scenario documents and required sections | 43 passed |
| Reference paths with explicit stages | 274 passed |
| Combination enumeration and unique candidate identities | 62,181 passed |
| Invalid cloud and Kubernetes combination probes | Passed |
| Mermaid syntax and SVG rendering | 377 passed |
| Flowchart node overlap and label containment | Passed for rendered flowchart shapes |
| Nonempty diagram geometry and visible labels | Passed |
| Document and editable-source consistency | Passed |
| Render evidence matches source SHA256 | Passed |
| Static PNG and SVG examples | 13 exported |

The document validator checks local file/heading links, balanced code fences, complete scenario indexing, exact embedded/source diagram agreement, candidate uniqueness, eligible CI/IaC scope, and rejection of deliberately invalid combinations. The final local-link count is reported by the validator because gallery and tooling links add to the total.

Mermaid 12.1.0 and Playwright 1.64.0 rendered every source in an isolated Chromium test browser. The renderer recorded geometry, label and flowchart node checks with source hashes in [diagram_validation.json](diagram_validation.json). The logical-model and sequence samples were visually reviewed for readable labels and relationships; representative data flow, governance and retrieval samples were also inspected.

## Reproduce the checks

```sh
python3 data_system_design/tools/validate_design_docs.py
python3 data_system_design/tools/enumerate_designs.py --count
# See DIAGRAM_GALLERY.md for locked dependency and browser setup.
node data_system_design/tools/render_diagrams.cjs
```

## Limits of this verification

An assembled candidate is an original proposed architecture, not a connector certification or deployed benchmark. These checks do not establish cloud regional availability, tier/edition capabilities, licensing, private-network connectivity, complete reader/writer interoperability, real data correctness, cost or latency targets. The scenario and compatibility documents explicitly state the integration and operational evidence required before implementation. GitHub may use a different Mermaid renderer version; the diagrams use basic flowchart, sequence, ER and state syntax, and static examples provide a fallback.
