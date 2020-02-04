import networkx as nx
import random
import matplotlib.pyplot as plt

nodeList=[]
numberOfNodes=random.randint(8, 12)
alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
G=nx.Graph()
print(numberOfNodes)
print(type(list(G.nodes)))
for i in range(numberOfNodes):
    G.add_node(alphabet[i])
nx.draw(G, with_labels=True)
plt.show(G)
for i in G.nodes:
    r=random.randint(0,1)
    if r==0:
        r=2
    else:
        r=4
    for j in range(4):
        G.add_edge(i, list(G.nodes)[random.randint(0, numberOfNodes-1)])
print(G.edges)
nx.draw(G, with_labels=True)
plt.show(G)
