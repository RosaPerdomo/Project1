from node import *
from segment import *
import matplotlib.pyplot as plt 
import numpy as np

class Graph:
    def __init__ (self):
        self.node = []
        self.segment = []

def AddNode (g, n):
    for node in g.node:
        if node.name == n.name:
            return False
    g.node.append(n)
    return True

def DetectEntry (entryNode):
    text = entryNode.replace(',', ' ')
    partes = text.split(' ')
    if len(partes) == 3:
        if partes[1].isdigit():
            name = partes[0]
            x = float(partes[1])
            y = float(partes[2])
            d = Node(name, x, y)
        elif partes[1].isalpha():
            d = [partes[0], partes[1], partes[2]]
    return d

def DeleteSegment (g, s):
    newsegments = []
    for d in g.segment:
        if d.name != s:
            newsegments.append(d)
    g.segment = newsegments
    return g

def DeleteNode (g, n):
    newnodes = []
    for d in g.node:
        if d.name != n:
            newnodes.append(d)
    g.node = newnodes
    newsegments = []
    for d in g.segment:
        if d.origin.name != n and d.destination.name != n:
            newsegments.append(d)
    g.segment = newsegments
    return g

def AddSegment (g, segmentName, nameOriginNode, nameDestinationNode):
    nO = False
    nD = False
    for node in g.node:
        if node.name == nameOriginNode:
            nO = True
            n1 = node
        elif node.name == nameDestinationNode:
            nD = True
            n2 = node
    if nO == True and nD == True:
        n1.neighbors.append(n2)
        s = Segment (segmentName, n1, n2)
        g.segment.append(s)
        return True
    else:
        return False
    
def GetClosest (g, x, y):
    point = Node ('p', x, y)
    closest = g.node[0]
    min_dist = Distance(closest, point)
    for n in g.node[1:]:
        d = Distance(n, point)
        if d < min_dist:
            closest = n
            min_dist = d
    return closest

def Plot(g):
    for n in g.node:
        plt.plot(n.x ,n.y, 'o', color='red', markersize=3)
        plt.text(n.x, n.y, f'{n.name}', fontsize=8, color='black')
    for s in g.segment:
        plt.arrow(s.origin.x, s.origin.y, s.destination.x - s.origin.x, s.destination.y - s.origin.y, head_width=0.2, head_length=0.3, fc='blue', ec='blue', linewidth=0.5)
        midx = (s.origin.x + s.destination.x) / 2
        midy = (s.origin.y + s.destination.y) / 2
        plt.text(midx, midy, f'{s.cost} km', fontsize=7, weight='bold')
    plt.grid(color='gray', linestyle='dashed', linewidth=0.5)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

def PlotNode(g, nameOrigin):
    found = False
    origin = None

    for n in g.node:
        if n.name == nameOrigin:
            origin = n
            plt.plot(n.x, n.y, 'o', color='blue', markersize=5)
            plt.text(n.x, n.y, f'{n.name}', fontsize=8, color='black')
            found = True
            break
    if found == False:
        return False
    
    for s in g.segment:
        if s.origin.name == nameOrigin:
            plt.plot(s.destination.x, s.destination.y, 'o', color = 'green', markersize = 3)
            plt.text(s.destination.x, s.destination.y, f'{s.destination.name}', fontsize=8, color='black')
            plt.arrow(s.origin.x, s.origin.y, s.destination.x - s.origin.x, s.destination.y - s.origin.y, head_width=0.2, head_length=0.3, fc='red', ec='red', linewidth=0.5)
            midx = (s.origin.x + s.destination.x) / 2
            midy = (s.origin.y + s.destination.y) / 2
            plt.text(midx, midy, f'{s.cost} km', fontsize=7, weight='bold')
    
    for n in g.node:
        for neighbor in origin.neighbors:
            if n != neighbor:
                plt.plot(n.x, n.y, 'o', color='gray', markersize=3)
                plt.text(n.x, n.y, f'{n.name}', fontsize=8, color='black')

    plt.grid(color='grey', linestyle='dashed', linewidth=0.5)
    plt.show()

def LoadFile (fileName):
    X = open(fileName, 'r')
    lines = X.readlines()
    g = Graph()
    type = 'x'
    for line in lines:
        line = line.strip()
        if line == 'Nodes:':
            type = 'n'
            continue
        elif line == 'Segments:':
            type = 's'
            continue
        if type == 'n':
            trozo = line.split(' ')
            if len(trozo) == 3:
                name = trozo[0]
                x = float(trozo[1])
                y = float(trozo[2])
                n = Node(name, x, y)
                AddNode(g, n)
        elif type == 's':
            trozo = line.split(' ')
            if len(trozo) == 3:
                name = trozo[0]
                origin = trozo[1]
                destination = trozo[2]
                AddSegment(g, name, origin, destination)
        else:
            break
    return g

def PlotFile(fileName):
    g = LoadFile(fileName)
    Plot(g)

def NewGraph(g):
    g.node.clear()
    g.segment.clear()
    return g

def SaveGraph(g):
    X = open('Graph.txt', 'w')
    X.write('Nodes:\n')
    for n in g.node:
        X.write(f'{n.name} {n.x} {n.y}\n')
    X.write('Segments:\n')
    for s in g.segment:
        X.write(f'{s.name} {s.origin.name} {s.destination.name}\n')
    print('Graph saved successfully.')