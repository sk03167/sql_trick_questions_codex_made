#!/usr/bin/env python3
"""Validate catalog completeness, links, diagram consistency, and assembly constraints."""
from pathlib import Path
import hashlib,json,re,sys
from enumerate_designs import candidates
ROOT=Path(__file__).resolve().parents[1]
REQUIRED=['Requirements to clarify','Data design','Governance and infrastructure automation','Code delivery and runtime automation','Tests to run and automate','Failure recovery and tradeoffs','Explore the documented combinations','Source references']

def validate(root=ROOT):
    items=json.loads((root/'design_candidates.json').read_text())
    diagrams=json.loads((root/'diagram_manifest.json').read_text())
    files=sorted((root/'scenarios').glob('S*.md'))
    assert len(files)==43,f'Expected 43 scenario documents, got {len(files)}'
    assert len({d['id'] for d in diagrams})==len(diagrams),'Duplicate diagram ID'
    scenario_ids={f.name[:3] for f in files}
    assert scenario_ids=={f'S{i:02}' for i in range(1,44)}
    assert {x['scenario'] for x in items}==scenario_ids
    assert len({(x['scenario'],x['reference']['id']) for x in items})==len(items)
    for f in files:
        text=f.read_text()
        for heading in REQUIRED:assert f'## {heading}\n' in text,f'Missing {heading} in {f.name}'
        blocks=re.findall(r'```mermaid\n(.*?)\n```',text,re.S)
        manifest=[d['source'] for d in diagrams if d['scenario']==f.name[:3]]
        assert blocks==manifest,f'Diagram manifest mismatch {f.name}'
        assert len(blocks)>=6,f'Insufficient diagrams in {f.name}'
        assert text.count('**Why this path helps:**')>=4
        assert 'What must be designed and verified' in text
        assert 'Replace each component deliberately' in text
    for d in diagrams:
        assert (root/d['path']).read_text().strip()==d['source'].strip(),f'Changed diagram {d["id"]}'
        assert d['summary'].strip()
    doc_files=files+list(root.glob('*.md'))+[root.parent/'DATA_SYSTEM_DESIGN_INDEX.md']
    links=0
    for f in doc_files:
        text=f.read_text()
        assert text.count('```')%2==0,f'Unbalanced code fences in {f.name}'
        for target in re.findall(r'\]\(([^)]+)\)',text):
            if '://' in target:continue
            path,sep,fragment=target.partition('#')
            dest=(f.parent/path).resolve() if path else f
            assert dest.exists(),f'Broken file link in {f.name}: {target}'
            if fragment:
                headings=re.findall(r'^#+ (.+)$',dest.read_text(),re.M)
                slugs={re.sub(r'[^\w\- ]','',h.lower()).replace(' ','-') for h in headings}
                assert fragment in slugs,f'Broken heading link in {f.name}: {target}'
            links+=1
    count=0;identities=set();ci_seen=set();cloud_seen=set()
    for item in candidates(items):
        count+=1
        ident=tuple(item[k] for k in ['scenario','reference_path','cloud','data_bundle','runtime_orchestration','governance','ci_id','iac'])
        assert ident not in identities,f'Duplicate design identity {ident}'
        identities.add(ident);ci_seen.add(item['ci_id']);cloud_seen.add(item['cloud'])
        if item['ci_id'] in {'aws','azure','gcp'}:assert item['cloud']==item['ci_id']
        if item['ci_id'] in {'argo','tekton'}:
            base=next(x['reference'] for x in items if x['scenario']==item['scenario'] and x['reference']['id']==item['reference_path'])
            assert base['k8s']
        assert item['qualification'] and item['status'].startswith('proposed')
        assert all(item['stages'][k] for k in ['ingest','storage','compute','serve'])
    assert ci_seen=={'github','jenkins','gitlab','azure','aws','gcp','argo','tekton'}
    assert cloud_seen=={'aws','azure','gcp','oss','oci','ibm'}
    # Independent structural count checks the generator and detects omissions.
    expected=sum(len(x['data_variants'])*len(x['schedulers'])*len(x['governance'])*sum(len(a['infra']) for a in x['automation']) for x in items)
    assert count==expected
    # Adversarial records prove invalid cloud and runtime combinations are excluded.
    sample=items[0].copy(); sample['reference']=sample['reference'].copy(); sample['reference']['cloud']='azure';sample['reference']['k8s']=False
    sample['automation']=[{'id':'aws','name':'bad cloud','clouds':['aws'],'runtime':'any','infra':['Terraform']}, {'id':'argo','name':'bad runtime','clouds':['*'],'runtime':'k8s','infra':['Terraform']}]
    assert list(candidates([sample]))==[]
    sample['reference']['k8s']=True
    assert {x['ci_id'] for x in candidates([sample])}=={'argo'}
    index=(root.parent/'DATA_SYSTEM_DESIGN_INDEX.md').read_text()
    assert f'**{count:,} assembled design candidates**' in index
    for f in files:assert f.name in index,f'Missing scenario from index: {f.name}'
    render_path=root/'diagram_validation.json'
    if render_path.exists():
        render=json.loads(render_path.read_text())
        assert render['errors']==[] and render['checked']==len(diagrams)
        proof={x['id']:x for x in render['diagrams']}
        for d in diagrams:
            assert proof[d['id']]['sourceSha256']==hashlib.sha256(d['source'].encode()).hexdigest(),f'Stale diagram render: {d["id"]}'
    return dict(scenarios=len(files),reference_paths=len(items),diagrams=len(diagrams),assemblies=count,local_links=links)

if __name__=='__main__':
    result=validate()
    print('PASS: '+', '.join(f'{v} {k}' for k,v in result.items()))
