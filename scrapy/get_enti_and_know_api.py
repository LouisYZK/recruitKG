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
class get_en_know_api():

    def __init__(self, doc):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        }
        params = {
            'grant_type': 'client_credentials',
            'client_id': 'e8EfF4UvwtUskxKp7ALRUGAZ',
            'client_secret': 'Kh4hAqFxzZEKIEEzFVn0qgjr1Mo5Cqxn'
        }
        self.doc = doc
        self.token = requests.post('https://aip.baidubce.com/oauth/2.0/token', params=params).json()['access_token']

    def flatten(self, items):
        for x in items:
            if hasattr(x,'__iter__') and not isinstance(x, (str, bytes)):
                # for sub_x in flatten(x):
                #     yield sub_x
                yield from self.flatten(x)
            else:
                yield x

    def get_entity(self):
        """
            length of doc require to be less than 64
        """
        doc = clean_doc(self.doc)
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
                            params={'access_token': self.token},
                            headers=header,
                            json={"data": chaxun}).json()['entity_annotation']
                for item in res:
                    enti.append(item['mention'])
            except KeyError as e:
                print(e)
                print('chauxn:', chaxun)
                continue
        self.entities = enti
        return enti

    def get_knows(self):
        seen_en = set()
        url = 'http://zhishi.me/api/entity/'
        self.triple = []
        for entity in self.entities:
            if entity not in seen_en:
                url = url + entity
                try:
                    time.sleep(3)
                    knows = requests.get(url, headers=self.headers).json()
                    baike = [k for k in knows.keys()]
                    info = [b for b in baike if 'infobox' in knows[b]]
                    print(info)
                    res_know = knows[info[0]]['infobox']
                    seen_en.add(entity)
                    for rel, en in res_know.items():
                        self.triple.append((entity, rel, en[0]))
                    # return res_know
                except Exception as e:
                    print(entity)
                    print(e)
        return self.triple

    def en_store_to_json(self, entities):
        with open('./entities.json', 'w') as fp:
            fp.truncate()
            json.dump(entities, fp)

    def know_store_to_json(self, knows):
        """konows: {'en': {'relation': another_en}}
        """
        with open('./knows.json', 'w') as fp:
            fp.truncate()
            json.dump(knows, fp)

if __name__ == '__main__':
    user_doc = "C++Java，还会一丢丢Python.使用Django开发过大型数据库管理框架。。。"
    api = get_en_know_api(user_doc)
    print(api.get_entity())
    print(api.get_knows())