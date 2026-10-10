#!/usr/bin/env python3
"""Execute documented SQL in isolated databases and compare independent oracles."""
from pathlib import Path
from collections import defaultdict, Counter, deque
from statistics import median
import argparse
import json
import random
import re
import sqlite3
import sys

ROOT = Path(__file__).resolve().parent
CATALOG = json.loads((ROOT/'catalog.json').read_text())
BY_ID = {q['id']: q for q in CATALOG}
CHECKS = Counter()


def execute(qid, replacements=None, alternative=None):
    with sqlite3.connect(':memory:') as db:
        # Abort accidental unbounded queries rather than hanging the verifier.
        steps = [0]
        def guard():
            steps[0] += 1
            return steps[0] > 10000
        db.set_progress_handler(guard, 1000)
        db.executescript((ROOT/'sql'/f'{qid}_setup.sql').read_text())
        if replacements is not None:
            for name, rows in replacements.items():
                db.execute(f'DELETE FROM {name}')
                if rows:
                    placeholders=','.join('?' for _ in rows[0])
                    db.executemany(f'INSERT INTO {name} VALUES ({placeholders})', rows)
        suffix = 'solution' if alternative is None else f'alternative_{alternative}'
        return db.execute((ROOT/'sql'/f'{qid}_{suffix}.sql').read_text()).fetchall()


def check(qid, expected, replacements=None, family='samples', alternatives=False):
    expected=[tuple(row) for row in expected]
    got=execute(qid,replacements)
    if got!=expected:
        raise AssertionError(f'{qid} {family}: expected {expected!r}, got {got!r}; input={replacements!r}')
    CHECKS[family]+=1
    if alternatives:
        for i in range(1,len(BY_ID[qid]['alternatives'])+1):
            got=execute(qid,replacements,alternative=i)
            if got!=expected:
                raise AssertionError(f'{qid} alternative {i} {family}: expected {expected!r}, got {got!r}')
            CHECKS['alternatives' if family=='samples' else family]+=1


def samples(selected):
    questions=(ROOT/'QUESTIONS.md').read_text()
    solutions=(ROOT/'SOLUTIONS.md').read_text()
    assert len(CATALOG)==50 and len(BY_ID)==50
    assert len(re.findall(r'^## Q\d\d ', questions, re.M))==50
    assert len(re.findall(r'^## Q\d\d ', solutions, re.M))==50
    for qid in sorted(selected):
        q=BY_ID[qid]
        sql=(ROOT/'sql'/f'{qid}_solution.sql').read_text().strip()
        assert sql==q['sql'].strip()
        assert f'```sql\n{sql}\n```' in solutions
        setup=(ROOT/'sql'/f'{qid}_setup.sql').read_text().strip()
        assert f'```sql\n{setup}\n```' in questions
        check(qid,q['expected'],alternatives=True)
        for i,(name,sql) in enumerate(q['alternatives'],1):
            extracted=(ROOT/'sql'/f'{qid}_alternative_{i}.sql').read_text().strip()
            assert extracted==sql.strip()
            assert f'```sql\n{extracted}\n```' in solutions
    # Check every internal file+heading link in all three study files.
    for path in [ROOT/'README.md',ROOT/'QUESTIONS.md',ROOT/'SOLUTIONS.md']:
        content=path.read_text()
        for target in re.findall(r'\]\(([^)]+)\)', content):
            if '://' in target: continue
            filename, _, fragment=target.partition('#')
            dest=path.parent/filename if filename else path
            assert dest.exists(), f'Broken file link {path.name}: {target}'
            if fragment:
                headings=re.findall(r'^#+ (.+)$',dest.read_text(),re.M)
                slugs={re.sub(r'[^\w\- ]','',h.lower()).replace(' ','-') for h in headings}
                assert fragment in slugs, f'Broken heading link {path.name}: {target}'


def explicit_edges(selected):
    cases = [
      ('Q01',{'routes':[]},[]),
      ('Q02',{'pairs':[(1,3,3)]},[]),
      ('Q06',{'observations':[]},[]),
      ('Q08',{'ids':[]},[(1,12)]),
      ('Q09',{'events':[(1,1,0),(2,1,30),(3,1,60)]},[(1,1,0,60,3)]),
      ('Q13',{'intervals':[]},[]),
      ('Q14',{'bookings':[]},[(0,20)]),
      ('Q14',{'bookings':[(1,0,20)]},[]),
      ('Q16',{'ranges':[]},[(0,)]),
      ('Q17',{'changes':[]},[(1,10),(2,10),(3,10),(4,10)]),
      ('Q20',{'purchases':[]},[(1,),(2,),(3,)]),
      ('Q21',{'orders':[]},[(1,0),(2,0),(3,0)]),
      ('Q22',{'orders':[],'payments':[]},[(1,0,0),(2,0,0)]),
      ('Q23',{'tags':[]},[(0,)]),
      ('Q24',{'old_snapshot':[],'new_snapshot':[]},[]),
      ('Q25',{'old_bag':[],'new_bag':[]},[]),
      ('Q26',{'required':[]},[(1,),(2,),(3,),(4,)]),
      ('Q27',{'required':[]},[(4,)]),
      ('Q28',{'basket':[]},[(a,b) for a in range(1,6) for b in range(a+1,6)]),
      ('Q29',{'scores':[]},[]),
      ('Q30',{'policies':[]},[(0,)]),
      ('Q33',{'readings':[(1,1,1,None),(2,1,2,None)]},[(1,None),(2,None)]),
      ('Q38',{'frequencies':[(2,5)]},[(2.0,)]),
      ('Q39',{'queue':[(1,'too heavy',1001)]},[]),
      ('Q46',{'reports':[(1,1)]},[]),
      ('Q47',{'nodes':[(9,None)]},[(9,'Root')]),
      ('Q49',{'demands':[]},[]),
      ('Q50',{'movements':[(1,'A','IN',3,5)]},[('A',3,15)])
    ]
    for qid,data,expected in cases:
        if qid in selected: check(qid,expected,data,'explicit edge cases',alternatives=True)


def randomized(selected, cases=100):
    rng=random.Random(20261010)
    for _ in range(cases):
        if 'Q01' in selected:
            rows=[(i,rng.choice('ABC'),rng.choice('ABC'),rng.randrange(3)) for i in range(1,rng.randrange(1,25))]
            keep={}
            for row in rows:
                key=(*sorted(row[1:3]),row[3])
                keep.setdefault(key,row)
            check('Q01',sorted(keep.values()),{'routes':rows},'random unordered pairs',True)
        if 'Q05' in selected:
            nodes=list(range(1,rng.randrange(2,9)))
            edges=[(rng.choice(nodes),rng.choice(nodes)) for _ in range(rng.randrange(20))]
            adj=defaultdict(set)
            for a,b in edges: adj[a].add(b);adj[b].add(a)
            expected=[]
            for n in nodes:
                seen={n};todo=[n]
                while todo:
                    for nxt in adj[todo.pop()]:
                        if nxt not in seen:seen.add(nxt);todo.append(nxt)
                expected.append((n,min(seen)))
            check('Q05',expected,{'nodes':[(n,) for n in nodes],'edges':edges},'random cyclic components')
        if 'Q06' in selected:
            vals=[rng.randrange(-5,20) for _ in range(rng.randrange(30))]
            runs=[]
            for v in sorted(set(vals)):
                if not runs or v!=runs[-1][-1]+1:runs.append([v])
                else:runs[-1].append(v)
            check('Q06',[(r[0],r[-1],len(r)) for r in runs],{'observations':[(v,) for v in vals]},'random integer islands',True)
        rows=[]
        for i in range(1,rng.randrange(1,15)):
            s=rng.randrange(0,20);e=rng.randrange(s+1,25)
            rows.append((i,s,e))
        packed=[]
        for _,s,e in sorted(rows,key=lambda r:(r[1],r[2],r[0])):
            if not packed or s>packed[-1][1]:packed.append([s,e])
            else:packed[-1][1]=max(e,packed[-1][1])
        if 'Q13' in selected:check('Q13',packed,{'intervals':rows},'random nested intervals')
        if 'Q16' in selected:check('Q16',[(sum(e-s for s,e in packed),)],{'ranges':rows},'random union durations')
        if 'Q15' in selected:
            times=sorted({v for _,s,e in rows for v in (s,e)})
            segments=[(s,e,sum(a<=s<b for _,a,b in rows)) for s,e in zip(times,times[1:])]
            peak=max((count for s,e,count in segments),default=0)
            check('Q15',[x for x in segments if x[2]==peak],{'meetings':rows},'random tied concurrency')
        if any(q in selected for q in ('Q26','Q27','Q28')):
            ids=list(range(1,6));req=set(rng.sample(list('ABC'),rng.randrange(4)))
            baskets={i:[rng.choice('ABCX') for _ in range(rng.randrange(6))] for i in ids}
            rows=[(i,p) for i,ps in baskets.items() for p in ps]
            if 'Q26' in selected:check('Q26',[(i,) for i in ids if req<=set(baskets[i])],{'customers':[(i,) for i in ids],'purchases':rows,'required':[(p,) for p in sorted(req)]},'random universal coverage',True)
            if 'Q27' in selected:check('Q27',[(i,) for i in ids if req==set(baskets[i])],{'customers':[(i,) for i in ids],'purchases':rows,'required':[(p,) for p in sorted(req)]},'random exact sets')
            if 'Q28' in selected:check('Q28',[(a,b) for a in ids for b in ids if a<b and set(baskets[a])==set(baskets[b])],{'basket':rows},'random basket equality')
        if 'Q37' in selected:
            vals={c:[rng.randrange(-10,11) for _ in range(rng.randrange(1,12))] for c in ('A','B','C')}
            rows=[(i,c,v) for i,(c,v) in enumerate(((c,v) for c,vs in vals.items() for v in vs),1)]
            check('Q37',[(c,float(median(vs))) for c,vs in vals.items()],{'employees':rows},'random observation medians')
        if 'Q38' in selected:
            rows=[(v,rng.randrange(1,8)) for v in sorted(rng.sample(range(-10,11),rng.randrange(1,8)))]
            expanded=[v for v,freq in rows for _ in range(freq)]
            check('Q38',[(float(median(expanded)),)],{'frequencies':rows},'random frequency medians')
        if 'Q41' in selected:
            seq=0;rows=[]
            for i in range(rng.randrange(20)):
                seq+=rng.randrange(1,5);rows.append((seq,rng.choice([None,1,2,3])))
            good=set();prev=object();length=0
            for _,v in rows:
                length=length+1 if v==prev else 1;prev=v
                if v is not None and length>=3:good.add(v)
            check('Q41',[(v,) for v in sorted(good)],{'logs':rows},'random adjacent runs',True)
        if 'Q46' in selected:
            rows=[(rng.randrange(1,8),rng.randrange(1,8)) for _ in range(rng.randrange(20))]
            adj=defaultdict(set)
            for a,b in rows:adj[a].add(b)
            seen={1};todo=[1]
            while todo:
                for n in adj[todo.pop()]:
                    if n not in seen:seen.add(n);todo.append(n)
            check('Q46',[(v,) for v in sorted(seen-{1})],{'reports':rows},'random cyclic descendants')
        if 'Q49' in selected:
            ss=[(i,rng.randrange(1,10)) for i in range(1,rng.randrange(2,8))]
            remaining=sum(q for _,q in ss);ds=[]
            for i in range(1,rng.randrange(2,8)):
                if remaining==0:break
                qty=rng.randrange(1,remaining+1);ds.append((i,qty));remaining-=qty
            left=dict(ss);cursor=0;alloc=[]
            for did,qty in ds:
                while qty:
                    sid=ss[cursor][0];take=min(left[sid],qty)
                    alloc.append((did,sid,take));left[sid]-=take;qty-=take
                    if left[sid]==0:cursor+=1
            check('Q49',alloc,{'supplies':ss,'demands':ds},'random FIFO allocations')
        if 'Q50' in selected:
            moves=[];stock={};batch={p:deque() for p in 'AB'};seq=0
            for p in 'AB':
                for _ in range(12):
                    seq+=1;available=sum(q for q,c in batch[p])
                    if available and rng.random()<0.45:
                        qty=rng.randrange(1,available+1);moves.append((seq,p,'OUT',qty,None));need=qty
                        while need:
                            q,c=batch[p].popleft();take=min(q,need);need-=take
                            if q>take:batch[p].appendleft((q-take,c))
                    else:
                        qty=rng.randrange(1,8);cost=rng.randrange(1,20)
                        moves.append((seq,p,'IN',qty,cost));batch[p].append((qty,cost))
            expected=[(p,sum(q for q,c in batch[p]),sum(q*c for q,c in batch[p])) for p in 'AB']
            check('Q50',expected,{'movements':moves},'random FIFO valuation')


def write_report():
    rows='\n'.join(f'| {name} | {n} |' for name,n in CHECKS.items())
    (ROOT/'VERIFICATION.md').write_text(f'''# SQL Catalog Verification

Verified on October 10, 2026 with Python {sys.version.split()[0]} and SQLite {sqlite3.sqlite_version}.

All {sum(CHECKS.values())} query checks passed. Every primary solution and documented alternative was executed in a fresh in-memory database and compared with independent expected rows. Embedded document SQL was checked against the executable files. Internal document file and heading links were checked.

| Check family | Passed query checks |
| --- | --- |
{rows}

Randomized fixtures use seed 20261010 with 100 generated cases per selected family. Python reference oracles independently normalize pairs, traverse graphs, merge intervals, count concurrency, compare sets, compute medians, detect runs, and simulate FIFO consumption. Alternative solutions are also checked when present in a tested family.

Explicit cases include empty inputs, an empty required product set, a singleton root, self cycles, no qualifying children, all-NULL values, the exact inactivity threshold, a fully occupied time window, capacity overflow at the first person, and a fully consumed FIFO product.

Run `python3 verify.py` to reproduce the full verification; use `--question Q13` to focus on one exercise. A focused run does not overwrite this full-run report.

These checks verify the reference dialect and declared contracts. They are not execution tests for PostgreSQL, SQL Server, MySQL, or Spark SQL, not a proof for all possible inputs, and not performance benchmarks. SQLite permits some expressions that stricter engines reject, so translation still needs engine-specific review and execution.
''')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--question',choices=sorted(BY_ID))
    args=parser.parse_args()
    assert sqlite3.sqlite_version_info>=(3,28,0),'SQLite 3.28+ required'
    selected={args.question} if args.question else set(BY_ID)
    samples(selected);explicit_edges(selected);randomized(selected)
    if not args.question:write_report()
    print(f'PASS: {len(selected)} exercises; {sum(CHECKS.values())} query checks; SQLite {sqlite3.sqlite_version}')
    for family,n in CHECKS.items():print(f'  {family}: {n}')

if __name__=='__main__':main()
