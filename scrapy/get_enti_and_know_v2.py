import sqlite3
import requests
import json
import time
import itertools
from process import clean_doc

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
    doc = clean_doc(doc)
    length = len(doc)
    num = length // 63
    if num < 1: num = 1
    header = {
        'content-type': 'application/json'
    }
    enti = []
    for i in range(num):
        time.sleep(1)
        chaxun = doc[i * 63: (i + 1)*63].strip()
        try:
            res = requests.post('https://aip.baidubce.com/rpc/2.0/kg/v1/cognitive/entity_annotation', 
                        params={'access_token': token},
                        headers=header,
                        json={"data": chaxun}).json()['entity_annotation']
            for item in res:
                enti.append(item['mention'])
        except KeyError as e:
            print(e)
            print('chauxn:', chaxun)
            continue
    return enti

def get_knows(entity):
    url = 'http://zhishi.me/api/entity/'
    if entity not in seen_en:
        url = url + entity
        try:
            knows = requests.get(url, headers=headers).json()
            baike = [k for k in knows.keys()]
            info = [b for b in baike if 'infobox' in knows[b]]
            print(info)
            res_know = knows[info[0]]['infobox']
            seen_en.add(entity)
            return res_know
        except Exception as e:
            print(e)
            return None

def en_store_to_json(entities):
    with open('./entities.json', 'w') as fp:
        fp.truncate()
        json.dump(entities, fp)

def know_store_to_json(knows):
    """konows: {'en': {'relation': another_en}}
    """
    with open('./knows.json', 'w') as fp:
        fp.truncate()
        json.dump(knows, fp)


if __name__ == '__main__':
    # conn = sqlite3.connect('zhilian_doc.db')
    # cur = conn.cursor()
    # data = cur.execute('select * from zhilian_doc')

    # en = {}
    # knows = {}
    # seen_en = set()

    # tt = 0
    # for t in itertools.count():
    #     name, pos, doc = next(data)
    #     entities = get_entity(doc)
    #     print(entities)
    #     print('..............第', t, '个岗位................')
    #     en[name + pos] = entities
    #     en_store_to_json(en)
    #     for item in entities:
    #         know = get_knows(item)
    #         if know is not None:
    #             knows[item] = know
    #             know_store_to_json(knows)
    #             tt += 1
    #             print('......................收集到了.................', tt, '个实体的知识')
    user_doc = "C++Java，还会一丢丢Python.使用Django开发过大型数据库管理框架。。。"

    print(get_entity(user_doc))
            