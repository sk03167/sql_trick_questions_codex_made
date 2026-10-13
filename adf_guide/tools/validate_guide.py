from pathlib import Path
import ast,json,re,hashlib,os
B=Path(__file__).resolve().parents[1];R=B.parent
catalog=json.loads((B/'catalog.json').read_text())
for entry in catalog['chapters']+catalog['scenarios']:
 p=R/entry['path'];assert p.is_file(),p;text=p.read_text()
 for heading in ['Data design','Governance','Code push','Tests']:assert heading.lower() in text.lower(),(p,heading)
def owned_files():
 for root,dirs,names in os.walk(B):
  dirs[:]=[d for d in dirs if d not in {'node_modules','downloads','arm-output','private','.terraform','.databricks','__pycache__','.venv','.git'}]
  for name in names:yield Path(root)/name
files=list(owned_files());markdown=[p for p in files if p.suffix=='.md']+[R/'AZURE_DATA_FACTORY_GUIDE_INDEX.md']
links=0;actual=[]
for p in markdown:
 text=p.read_text();assert len(re.findall(r'^```[^\n]*$',text,re.M))%2==0,(p,'Unclosed fence')
 for dest in re.findall(r'\]\(([^)]+)\)',text):
  if dest.startswith(('https://','http://','#','mailto:')):continue
  target=dest.split('#',1)[0]
  if target:assert (p.parent/target).exists(),(p,target);links+=1
 for i,s in enumerate(re.findall(r'```mermaid\n(.*?)```',text,re.S),1):actual.append((p.stem+f'-{i}',s.strip()))
for p in files:
 if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p))
 if p.suffix=='.json':json.loads(p.read_text())
manifest=json.loads((B/'diagram_manifest.json').read_text());assert sorted(actual)==sorted((d['id'],d['source']) for d in manifest),'Stale manifest'
report_path=B/'diagram_validation.json'
if report_path.exists():
 report=json.loads(report_path.read_text());assert not report['errors'];assert report['checked']==len(manifest)
 checked={d['id']:d for d in report['diagrams']}
 for d in manifest:assert checked[d['id']]['sourceSha256']==hashlib.sha256(d['source'].encode()).hexdigest(),d['id']
print(f"PASS: {len(catalog['chapters'])} chapters, {len(catalog['scenarios'])} scenarios, {links} local links, owned Python/JSON, {len(manifest)} diagrams.")
