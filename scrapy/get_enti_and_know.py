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

def get_entity(doc):
    url = 'http://shuyantech.com/api/entitylinking/cutsegment'
    doc = doc.split('。')
    entities = []

    for item in doc:
        params = {'q':item}
        r = requests.get(url, params=params, headers=headers)
        entity = json.loads(r.text)['entities']
        entities.append([item2[1] for item2 in entity])
    return entities

def get_triple_tuple(entities):
    url = 'http://shuyantech.com/api/cndbpedia/avpair'
    know = {}
    for item in entities:
        if item not in seen_entity:
            seen_entity.add(item)
            params = {'q':item}
            text = requests.get(url, params=params, headers=headers).text
            knowledge = json.loads(text)['ret']
            know[item] = knowledge
    return know

def en_store_to_json(name, pos, entities):
    en = {}
    with open('./entities.json', 'a') as fp:
        en[name + pos] = entities
        json.dump(en, fp)

def konw_store_to_json(name, pos, knows):
    with open('./knows.json', 'a') as fp:
        json.dump(knows, fp)

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").content

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

conn = sqlite3.connect('zhilian_doc.db')
cur = conn.cursor()
data = cur.execute('select * from zhilian_doc')

seen_entity = set()

name, pos, doc = next(data)
entities = get_entity(doc)

while True:
    name, pos, doc = next(data)

    entities = get_entity(doc)
    entities = list(flatten(entities))
    knows = get_triple_tuple(entities)
    print(entities)
    en_store_to_json(name, pos, entities)
    konw_store_to_json(name, pos, knows)
