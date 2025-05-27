from node import *
from segment import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math
from path import *

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

def DeleteSegment (g, s):
    newsegments = []
    for d in g.segment:
        if d.name != s:
            newsegments.append(d)
    g.segment = newsegments
    return g

def DeleteNode (g, n):
    newNodes = []
    for d in g.node:
        if d.name != n:
            newNodes.append(d)
    g.node = newNodes
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
        return s, True
    else:
        return False
    
def GetClosest(g, x, y):
    point = Node('p', x, y)
    closest = None
    min_dist = float('inf')
    for n in g.node:
        if n != point:
            d = Distance(n, point)
            if d < min_dist:
                closest = n
                min_dist = d
    return closest

def Plot(g, is_geographic=False, reacMode=False):
    gnodes = []
    gsegments = []
    fig, ax = plt.subplots(figsize=(12, 8))
    current_node = None
    reach_node = None
    last_random_click = None
    
    if is_geographic:
        head_size = 0.05
        node_size = 2
        font_size = 6
        tolerance = 0.02
    else:
        head_size = 0.2
        node_size = 5
        font_size = 8
        tolerance = 0.5
    
    def draw_full_graph():
        ax.clear()
        gnodes.clear()
        gsegments.clear()

        try:
            gnodes.extend(g.node)
            gsegments.extend(g.segment)
        except AttributeError:
            print("Graph does not have 'node' or 'segment' attributes.")
            return
        
        for n in g.node:
            if n == current_node:
                color = 'blue'
            else:
                if n.type == 'airport':
                    color = 'orange'
                else:
                    color = 'green'
            ax.plot(n.x, n.y, 'o', color=color, markersize=node_size)
            ax.text(n.x, n.y, f'{n.name}', fontsize=font_size, color='black',
                   ha='center', va='center')
 
        for s in g.segment:
            dx = s.destination.x - s.origin.x
            dy = s.destination.y - s.origin.y
            distance = (dx**2 + dy**2)**0.5
            
            # Solo mostrar flechas para segmentos suficientemente largos
            if distance > head_size * 3:
                ax.arrow(s.origin.x, s.origin.y, 
                        dx, dy,
                        head_width=head_size, 
                        head_length=head_size*1.5,
                        fc='blue', ec='blue', 
                        linewidth=0.5, 
                        length_includes_head=True,
                        alpha=0.7)
            else:
                ax.plot([s.origin.x, s.destination.x],
                        [s.origin.y, s.destination.y],
                        'b-', linewidth=0.5, alpha=0.7)
            
            midx = (s.origin.x + s.destination.x)/2
            midy = (s.origin.y + s.destination.y)/2
            ax.text(midx, midy, f'{s.cost:.1f}', 
                    fontsize=font_size-1, weight='bold',
                    ha='center', va='center')
        
        ax.grid(color='gray', linestyle='dashed', linewidth=0.3, alpha=0.5)
        ax.set_xlabel("Longitude" if is_geographic else "X")
        ax.set_ylabel("Latitude" if is_geographic else "Y")
        ax.set_title("Airspace Network" if is_geographic else "Graph View")

    def PlotNode(node):
        ax.clear()
        gnodes.clear()
        gsegments.clear()
        
        gnodes.append(node)

        ax.plot(node.x, node.y, 'o', color='red', markersize=node_size*1.5)
        ax.text(node.x, node.y, f'{node.name}', fontsize=font_size+1, 
               color='black', ha='center', va='center', weight='bold')
        
        for s in g.segment:
            if s.origin.name == node.name:
                gsegments.append(s)
                gnodes.append(s.destination)
                c = 'orange' if node.type == 'airport' else 'green'
                ax.plot(s.destination.x, s.destination.y, 'o', 
                       color=c , markersize=node_size)
                ax.text(s.destination.x, s.destination.y, f'{s.destination.name}', 
                       fontsize=font_size, color='black', ha='center', va='center')
                
                dx = s.destination.x - s.origin.x
                dy = s.destination.y - s.origin.y
                ax.arrow(s.origin.x, s.origin.y, 
                        dx, dy,
                        head_width=head_size, 
                        head_length=head_size*1.5,
                        fc='blue', ec='blue', 
                        linewidth=0.5,
                        length_includes_head=True,
                        alpha=0.8)
                
                midx = (s.origin.x + s.destination.x)/2
                midy = (s.origin.y + s.destination.y)/2
                ax.text(midx, midy, f'{s.cost:.1f}', 
                       fontsize=font_size, weight='bold',
                       ha='center', va='center')
        
        for n in g.node:
            if n != node and not any(s.origin == node and s.destination == n for s in g.segment):
                ax.plot(n.x, n.y, 'o', color='gray', markersize=node_size, alpha=0.5)
                ax.text(n.x, n.y, f'{n.name}', fontsize=font_size-1, 
                       color='gray', ha='center', va='center', alpha=0.7)
        
        ax.grid(color='gray', linestyle='dashed', linewidth=0.3, alpha=0.5)
        ax.set_xlabel("Longitude" if is_geographic else "X")
        ax.set_ylabel("Latitude" if is_geographic else "Y")
        ax.set_title(f"Connections from {node.name}")
    
    def PlotReachability(node):
        ax.clear()
        gnodes.clear()
        gsegments.clear()

        lista = Reachability(g, node.name)
        origin = lista[0]
        
        if is_geographic:
            head_size = 0.05
            node_size_main = 5
            node_size_secondary = 3
            font_size = 7
        else:
            head_size = 0.2
            node_size_main = 8
            node_size_secondary = 5
            font_size = 8
        
        for n in g.node:
            if n == origin:
                gnodes.append(n)
                ax.plot(n.x, n.y, 'o', color='red', markersize=node_size_main)
                ax.text(n.x, n.y, f'{n.name}', fontsize=font_size+1, color='black', 
                    ha='center', va='center', weight='bold')
            elif n in lista:
                gnodes.append(n)
                c = 'orange' if n.type == 'airport' else 'green'
                ax.plot(n.x, n.y, 'o', color=c, markersize=node_size_main)
                ax.text(n.x, n.y, f'{n.name}', fontsize=font_size, color='black',
                    ha='center', va='center')
            else:
                ax.plot(n.x, n.y, 'o', color='gray', markersize=node_size_secondary, alpha=0.5)
                ax.text(n.x, n.y, f'{n.name}', fontsize=font_size-1, color='gray',
                    ha='center', va='center', alpha=0.7)
        
        for s in g.segment:
            if s.origin in lista and s.destination in lista:
                gsegments.append(s)
                ax.arrow(s.origin.x, s.origin.y, 
                        s.destination.x - s.origin.x, 
                        s.destination.y - s.origin.y,
                        head_width=head_size, 
                        head_length=head_size*1.5,
                        fc='blue', ec='blue', 
                        linewidth=0.7, 
                        length_includes_head=True,
                        alpha=0.8)
                
                midx = (s.origin.x + s.destination.x)/2
                midy = (s.origin.y + s.destination.y)/2
                ax.text(midx, midy, f'{s.cost:.1f} km', 
                    fontsize=font_size, weight='bold',
                    ha='center', va='center')
            else:
                ax.plot([s.origin.x, s.destination.x],
                    [s.origin.y, s.destination.y],
                    'gray', linewidth=0.3, alpha=0.3)
        
        ax.grid(color='gray', linestyle='dashed', linewidth=0.3, alpha=0.5)
        ax.set_xlabel("Longitude" if is_geographic else "X")
        ax.set_ylabel("Latitude" if is_geographic else "Y")
        ax.set_title(f"Reachable Nodes from {origin.name} (Total: {len(lista)})")

    def PlotShortestPath(origin, destination):
        ax.clear()
        gnodes.clear()
        gsegments.clear()

        if is_geographic:
            node_size_main = 5
            node_size_secondary = 3
            path_width = 1.5
        else:
            node_size_main = 8
            node_size_secondary = 5
            path_width = 2
        
        p = FindShortestPath(g, origin.name, destination.name)

        for n in g.node:
            if n in p.nodes:
                gnodes.append(n)
                c = 'orange' if n.type == 'airport' else 'blue'
                ax.plot(n.x, n.y, 'o', color=c, markersize=node_size_main)
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
                gsegments.append(segment)
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

    def PlotGetClosest(x, y):
        ax.clear()
        gnodes.clear()
        gsegments.clear()

        if is_geographic:
            return

        if is_geographic:
            node_size_main = 5
            node_size_secondary = 3
            path_width = 1.5
        else:
            node_size_main = 8
            node_size_secondary = 5
            path_width = 2
        
        closest = GetClosest(g, x, y)
        gnodes.append(closest)
        gnodes.append(Node('p', x, y))  # Punto de clic
        gsegments.append(Segment('closest', closest, Node('p', x, y)))

        print(closest.name)
        for n in g.node:
            if n == closest:
                ax.plot(n.x, n.y, 'o', color='orange', markersize=node_size_main)
            else:
                ax.plot(n.x, n.y, 'o', color='gray', markersize=node_size_secondary, alpha=0.5)

        ax.plot(x, y, 'x', color='red', markersize=12)  # marcar donde hiciste click

        ax.grid(color='gray', linestyle='dashed', linewidth=0.3, alpha=0.5)
        ax.set_xlabel("Longitude" if is_geographic else "X")
        ax.set_ylabel("Latitude" if is_geographic else "Y")
        ax.set_title(f"Closest Point: {closest.name}")

    def on_click(event):
        nonlocal current_node, reach_node, last_random_click
        if event.xdata is None or event.ydata is None:
            return
        
        clicked_node = None
        min_dist = float('inf')
        
        for n in g.node:
            dx = event.xdata - n.x
            dy = event.ydata - n.y
            dist = dx**2 + dy**2
            if dist < min_dist and dist < tolerance**2:
                min_dist = dist
                clicked_node = n

        if clicked_node:
            last_random_click = None
            if reacMode:
                if reach_node is None:
                    reach_node = clicked_node
                    current_node = clicked_node
                    PlotReachability(reach_node)
                elif clicked_node == reach_node:
                    reach_node = None
                    current_node = None
                    draw_full_graph()
                elif clicked_node == current_node:
                    current_node = reach_node
                    PlotReachability(reach_node)
                else:
                    try:
                        PlotShortestPath(reach_node, clicked_node)
                        current_node = clicked_node
                    except Exception as e:
                        draw_full_graph()
                        current_node = None
                        reach_node = None
            else:
                if current_node == clicked_node:
                    current_node = None
                    draw_full_graph()
                else:
                    current_node = clicked_node
                    PlotNode(current_node)
        else:
            if not is_geographic and not reacMode:
                if last_random_click is None:
                    last_random_click = (event.xdata, event.ydata)
                    PlotGetClosest(event.xdata, event.ydata)
                else:
                    last_random_click = None
                    draw_full_graph()
        fig.canvas.draw()

    draw_full_graph()
    fig.canvas.mpl_connect('button_press_event', on_click)
    
    return fig, gnodes, gsegments

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
    return Plot(g)

def NewGraph(g):
    g.node.clear()
    g.segment.clear()
    return g

def SaveGraph(g, fileName):
    X = open(fileName, 'w')
    X.write('Nodes:\n')
    for n in g.node:
        X.write(f'{n.name} {n.x} {n.y}\n')
    X.write('Segments:\n')
    for s in g.segment:
        X.write(f'{s.name} {s.origin.name} {s.destination.name}\n')
    print('Graph saved successfully.')

def Reachability(g, startNodeName):
    start_node = None
    for n in g.node:
        if n.name == startNodeName:
            start_node = n
            break
    print(f'Start node: {start_node.name}')
    lista = [start_node]
    i = 0
    
    while i < len(lista):
        actual = lista[i]
        for vecino in actual.neighbors:
            # aqui miro si el vecino ya esta en la lista esa
            finalizado = False
            for nodo in lista:
                if nodo == vecino:
                    finalizado = True
                    break
            
            if not finalizado:
                for s in g.segment:
                    if s.origin == actual and s.destination == vecino:
                        lista.append(vecino)
                        print(f'Adding segment: {s.name}')
                        break
        i += 1
    return lista

def FindShortestPath (g, originName, destinationName):
    alcanzables = Reachability(g, originName)
    destination = None
    origin = None
    for n in g.node:
        if n.name == destinationName:
            destination = n
        if n.name == originName:
            origin = n
        if destination and origin:
            break
    if destination not in alcanzables:
        return None
    
    caminos_posibles = [[origin]]
    costes_acumulados = [0.0]
    while caminos_posibles: #mientras haya caminos posibles dentro de la lista esa...
        menor_coste = costes_acumulados[0]
        index_menor = 0
        i = 0
        while i < len(caminos_posibles): #aqui miro cual es el camino mas corto
            if costes_acumulados[i] < menor_coste:
                menor_coste = costes_acumulados[i]
                index_menor = i
            i += 1
        
        camino_actual = caminos_posibles.pop(index_menor)
        coste_actual = costes_acumulados.pop(index_menor)
        ultimo_nodo = camino_actual[-1]

        if ultimo_nodo == destination: #aqui es donde acaba ya toda la funcion
            path_resultado = Path(origin)
            for node in camino_actual[1:]:
                last = path_resultado.nodes[-1]
                path_resultado.cost += round(Distance(last, node), 2)
                path_resultado.nodes.append(node)
            return path_resultado
        
        for vecino in ultimo_nodo.neighbors: #aqui mira los vecinos del ultimo nodo
            vecino_en_camino = False
            for node in camino_actual: #esto es para ver si el vecino ya esta en la lista de caminos o no y no volver a añadirlo
                if node == vecino:
                    vecino_en_camino = True
                    break
            
            if not vecino_en_camino: #aqui es donde añado los nodos y el cost nuevos para volver al bucle
                coste_segmento = 0
                for segment in g.segment:
                    if segment.origin == ultimo_nodo and segment.destination == vecino:
                        coste_segmento = segment.cost
                        break
                if coste_segmento > 0:
                    nuevo_camino = camino_actual.copy() #con el .copy() hago una copia del camino actual y no lo modifico
                    nuevo_camino.append(vecino)
                    caminos_posibles.append(nuevo_camino)
                    costes_acumulados.append(coste_actual + coste_segmento)
    return None

