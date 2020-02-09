import networkx as nx
import random
import matplotlib.pyplot as plt

def findOddNodes(graph):
    """takes a multigraph as an input and returns a list of nodes that
    have an odd degree"""
    edgeList=graph.edges
    print(edgeList)
    edgeCounter={}
    oddNodes=[]
    for i in graph.nodes:
        edgeCounter[i]=0
    for e in edgeList:
        for n in e[0:2]:
            edgeCounter[n]+=1
    for k, v in edgeCounter.items():
        if v%2==1:
            oddNodes.append(k)
    return oddNodes

def giveGraphEvenNodes(graph):
    """given a graph, it makes all of its nodes even by adding new edges between 
    the odd nodes. utilizes findOddNodes() function"""
    oddNodes=findOddNodes(graph)
    while len(oddNodes)!=0:
        node=oddNodes[0]
        rand=random.randint(1, len(oddNodes)-1)
        graph.add_edge(node, oddNodes[rand])
        oddNodes.pop(rand)
        oddNodes.pop(0)
    return graph

def buildEvenGraph(minNodes, maxNodes):
    numberOfNodes=random.randint(minNodes, maxNodes)
    alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    G=nx.MultiGraph()
    print('Number of Nodes: '+str(numberOfNodes))
    for i in range(numberOfNodes):
        G.add_node(alphabet[i])
    for i in range(len(G.nodes)):
        for j in range(2):
            otherNodeIndex=random.randint(0, numberOfNodes-1)
            while otherNodeIndex==i:
                otherNodeIndex=random.randint(0, numberOfNodes-1)
            G.add_edge(list(G.nodes)[i], list(G.nodes)[otherNodeIndex])
    giveGraphEvenNodes(G)
    nx.draw(G, with_labels=True)
    plt.show(G)
    return G

G=buildEvenGraph(6, 12)
print(findOddNodes(G))
print(G.edges)

#buildEvenGraph() makes a graph with a number of nodes between the two paraemeters you give it
