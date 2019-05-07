from random import uniform, sample
import numpy as np
from copy import deepcopy
from tqdm import tqdm
import json
import pickle


class TransE:
    def __init__(self, entityList, relationList, tripleList, margin=1, learingRate=0.00001, dim=10, L1=True, batch_size=150):
        self.margin = margin
        self.learingRate = learingRate
        self.dim = dim#向量维度

        self.entityList = entityList
        #一开始，entityList是entity的list；初始化后，变为字典，key是entity，values是其向量（使用narray）。
        self.relationList = relationList#理由同上
        self.tripleList = tripleList#理由同上
        self.loss = 0
        self.L1 = L1

        self.loss_his = []
        self.batch_size = batch_size

    def initialize(self):
        '''
        初始化向量
        '''
        entityVectorList = {}
        relationVectorList = {}
        for entity in tqdm(self.entityList):
            n = 0
            entityVector = []
            while n < self.dim:
                ram = init(self.dim)#初始化的范围
                entityVector.append(ram)
                n += 1
            entityVector = norm(entityVector)#归一化
            entityVectorList[entity] = entityVector
        print("entityVector初始化完成，数量是%d"%len(entityVectorList))
        for relation in tqdm(self. relationList):
            n = 0
            relationVector = []
            while n < self.dim:
                ram = init(self.dim)#初始化的范围
                relationVector.append(ram)
                n += 1
            relationVector = norm(relationVector)#归一化
            relationVectorList[relation] = relationVector
        print("relationVectorList初始化完成，数量是%d"%len(relationVectorList))
        self.entityList = entityVectorList
        self.relationList = relationVectorList

    def transE(self, cI=20):
        print("训练开始")
        for cycleIndex in range(cI):
            Sbatch = self.getSample(self.batch_size)
            Tbatch = []
            #元组对（原三元组，打碎的三元组）的列表 ：{((h,r,t),(h',r,t'))}
            for sbatch in Sbatch:
                tripletWithCorruptedTriplet = (sbatch, self.getCorruptedTriplet(sbatch))
                if(tripletWithCorruptedTriplet not in Tbatch):
                    Tbatch.append(tripletWithCorruptedTriplet)
            self.update(Tbatch)
            self.loss_his.append(self.loss)
            if cycleIndex % 100 == 0:
                print("第%d次循环"%cycleIndex)
                print(self.loss)
                # self.writeRelationVector("c:\\relationVector.txt")
                self.writeEntilyVector("entityVector_"+str(self.dim)+'_'+str(self.learingRate)+'.pkl')
                self.writeRelationVector("relationVector_"+str(self.dim)+'_'+str(self.learingRate)+'.pkl')
                self.loss = 0

    def getSample(self, size):
        return sample(self.tripleList, size)

    def getCorruptedTriplet(self, triplet):
        '''
        training triplets with either the head or tail replaced by a random entity (but not both at the same time)
        :param triplet:
        :return corruptedTriplet:
        '''
        i = uniform(-1, 1)
        if i < 0:#小于0，打坏三元组的第一项
            while True:
                entityTemp = sample(self.entityList.keys(), 1)[0]
                if entityTemp != triplet[0]:
                    break
            corruptedTriplet = (entityTemp, triplet[1], triplet[2])
        else:#大于等于0，打坏三元组的第二项
            while True:
                entityTemp = sample(self.entityList.keys(), 1)[0]
                if entityTemp != triplet[1]:
                    break
            corruptedTriplet = (triplet[0], entityTemp, triplet[2])
        return corruptedTriplet

    def update(self, Tbatch):
        copyEntityList = deepcopy(self.entityList)
        copyRelationList = deepcopy(self.relationList)
        
        for tripletWithCorruptedTriplet in Tbatch:
            headEntityVector = copyEntityList[tripletWithCorruptedTriplet[0][0]]#tripletWithCorruptedTriplet是原三元组和打碎的三元组的元组tuple
            tailEntityVector = copyEntityList[tripletWithCorruptedTriplet[0][1]]
            relationVector = copyRelationList[tripletWithCorruptedTriplet[0][2]]
            headEntityVectorWithCorruptedTriplet = copyEntityList[tripletWithCorruptedTriplet[1][0]]
            tailEntityVectorWithCorruptedTriplet = copyEntityList[tripletWithCorruptedTriplet[1][1]]
            
            headEntityVectorBeforeBatch = self.entityList[tripletWithCorruptedTriplet[0][0]]#tripletWithCorruptedTriplet是原三元组和打碎的三元组的元组tuple
            tailEntityVectorBeforeBatch = self.entityList[tripletWithCorruptedTriplet[0][1]]
            relationVectorBeforeBatch = self.relationList[tripletWithCorruptedTriplet[0][2]]
            headEntityVectorWithCorruptedTripletBeforeBatch = self.entityList[tripletWithCorruptedTriplet[1][0]]
            tailEntityVectorWithCorruptedTripletBeforeBatch = self.entityList[tripletWithCorruptedTriplet[1][1]]
            
            if self.L1:
                distTriplet = distanceL1(headEntityVectorBeforeBatch, tailEntityVectorBeforeBatch, relationVectorBeforeBatch)
                distCorruptedTriplet = distanceL1(headEntityVectorWithCorruptedTripletBeforeBatch, tailEntityVectorWithCorruptedTripletBeforeBatch ,  relationVectorBeforeBatch)
            else:
                distTriplet = distanceL2(headEntityVectorBeforeBatch, tailEntityVectorBeforeBatch, relationVectorBeforeBatch)
                distCorruptedTriplet = distanceL2(headEntityVectorWithCorruptedTripletBeforeBatch, tailEntityVectorWithCorruptedTripletBeforeBatch ,  relationVectorBeforeBatch)
            eg = self.margin + distTriplet - distCorruptedTriplet
            self.loss += eg
            if eg > 0: #[function]+ 是一个取正值的函数
                # self.loss += eg
                # self.loss = eg
                if self.L1:
                    tempPositive = 2 * self.learingRate * (tailEntityVectorBeforeBatch - headEntityVectorBeforeBatch - relationVectorBeforeBatch)
                    tempNegtative = 2 * self.learingRate * (tailEntityVectorWithCorruptedTripletBeforeBatch - headEntityVectorWithCorruptedTripletBeforeBatch - relationVectorBeforeBatch)
                    tempPositiveL1 = []
                    tempNegtativeL1 = []
                    for i in range(self.dim):#不知道有没有pythonic的写法（比如列表推倒或者numpy的函数）？
                        if tempPositive[i] >= 0:
                            tempPositiveL1.append(1)
                        else:
                            tempPositiveL1.append(-1)
                        if tempNegtative[i] >= 0:
                            tempNegtativeL1.append(1)
                        else:
                            tempNegtativeL1.append(-1)
                    tempPositive = np.array(tempPositiveL1)  
                    tempNegtative = np.array(tempNegtativeL1)

                else:
                    tempPositive = 2 * self.learingRate * (tailEntityVectorBeforeBatch - headEntityVectorBeforeBatch - relationVectorBeforeBatch)
                    tempNegtative = 2 * self.learingRate * (tailEntityVectorWithCorruptedTripletBeforeBatch - headEntityVectorWithCorruptedTripletBeforeBatch - relationVectorBeforeBatch)
    
                headEntityVector = headEntityVector + tempPositive
                tailEntityVector = tailEntityVector - tempPositive
                relationVector = relationVector + tempPositive - tempNegtative
                headEntityVectorWithCorruptedTriplet = headEntityVectorWithCorruptedTriplet - tempNegtative
                tailEntityVectorWithCorruptedTriplet = tailEntityVectorWithCorruptedTriplet + tempNegtative

                #只归一化这几个刚更新的向量，而不是按原论文那些一口气全更新了
                copyEntityList[tripletWithCorruptedTriplet[0][0]] = norm(headEntityVector)
                copyEntityList[tripletWithCorruptedTriplet[0][1]] = norm(tailEntityVector)
                copyRelationList[tripletWithCorruptedTriplet[0][2]] = norm(relationVector)
                copyEntityList[tripletWithCorruptedTriplet[1][0]] = norm(headEntityVectorWithCorruptedTriplet)
                copyEntityList[tripletWithCorruptedTriplet[1][1]] = norm(tailEntityVectorWithCorruptedTriplet)
        self.loss /= len(Tbatch)   
        self.entityList = copyEntityList
        self.relationList = copyRelationList
        
    def writeEntilyVector(self, dir):
        print("写入实体")
        # entityVectorFile = open(dir, 'w')
        # for entity in self.entityList.keys():
        #     entityVectorFile.write(entity+"\t")
        #     entityVectorFile.write(str(self.entityList[entity].tolist()))
        #     entityVectorFile.write("\n")
        # entityVectorFile.close()
        with open(dir, 'wb') as fp:
            pickle.dump(self.entityList, fp)

    def writeRelationVector(self, dir):
        print('写入关系')
        with open(dir, 'wb') as fp:
            pickle.dump(self.relationList, fp)

def init(dim):
    return uniform(-6/(dim**0.5), 6/(dim**0.5))

def distanceL1(h, t ,r):
    s = h + r - t
    sum = np.abs(s).sum()
    return sum

def distanceL2(h, t, r):
    s = h + r - t
    sum = (s*s).sum()
    return sum
 
def norm(list):
    '''
    归一化
    :param 向量
    :return: 向量的平方和的开方后的向量
    '''
    var = np.linalg.norm(list)
    i = 0
    while i < len(list):
        list[i] = list[i]/var
        i += 1
    return np.array(list)

def meric_mean_rank(tripleList, entityList, relationList,
                    entityVector, relationVector):
    """user mean_rank to evaluate the vector result
    """
    print('start evaluating by mean_rank!')
    # (h, r, t) --> (h', r, t)
    h_rank = []
    for triple in tqdm(tripleList):
        h, t, r = triple
        h_vec, t_vec, r_vec = entityVector[h], entityVector[t], relationVector[r]
        h_vec, t_vec, r_vec = np.array(h_vec), np.array(t_vec), np.array(r_vec)
        replace_h_distance = {}
        for h_else in entityList:
            # print('h_else:', h_else)
            h_else_vec = entityVector[h_else]
            h_else_vec = np.array(h_else_vec)
            replace_h_distance[h_else] = distanceL1(h_else_vec, t_vec, r_vec)
        # sort the distance dict by the values:
        rank_le = sorted(replace_h_distance, key=lambda x: replace_h_distance[x])
        ind = rank_le.index(h)
        h_rank.append(ind)
    
    # (h, r, t) --> (h, r, t')
    t_rank = []
    for triple in tqdm(tripleList):
        h, t, r = triple
        h_vec, t_vec, r_vec = entityVector[h], entityVector[t], relationVector[r]
        h_vec, t_vec, r_vec = np.array(h_vec), np.array(t_vec), np.array(r_vec)
        replace_t_distance = {}
        for t_else in entityList:
            t_else_vec = entityVector[t_else]
            t_else_vec = np.array(t_else_vec)
            replace_t_distance[t_else] = distanceL1(h_vec, t_else_vec, r_vec)
        # sort the distance dict by the values:
        rank_le = sorted(replace_t_distance, key=lambda x: replace_t_distance[x])
        ind = rank_le.index(t)
        t_rank.append(ind)
    return h_rank, t_rank
    
def meric_hit(h_rank, t_rank, N=50):
    """evaluate the vector result by hit-N method
       N: the rate of the true entities in the topN rank
       return the mean rate
    """
    print('start evaluating by Hit')
    num = 0
    for r1 in h_rank:
        if r1 <= N:
            num += 1
    rate_h = num / len(h_rank) * 100

    num = 0
    for r2 in t_rank:
        if r2 <= N:
            num += 1
    rate_t = num / len(t_rank) * 100
    
    return (rate_h + rate_t) / 2 
    
    

if __name__ == '__main__':
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
    transE.transE(100)
    # print(transE.loss_his)
    r1, r2 = meric_mean_rank(tripleList, entityList, relationList, transE.entityList, transE.relationList)
    print(meric_hit(r1, r2))
    # transE.writeEntilyVector('entityVector.pkl')
    # transE.writeRelationVector("relationVector.pkl")