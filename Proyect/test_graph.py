from graph import *
from path import *

def CreateGraph_1 ():
    G = Graph()
    AddNode(G, Node("A",1,20))
    AddNode(G, Node("B",8,17))
    AddNode(G, Node("C",15,20))
    AddNode(G, Node("D",18,15))
    AddNode(G, Node("E",2,4))
    AddNode(G, Node("F",6,5))
    AddNode(G, Node("G",12,12))
    AddNode(G, Node("H",10,3))
    AddNode(G, Node("I",19,1))
    AddNode(G, Node("J",13,5))
    AddNode(G, Node("K",3,15))
    AddNode(G, Node("L",4,10))
    AddSegment(G, "AE","A", "E")
    AddSegment(G, "AK","A", "K")
    AddSegment(G, "BC","B", 'C')
    AddSegment(G, "BK","B", 'K')
    AddSegment(G, "BG","B", 'G')
    AddSegment(G, "CG","C", 'G')
    AddSegment(G, "DG","D", 'G')
    AddSegment(G, "DH","D", 'H')
    AddSegment(G, "EF","E", 'F')
    AddSegment(G, "GB","G", 'B')
    AddSegment(G, "GH","G", 'H')
    AddSegment(G, "ID","I", 'D')
    AddSegment(G, "IJ","I", 'J')
    AddSegment(G, "JI","J", 'I')
    AddSegment(G, "KA","K", 'A')
    AddSegment(G, "LK","L", 'K')
    AddSegment(G, "LF","L", 'F')
    return G
print ("Probando el grafo...")
G = CreateGraph_1 ()
Plot(G)
n = GetClosest(G,15,5)
print (n.name) # La respuesta debe ser J
n = GetClosest(G,8,19)
print (n.name) # La respuesta debe ser B

print(DetectEntry('A 1 1'))
print(DetectEntry('AB A B'))


PlotReachability(G, Reachability(G, 'D'))

PlotPath(G, FindShortestPath(G, 'A', 'F'))