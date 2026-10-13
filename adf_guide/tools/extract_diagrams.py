from pathlib import Path
import json,re,os
b=Path(__file__).resolve().parents[1];r=b.parent;manifest=[]
for root,dirs,names in os.walk(b):
 dirs[:]=[d for d in dirs if d not in {'node_modules','downloads','arm-output','private','__pycache__','.venv'}]
 for name in sorted(names):
  if not name.endswith('.md'):continue
  p=Path(root)/name;text=p.read_text()
  for i,s in enumerate(re.findall(r'```mermaid\n(.*?)```',text,re.S),1):
   manifest.append(dict(id=p.stem+f'-{i}',path=str(p.relative_to(r)),source=s.strip(),summary=text.splitlines()[0].lstrip('# ')))
manifest.sort(key=lambda d:(d['path'],d['id']))
(b/'diagram_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Extracted',len(manifest),'authored diagrams')
