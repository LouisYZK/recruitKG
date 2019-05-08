import numpy as np
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from transE import distanceL1


h_rank = []
t_rank = []
def worker_h(triple, entityList, relationList,
             entityVector, relationVector):
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
    global h_rank
    h_rank.append(ind)

def worker_t(triple, entityList, relationList,
             entityVector, relationVector):
    # (h, r, t) --> (h, r, t')
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
    global t_rank
    t_rank.append(ind)

def meric_mean_rank(tripleList, entityList, relationList,
                    entityVector, relationVector):
    """user mean_rank to evaluate the vector result
    """
    print('start evaluating by mean_rank!')
    # (h, r, t) --> (h', r, t)
    with ThreadPoolExecutor(max_workers=4) as executor:
        for triple in tqdm(tripleList):
            executor.submit(worker_h(triple, entityList, relationList,
                    entityVector, relationVector))

    with ThreadPoolExecutor(max_workers=4) as executor:
        for triple in tqdm(tripleList):
            executor.submit(worker_t(triple, entityList, relationList,
                    entityVector, relationVector))
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
    pass