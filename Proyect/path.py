from node import *
from graph import *
import matplotlib.pyplot as plt 
import numpy as np

class Path:
    def __init__ (self, origin):
        self.nodes = [origin]
        self.cost = 0.0

def AddNodeToPath(path, node): #MIRAR
    add = True
    for a in path.nodes:
        if a == node:
            add = False
            break
    if add == True:
        last = path.nodes[-1]
        path.cost += round(Distance(last, node), 2)
        path.nodes.append(node)
    return add

def ContainsNode (p, node):
    for a in p.nodes:
        if a == node:
            return True
    return False

def CostToNode (p, node):
    total = 0.0
    i = 0
    if node not in p.nodes:
        return -1
    while i < len(p.nodes)-1 :
        a = p.nodes[i]
        b = p.nodes[i + 1]
        if a == node:
            break
        else:
            total += round(Distance(a, b), 2)
        i += 1
    return total

def PlotPath(g, p, is_geographic=False):
    fig, ax = plt.subplots(figsize=(12, 8))
    
    if is_geographic:
        head_size = 0.05
        node_size_main = 5
        node_size_secondary = 3
        font_size = 7
        path_width = 1.5
    else:
        head_size = 0.2
        node_size_main = 8
        node_size_secondary = 5
        font_size = 8
        path_width = 2
    
    for n in g.node:
        if n in p.nodes:
            ax.plot(n.x, n.y, 'o', color='blue', markersize=node_size_main)
            ax.text(n.x, n.y, f'{n.name}', fontsize=font_size+1, color='black',
                   ha='center', va='center', weight='bold')
        else:
            ax.plot(n.x, n.y, 'o', color='gray', markersize=node_size_secondary, alpha=0.5)
            ax.text(n.x, n.y, f'{n.name}', fontsize=font_size-1, color='gray',
                   ha='center', va='center', alpha=0.7)
    
    for s in g.segment:
        ax.plot([s.origin.x, s.destination.x],
               [s.origin.y, s.destination.y],
               'gray', linewidth=0.3, alpha=0.3)
    
    for i in range(len(p.nodes) - 1):
        origin = p.nodes[i]
        destination = p.nodes[i+1]
        
        segment = None
        for s in g.segment:
            if (s.origin == origin and s.destination == destination) or \
               (s.origin == destination and s.destination == origin):
                segment = s
                break
        
        if segment:
            ax.arrow(origin.x, origin.y, 
                    destination.x - origin.x, 
                    destination.y - origin.y,
                    head_width=head_size, 
                    head_length=head_size*1.5,
                    fc='blue', ec='blue', 
                    linewidth=path_width, 
                    length_includes_head=True,
                    alpha=0.8)
            

            midx = (origin.x + destination.x)/2
            midy = (origin.y + destination.y)/2
            ax.text(midx, midy, f'{segment.cost:.1f} km', 
                   fontsize=font_size, weight='bold',
                   ha='center', va='center', color='blue')
    
    ax.grid(color='gray', linestyle='dashed', linewidth=0.3, alpha=0.5)
    ax.set_xlabel("Longitude" if is_geographic else "X")
    ax.set_ylabel("Latitude" if is_geographic else "Y")
    ax.set_title(f"Shortest Path Visualization - Total Cost: {round(p.cost, 2)} km")
    
    return fig