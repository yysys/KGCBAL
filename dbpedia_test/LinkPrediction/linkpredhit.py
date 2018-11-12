import linkpred
from datetime import datetime
from sys import argv
import numpy as np

def getPredictor(name, G):
    return {
        'CommonNeighbours':linkpred.predictors.CommonNeighbours(G, excluded=G.edges()),
        'AdamicAdar': linkpred.predictors.AdamicAdar(G, excluded=G.edges()),
        'Jaccard': linkpred.predictors.Jaccard(G, excluded=G.edges()),
        'ResourceAllocation': linkpred.predictors.ResourceAllocation(G, excluded=G.edges()),
        'DegreeProduct': linkpred.predictors.DegreeProduct(G, excluded=G.edges()),
        'GraphDistance': linkpred.predictors.GraphDistance(G, excluded=G.edges()),
        'Katz': linkpred.predictors.Katz(G, excluded=G.edges()),
        'Community': linkpred.predictors.Community(G, excluded=G.edges()),
        'Random': linkpred.predictors.Random(G, excluded=G.edges()),
        'RootedPageRank': linkpred.predictors.RootedPageRank(G, excluded=G.edges()),
        'SimRank': linkpred.predictors.SimRank(G, excluded=G.edges())
    }.get(name, 'error')

def is_set_overlap(initial_set, set):
    cnt = 0
    for key in initial_set:
        if key in set:
            cnt = cnt + 1

    threshold = int(min(initial_set.__len__(), set.__len__()) * 0.01)
    if cnt > threshold:
        return True
    else:
        return False

def merge_set(initial_set, set):
    for key in set:
        if key not in initial_set:
            initial_set[key] = 1

    return initial_set

def loop(sets):

    ans = []
    initial_set = sets[0]

    for i, set in enumerate(sets):
        if i == 0:
            continue
        if is_set_overlap(initial_set, set):
            initial_set = merge_set(initial_set, set)
        else:
            ans.append(set)

    return initial_set, ans

def getEntitiesSet(triples):

    global sets
    sets = []

    dict_R = {}
    cnt_R = 0
    for i, triple in enumerate(triples):
        e1 = triple[0]
        r = triple[1]
        e2 = triple[2]

        if r not in dict_R:
            dict_R[r] = cnt_R
            cnt_R = cnt_R + 1

    for i in range(dict_R.__len__()):
        sets.append({})
        sets.append({})

    for i, triple in enumerate(triples):
        e1 = triple[0]
        r = triple[1]
        e2 = triple[2]

        r_number = dict_R[r]
        sets[r_number*2][e1] = 1
        sets[r_number*2+1][e2] = 1

    results = []
    while sets.__len__() != 0:
        res, sets = loop(sets)
        results.append(res)
    sets = results

    global sets_relation_form
    sets_relation_form = np.zeros([sets.__len__(), sets.__len__()])

    for i, triple in enumerate(triples):
        e1 = triple[0]
        r = triple[1]
        e2 = triple[2]

        for j, set1 in enumerate(sets):
            if e1 in set1:
                for k, set2 in enumerate(sets):
                    if e2 in set2:
                        sets_relation_form[j][k] = sets_relation_form[j][k] + 1

    for j, set1 in enumerate(sets):
        for k, set2 in enumerate(sets):
            if sets_relation_form[j][k] > 2:
                sets_relation_form[j][k] = 1
            else:
                sets_relation_form[j][k] = 0

    print('The size of sets : ' + str(sets.__len__()))

    for j, set1 in enumerate(sets):
        print(set1.__len__())
        for k, s in enumerate(set1):
            print(s)
            if (k > 5):
                break


    '''
    for j, set1 in enumerate(sets):
        print("AAA " + str(set1.__len__()))
        for k, set2 in enumerate(sets):
            print(sets_relation_form[j][k], ' ')
        print('\n')
    '''
def check(entity1, entity2):

    global sets, sets_relation_form

    for i, set1 in enumerate(sets):
        if entity1 in set1:
            for j, set2 in enumerate(sets):
                if entity2 in set2:
                    if sets_relation_form[i][j] > 0.1:
                        return True

    return False

def getHitRate(batchList, notInTriples):
    pairDict = {}
    for i, triple in enumerate(notInTriples):
        e1 = triple[0]
        r = triple[1]
        e2 = triple[2]

        pairDict[(e1, e2)] = 1
        pairDict[(e2, e1)] = 1

    hit = 0
    cnt = 0
    for key in batchList:
        cnt = cnt + 1
        u, v = key
        newPair = (u, v)

        if newPair in pairDict:
            hit = hit + 1

    hitRate = 1.0 * hit / cnt
    hitRate2 = 1.0 * hit / notInTriples.__len__()

    return hitRate, hitRate2

def get_batch_with_check(results, batch):
    ans = []
    cnt = 0
    debug_cnt1 = 0
    debug_cnt2 = 0
    for (x, y), score in results.ranked_items():
        debug_cnt1 = debug_cnt1 + 1
        if check(x, y):
            debug_cnt2 = debug_cnt2 + 1
            ans.append((x, y))
            cnt = cnt + 1
            if cnt >= batch:
                break

    print("----debug----cnt1: " + str(debug_cnt1) + " ---- " + str(debug_cnt2))

    return ans

def get_batch_without_check(results, batch):
    ans = []
    cnt = 0
    for (x, y), score in results.ranked_items():
        ans.append((x, y))
        cnt = cnt + 1
        if cnt >= batch:
            break

    return ans

def hit(rate, batch, option):

    timestramp1 = datetime.now()
    in_file = open('./data/dbpedia50/smallScaleTrain' + str(rate) + '.txt', 'r')
    in_file2 = open('./data/dbpedia50/notSimpleData' + str(rate) + '.txt', 'r')

    triples = []
    for line in in_file:
        inputs = line.strip().split('\t')
        e1 = inputs[0]
        r = inputs[1]
        e2 = inputs[2]
        triples.append([e1, r, e2])
    notInTriples = []
    for line in in_file2:
        inputs = line.strip().split('\t')
        e1 = inputs[0]
        r = inputs[1]
        e2 = inputs[2]
        notInTriples.append([e1, r, e2])

    G = linkpred.read_network('./data/dbpedia50_' + str(rate) + '.net')
    timestramp2 = datetime.now()
    load_data_time = timestramp2 - timestramp1

    #getEntitiesSet(triples)

    timestramp1 = datetime.now()
    predictor = getPredictor(option, G)
    results = predictor.predict()
    timestramp2 = datetime.now()
    rooted_pagerank_time = timestramp2 - timestramp1

    timestramp1 = datetime.now()
    getEntitiesSet(triples)
    batchList_with_check = get_batch_with_check(results, batch)
    hitRate_with_check, hitRate_with_check2 = getHitRate(batchList_with_check, notInTriples)
    timestramp2 = datetime.now()
    entities_cluster_check_time = timestramp2 - timestramp1

    timestramp1 = datetime.now()
    batchList_without_check = get_batch_without_check(results, batch)
    hitRate_without_check, hitRate_without_check2 = getHitRate(batchList_without_check, notInTriples)
    timestramp2 = datetime.now()
    top_check_time = timestramp2 - timestramp1

    out_file = open('./log.txt', 'a')
    out_file.write('\n')
    out_file.write('rate: ' + rate + ' batch: ' + str(batch) + ' option ' + option + '\n')
    out_file.write('load_time: ' + str(load_data_time) + '\n')
    out_file.write('rooted_pagerank_time: ' + str(rooted_pagerank_time) + '\n')
    out_file.write('entities_cluster_check_time: ' + str(entities_cluster_check_time) + '\n')
    out_file.write('top_check_time: ' + str(top_check_time) + '\n')
    out_file.write('The hit rate without check of ' + option + ' is ' + str(hitRate_without_check) + ' ' + str(hitRate_without_check2) + '\n')
    out_file.write('The hit rate with check of ' + option + ' is ' + str(hitRate_with_check) + ' ' + str(hitRate_with_check2) + '\n')
    out_file.close()

    results_file = open('./data/results/dbpedia50_' + str(rate) + '_' + str(batch) + '_results.txt', 'w')
    for pair in batchList_with_check:
        x, y = pair
        results_file.write(x + '\t' + y + '\n')
    results_file.close()

if __name__ == "__main__":
    rate = argv[1]
    batch = int(argv[2])
    option = argv[3]

    hit(rate, batch, option)
