#############
## CHANGED ##
#############
# deleted all existing comments and created descriptions of each function above including return values
# changed variable names and added comments in loadgraph(), changed small things, can still make changes
# changed all menu operation titles
# changed user input file to default node.nd
# changed all terminal input messages to different language and format
# added nodeProcessingTime to graph() class and added node weights to dijkstras
# updated menu interactions and spacing
# created printDefaultNodeDelay() and added option 3 to the menu
# 
#
#### NOTES ####
# put node.nd in node.py and change loadgraph
# change output of display()
# need to change the default values from node.nd
from random import randint
from collections import defaultdict
import random


### Declaring Node and Edge Data for Network ###
nodes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
# edges = {  
#     'a':[['b', 17], ['c', 8]], 
#     'b':[['c', 10], ['d', 15]], 
#     'c':[['d', 20], ['e', 12]], 
#     'd':[['f', 26]],
#     'e':[['f', 15]], 
#     'f':[['g', 8]],
#     'g':[['h', 14]]
#     }
edges = [   
    "a b 10",
    "a c 15",
    "b c 25",
    "b d 10",
    "c d 10",
    "c e 20",
    "d f 30",
    "e f 15",
    "f g 10",
    "g h 10"
    ]  
failureProbability = {
    'a':10,
    'b':10,
    'c':12,
    'd':5,
    'e':8,
    'f':20,
    'g':16,
    'h':3
}


### Graph Class ###
#  nodes: set of nodes' names
#  edges: dictionary of graph edge values from each node
#  distances: dictionary of distances to other nodes from each node
#  failureLikelihood: likelihood for a node to fail 
#  nodeProcessingTime: random float between 0 and 5 to simulate node processing delay
#  -  edge weights and node processing time weight are both used by dijkstras algorithm to calulate delay
class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}
        self.nodeProcessingTime = []
        self.failureLikelihood = defaultdict(list)

    def addNode(self, value, failureLikelihood):
        self.nodes.add(value)
        self.failureLikelihood[value].append(failureLikelihood)
        self.nodeProcessingTime.append(random.random()*5)

    def removeNode(self, node):
        self.nodes.remove(node)
        print(self.edges[node])
        del self.edges[node]
        for i in self.nodes:
                for j in range(0, len(self.edges[i])):
                    if(self.edges[i][j] == node):
                        del self.edges[i][j]
                        break

    def addEdge(self, first, last, weight):
        self.edges[first].append(last)
        self.edges[last].append(first)
        self.distances[(first, last)] = weight
        self.distances[(last, first)] = weight

    def printDefaultNodeDelay(self):
        count = 0
        for node in self.nodes:
            print("Node " + node + ": " + str(round(self.nodeProcessingTime[count],3)) + " seconds")
            count += 1

    #def printDefaultNodeDelay(self, node):
    #    nodeCount = 0
    #    tempDelay = None
    #    for locator in self.nodes:
    #        if locator == node:
    #            tempDelay = self.nodeProcessingTime[nodeCount]
    #        nodeCount += 1
    #    print("Node " + node + "'s Simulated Processing Delay: " + round(tempDelay, 3) + " seconds")

    def display(self):
        print("\nNodes: ", end='\n')
        for i in self.nodes:
            print(i, ' ', end='')

        print("\n\nLikelihood to Fail:")
        for j in self.nodes:
            print("Node", j, ': ', self.failureLikelihood[j][0], "%")

        print("\nEdges' Connections: ")
        spacingCounter = 0
        for k in self.nodes:
            if spacingCounter > 0:
                print('')
            print("Node", k, ':  ', end='')
            spacingCounter += 1
            for edge in self.edges[k]:
                print(edge, '', end='')

### Dijkstras Algorithm ###
#  Calculates the shortest distance for and from each mesh node
#  Orders distances for each node to other nodes in lists
#  Returns shortest path
def dijkstraAlg(graph, start):
  # generic dijkstra methodology with addition of node processing weight (processing delay)
  totalDistance = {start: 0}
  path = {}
  nodes = set(graph.nodes)
  processingTimes = graph.nodeProcessingTime
  
  while nodes:
    minNode = None
    nodeCount = 0
    for node in nodes:
      if node in totalDistance:
        minNode = node
        if totalDistance[node] < totalDistance[minNode]:
          nodeCount += 1

    if minNode is None:
      break

    nodes.remove(minNode)
    currentWeight = totalDistance[minNode] + processingTimes[nodeCount]
    del processingTimes[nodeCount]

    for edge in graph.edges[minNode]:
      weight = currentWeight + graph.distances[(minNode, edge)]
      if edge not in totalDistance or weight < totalDistance[edge]:
        totalDistance[edge] = weight
        path[edge] = minNode
        
  print("Distance from Node", str(start), ": (Including Node Delay)")
  for key in totalDistance.keys():
    print("Node", key, ":", round(totalDistance[str(key)], 3))

  print("\nLast Hop from Node", str(start), ":")
  for key in path.keys():
    print("To Node", key, ':', str(path[key]))

  return totalDistance


### Load Graph ###
#  Opens the node data file and reads it line by line, separating data by specified characters
#  Then, instantiates nodes/edges and their according data to the graph class
#  Returns a complete graph
def loadGraph(graph, node, edge, failureProb):
    for n in node:
        graph.addNode(n, failureProb[n])
    for e in edge:
        edgeDef = e.split(' ')
        graph.addEdge(edgeDef[0], edgeDef[1], int(edgeDef[2]))
    # for e in edge:
    #     for arr in e:
    #         for edgearr in arr:
    #             graph.addEdge(str(e), str(edgearr[0]), int(edgearr[1]))

    return graph
        

### Node Failure Operation ###
#  Program instructions for when a mesh node fails
#  Takes whole graph as input, searches for failed nodes, removes failed nodes from graph
#  Returns nothing, displays terminal messages
def NodeFailure(graph):
    while True:
        for node in graph.nodes:
            check = randint(0,100)
            if check < graph.failureLikelihood[node][0]:
                print("Node", node, "has failed.")
                print("Node", node, "and it's according edges have been removed from the graph.")
                graph.removeNode(node)
                return
    return


### Menu Function ###
#  Displays options for user in the terminal
#  Program operation is responsive to user's input 
#  Returns user's menu decision
def Menu():
    print("\n\n\n+----------------------+")
    print("| Please Select Option |")
    print("+----------------------+")
    print("[1] Simulate Until Failure")
    print("[2] Create Node")
    print("[3] Create Edge Between Nodes")
    print("[4] Force Node Failure")
    print("[5] Display Node Processing Delay")
    print("[6] Calculate Node's Distance to Surrounding Nodes")
    print("[7] Display Graph")
    print("[8] Exit\n")
    userInput = input("Select Option:  ")
    return userInput

def main():
    for i in range(0,25):
        print("\n\n\n")
    print("##################################################")
    print("##               Welcome to the                 ##")
    print("## DYNAMIC ROUTING IN FAULTY NETWORK SIMULATION ##")
    print("## -------------------------------------------- ##")
    print("##        Jason Brown   &   Colton Morley       ##")
    print("##################################################")

    # graph = loadGraph('Node.nd')
    graph = Graph()
    loadGraph(graph, nodes, edges, failureProbability)
    userInput = 0

    ### Program routes based upon user input ###
    while userInput is not '8':
        userInput = Menu()

        if userInput is '1':

            # natural failure given default failure probabilities
            NodeFailure(graph)

        elif userInput is '2':

            nodeToAdd = input("New Node Label: ")
            while nodeToAdd in graph.nodes:
                print("Node " + nodeToAdd + " already exists. Please Try Again.")
                nodeToAdd = input("New Node Label: ")
            percentageFailure = input("Enter Failure Likelihood (%): ")
            graph.addNode(str(nodeToAdd), int(percentageFailure))
            print("Node", nodeToAdd, "has been created.")

        elif userInput == '3':

            tempArr = []
            for node in graph.nodes:
                tempArr.append(node)
            print("Nodes: ", end="\n")
            for i in tempArr:
                print(i, " ", end="")
            firstNode = input("\nStarting Node: ")
            while firstNode not in graph.nodes:
                print("Invalid Input. Please Try Again.\n")
                firstNode = input("Starting Node: ")
            secondNode = input("Ending Node: ")
            while secondNode not in graph.nodes:
                print("Invalid Input. Please Try Again.\n")
                secondNode = input("Ending Node: ")
            weight = input("Edge Weight: ")
            while int(weight) < 0:
                print("Invalid Input. Please Try Again.\n")
                weight = input("Edge Weight: ")
            graph.addEdge(str(firstNode), str(secondNode), int(weight))
            print("Edge has been created.")

        elif userInput is '4':

            tempArr = []
            for node in graph.nodes:
                tempArr.append(node)
            print("Nodes: ", end="\n")
            for i in tempArr:
                print(i, " ", end="")
            nodeToFail = input("\nEnter Node to Fail: ")
            while nodeToFail not in graph.nodes:
                print("Invalid Input. Please Try Again.\n")
                nodeToFail = input("\nEnter Node to Fail: ")
            graph.removeNode(nodeToFail)
            print("Node " + nodeToFail + " was forced to fail and has been removed.")

        elif userInput is '5':

            print("\nNode Processing Times:")
            graph.printDefaultNodeDelay()

        elif userInput is '6':

            tempArr = []
            for node in graph.nodes:
                tempArr.append(node)
            print("Nodes: ", end="\n")
            for i in tempArr:
                print(i, " ", end="")
            nodeToStart = ''
            first = True
            while nodeToStart not in graph.nodes:
                if first is False:
                    input("Invalid Input. Please Try Again.\n")
                else:
                    first = False
                nodeToStart = input("\nStarting Node: ")
            print("Running Dijkstra's Algorithm...\n")
            dijkstraAlg(graph, str(nodeToStart))
            

        elif userInput is '7':
            graph.display()
        elif userInput is '8':
            break
        else:
            print("Invalid Input. Please Try Again.\n")

    return

if __name__ == '__main__': main()