import sqlite3
import requests
import json
import time
import itertools
import pickle
from process import clean_doc

"""
This Version3 uses the api-key of CN-Dbpedia
"""
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
        self.doc = doc
        self.api_key = '25f40a85fc2245c84611f593f12f311'

    def flatten(self, items):
        for x in items:
            if hasattr(x,'__iter__') and not isinstance(x, (str, bytes)):
                # for sub_x in flatten(x):
                #     yield sub_x
                yield from self.flatten(x)
            else:
                yield x

    def get_entity(self):
        url = 'http://shuyantech.com/api/entitylinking/cutsegment'
        doc = self.doc.split('。')
        entities = []

        for item in doc:
            params = {'q':item, 'apikey': self.api_key}
            r = requests.get(url, params=params, headers=self.headers)
            entity = json.loads(r.text)['entities']
            entities.append([item2[1] for item2 in entity])
        return list(self.flatten(entities))

    def get_knows(self, entities):
        url = 'http://shuyantech.com/api/cndbpedia/avpair'
        know = {}
        seen_entity = set()
        for item in entities:
            if item not in seen_entity:
                seen_entity.add(item)
                params = {'q':item, 'apikey': self.api_key}
                text = requests.get(url, params=params, headers=self.headers).text
                knowledge = json.loads(text)['ret']
                know[item] = knowledge
        return know

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
    # user_doc = "C++Java，还会一丢丢Python.使用Django开发过大型数据库管理框架。。。"
    # api = get_en_know_api(user_doc)
    # ens = api.get_entity()
    # print(ens)
    # print(api.get_knows(ens))
    conn = sqlite3.connect('zhilian_doc.db')
    cur = conn.cursor()
    data = cur.execute('select * from zhilian_doc')

    seen_entity = set()
    pos_en = {}
    pos_know = {}

    null_return = []
    while True:
        try:
            time.sleep(0.5)
            name, pos, doc = next(data)
            if name+'_'+ pos not in exist_name: 
            api = get_en_know_api(doc)
            entities = api.get_entity()
            if len(entities) == 0:
                null_return.append([name, pos, doc])
            pos_en[name+'_'+pos] = entities
            api.en_store_to_json(pos_en)
            print(entities)
            # time.sleep(0.5)
            # knows = api.get_knows(entities)
            # pos_know[name+'_'+pos] = knows
            # api.know_store_to_json(pos_know)
        except Exception as e:
            print(e)
            continue
        finally:
            with open('null_return.pkl', 'wb') as fp:
                fp.truncate()
                pickle.dump(null_return, fp)
        # en_store_to_json(name, pos, entities)
        # konw_store_to_json(name, pos, knows)