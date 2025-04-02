import tkinter as tk
from tkinter import messagebox
import matplotlib as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from node import *
from segment import *
from graph import *

def ExampleGraph ():
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
 AddSegment(G, "AB","A","B")
 AddSegment(G, "AE","A","E")
 AddSegment(G, "AK","A","K")
 AddSegment(G, "BA","B","A")
 AddSegment(G, "BC","B","C")
 AddSegment(G, "BF","B","F")
 AddSegment(G, "BK","B","K")
 AddSegment(G, "BG","B","G")
 AddSegment(G, "CD","C","D")
 AddSegment(G, "CG","C","G")
 AddSegment(G, "DG","D","G")
 AddSegment(G, "DH","D","H")
 AddSegment(G, "DI","D","I")
 AddSegment(G, "EF","E","F")
 AddSegment(G, "FL","F","L")
 AddSegment(G, "GB","G","B")
 AddSegment(G, "GF","G","F")
 AddSegment(G, "GH","G","H")
 AddSegment(G, "ID","I","D")
 AddSegment(G, "IJ","I","J")
 AddSegment(G, "JI","J","I")
 AddSegment(G, "KA","K","A")
 AddSegment(G, "KL","K","L")
 AddSegment(G, "LK","L","K")
 AddSegment(G, "LF","L","F")
 return G
G = ExampleGraph()


def InterfaceGraph():
    ####### base ######
    root = tk.Tk()
    root.geometry('600x300')
    root.title('Interface')
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=3)
    root.rowconfigure(2, weight=3)
    # Select
    select_frame = tk.LabelFrame(root, text = 'Select:')
    select_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    select_frame.rowconfigure(0, weight=1)
    select_frame.rowconfigure(1, weight=1)
    select_frame.columnconfigure(0, weight=1)
    select_frame.columnconfigure(1, weight=1)
    select_frame.columnconfigure(2, weight=1)

    tk.Label(select_frame, text="File Path:").grid(row=0, column=0, sticky=tk.W, padx=5)
    tk.Label(select_frame, text="Node:").grid(row=0, column=1, sticky=tk.W, padx=5)
    tk.Label(select_frame, text="Segment:").grid(row=0, column=2, sticky=tk.W, padx=5)

    entryFile = tk.Entry(select_frame)
    entryFile.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    entryNode = tk.Entry(select_frame)
    entryNode.grid(row=1, column=1, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    entrySelect = tk.Entry(select_frame)
    entrySelect.grid(row=1, column=2, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    # example graph
    example_graph_frame = tk.LabelFrame(root, text = 'Example Graph')
    example_graph_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    example_graph_frame.rowconfigure(0, weight=1)
    example_graph_frame.columnconfigure(0, weight=1)
    example_graph_frame.columnconfigure(1, weight=1)

    button1 = tk.Button(example_graph_frame, text = 'Show Example Graph', command=lambda: Plot(G))
    button1.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    button2 = tk.Button(example_graph_frame, text = 'Show Example Node Neighbors', command=lambda: PlotNode(G, 'C'))
    button2.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    # Load Graph
    load_graph_frame = tk.LabelFrame(root, text = 'Load Graph')
    load_graph_frame.grid(row=1, rowspan=2, column=2, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    
    load_graph_frame.rowconfigure(0, weight=1)
    load_graph_frame.rowconfigure(1, weight=1)
    load_graph_frame.columnconfigure(0, weight=1)
    load_graph_frame.columnconfigure(1, weight=1)

    LoadGraph = tk.Button(load_graph_frame, text = 'Load Graph from File', command=lambda: PlotFile(entryFile.get()))
    LoadGraph.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    GraphNode = tk.Button(load_graph_frame, text = 'Show Node Neighbors', command=lambda: PlotNode(LoadFile(entryFile.get()), entryNode.get()))
    GraphNode.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    GraphNode = tk.Button(load_graph_frame, text = 'New Graph', command=lambda: PlotFile(entryNode.get()))
    GraphNode.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    GraphNode = tk.Button(load_graph_frame, text = 'Save Graph', command=lambda: SaveGraph(LoadFile(entryFile.get())))
    GraphNode.grid(row=1, column=1, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    #Select Node
    select_node_frame = tk.LabelFrame(root, text = 'Select Node')
    select_node_frame.grid(row=2, column=1, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    
    select_node_frame.rowconfigure(0, weight=1)
    select_node_frame.rowconfigure(1, weight=1)
    select_node_frame.columnconfigure(0, weight=1)

    entry2 = tk.Entry(select_node_frame)
    entry2.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    button4 = tk.Button(select_node_frame, text = 'Plot', command=lambda: PlotNode(PlotFile(entry1.get()), entry2.get()))
    button4.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    root.mainloop()

InterfaceGraph()