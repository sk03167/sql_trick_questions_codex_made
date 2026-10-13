"""Focused local acceptance oracle. This is not an ADF/SQL execution emulator."""
from pathlib import Path,PurePosixPath
from decimal import Decimal
import csv,hashlib,re
from copy import deepcopy

def batch_prefix(root,batch):
    if not re.fullmatch(r'[a-z][a-z0-9-]{0,99}',batch):raise ValueError('Invalid batch ID')
    path=PurePosixPath(root)
    if path.is_absolute() or '..' in path.parts or not root:raise ValueError('Invalid relative root')
    return str(path/('batch='+batch))

def summarize_csv(paths):
    count,totals,ids=0,{},set()
    for path in paths:
        with Path(path).open(newline='') as stream:
            rows=csv.DictReader(stream)
            if rows.fieldnames!=['order_id','amount','region']:raise ValueError('Unexpected schema')
            for row in rows:
                if not row['order_id'] or row['order_id'] in ids:raise ValueError('Duplicate/missing order ID')
                ids.add(row['order_id'])
                if not re.fullmatch(r'[0-9]{1,16}(\.[0-9]{1,2})?',row['amount']):raise ValueError('Invalid cents')
                if not row['region']:raise ValueError('Missing region')
                amount=Decimal(row['amount']);totals[row['region']]=totals.get(row['region'],Decimal('0.00'))+amount
                count+=1
    return {'records':count,'revenue':totals}

def verify_copy(source,sink,names):
    if len(names)!=len(set(names)):raise ValueError('Duplicate expected filename')
    for name in names:
        p=PurePosixPath(name)
        if p.is_absolute() or '..' in p.parts:raise ValueError('Unsafe relative filename')
    def inventory(root):return {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    source,sink=Path(source),Path(sink)
    if inventory(source)!=set(names) or inventory(sink)!=set(names):raise ValueError('Incomplete or unexpected file set')
    for name in names:
        a=hashlib.sha256((source/name).read_bytes()).digest();b=hashlib.sha256((sink/name).read_bytes()).digest()
        if a!=b:raise ValueError('Changed/corrupt copy content')
    return summarize_csv([sink/name for name in names])

def commit_changes(state,watermark,expected_low,high,events):
    if watermark!=expected_low or high<expected_low:raise ValueError('Stale/invalid boundary')
    candidate=deepcopy(state);seen={}
    for event in events:
        e=dict(event);key=e['order_id'];v=e['version']
        if not isinstance(v,int) or isinstance(v,bool) or not expected_low<v<=high:raise ValueError('Outside source interval')
        if e['op'] not in {'I','U','D'}:raise ValueError('Invalid operation')
        payload=(e['op'],None if e['op']=='D' else e.get('amount'))
        position=(key,v)
        if position in seen and seen[position]!=payload:raise ValueError('Conflicting key/version')
        seen[position]=payload
        old=candidate.get(key)
        if old is not None and old['version']==v:
            old_payload=(old['op'],None if old['op']=='D' else old.get('amount'))
            if old_payload!=payload:raise ValueError('Conflict with retained state')
        if old is None or v>old['version']:candidate[key]=e
    return candidate,high

def live_keys(state):return {k for k,v in state.items() if v['op']!='D'}
