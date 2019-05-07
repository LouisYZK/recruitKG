import argparse
import json
import numpy as np
import pickle
from transE import TransE
from metric import meric_mean_rank

parser = argparse.ArgumentParser()
parser.add_argument('epoch', type=int, help='definite the training epoch')
parser.add_argument('type', type=str, help='definite the traing type dim or batch or lr')
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

if args.type == 'dim':
    for d in [10, 50, 100, 150, 200]:
        transE = TransE(entityList,relationList,tripleList, margin=1, dim=d, learingRate=0.001, L1=False)
        transE.initialize()
        transE.transE(args.epoch)
        # print(transE.loss_his)
        rank1, rank2 = meric_mean_rank(tripleList, entityList, relationList, transE.entityList, transE.relationList)
        rank = {}
        # rank1, rank2 = np.array(rank1), np.rank2(rank2)
        rank['rank_h'] = rank1
        rank['rank_t'] = rank2
        with open('rank_mean_dim_' + str(d)+ '.pkl', 'wb') as fp:
            pickle.dump(rank, fp)
# print(meric_hit(r1, r2))

if args.type == 'lr':
    for lr in [0.01, 0.001, 0.0001, 0.00001]:
        transE = TransE(entityList,relationList,tripleList, margin=1, dim=100, learingRate=lr, L1=False)
        transE.initialize()
        transE.transE(args.epoch)
        # print(transE.loss_his)
        rank1, rank2 = meric_mean_rank(tripleList, entityList, relationList, transE.entityList, transE.relationList)
        rank = {}
        # rank1, rank2 = np.array(rank1), np.rank2(rank2)
        rank['rank_h'] = rank1
        rank['rank_t'] = rank2
        with open('rank_mean_lr_' + str(lr) + '.pkl', 'wb') as fp:
            pickle.dump(rank, fp)

if args.type == 'batch':
    for batch_size in [50, 100, 150, 200, 300]:
        transE = TransE(entityList,relationList,tripleList, margin=1, dim=100, learingRate=0.001, L1=False, batch_size=batch_size)
        transE.initialize()
        transE.transE(args.epoch)
        # print(transE.loss_his)
        rank1, rank2 = meric_mean_rank(tripleList, entityList, relationList, transE.entityList, transE.relationList)
        rank = {}
        # rank1, rank2 = np.array(rank1), np.rank2(rank2)
        rank['rank_h'] = rank1
        rank['rank_t'] = rank2
        with open('rank_mean_batch_' + str(batch_size)+ '.pkl', 'wb') as fp:
            pickle.dump(rank, fp)