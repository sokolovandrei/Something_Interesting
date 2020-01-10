import json
import requests
from pprint import pprint
from requests.auth import HTTPBasicAuth

if __name__ == "__main__":
    auth = HTTPBasicAuth('admin','1qaz!QAZ')
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    url = 'http://10.1.8.235/ins'

    payload = {
       "ins_api": {
           "version": "1.0",
           "type": "cli_show",
           "chunk": "0",
           "sid": "1",
           "input": 'show ip route vrf Tenant-2',
           "output_format": "json"
           }
    }
    response = requests.post(url, data=json.dumps(payload),
                             headers=headers, auth=auth)

    result = response.text 
    result_dict = json.loads(result)
  
    pprint(result_dict['ins_api']['outputs']['output']['body'])
