#!/usr/bin/env python3
"""Explore all documented architecture assemblies; no infrastructure is deployed."""
from pathlib import Path
import argparse,itertools,json,sys
ROOT=Path(__file__).resolve().parents[1]

def candidates(items,scenario=None,cloud=None,stack=None):
    for item in items:
        base=item['reference']
        if scenario and item['scenario']!=scenario:continue
        if cloud and base['cloud']!=cloud:continue
        if stack and base['id']!=stack:continue
        for bundle,scheduler,governance,automation in itertools.product(item['data_variants'],item['schedulers'],item['governance'],item['automation']):
            if '*' not in automation['clouds'] and base['cloud'] not in automation['clouds']:continue
            if automation['runtime']=='k8s' and not base['k8s']:continue
            for infra in automation['infra']:
                yield dict(scenario=item['scenario'],reference_path=base['id'],cloud=base['cloud'],data_bundle=bundle['id'],
                  stages={k:bundle[k] for k in ['ingest','storage','compute','serve']},runtime_orchestration=scheduler,
                  governance=governance,ci=automation['name'],ci_id=automation['id'],iac=infra,
                  qualification=bundle['qualification'],status='proposed design candidate; integration checks required')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scenario',help='Scenario ID, for example S12')
    parser.add_argument('--cloud',choices=['aws','azure','gcp','oss','oci','ibm'])
    parser.add_argument('--stack',help='Reference path ID, for example snowflake or oss')
    parser.add_argument('--count',action='store_true')
    parser.add_argument('--all',action='store_true',help='Export all matching documented candidates')
    parser.add_argument('--limit',type=int,default=20,help='Maximum printed candidates unless --all is set')
    parser.add_argument('--output',type=Path,help='Write JSONL to this file')
    args=parser.parse_args()
    if args.limit<0:parser.error('--limit cannot be negative')
    items=json.loads((ROOT/'design_candidates.json').read_text())
    if args.scenario and args.scenario not in {i['scenario'] for i in items}:parser.error('Unknown scenario ID')
    if args.stack and args.stack not in {i['reference']['id'] for i in items}:parser.error('Unknown reference path ID')
    iterator=candidates(items,args.scenario,args.cloud,args.stack)
    if args.count:
        print(sum(1 for _ in iterator));return
    stream=args.output.open('w',encoding='utf-8') if args.output else sys.stdout
    try:
        for item in iterator if args.all else itertools.islice(iterator,args.limit):
            print(json.dumps(item,separators=(',',':')),file=stream)
    finally:
        if args.output:stream.close()
if __name__=='__main__':main()
