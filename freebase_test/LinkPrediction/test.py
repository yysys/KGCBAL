
import linkpred
from datetime import datetime

G = linkpred.read_network("./data/Freebase13.net")

a = datetime.now()
neighbour_rank1 = linkpred.predictors.CommonNeighbours(G, excluded=G.edges())
neighbour_rank_results1 = neighbour_rank1.predict()
b = datetime.now()
print("The time of CommonNeighbores: " + str(b-a))

a = datetime.now()
neighbour_rank2 = linkpred.predictors.AdamicAdar(G, excluded=G.edges())
neighbour_rank_results2 = neighbour_rank2.predict()
b = datetime.now()
print("The time of AdamicAdar: " + str(b-a))

a = datetime.now()
neighbour_rank3 = linkpred.predictors.Jaccard(G, excluded=G.edges())
neighbour_rank_results3 = neighbour_rank3.predict()
b = datetime.now()
print("The time of Jaccard: " + str(b-a))

a = datetime.now()
neighbour_rank4 = linkpred.predictors.ResourceAllocation(G, excluded=G.edges())
neighbour_rank_results4 = neighbour_rank4.predict()
b = datetime.now()
print("The time of ResourceAllocation: " + str(b-a))

a = datetime.now()
neighbour_rank5 = linkpred.predictors.DegreeProduct(G, excluded=G.edges())
neighbour_rank_results5 = neighbour_rank5.predict()
b = datetime.now()
print("The time of PreferentialAttachment: " + str(b-a))

'''
# We exclude edges already present, to predict only new links
neighbour_rank = linkpred.predictors.CommonNeighbours(G, excluded=G.edges())

neighbour_rank_results = neighbour_rank.predict()
'''

'''
GG = linkpred.read_network("./examples/inf1990-2004.net")

print(GG.node())
'''
# We exclude edges already present, to predict only new links
#neighbour_rank = linkpred.predictors.CommonNeighbours(GG, excluded=GG.edges())



'''
for a, b in neighbour_rank.likely_pairs():
    print("BBBB")
'''


