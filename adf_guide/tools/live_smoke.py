"""Opt-in live ADF parameter-only smoke. Not called by the guide's local CI."""
import argparse,json,subprocess,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--resource-group',required=True);p.add_argument('--factory',required=True);p.add_argument('--parameters',required=True);p.add_argument('--timeout',type=int,default=600);a=p.parse_args()
if a.timeout<=0:raise ValueError('Positive timeout required')
params=json.loads(Path(a.parameters).read_text())
def az(*parts):
    r=subprocess.run(['az','datafactory',*parts,'-o','json'],check=True,capture_output=True,text=True)
    return json.loads(r.stdout)
created=az('pipeline','create-run','--resource-group',a.resource_group,'--factory-name',a.factory,'--name','pl_parallel_parent','--parameters',json.dumps(params))
run_id=created['runId'];deadline=time.monotonic()+a.timeout
while time.monotonic()<deadline:
    run=az('pipeline-run','show','--resource-group',a.resource_group,'--factory-name',a.factory,'--run-id',run_id)
    status=run['status']
    if status=='Succeeded':print(json.dumps({'runId':run_id,'status':status}));break
    if status in {'Failed','Cancelled'}:raise RuntimeError(f'ADF smoke {run_id}: {status}')
    time.sleep(10)
else:raise TimeoutError(f'ADF smoke timeout: {run_id}; inspect/cancel live run through approved procedure')
