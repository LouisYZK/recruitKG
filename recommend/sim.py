import pickle
import json
from collections import defaultdict
import sys
sys.path.append('../')
sys.path.append('../scrapy')
from scrapy.get_enti_and_know_api import get_en_know_api

"""
Input:
    User's doc, extract the entity and relation
Output:
    Top K's most similary position.

User's entity: 
    {'user_name': [en1, en2m ....]}
TopK position:
    {'user_bame': [(pos1, sim_val), (pos2, sim_val), ...]}
"""

class similary():
    def __init__(self, user_doc):
        self.user_doc = user_doc
    
    def initialize(self):
        """prepare the position info and vector.
        """
        with open('entityVector.pkl', 'rb') as fp:
            self.entity_vec = pickle.load(fp)
        with open('relationVector.pkl', 'rb') as fp:
            self.relation_vec =pickle.load(fp)
        
        with open('../scrapy/entities.json', 'r') as fp:
            self.pos_en = json.load(fp)

        with open('../scrapy/knows.json', 'r') as fp:
            knows = json.load(fp)
            triple = []
            for en, rel_en in knows.items():
                for rel, en2 in rel_en.items():
                    triple.append((en, rel, en2[0]))

        self.pos_relations = defaultdict(list)

        for pos, ens in self.pos_en.items():
            rel_unique = set()
            for triple_item in triple:
                if triple_item[0] in ens or triple_item[2] in ens:
                    if triple_item[1] not in rel_unique:
                        self.pos_relations[pos].append(triple_item[1])
                        rel_unique.add(triple_item[1])
        
        print('variables preparing finished!')
    
    def get_user_en_rel(self):
        self.user_en_rel = {}
        api = get_en_know_api(self.user_doc)
        entities = api.get_entity()
        self.user_en_rel['ens'] = entities
        self.user_en_rel['rels'] = api.get_knows()
        
        print("User's ens and knows preparing finished!")

    def get_sim_pos(self, num=5):
        pass
        


if __name__ == '__main__':
    user_doc = "C++Java，还会一丢丢Python"
    sim = similary(user_doc)
    sim.initialize()
    sim.get_user_en_rel()
    # print(sim.pos_en)
    print(sim.user_en_rel)