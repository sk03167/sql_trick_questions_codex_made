# Generated ARM snapshot and verified parameter contract

These two ARM JSON files were generated from this guide's source using the official Microsoft utility. EXPORT_METADATA.json records runtime/wrapper version, current downloaded validation-bundle hash, generated resource count and parameter names. Source endpoints and factory ID are illustrative; generation is not deployment.

| Parameter | Purpose |
|---|---|
| factoryName | Actual target factory name |
| ls_adls_properties_parameters_p_account_url_defaultValue | Target ADLS linked-service account URL default |
| ls_rest_public_example_properties_typeProperties_url | Target REST base URL |

The custom definition parameterizes non-sensitive endpoints without replacing the runtime `@linkedService().p_account_url` expression itself. Review custom definitions when adding real connector secret/auth settings; this minimal project isn't a complete enterprise parameterization policy.

Generate real environment parameters with tools/make_parameters.py, or adapt templates/test.parameters.example.json. The helper rejects a changed export parameter contract so missing endpoint overrides are visible. The file's default REST endpoint deliberately remains fake until adapted.

Regenerate through `npm run build -- export ... arm-output` and promote that same tested artifact. Generated pre/post deployment scripts/linked templates are available in the export output; they are not duplicated as manually maintained source here. Application ARM assumes the target factory/platform is already provisioned. Trigger state restoration/cleanup is governed by the release process; don't assume generated ARM alone starts or preserves every intended operational state.
