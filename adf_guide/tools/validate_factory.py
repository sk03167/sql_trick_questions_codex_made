"""Focused source graph/parameter contract checks, not Microsoft's full validator."""
from pathlib import Path
import json,re
B=Path(__file__).resolve().parents[1];F=B/'examples/factory'
entities={}
for kind in ['pipeline','dataset','linkedService','trigger','factory']:
 entities[kind]={}
 for path in (F/kind).glob('*.json'):
  obj=json.loads(path.read_text());assert obj['name']==path.stem,path
  assert obj['name'] not in entities[kind],path;entities[kind][obj['name']]=obj

def walk(value):
 yield value
 if isinstance(value,dict):
  for v in value.values():yield from walk(v)
 elif isinstance(value,list):
  for v in value:yield from walk(v)
refs=0;expressions=0
mapping={'DatasetReference':'dataset','LinkedServiceReference':'linkedService','PipelineReference':'pipeline'}
for kind,objects in entities.items():
 for name,obj in objects.items():
  declared=set(obj['properties'].get('parameters',{}))
  for value in walk(obj):
   if isinstance(value,dict) and value.get('type') in mapping:
    target_kind=mapping[value['type']];target=value['referenceName'];assert target in entities[target_kind],(kind,name,target)
    supplied=set(value.get('parameters',{}));allowed=set(entities[target_kind][target]['properties'].get('parameters',{}))
    assert supplied<=allowed,(name,target,'Unknown reference parameters',supplied-allowed);refs+=1
   if isinstance(value,str):
    scope={'pipeline':'pipeline','dataset':'dataset','linkedService':'linkedService'}.get(kind)
    if scope:
     pattern=rf'{scope}\(\)\.(?:parameters\.)?([A-Za-z_][A-Za-z_0-9]*)'
     for parameter in re.findall(pattern,value):
      if parameter in {'RunId','TriggerTime','globalParameters'}:continue
      assert parameter in declared,(kind,name,parameter);expressions+=1
    # Samples must contain no stored plaintext access token/password.
   if isinstance(value,dict):
    for sensitive in ['password','accountKey','servicePrincipalKey','clientSecret']:
     if sensitive in value:assert isinstance(value[sensitive],dict) and value[sensitive].get('type') in {'AzureKeyVaultSecret','SecureString'},(name,sensitive)

def activities(items,pipeline):
 names={a['name'] for a in items};assert len(names)==len(items),(pipeline,'Duplicate activity')
 for a in items:
  for dep in a.get('dependsOn',[]):
   assert dep['activity'] in names,(pipeline,a['name'],dep)
   assert set(dep['dependencyConditions'])<={'Succeeded','Failed','Skipped','Completed'},dep
  props=a.get('typeProperties',{})
  for group in ['activities','ifTrueActivities','ifFalseActivities','defaultActivities']:
   if group in props:activities(props[group],pipeline)
  if a['type']=='ForEach':
   for nested in walk(props.get('activities',[])):
    if isinstance(nested,dict):assert nested.get('type') not in {'SetVariable','AppendVariable'},(pipeline,'Sample parallel loop must pass immutable child inputs')
for name,obj in entities['pipeline'].items():activities(obj['properties']['activities'],name)
for name,obj in entities['trigger'].items():assert obj['properties']['runtimeState']=='Stopped',(name,'Example trigger must remain stopped')
arm=json.loads((B/'examples/generated_arm/ARMTemplateForFactory.json').read_text())
param=json.loads((B/'examples/templates/test.parameters.example.json').read_text())
assert set(arm['parameters'])==set(param['parameters']),'Environment/export parameter contract differs'
assert len(arm['resources'])==sum(len(entities[x]) for x in ['pipeline','dataset','linkedService','trigger'])
print(f'PASS: {sum(map(len,entities.values()))} source objects; {refs} references; {expressions} scoped parameter uses; child graph, stopped trigger and ARM override contracts.')
print('Also run Microsoft validate/export and live ADF tests; this checker covers only the supplied educational contracts.')
