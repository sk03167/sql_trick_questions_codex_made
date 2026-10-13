"""Repository-local completeness, link, fixture, code-syntax, and diagram checks."""
from pathlib import Path
import ast,json,re,hashlib
from urllib.parse import unquote
BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parent
catalog=json.loads((BASE/'catalog.json').read_text())
for entry in catalog['chapters']+catalog['scenarios']:
    p=ROOT/entry['path'];assert p.is_file(),p
    text=p.read_text()
    for heading in ['Data design','Governance','Tests']:
        assert heading.lower() in text.lower(),(p,heading)
    assert 'code push' in text.lower() or 'ci/cd' in text.lower(),(p,'Code automation section missing')
markdown=list(BASE.rglob('*.md'))+[ROOT/'DATABRICKS_GUIDE_INDEX.md']
links=0
actual=[]
for p in markdown:
    text=p.read_text()
    fences=re.findall(r'^```[^\n]*$',text,re.M)
    assert len(fences)%2==0,(p,'Unclosed fence')
    for destination in re.findall(r'\]\(([^)]+)\)',text):
        if destination.startswith(('https://','http://','#','mailto:')):continue
        target=destination.split('#',1)[0].strip('<>')
        if target:
            assert (p.parent/unquote(target)).exists(),(p,target)
            links+=1
    for i,source in enumerate(re.findall(r'```mermaid\n(.*?)```',text,re.S),1):
        actual.append((p.stem+f'-{i}',source.strip()))
for p in BASE.rglob('*.py'):
    ast.parse(p.read_text(),filename=str(p))
for p in (BASE/'examples/fixtures').glob('orders_*.json'):
    for line in p.read_text().splitlines():assert isinstance(json.loads(line),dict),p
manifest=json.loads((BASE/'diagram_manifest.json').read_text())
assert sorted(actual)==sorted((d['id'],d['source']) for d in manifest),'Stale diagram manifest'
report_path=BASE/'diagram_validation.json'
if report_path.exists():
    report=json.loads(report_path.read_text());assert not report['errors'],report['errors']
    assert report['checked']==len(manifest)
    byid={d['id']:d for d in report['diagrams']}
    for d in manifest:assert byid[d['id']]['sourceSha256']==hashlib.sha256(d['source'].encode()).hexdigest(),d['id']
print(f"PASS: {len(catalog['chapters'])} chapters, {len(catalog['scenarios'])} scenarios, {links} local references, Python syntax/JSON fixtures, {len(manifest)} diagrams coherent.")
