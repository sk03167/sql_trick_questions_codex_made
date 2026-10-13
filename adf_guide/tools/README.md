# Verification and build tools

Use supported Node20/22 and Python3. Local commands are in VERIFICATION.md and examples/README.md.

- validate_factory.py checks the educational source graph and scoped parameter/override contracts; Microsoft's validator is required beyond its limited rules.
- validate_guide.py checks only owned files, pruning node_modules, downloads, arm-output and caches. It checks local links, Python/JSON syntax and editable-diagram/hash coherence.
- make_parameters.py generates actual target overrides from the verified three-key ARM contract; review source/custom parameter changes before using a changed contract.
- live_smoke.py is opt-in and calls a real factory through the authenticated Azure CLI; local CI never invokes it.
- render_diagrams.cjs parses/renders every Mermaid diagram in an isolated browser and exports ten samples. Geometry checks complement visual review; they aren't proof of every edge-label layout.
- extract_diagrams.py refreshes the authored Markdown Mermaid manifest after edits; then run validation/render.

The pinned Microsoft npm wrapper downloads its current validator bundle on each validate/export. Network access to Microsoft's bundle is required; no Azure credentials are used for source validation. Track the runtime/package/bundle hash and generated parameter contract. Don't commit downloaded bundles/node_modules or temporary ARM output directories. Regenerate/publish the same reviewed artifact through your configured release process.
