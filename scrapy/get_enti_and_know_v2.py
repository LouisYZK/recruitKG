import sqlite3
import requests
import json
import time
"""
Input: doc from zhilian_doc.db
Aim:
    get the entities/knowledges in the doc.
    store them into entites.json/knowledges.json

entities.json:
{
    'name+position':List(entities),
}
konwledges.json:
{
    'entity':[
        ['relation', 'entity'],
        ...
    ],
}
"""
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }

def flatten(items):
    for x in items:
        if hasattr(x,'__iter__') and not isinstance(x, (str, bytes)):
            # for sub_x in flatten(x):
            #     yield sub_x
            yield from flatten(x)
        else:
            yield x

params = {
    'grant_type': 'client_credentials',
    'client_id': 'e8EfF4UvwtUskxKp7ALRUGAZ',
    'client_secret': 'Kh4hAqFxzZEKIEEzFVn0qgjr1Mo5Cqxn'
}
token = requests.post('https://aip.baidubce.com/oauth/2.0/token', params=params).json()['access_token']

def get_entity(doc):
    """
        length of doc require to be less than 64
    """
    length = len(doc)
    num = length // 63
    header = {
        'content-type': 'application/json'
    }
    enti = []
    for i in range(num):
        chaxun = doc[i * 63: (i + 1)*63]
        res = requests.post('https://aip.baidubce.com/rpc/2.0/kg/v1/cognitive/entity_annotation', 
                    params={'access_token': token},
                    headers=header,
                    json={"data": chaxun}).json()['entity_annotation']
        for item in res:
            enti.append(item['mention'])
    return enti
        
def en_store_to_json(entities):
    with open('./entities.json', 'w') as fp:
        fp.truncate()
        json.dump(entities, fp)

conn = sqlite3.connect('zhilian_doc.db')
cur = conn.cursor()
data = cur.execute('select * from zhilian_doc')

en = {}
while Ture:
    name, pos, doc = next(data)
    entities = get_entity(doc)
    print(entities)
    en[name + pos] = entities
    en_store_to_json(en)