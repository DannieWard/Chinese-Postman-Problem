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

def eulerize(graph):
    """given a graph, this function uses networkx's find shortest path function to duplicated
    specific edges to give each graph an even degree by duplicating the least edges possible"""
    odds=findOddNodes(graph)
    while len(odds)!=0: #as long as there are odd nodes remaining
        pathDict=nx.shortest_path(graph, odds[0]) #creates a dictionary of the shortest path to all the nodes
        shortest=("A", 20) #second element must be arbitrarily large
        for j in pathDict.keys(): #goes through the dictionary
            if j==odds[0]: #skips the nodes path to itself since it is not useful
                continue
            if j in odds and len(pathDict[j])<shortest[1]: 
                #if the ending node is odd and has a shorter length than our current shortest path
                shortest=(j, len(pathDict[j]))
        path=nx.shortest_path(graph, odds[0], shortest[0]) #this is our shortest path between odd nodes
        odds.pop(0) #removes both nodes from the odd nodes list
        odds.remove(shortest[0])
        for k in range(len(path)-1): #adds the new edges from the shortest path
            graph.add_edge(path[k], path[k+1])
    return graph

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
    eulerize(G)
    nx.draw(G, with_labels=True)
    plt.show(G)
    return G

def getStarterNode(graph):
    """returns a random node from the graph"""
    rand=random.randint(0, len(graph.nodes)-1)
    starterNode=list(graph.nodes)[rand]
    return starterNode


def findNewStarterNode(graph, visitedNodes):
    """given a set of visited nodes, it returns one that still has available edges"""
    node=random.choice(tuple(visitedNodes))
    while graph.degree(node)==0:
        node=random.choice(tuple(visitedNodes))
    return node
      
def findCircle(graph, startNode):
    """finds a circle in the graph and returns it as a list of nodes"""
#    while graph.degree(starterNode)==0:
#        starterNode=getStarterNode(graph)
    path=[startNode]
    firstNode=startNode
    nextNode=None
    while len(path)<2 or path[0]!=path[len(path)-1]: #continues adding nodes to circuit as long as the first node doesn't match the last
        try:
            rand=random.randint(0, len(graph.edges(firstNode, keys=False))-1) #if this fails, it means we've completed a cycle
        except:
            break
        newEdge=list((graph.edges(firstNode, keys=False)))[rand] #finds a random edge connected to the node
        nextNode=newEdge[1] #gets the next node
        path.append(nextNode) #adds it to the path
        graph.remove_edge(firstNode, nextNode) #removes the edge from the path
        firstNode=nextNode
    return path

def findEuler(graph):
    """creates an euler cycle of the given graph"""
    pathList=[]
    visitedNodeSet=set() #holds all the visited nodes
    newPath=findCircle(graph, getStarterNode(graph)) #creates the first cycle
    for i in newPath:
        visitedNodeSet.add(i) #adds all the nodes to the visited nodes set
    pathList.append(newPath) #adds the new path to the list of paths
    while len(list(graph.edges))!=0: #as long as the graph has edges
        startNode=findNewStarterNode(graph, visitedNodeSet) #find a valid start node (one that has been visited already)
        newPath=findCircle(graph, startNode) #get a new path
        pathList.append(newPath) #add it to the pathlist
        for i in newPath:
            visitedNodeSet.add(i) #add the visited nodes to the set
    finalPath=[] #will hold the final, concatonated path
    finalPath+=pathList.pop(0) #remove the first path and place it in the final path
    startNodes=[] #will hold the starting nodes of all the paths
    for i in pathList:
        startNodes.append(i[0]) #adds to the list of the paths start nodes. we will use these to search for spots to combine the paths
    while len(pathList)!=0: #while the pathlist still has paths in it
        for i in finalPath: #go through every node in the final path
            if i in startNodes: #if the node is the starting nodes of one of the paths we have
                pos=startNodes.index(i)
#                finalPath=finalPath[0:finalPath.index(i)]+pathList.pop(pos)+finalPath[finalPath.index(i)+1:] #add the path in
                startNodes.pop(pos) #remove it from the startNodes list so we aren't looking for it anymore
    return finalPath
    
    
G=buildEvenGraph(20, 25)
