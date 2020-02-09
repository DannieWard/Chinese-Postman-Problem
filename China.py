import networkx as nx
import random
import matplotlib.pyplot as plt

def findOddNodes(graph):
    """takes a multigraph as an input and returns a list of nodes that
    have an odd degree"""
    edgeList=graph.edges #creates a list holding the edges
    print(edgeList)
    edgeCounter={} #a dictionary that will hold the number of edges each node has
    oddNodes=[] #holds the list of odd nodes
    for i in graph.nodes:
        edgeCounter[i]=0 #initializes a counter in the dictionary for each node
    for e in edgeList: #goes through each edge in edgelist
        for n in e[0:2]: #goes through both nodes listed in each edge
            edgeCounter[n]+=1 #adds one to the nodes counter that the edge belongs to
    for k, v in edgeCounter.items(): #goes through each item in the dictionary
        if v%2==1: #if the node has an odd number of edges, it adds it to the list of odd nodes
            oddNodes.append(k)
    return oddNodes #returns the list of odd nodes

def giveGraphEvenNodes(graph):
    """given a graph, it makes all of its nodes even by adding new edges between 
    the odd nodes. utilizes findOddNodes() function"""
    oddNodes=findOddNodes(graph) #gets the list of odd nodes
    while len(oddNodes)!=0: #while there are still odd nodes
        node=oddNodes[0]
        rand=random.randint(1, len(oddNodes)-1)
        graph.add_edge(node, oddNodes[rand]) #creates an edge between two of the nodes
        oddNodes.pop(rand) #removes one of the nodes because it is no longer odd
        oddNodes.pop(0) #removes the other node
    return graph #returns the new graph with even nodes

def buildEvenGraph(minNodes, maxNodes):
    """ uses the findNodes() function and giveGraphEvenNodes() to create an even graph
    that has a Euler tour"""
    numberOfNodes=random.randint(minNodes, maxNodes) #picks a random number of nodes between the two parameters
    alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    G=nx.MultiGraph()
    print('Number of Nodes: '+str(numberOfNodes))
    for i in range(numberOfNodes):
        G.add_node(alphabet[i]) #adds the nodes by going through alphabet
    for i in range(len(G.nodes)):
        for j in range(2):
            #gets a random number to represent the edge the node will connect to
            otherNodeIndex=random.randint(0, numberOfNodes-1) 
            while otherNodeIndex==i: #makes sure the node isnt connecting to itself
                otherNodeIndex=random.randint(0, numberOfNodes-1)
            G.add_edge(list(G.nodes)[i], list(G.nodes)[otherNodeIndex]) #adds the edge
    giveGraphEvenNodes(G)
    nx.draw(G, with_labels=True)
    plt.show(G)
    return G

G=buildEvenGraph(6, 12)
print(findOddNodes(G))
print(G.edges)
