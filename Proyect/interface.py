import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import matplotlib as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from node import *
from segment import *
from graph import *
from path import *
from airSpace import *


def ExampleGraph ():
    G= Graph()
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
G = ExampleGraph()
g = Graph()

def InterfaceGraph():
    canvas_widget = None
    current_graph = None

    def show_example():
        nonlocal canvas_widget
        nonlocal current_graph

        current_graph = ExampleGraph()

        if canvas_widget:
            canvas_widget.destroy()
        
        fig = Plot(current_graph)  # Usa la nueva función Plot
        canvas = FigureCanvasTkAgg(fig, master=right_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
    
    def load_file():
        nonlocal current_graph
        nonlocal canvas_widget

        file_name = simpledialog.askstring('Load File', 'File Name:')
        current_graph = PlotFile(file_name)
        if Graph:
            if canvas_widget:
                canvas_widget.destroy()
        
            fig = Plot(current_graph)  # Usa la nueva función Plot
            canvas = FigureCanvasTkAgg(fig, master=right_frame)
            canvas.draw()
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True)
        else:
            messagebox.showwarning("Error", "File not found or invalid format.")
        return None
    
    def loadCat():
        nonlocal current_graph
        nonlocal canvas_widget

        a = LoadAirlineData('Cat_nav.txt', 'Cat_seg.txt', 'Cat_aer.txt')
        g = GetGraph(a)
        current_graph = g
        if Graph:
            if canvas_widget:
                canvas_widget.destroy()
        
            fig = Plot(current_graph, is_geographic=True)
            canvas = FigureCanvasTkAgg(fig, master=right_frame)
            canvas.draw()
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True)
        else:
            messagebox.showwarning("Error", "File not found or invalid format.")
        return None
    
    def save_file():
        nonlocal current_graph
        file_name = simpledialog.askstring('Save File', 'File Name:')
        if file_name:
            SaveGraph(current_graph, file_name)
            messagebox.showinfo("Success", "Graph saved successfully.")
        return None
    
    def add_node_button():
        nonlocal current_graph
        nonlocal canvas_widget
        nonlocal entry 

        if current_graph:
            repeated = False
            information = list(entry.get().split(' '))
            for nodeingraph in current_graph.node:
                if nodeingraph.name == information[0]:
                    repeated = True
                    break
            if repeated:
                messagebox.showwarning('ERROR', 'It already exist a node with that name.')
            else:
                x = float(information[1])
                y = float(information[2])
                info_node = Node(information[0], x, y)
                AddNode(current_graph, info_node)
                if canvas_widget:
                    canvas_widget.destroy()
                canvas = FigureCanvasTkAgg(Plot(current_graph), master = right_frame)            
                canvas.draw()
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=tk.BOTH, expand=True)
        else:
            current_graph = Graph()
            repeated = False
            information = list(entry.get().split(' '))
            for nodeingraph in current_graph.node:
                if nodeingraph.name == information[0]:
                    repeated = True
                    break
            if repeated:
                messagebox.showwarning('ERROR', 'It already exist a node with that name.')
            else:
                info_node = Node(information[0], information[1], information[2])
                AddNode(current_graph, info_node)
                if canvas_widget:
                    canvas_widget.destroy()
                canvas = FigureCanvasTkAgg(Plot(current_graph), master = right_frame)            
                canvas.draw()
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=tk.BOTH, expand=True)

    def del_node_button():
        nonlocal current_graph
        nonlocal canvas_widget
        nonlocal entry

        if current_graph:
            information = entry.get()
            delete_segments = []
            found = False
            try:
                for nodeingraph in current_graph.node:
                    if nodeingraph.name == information:
                        for segment in current_graph.segment:
                            if segment.destination == nodeingraph or segment.origin == nodeingraph:
                                delete_segments.append(segment.name)
                        for to_delete in delete_segments:
                            DeleteSegment(current_graph, to_delete)

                        DeleteNode(current_graph, nodeingraph)
                        if canvas_widget:
                            canvas_widget.destroy()
                        canvas = FigureCanvasTkAgg(Plot(current_graph), master = right_frame)
                        canvas.draw()
                        canvas_widget = canvas.get_tk_widget()
                        canvas_widget.pack(fill=tk.BOTH, expand=True)
                        found = True
                        break
            except:
                messagebox.showwarning("Error", "Node not found.")
        else:
            messagebox.showwarning("Error", "No graph loaded.")

    def add_segment_button():
        nonlocal current_graph
        nonlocal canvas_widget
        nonlocal entry

        if current_graph:
            repeated = False
            information = list(entry.get().split(" "))
            for segmentingraph in current_graph.segment:
                if segmentingraph.name == information[0]:
                    repeated = True
                    break
            if repeated:
                messagebox.showwarning('ERROR', 'It already exist a segment with that name.')
            else:
                try:
                    founded_node1 = None
                    founded_node2 = None
                    for nodeingraph in current_graph.node:
                        if nodeingraph.name == information[1]:
                            founded_node1 = nodeingraph
                        if nodeingraph.name == information[2]:
                            founded_node2 = nodeingraph
                    if founded_node1 and founded_node2:
                        infosegment = Segment(information[0], founded_node1, founded_node2)
                        AddSegment(current_graph, information[0], founded_node1.name, founded_node2.name)
                        if canvas_widget:
                            canvas_widget.destroy()
                        canvas = FigureCanvasTkAgg(Plot(current_graph), master = right_frame)
                        canvas.draw()
                        canvas_widget = canvas.get_tk_widget()
                        canvas_widget.pack(fill=tk.BOTH, expand=True)
                    else:
                        messagebox.showwarning("Error", "Node not found.")
                except:
                    messagebox.showwarning("Error", "Invalid segment information.")
        else:
            messagebox.showwarning("Error", "No graph loaded.")
    
    def del_segment_button():
        nonlocal current_graph
        nonlocal canvas_widget
        nonlocal entry
        found = False

        if current_graph:
            information = entry.get()
            for segmentingraph in current_graph.segment:
                if segmentingraph.name == information:
                    found = True
            
            if found:
                DeleteSegment(current_graph, information)
                if canvas_widget:
                    canvas_widget.destroy()
                canvas = FigureCanvasTkAgg(Plot(current_graph), master = right_frame)
                canvas.draw()
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=tk.BOTH, expand=True)
            else:
                messagebox.showwarning('ERROR', 'It doesn\'t exist a segment with that name.')
        else:
            messagebox.showwarning("Error", "No graph loaded.")
    
    def new_fuction():
        nonlocal current_graph
        nonlocal new_entry
        nonlocal canvas_widget

        information = int(new_entry.get())
        if current_graph:
            if information > 0:
                current_graph = Graph()
                for i in range(information):
                    node = Node(str(i), np.random.randint(1, 20), np.random.randint(1, 20))
                    AddNode(current_graph, node)
                if canvas_widget:
                    canvas_widget.destroy()
                canvas = FigureCanvasTkAgg(Plot(current_graph), master = right_frame)
                canvas.draw()
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=tk.BOTH, expand=True)
            else:
                messagebox.showwarning("Error", "Invalid number of nodes.")
        else:
            messagebox.showwarning("Error", "No graph loaded.")
    
    def reachability_g():
        nonlocal current_graph
        nonlocal canvas_widget
        
        if not current_graph:
            messagebox.showwarning("Error", "There is no graph loaded.")
            return
        
        origin = simpledialog.askstring('Origin', 'Origin Node:')
        if not origin:
            return
   
        origin_node = None
        for n in current_graph.node:
            if n.name == origin:
                origin_node = n
                break
        
        if not origin_node:
            messagebox.showwarning("Error", f"Node '{origin}' not found.")
            return

        reachable_nodes = Reachability(current_graph, origin)
        
        fig = PlotReachability(current_graph, reachable_nodes)
        
        if canvas_widget:
            canvas_widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig, master=right_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        return None
            
    def generalview():
        nonlocal current_graph
        nonlocal canvas_widget

        if current_graph:
            if canvas_widget:
                canvas_widget.destroy()
            canvas = FigureCanvasTkAgg(Plot(current_graph), master= right_frame)
            canvas.draw()
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True)
        else:
            messagebox.showwarning("Error", "No graph loaded.")
        return None

    def findshortestpath_g():
        nonlocal current_graph
        nonlocal canvas_widget
        
        origin = simpledialog.askstring('Origin', 'Origin Node:')
        destination = simpledialog.askstring('Destination', 'Destination Node:')
        current_path = FindShortestPath(current_graph, origin, destination)
        if current_path:
            current_graph = PlotPath(current_graph, current_path)
            if Graph:
                if canvas_widget:
                    canvas_widget.destroy()
                canvas = FigureCanvasTkAgg(current_graph, master= right_frame)
                canvas.draw()
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=tk.BOTH, expand=True)
        else: 
            messagebox.showwarning("Error", "File not found or invalid format.")
        return None

    def reachability_a():
        nonlocal current_graph
        nonlocal canvas_widget
        
        if not current_graph:
            messagebox.showwarning("Error", "There is no graph loaded.")
            return
        
        origin = simpledialog.askstring('Origin', 'Origin Node:')
        if not origin:
            return
   
        origin_node = None
        for n in current_graph.node:
            if n.name == origin:
                origin_node = n
                break
        
        if not origin_node:
            messagebox.showwarning("Error", f"Node '{origin}' not found.")
            return

        reachable_nodes = Reachability(current_graph, origin)
        
        fig = PlotReachability(current_graph, reachable_nodes, is_geographic=True)
        
        if canvas_widget:
            canvas_widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig, master=right_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        return None
    
    def findshortestpath_a():
        nonlocal current_graph
        nonlocal canvas_widget
        
        origin = simpledialog.askstring('Origin', 'Origin Node:')
        destination = simpledialog.askstring('Destination', 'Destination Node:')
        current_path = FindShortestPath(current_graph, origin, destination)
        if current_path:
            current_graph = PlotPath(current_graph, current_path, is_geographic=True)
            if Graph:
                if canvas_widget:
                    canvas_widget.destroy()
                canvas = FigureCanvasTkAgg(current_graph, master= right_frame)
                canvas.draw()
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=tk.BOTH, expand=True)
        else: 
            messagebox.showwarning("Error", "File not found or invalid format.")
        return None
    ####### base ######
    root = tk.Tk()
    root.geometry('1200x800')
    root.title('Interface')
    
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=3)

    notebook_frame = ttk.Frame(root)
    notebook_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    right_frame = tk.LabelFrame(root, text = 'Graph:')
    right_frame.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    right_frame.grid_propagate(True)

    right_frame.columnconfigure(0, weight=1)
    right_frame.rowconfigure(0, weight=1)

    notebook = ttk.Notebook(notebook_frame)
    notebook.pack(expand=True, fill='both')

    ######################################################
    ##### Pestaña 1: interfaz original con graficos######
    ######################################################

    pest1 = ttk.Frame(notebook)
    notebook.add(pest1, text="Graph Interface")

    left_frame_p1 = ttk.Frame(pest1)
    left_frame_p1.pack(expand=True, fill='both')

    left_frame_p1.columnconfigure(0, weight=1)
    left_frame_p1.rowconfigure(0, weight=1)
    left_frame_p1.rowconfigure(1, weight=1)
    left_frame_p1.rowconfigure(2, weight=2)
    left_frame_p1.rowconfigure(3, weight=2)
    left_frame_p1.rowconfigure(4, weight=2)

    #EXAMPLE BUTTON
    randomframe = tk.LabelFrame(left_frame_p1)
    randomframe.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    randomframe.columnconfigure(0, weight=1)
    randomframe.columnconfigure(1, weight=1)

    examplebutton = tk.Button(randomframe, text='Example', command=lambda: show_example())
    examplebutton.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    generalviewbutton = tk.Button(randomframe, text='General View', command=lambda: generalview())
    generalviewbutton.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    #PATH BUTTON
    pathframe = tk.LabelFrame(left_frame_p1, text = 'Path')
    pathframe.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    pathframe.columnconfigure(0, weight=1)
    pathframe.columnconfigure(1, weight=1)

    reachabilitybutton = tk.Button(pathframe, text='Reachability', command=lambda: reachability_g())
    reachabilitybutton.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    shortestpathbutton = tk.Button(pathframe, text='Shortest Path', command=lambda: findshortestpath_g())
    shortestpathbutton.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    #FILES BUTTONS
    filesframe = tk.LabelFrame(left_frame_p1, text = 'Files')
    filesframe.grid(row=2, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    filesframe.columnconfigure(0, weight=1)
    filesframe.rowconfigure(0, weight=1)
    filesframe.rowconfigure(1, weight=1)

    uploadbutton = tk.Button(filesframe, text='Load', command=lambda: load_file())
    uploadbutton.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    savebutton = tk.Button(filesframe, text='Save', command=lambda: save_file())
    savebutton.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    #EDIT BUTTONS
    editframe = tk.LabelFrame(left_frame_p1, text = 'Edit')
    editframe.grid(row=3, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    editframe.columnconfigure(0, weight=1)
    editframe.columnconfigure(1, weight=1)
    editframe.rowconfigure(0, weight=1)
    editframe.rowconfigure(1, weight=1)
    editframe.rowconfigure(2, weight=2)

    addnodebutton = tk.Button(editframe, text='Add Node', command=lambda: add_node_button())
    addnodebutton.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    delnodebutton = tk.Button(editframe, text='Delete Node', command=lambda: del_node_button())
    delnodebutton.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    addsegmentbutton = tk.Button(editframe, text='Add Segment', command=lambda: add_segment_button())
    addsegmentbutton.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    delsegmentbutton = tk.Button(editframe, text='Delete Segment', command=lambda: del_segment_button())
    delsegmentbutton.grid(row=1, column=1, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    entry = tk.Entry(editframe)
    entry.grid(row=2, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    #NEW FUNCTION BUTTON
    newframe = tk.LabelFrame(left_frame_p1, text = 'New Function')
    newframe.grid(row=4, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    newframe.columnconfigure(0, weight=1)
    newframe.rowconfigure(0, weight=1)
    newframe.rowconfigure(1, weight=1)

    newbutton = tk.Button(newframe, text='New Graph', command=lambda: new_fuction())
    newbutton.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    new_entry = tk.Entry(newframe)
    new_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    ######################################################
    ##### Pestaña 2: interfaz con nodos de cat, esp, eu###
    ######################################################

    pest2 = ttk.Frame(notebook)
    notebook.add(pest2, text="Airspace Interface")

    left_frame_p2 = ttk.Frame(pest2)
    left_frame_p2.pack(expand=True, fill='both')

    left_frame_p2.columnconfigure(0, weight=1)
    left_frame_p2.rowconfigure(0, weight=1)
    left_frame_p2.rowconfigure(1, weight=3)

    #Path buttons
    pathframe = tk.LabelFrame(left_frame_p2, text = 'Path')
    pathframe.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    pathframe.columnconfigure(0, weight=1)
    pathframe.columnconfigure(1, weight=1)

    reachabilitybutton = tk.Button(pathframe, text='Reachability', command=lambda: reachability_a())
    reachabilitybutton.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    shortestpathbutton = tk.Button(pathframe, text='Shortest Path', command=lambda: findshortestpath_a())
    shortestpathbutton.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    #Files buttons
    filesframe = tk.LabelFrame(left_frame_p2, text = 'Files')
    filesframe.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    
    filesframe.columnconfigure(0, weight=1)
    filesframe.rowconfigure(0, weight=1)
    filesframe.rowconfigure(1, weight=1)
    filesframe.rowconfigure(2, weight=1)

    catbutton = tk.Button(filesframe, text='Load Cat', command=lambda: loadCat())
    catbutton.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    espbutton = tk.Button(filesframe, text='Load Esp', command=lambda: messagebox.showwarning("Error", "Not implemented yet."))
    espbutton.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    eubutton = tk.Button(filesframe, text='Load Eu', command=lambda: messagebox.showwarning("Error", "Not implemented yet."))
    eubutton.grid(row=2, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    root.mainloop()
InterfaceGraph()