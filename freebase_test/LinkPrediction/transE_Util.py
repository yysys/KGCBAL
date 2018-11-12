
import os
import random

def trans_Freebase_to_transHdata(rate):

    in_file = open('./data/Freebase13/smallScaleTrain' + str(rate) + '.txt', 'r')
    in_file2 = open('./data/Freebase13/notSimpleData' + str(rate) + '.txt', 'r')
    #linkpred_results500_file = open('./data/results/Freebase13_' + str(rate) + '_500_results.txt', 'r')
    linkpred_results1000_file = open('./data/results/Freebase13_' + str(rate) + '_1000_results.txt', 'r')
    linkpred_results2000_file = open('./data/results/Freebase13_' + str(rate) + '_2000_results.txt', 'r')

    triples = []
    entities = []
    relations = []
    linkpred_results500 = []
    linkpred_results1000 = []
    linkpred_results2000 = []

    dict_E = {}
    dict_R = {}

    for line in in_file:
        inputs = line.strip().split('\t')
        e1 = inputs[0]
        r = inputs[1]
        e2 = inputs[2]

        if e1 not in dict_E:
            dict_E[e1] = 1
            entities.append(e1)

        if e2 not in dict_E:
            dict_E[e2] = 1
            entities.append(e2)

        if r not in dict_R:
            dict_R[r] = 1
            relations.append(r)

        triples.append([e1, r, e2])

    ground_truth_triples = {}
    for line in in_file2:
        inputs = line.strip().split('\t')
        e1 = inputs[0]
        r = inputs[1]
        e2 = inputs[2]

        if (e1, r, e2) not in ground_truth_triples:
            ground_truth_triples[(e1, r, e2)] = 1
    '''
    for line in linkpred_results500_file:
        inputs = line.strip().split('\t')
        e1 = inputs[0]
        e2 = inputs[1]

        linkpred_results500.append((e1, e2))
    '''
    for line in linkpred_results1000_file:
        inputs = line.strip().split('\t')
        e1 = inputs[0]
        e2 = inputs[1]

        linkpred_results1000.append((e1, e2))

    for line in linkpred_results2000_file:
        inputs = line.strip().split('\t')
        e1 = inputs[0]
        e2 = inputs[1]

        linkpred_results2000.append((e1, e2))


    out_dir = './data/transH_data/' + str(rate)

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    out_entities_file = open(out_dir + '/entity2id.txt', 'w')
    out_relations_file = open(out_dir + '/relation2id.txt', 'w')
    out_train_file = open(out_dir + '/train.txt', 'w')
    out_test500_file = open(out_dir + '/test500.txt', 'w')
    out_test1000_file = open(out_dir + '/test1000.txt', 'w')
    out_test2000_file = open(out_dir + '/test2000.txt', 'w')

    for i, entity in enumerate(entities):
        out_entities_file.write(str(entity) + '\t' + str(i) + '\n')

    for i, relation in enumerate(relations):
        out_relations_file.write(str(relation) + '\t' + str(i) + '\n')

    for i, triple in enumerate(triples):
        e1 = triple[0]
        r = triple[1]
        e2 = triple[2]

        out_train_file.write(e2 + '\t' + e1 + '\t' + r + '\n')

    for entity_pair in linkpred_results500:
        u, v = entity_pair
        flag = 0
        for r in relations:
            if (u, r, v) in ground_truth_triples:
                out_test500_file.write(v + '\t' + u + '\t' + r + '\t1\n')
                flag = 1
                break
            if (v, r, u) in ground_truth_triples:
                out_test500_file.write(u + '\t' + v + '\t' + r + '\t1\n')
                flag = 1
                break
        if (flag == 0):
            r_id = random.randint(0, relations.__len__() - 1)
            out_test500_file.write(v + '\t' + u + '\t' + relations[r_id] + '\t0\n')


    for entity_pair in linkpred_results1000:
        u, v = entity_pair
        flag = 0
        for r in relations:
            if (u, r, v) in ground_truth_triples:
                out_test1000_file.write(v + '\t' + u + '\t' + r + '\t1\n')
                flag = 1
                break
            if (v, r, u) in ground_truth_triples:
                out_test1000_file.write(u + '\t' + v + '\t' + r + '\t1\n')
                flag = 1
                break
        if (flag == 0):
            r_id = random.randint(0, relations.__len__() - 1)
            out_test1000_file.write(v + '\t' + u + '\t' + relations[r_id] + '\t0\n')

    for entity_pair in linkpred_results2000:
        u, v = entity_pair
        flag = 0
        for r in relations:
            if (u, r, v) in ground_truth_triples:
                out_test2000_file.write(v + '\t' + u + '\t' + r + '\t1\n')
                flag = 1
                break
            if (v, r, u) in ground_truth_triples:
                out_test2000_file.write(u + '\t' + v + '\t' + r + '\t1\n')
                flag = 1
                break
        if (flag == 0):
            r_id = random.randint(0, relations.__len__() - 1)
            out_test2000_file.write(v + '\t' + u + '\t' + relations[r_id] + '\t0\n')

    out_test500_file.close()
    out_test1000_file.close()
    out_test2000_file.close()

trans_Freebase_to_transHdata(55)
trans_Freebase_to_transHdata(60)
trans_Freebase_to_transHdata(65)
trans_Freebase_to_transHdata(70)
trans_Freebase_to_transHdata(75)
trans_Freebase_to_transHdata(80)
trans_Freebase_to_transHdata(85)
trans_Freebase_to_transHdata(90)
trans_Freebase_to_transHdata(95)

