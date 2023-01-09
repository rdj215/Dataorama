import json
import requests
def get_url(q): 
    url = q.get()
    print(url)
    res_json = get_response(url)
    return res_json

def req(url):
    res = requests.get(url) # make get request
    res_json = json.dumps(res.json(), indent=4) # wrap json object in srtings
    res_json = json.loads(res_json) # convert json object to dict
    # arr = []
    # print(f"Fields returned from this request: {res_json['fields'].keys()}")
    return res_json

def get_response(url, req):
    res_json = req(url)
    res_json_keys = res_json.keys()
    total = res_json['total_rows']
    return (res_json, total)