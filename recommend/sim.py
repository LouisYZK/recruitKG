import pickle
import json
import numpy as np
from collections import defaultdict
import sys
sys.path.append('../')
sys.path.append('../scrapy')
from scrapy.get_enti_and_know_v3 import get_en_know_api

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
        with open('entityVector_100_0.001.pkl', 'rb') as fp:
            self.entity_vec = pickle.load(fp)
        with open('relationVector_100_0.001.pkl', 'rb') as fp:
            self.relation_vec =pickle.load(fp)
        
        with open('../scrapy/entities.json', 'r') as fp:
            self.pos_en = json.load(fp)

        with open('../scrapy/knows.json', 'r') as fp:
            knows = json.load(fp)
            triple = []
            for en, rel_en in knows.items():
                for rel, en2 in rel_en:
                    triple.append((en, rel, en2))

        # self.pos_relations = defaultdict(list)

        # for pos, ens in self.pos_en.items():
        #     rel_unique = set()
        #     for triple_item in triple:
        #         if triple_item[0] in ens or triple_item[2] in ens:
        #             if triple_item[1] not in rel_unique:
        #                 self.pos_relations[pos].append(triple_item[1])
        #                 rel_unique.add(triple_item[1])
        with open('pos_en_vec.pkl', 'rb') as fp:
            self.pos_en_vec = pickle.load(fp)
        
        with open('pos_rel_vec.pkl', 'rb') as fp:
            self.pos_rel_vec = pickle.load(fp)
        
        
        print('variables preparing finished!')
    

    def get_user_en_rel(self):
        self.user_en_rel = {}
        api = get_en_know_api(self.user_doc)
        entities = api.get_entity()
        self.user_en_rel['ens'] = entities
        self.user_en_rel['rels'] = api.get_knows(entities)
        
        print("User's ens and knows preparing finished!")

    def get_sim_pos(self, num=5):
        """return topk most simmilary positions
        """
        user_en = self.user_en_rel['ens']
        user_rel = self.user_en_rel['rels']
        user_en_vector = []
        user_rel_vector = []
        # for en in user_en:
        #     if en in self.entity_vec.keys():
        #         user_en_vector.append(self.entity_vec.get(en))
        # for rel in user_rel:
        #     if rel in self.relation_vec.keys():
        #         user_rel_vector.append(self.relation_vec.get(rel))
        for en in user_en:
            if en in self.entity_vec.keys():
                user_en_vector.append(self.entity_vec.get(en))
        for en, knows in user_rel.items():
            if en in self.entity_vec.keys():
                user_en_vector.append(self.entity_vec.get(en))
            for rel, en2 in knows:
                if en2 in self.entity_vec.keys():
                    user_en_vector.append(self.entity_vec.get(en2))
                if rel in self.relation_vec.keys():
                    user_rel_vector.append(self.relation_vec.get(rel))

        user_en_vector = np.vstack(user_en_vector)
        user_rel_vector = np.vstack(user_rel_vector)
        
        # pos_en_vector = defaultdict(list)
        # pos_rel_vector = defaultdict(list)
        # for name, ens in self.pos_en.items():
        #     for en in ens:
        #         if en in self.entity_vec.keys():
        #             pos_en_vector[name].append(self.entity_vec.get(en)) 
        
        # for name, rels in self.pos_relations.items():
        #     for rel in rels:
        #         if rel in self.relation_vec.keys():
        #             pos_rel_vector[name].append(self.relation_vec.get(rel))

        print('users and positions en-rel to vector already have been prepared!')
        

        sim_pos = {}
        
        for pos_en_vec, pos_rel_vec in zip(self.pos_en_vec.items(), self.pos_rel_vec.items()):
            name1, en_vec = pos_en_vec
            name2, rel_vec = pos_rel_vec
            assert name1 == name2
            en_vec, rel_vec = np.vstack(en_vec), np.vstack(rel_vec)
            assert en_vec.shape[1] == 100
            sim_pos[name1] = np.mean(np.dot(user_en_vector, en_vec.T)) + np.mean(np.dot(user_rel_vector, rel_vec.T))
        sim_name = sorted(sim_pos, key=lambda x: sim_pos[x]) # list of keys
        for name in sim_name[-10:]:
            print(name, sim_pos[name])
        return list(reversed(sim_name[-10:]))
             
        


if __name__ == '__main__':
    user_doc = "Python做过数据分析，会点Linux"
    sim = similary(user_doc)
    sim.initialize()
    sim.get_user_en_rel()
    # print(sim.pos_en)
    # print(sim.pos_en)
    # print(sim.pos_relations)
    print(sim.user_en_rel)

    print(sim.get_sim_pos())