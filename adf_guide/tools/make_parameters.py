"""Generate target parameter JSON from the verified educational export contract."""
import argparse,json
from pathlib import Path
from urllib.parse import urlsplit
parser=argparse.ArgumentParser()
parser.add_argument('--template',required=True);parser.add_argument('--factory',required=True)
parser.add_argument('--storage-url',required=True);parser.add_argument('--rest-url',required=True)
parser.add_argument('--output',required=True);args=parser.parse_args()
for value in [args.storage_url,args.rest_url]:
    if urlsplit(value).scheme!='https' or not urlsplit(value).hostname:raise ValueError('Use actual HTTPS endpoints')
spec=json.loads(Path(args.template).read_text())['parameters']
values={'factoryName':args.factory,
        'ls_adls_properties_parameters_p_account_url_defaultValue':args.storage_url,
        'ls_rest_public_example_properties_typeProperties_url':args.rest_url}
if set(spec)!=set(values):raise ValueError('Generated parameter contract changed; review keys before deployment')
obj={'$schema':'https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#','contentVersion':'1.0.0.0','parameters':{k:{'value':v} for k,v in values.items()}}
Path(args.output).write_text(json.dumps(obj,indent=2)+'\n')
