import json
import pickle
from collections import defaultdict 
def initialize():
    """prepare the position info and vector.
    """
    with open('entityVector_100_0.001.pkl', 'rb') as fp:
        entity_vec = pickle.load(fp)
    with open('relationVector_100_0.001.pkl', 'rb') as fp:
        relation_vec =pickle.load(fp)
    
    with open('../scrapy/entities.json', 'r') as fp:
        pos_en = json.load(fp)

    with open('../scrapy/knows.json', 'r') as fp:
        knows = json.load(fp)
        triple = []
        for en, rel_en in knows.items():
            for rel, en2 in rel_en:
                triple.append((en, rel, en2))

    pos_relations = defaultdict(list)

    for pos, ens in pos_en.items():
        rel_unique = set()
        for triple_item in triple:
            if triple_item[0] in ens or triple_item[2] in ens:
                if triple_item[1] not in rel_unique:
                    pos_relations[pos].append(triple_item[1])
                    rel_unique.add(triple_item[1])

    pos_en_vector = defaultdict(list)
    pos_rel_vector = defaultdict(list)
    for name, ens in pos_en.items():
        for en in ens:
            if en in entity_vec.keys():
                pos_en_vector[name].append(entity_vec.get(en)) 
    
    for name, rels in pos_relations.items():
        for rel in rels:
            if rel in relation_vec.keys():
                pos_rel_vector[name].append(relation_vec.get(rel))

    with open('pos_en_vec.pkl', 'wb') as fp:
        pickle.dump(pos_en_vector, fp)
    
    with open('pos_rel_vec.pkl', 'wb') as fp:
        pickle.dump(pos_rel_vector, fp)

    print('transform finished!')

initialize()