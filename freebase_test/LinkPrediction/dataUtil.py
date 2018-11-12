import random

def trans(in_file_string, sep, out_file_string, network_name):

    in_file = open(in_file_string, 'r')
    out_file = open(out_file_string, 'w')

    dict_E = {}
    triples = []
    E_cnt = 0

    for line in in_file:
        inputs = line.strip().split(sep)
        e1 = inputs[0]
        r = inputs[1]
        e2 = inputs[2]

        if '"' + e1 + '"' not in dict_E:
            E_cnt = E_cnt + 1
            dict_E['"' + e1 + '"'] = E_cnt

        if '"' + e2 + '"' not in dict_E:
            E_cnt = E_cnt + 1
            dict_E['"' + e2 + '"'] = E_cnt

        triples.append([dict_E['"' + e1 + '"'], r, dict_E['"' + e2 + '"']])

    out_file.write('*network ' + network_name + '\n')
    out_file.write('*vertices ' + str(dict_E.__len__()) + '\n')
    for e in dict_E:
        out_file.write(str(dict_E[e]) + ' ' + e +'\n')

    out_file.write('*edges\n')
    for triple in triples:
        out_file.write(str(triple[0]) + ' ' + str(triple[2]) + ' 1\n')

    out_file.close()

def simplifyNetwork(in_file_string, sep, out_file_string):

    in_file = open(in_file_string, 'r')
    out_file = open(out_file_string, 'w')

    dict_E = {}
    entities = []
    triples = []

    cnt = 0
    for line in in_file:
        inputs = line.strip().split(sep=sep)
        e1 = inputs[0]
        r = inputs[1]
        e2 = inputs[2]

        if e1 not in dict_E:
            cnt = cnt + 1
            dict_E[e1] = cnt
            entities.append(e1)
        if e2 not in dict_E:
            cnt = cnt + 1
            dict_E[e2] = cnt
            entities.append(e2)

        triples.append([e1, r, e2])

    entitiesDict = {}
    triplesDropScale = int(dict_E.__len__() * 0.15)
    triples2 = []

    for i in range(triplesDropScale):
        while True:
            id = random.randint(0, triples.__len__() - 1)

            if triples[id][0] not in entitiesDict:
                entitiesDict[triples[id][0]] = 1
                break

    for i, triple in enumerate(triples):
        e1 = triple[0]
        r = triple[1]
        e2 = triple[2]

        if e1 == e2:
            continue

        if e1 in entitiesDict or e2 in entitiesDict:
            triples2.append([e1, r, e2])

    triples = triples2

    simplifiedEntitiesDict = {}
    simplifiedEntitiesDict['male'] = 1
    simplifiedEntitiesDict['female'] = 1
    simplifiedEntitiesScale = int(dict_E.__len__() * 0.65)

    for i in range(simplifiedEntitiesScale):
        while True:
            id = random.randint(0, dict_E.__len__() - 1)
            #if entities[id] == 'male' or entities[id] == 'female':
            #    continue
            if entities[id] not in simplifiedEntitiesDict:
                simplifiedEntitiesDict[entities[id]] = 1
                break

    simplifiedTriples = []

    for i, triple in enumerate(triples):
        e1 = triple[0]
        r = triple[1]
        e2 = triple[2]

        if e1 == e2:
            continue

        if e1 in simplifiedEntitiesDict and e2 in simplifiedEntitiesDict:
            simplifiedTriples.append([e1, r, e2])

    for i, triple in enumerate(simplifiedTriples):
        e1 = triple[0]
        r = triple[1]
        e2 = triple[2]

        out_file.write(e1 + '\t' + r + '\t' + e2 +'\n')

    out_file.close()

def survey(in_file_string, sep):
    in_file = open(in_file_string, 'r')

    dict_E = {}
    dict_R = {}
    triples = []
    E_cnt = 0

    for line in in_file:
        inputs = line.strip().split(sep=sep)
        e1 = inputs[0]
        r = inputs[1]
        e2 = inputs[2]

        triples.append([e1, r, e2])

        if e1 not in dict_E:
            E_cnt = E_cnt + 1
            dict_E[e1] = E_cnt

        if e2 not in dict_E:
            E_cnt = E_cnt + 1
            dict_E[e2] = E_cnt

        if r not in dict_R:
            dict_R[r] = 1

    print(dict_E.__len__())
    print(dict_R.__len__())
    print(triples.__len__())


#survey('./data/Freebase13/train.txt', '\t')

simplifyNetwork('./data/Freebase13/train.txt', '\t', './data/Freebase13/smallScaleTrain.txt')
survey('./data/Freebase13/smallScaleTrain.txt', '\t')
trans('./data/Freebase13/smallScaleTrain.txt', '\t', './data/Freebase13.net', 'freebase13 network')



def drop(rate):
    in_file = open('./data/Freebase13/smallScaleTrain.txt', 'r')
    out_file = open('./data/Freebase13/smallScaleTrain' + str(rate) + '.txt', 'w')
    out_file2 = open('./data/Freebase13/notSimpleData' + str(rate) + '.txt', 'w')
    triples = []

    for line in in_file:
        inputs = line.strip().split('\t')
        e1 = inputs[0]
        r = inputs[1]
        e2 = inputs[2]

        triples.append([e1, r, e2])


    simpleTriplesScale = int(triples.__len__() * (int(rate) * 1.0 / 100 ))
    simpleTriplesDict = {}
    simpleTriples = []

    for i in range(simpleTriplesScale):
        id = random.randint(0, triples.__len__()-1)
        if id not in simpleTriplesDict:
            simpleTriplesDict[id] = 1
            simpleTriples.append(triples[id])

    for i, triple in enumerate(triples):
        if i not in simpleTriplesDict:
            e1 = triple[0]
            r = triple[1]
            e2 = triple[2]

            out_file2.write(e1 + '\t' + r + '\t' + e2 + '\n')

    for i, triple in enumerate(simpleTriples):
        e1 = triple[0]
        r = triple[1]
        e2 = triple[2]

        out_file.write(e1 + '\t' + r + '\t' + e2 + '\n')

    out_file.close()
    out_file2.close()

def transToNetworkx(rate):
    trans('./data/Freebase13/smallScaleTrain' + str(rate) + '.txt',
          '\t', './data/Freebase13_' + str(rate) + '.net', 'freebase13 network')

def drop_and_trans_55_to_95():
    in_file = open('./data/Freebase13/smallScaleTrain.txt', 'r')
    triples = []

    for line in in_file:
        inputs = line.strip().split('\t')
        e1 = inputs[0]
        r = inputs[1]
        e2 = inputs[2]

        triples.append([e1, r, e2])

    simpleTriplesScale = int(triples.__len__() * (50 * 1.0 / 100))
    everyTriples = int(triples.__len__() * (5 * 1.0 / 100))
    simpleTriplesDict = {}
    simpleTriples = []

    cnt = 0
    while cnt < simpleTriplesScale:
        id = random.randint(0, triples.__len__() - 1)
        if id not in simpleTriplesDict:
            simpleTriplesDict[id] = 1
            simpleTriples.append(triples[id])
            cnt = cnt + 1

    for i in range(9):
        cnt = 0
        while cnt < everyTriples:
            id = random.randint(0, triples.__len__() - 1)
            if id not in simpleTriplesDict:
                simpleTriplesDict[id] = 1
                simpleTriples.append(triples[id])
                cnt = cnt + 1

        out_file = open('./data/Freebase13/smallScaleTrain' + str(55 + i * 5) + '.txt', 'w')
        out_file2 = open('./data/Freebase13/notSimpleData' + str(55 + i * 5) + '.txt', 'w')

        for j, triple in enumerate(triples):
            if j not in simpleTriplesDict:
                e1 = triple[0]
                r = triple[1]
                e2 = triple[2]

                out_file2.write(e1 + '\t' + r + '\t' + e2 + '\n')

        for j, triple in enumerate(simpleTriples):
            e1 = triple[0]
            r = triple[1]
            e2 = triple[2]

            out_file.write(e1 + '\t' + r + '\t' + e2 + '\n')

        out_file.close()
        out_file2.close()

    transToNetworkx(55)
    transToNetworkx(60)
    transToNetworkx(65)
    transToNetworkx(70)
    transToNetworkx(75)
    transToNetworkx(80)
    transToNetworkx(85)
    transToNetworkx(90)
    transToNetworkx(95)

drop_and_trans_55_to_95()