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

    timestramp1 = datetime.now()
    predictor = getPredictor(option, G)
    results = predictor.predict()
    timestramp2 = datetime.now()
    rooted_pagerank_time = timestramp2 - timestramp1

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
    out_file.write('top_check_time: ' + str(top_check_time) + '\n')
    out_file.write('The hit rate of ' + option + ' is ' + str(hitRate_without_check) + ' ' + str(hitRate_without_check2) + '\n')
    out_file.close()

if __name__ == "__main__":
    rate = argv[1]
    batch = int(argv[2])
    option = argv[3]

    hit(rate, batch, option)
