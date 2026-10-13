"""Check a newly generated artifact against the reviewed educational contract."""
from pathlib import Path
import json,sys
b=Path(__file__).resolve().parents[1];out=Path(sys.argv[1])
actual=json.loads((out/'ARMTemplateForFactory.json').read_text())
expected=json.loads((b/'examples/generated_arm/ARMTemplateForFactory.json').read_text())
assert set(actual['parameters'])==set(expected['parameters']),'ARM parameter keys changed; review overrides'
assert len(actual['resources'])==len(expected['resources']),'Resource count changed; review generated source snapshot'
for key,value in actual['parameters'].items():assert value['type']==expected['parameters'][key]['type'],key
print('PASS: newly exported resource count, parameter keys and types match reviewed contract; no deployment performed.')
