import sqlite3
import requests
import json
import time
import itertools
import pickle
from process import clean_doc
from tqdm import tqdm
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
                for k in knowledge:
                    if k[0] == 'DESC':
                        knowledge.remove(k)
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

def get_know(entity):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        }
    api_key = '25f40a85fc2245c84611f593f12f311'
    url = 'http://shuyantech.com/api/cndbpedia/avpair'
    params = {'q':entity, 'apikey': api_key}
    text = requests.get(url, params=params, headers=headers).text
    knowledge = json.loads(text)['ret']
    for item in knowledge:
        if item[0] == 'DESC':
            knowledge.remove(item)
    
    return knowledge

if __name__ == '__main__':
    
    # conn = sqlite3.connect('zhilian_doc.db')
    # cur = conn.cursor()
    # data = cur.execute('select * from zhilian_doc')

    # seen_entity = set()
    # pos_en = {}
    # pos_know = {}

    # null_return = []
    # while True:
    #     try:
    #         time.sleep(0.5)
    #         name, pos, doc = next(data)
    #         api = get_en_know_api(doc)
    #         entities = api.get_entity()
    #         if len(entities) == 0:
    #             null_return.append([name, pos, doc])
    #         pos_en[name+'_'+pos] = entities
    #         api.en_store_to_json(pos_en)
    #         print(entities)
    #         # time.sleep(0.5)
    #         # knows = api.get_knows(entities)
    #         # pos_know[name+'_'+pos] = knows
    #         # api.know_store_to_json(pos_know)
    #     except Exception as e:
    #         print(e)
    #         continue
    #     finally:
    #         with open('null_return.pkl', 'wb') as fp:
    #             fp.truncate()
    #             pickle.dump(null_return, fp)
        # en_store_to_json(name, pos, entities)
        # konw_store_to_json(name, pos, knows)
    
    with open('entities.json', 'r') as fp:
        ens = json.load(fp)
    
    # null_return_update = []
    # while True:
    #     try:
    #         name, pos, doc = next(data)
    #         if len(doc) > 0 and name+'_'+ pos not in ens.keys():
    #             api = get_en_know_api(doc)
    #             entities = api.get_entity()
    #             print(entities)
    #             if len(entities) > 0:
    #                 ens.update({name+'_'+ pos: entities})
    #                 api.en_store_to_json(ens)
    #             else:
    #                 null_return_update.append([name, pos, doc])
    #         else:
    #             print(name+'_'+ pos, '已经采集过')
    #     except Exception as e:
    #         print(e)
    #         with open('null_return.pkl', 'wb') as fp:
    #             fp.truncate()
    #             pickle.dump(null_return_update, fp)
    # with open('knows.json', 'r') as fp:
    #     knows = json.load(fp)
    knows = {}
    for name, entities in ens.items():
        for en in entities:
            try:
                if en not in knows.keys():
                    new_know = get_know(en)
                    if len(new_know) > 0 and type(new_know) is list:
                        knows.update({en: new_know})
                        print('获取了实体：', en, '的知识')
            except Exception as e:
                print(e)
                with open('knows.json', 'w') as fp:
                    json.dump(knows, fp)
        