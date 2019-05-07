import argparse
import json
from transE import TransE, meric_mean_rank, meric_hit

parser = argparse.ArgumentParser()
parser.add_argument('epoch', type=int, help='definite the training epoch')
args = parser.parse_args()

with open('../scrapy/knows.json', 'r') as fp:
    knows = json.load(fp)

entityList = []
relationList = []
tripleList = []
for en, en_rel in knows.items():
    entityList.append(en)
    for rel, en2 in en_rel.items():
        relationList.append(rel)
        entityList.append(en2[0])
        tripleList.append((en, en2[0], rel))

transE = TransE(entityList,relationList,tripleList, margin=1, dim=100, learingRate=0.001, L1=False)
transE.initialize()
transE.transE(args.epoch)
# print(transE.loss_his)
r1, r2 = meric_mean_rank(tripleList, entityList, relationList, transE.entityList, transE.relationList)
print(meric_hit(r1, r2))