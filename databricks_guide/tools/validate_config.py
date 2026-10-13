"""Offline configuration-shape checks; does not contact a Databricks workspace."""
from pathlib import Path
import json,re,sys
import yaml,regex
from jsonschema import Draft202012Validator, validators, ValidationError
BASE=Path(__file__).resolve().parents[1]

def unicode_pattern(validator, pattern, instance, schema):
    # The official CLI schema uses Unicode \p{L}/\p{N}, unsupported by Python re.
    if isinstance(instance,str) and not regex.search(pattern,instance):
        yield ValidationError(f'{instance!r} does not match {pattern!r}')
Validator=validators.extend(Draft202012Validator,{'pattern':unicode_pattern})
schema=json.loads((BASE/'tools/bundle-schema-cli-1.18.0.json').read_text())
v=Validator(schema)
examples=BASE/'examples'
bundles=[examples/'databricks.yml',examples/'lakeflow_bundle/databricks.yml',examples/'templates/classic-job.example.yml',examples/'templates/for-each.example.yml']
count=0
for p in sorted(examples.rglob('*.yml')):
    yaml.safe_load(p.read_text());count+=1
for p in bundles:
    obj=yaml.safe_load(p.read_text())
    if p==examples/'databricks.yml':
        obj.update(yaml.safe_load((examples/'resources/orders.job.yml').read_text()))
    errors=list(v.iter_errors(obj))
    if errors:
        for e in errors:print(p, list(e.absolute_path),e.message)
        raise SystemExit(1)
job=yaml.safe_load((examples/'resources/orders.job.yml').read_text())['resources']['jobs']['orders_daily']
keys={t['task_key'] for t in job['tasks']}
for task in job['tasks']:
    for dep in task.get('depends_on',[]):assert dep['task_key'] in keys,dep
    path=examples/'resources'/task['notebook_task']['notebook_path']
    assert path.is_file(),path
    assert path.read_text().startswith('# Databricks notebook source'),path
# Validate no unresolved custom bundle variable name and references are coherent.
for p in bundles:
    obj=yaml.safe_load(p.read_text());allowed=set(obj.get('variables',{}))
    content=p.read_text()
    if p==examples/'databricks.yml':content+=(examples/'resources/orders.job.yml').read_text()
    for variable in re.findall(r'\$\{var\.([a-zA-Z_][a-zA-Z_0-9]*)\}',content):
        assert variable in allowed,(p,variable)
print(f'PASS: {count} YAML files parse; {len(bundles)} bundle examples match CLI 1.18.0 schema; primary job paths/DAG/variables are coherent.')
print('Scope: offline shape checks only. Run authenticated bundle validate and workspace integration tests before deployment.')
