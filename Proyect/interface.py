import tkinter as tk
from tkinter import simpledialog, messagebox, ttk, colorchooser, Toplevel
import matplotlib as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import pygame

from node import *
from segment import *
from graph import *
from path import *
from airSpace import *
from KML import *


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
    knodes = []
    ksegments = []
    canvas_widget = None
    current_graph = None
    reacMode = False
    global texto_var
    import tkinter as tk

    class Tooltip: #####aquesta clase sirve para que al pasar sobre un boton pues salga un texto y tal
        def __init__(self, widget, text):
            self.widget = widget
            self.text = text
            self.tip_window = None
            widget.bind("<Enter>", self.show_tip) #que se muestre
            widget.bind("<Leave>", self.hide_tip)

        def show_tip(self, event=None):
            if self.tip_window or not self.text:
                return
            x = self.widget.winfo_rootx() + 20
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5 #la posicion de donde se mostrara
            self.tip_window = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)  # sin bordes
            tw.wm_geometry(f"+{x}+{y}")
            label = tk.Label(tw, text=self.text, background="#ffffe0", relief="solid", borderwidth=1, font=("Segoe UI", 9))
            label.pack(ipadx=4, ipady=2)

        def hide_tip(self, event=None):
            tw = self.tip_window
            if tw:
                tw.destroy()
            self.tip_window = None

    def export_to_kml():
        nonlocal current_graph, knodes, ksegments
        if knodes and ksegments:
            file_name = simpledialog.askstring('Save File', 'How do you want to save the KML file?')
            if file_name:
                GraphToKML(knodes, ksegments, filename=f'{file_name}.kml')
            else:
                return
            abrir = messagebox.askyesno("Success", "Graph exported to KML successfully.\n Do you want to open the file in Google Earth now?")
            if abrir:
                try:
                    sound('googleearth')
                    os.startfile(f'{file_name}.kml')
                except Exception as e:
                    messagebox.showerror("Error", f"Could not open the file:\n{e}")
        else:
            messagebox.showwarning("Error", "No graph loaded or graph is empty.")
    
    def refresh_plot(current_graph, reacMode=False, is_geographic=False):
        nonlocal canvas_widget, knodes, ksegments
        if canvas_widget:
            canvas_widget.destroy()

        fig, gnodes, gsegments = Plot(current_graph, reacMode=reacMode, is_geographic=is_geographic)
        knodes = gnodes
        ksegments = gsegments

        canvas = FigureCanvasTkAgg(fig, master=right_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        right_frame.pack_propagate(False)

        # aqui se obtienen los ejes
        ax = fig.axes[0]

        # variables del estado 
        state = {'press': None, 'x0': 0, 'y0': 0}

        def on_scroll(event):
            if event.inaxes:
                scale_factor = 1 / 1.2 if event.step > 0 else 1.2
                xlim = ax.get_xlim()
                ylim = ax.get_ylim()
                xdata = event.xdata
                ydata = event.ydata
                new_xlim = [xdata + (x - xdata) * scale_factor for x in xlim]
                new_ylim = [ydata + (y - ydata) * scale_factor for y in ylim]
                ax.set_xlim(new_xlim)
                ax.set_ylim(new_ylim)
                canvas.draw()

        def on_press(event):
            print(f"Pressed button: {event.button}")
            if event.button == 3 and event.inaxes: # boton derecho
                state['press'] = True
                state['x0'] = event.x
                state['y0'] = event.y

        def on_release(event):
            if event.button == 3:
                state['press'] = None
                state['x0'] = None
                state['y0'] = None

        def on_motion(event):
            if state['press'] and event.button == 3 and event.inaxes:
                dx = event.x - state['x0']
                dy = event.y - state['y0']
                state['x0'], state['y0'] = event.x, event.y

                xlim = ax.get_xlim()
                ylim = ax.get_ylim()

                width = canvas.get_tk_widget().winfo_width()
                height = canvas.get_tk_widget().winfo_height()
                #conversion a coordenadas de datos
                dx_data = dx * (xlim[1] - xlim[0]) / width
                dy_data = dy * (ylim[1] - ylim[0]) / height
                ax.set_xlim([x - dx_data for x in xlim])
                ax.set_ylim([y + dy_data for y in ylim])  # nota el signo
                canvas.draw()

        # aqui se conectanlos eventos
        canvas.mpl_connect("scroll_event", on_scroll)
        canvas.mpl_connect("button_press_event", on_press)
        canvas.mpl_connect("button_release_event", on_release)
        canvas.mpl_connect("motion_notify_event", on_motion)

    def resetview(current_graph):
        tabindex = notebook.index(notebook.select())
        if tabindex == 0:
            # estem en la pestaña dels graphs
            refresh_plot(current_graph, reacMode=reacMode, is_geographic=False)
        elif tabindex == 1:
            # l'altre pestaña dels avioncitos
            refresh_plot(current_graph, reacMode=reacMode, is_geographic=True)

    def set_reachability_mode_g():
        nonlocal reacMode, canvas_widget, current_graph
        reacMode = not reacMode
        if reacMode == True:
            texto_var.set("Click on a node to see its reachability.\nClick on another node to find the shortest path between them.")
        elif reacMode == False:
            texto_var.set("Click on a node to see its neighbors.\nClick on any point in the graph to find its closest node.")
        if current_graph:
            refresh_plot(current_graph, reacMode=reacMode)

    def set_reachability_mode_a():
        nonlocal reacMode, canvas_widget, current_graph
        reacMode = not reacMode
        if reacMode == True:
            texto_var.set("Click on a node to see its reachability.\nClick on another node to find the shortest path between them.")
        elif reacMode == False:
            texto_var.set("Click on a node to see its neighbors.\nClick on any point in the graph to find its closest node.")
        if current_graph:
            refresh_plot(current_graph, reacMode=reacMode, is_geographic=True)
    
    def show_example():
        nonlocal canvas_widget
        nonlocal current_graph

        current_graph = ExampleGraph()
        texto_var.set("Click on a node to see its neighbors.\nClick on any point in the graph to find its closest node.")
        refresh_plot(current_graph)
        sound('graf')
    
    def load_file():
        nonlocal current_graph
        nonlocal canvas_widget
        texto_var.set("Click on a node to see its neighbors.\nClick on any point in the graph to find its closest node.")
        file_name = simpledialog.askstring('Load File', 'File Name:')
        current_graph = LoadFile(file_name)
        if current_graph:
            refresh_plot(current_graph)
            sound('graf')
        else:
            sound('error')
            messagebox.showwarning("Error", "File not found or invalid format.")
        return None
    
    def loadCat():
        nonlocal current_graph
        nonlocal canvas_widget

        a = LoadAirlineData('cat/Cat_nav.txt', 'cat/Cat_seg.txt', 'cat/Cat_aer.txt')
        g = GetGraph(a)
        current_graph = g
        texto_var.set("This is the airspace of Catalonia!!!1! :D\nClick on a node to see its neighbors.")
        if current_graph:
            refresh_plot(current_graph, is_geographic=True)
            sound('graf')
        else:
            sound('error')
            messagebox.showwarning("Error", "File not found or invalid format.")
        return None
    
    def loadEu():
        nonlocal current_graph
        nonlocal canvas_widget

        a = LoadAirlineData('eu/ECAC_nav.txt', 'eu/ECAC_seg.txt', 'eu/ECAC_aer.txt')
        g = GetGraph(a)
        current_graph = g
        texto_var.set("This is the airspace of Europe!!!1! :D\nClick on a node to see its neighbors.")
        if current_graph:
            refresh_plot(current_graph, is_geographic=True)
            sound('graf')
        else:
            sound('error')
            messagebox.showwarning("Error", "File not found or invalid format.")
        return None
    
    def loadEsp():
        nonlocal current_graph
        nonlocal canvas_widget

        a = LoadAirlineData('spain/Spain_nav.txt', 'spain/Spain_seg.txt', 'spain/Spain_aer.txt')
        g = GetGraph(a)
        current_graph = g
        texto_var.set("This is the airspace of Spain!!!1! :D\nClick on a node to see its neighbors.")
        if current_graph:
            refresh_plot(current_graph, is_geographic=True)
            sound('graf')
        else:
            sound('error')
            messagebox.showwarning("Error", "File not found or invalid format.")
        return None
    
    def save_file():
        nonlocal current_graph
        file_name = simpledialog.askstring('Save File', 'How do you want to save the graph?')
        if file_name:
            SaveGraph(current_graph, fileName=f'{file_name}.txt')
            messagebox.showinfo("Success", "Graph saved successfully.")
            sound('create')
        return None
    
    def add_node_button():
        nonlocal current_graph
        nonlocal canvas_widget
        nonlocal entry 

        if current_graph:
            repeated = False
            information = list(entry.get().split(' '))
            if len(information) != 3:
                messagebox.showwarning('ERROR', 'Wrong format!')

            for nodeingraph in current_graph.node:
                if nodeingraph.name == information[0]:
                    repeated = True
                    break
            if repeated:
                sound('error')
                messagebox.showwarning('ERROR', 'It already exist a node with that name.')
            else:
                x = float(information[1])
                y = float(information[2])
                info_node = Node(information[0], x, y)
                AddNode(current_graph, info_node)
                sound('create')
                refresh_plot(current_graph)
        else:
            current_graph = Graph()
            repeated = False
            information = list(entry.get().split(' '))
            for nodeingraph in current_graph.node:
                if nodeingraph.name == information[0]:
                    repeated = True
                    break
            if repeated:
                sound('error')
                messagebox.showwarning('ERROR', 'It already exist a node with that name.')
            else:
                info_node = Node(information[0], information[1], information[2])
                AddNode(current_graph, info_node)
                sound('create')
                refresh_plot(current_graph)

    def del_node_button():
        nonlocal current_graph
        nonlocal canvas_widget
        nonlocal entry

        if current_graph:
            information = entry.get()
            delete_segments = []
            node_found = False

            for nodeingraph in current_graph.node:
                if nodeingraph.name == information:
                    node_found = True
                    for segment in current_graph.segment:
                        if segment.destination == nodeingraph or segment.origin == nodeingraph:
                            delete_segments.append(segment.name)
                    for to_delete in delete_segments:
                        DeleteSegment(current_graph, to_delete)

                    DeleteNode(current_graph, information)
                    sound('delete')
                    refresh_plot(current_graph)
                    break
            if not node_found:
                sound('error')
                messagebox.showwarning("Error", "Node not found.")
        else:
            sound('error')
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
                sound('error')
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
                        sound('create')
                        AddSegment(current_graph, information[0], founded_node1.name, founded_node2.name)
                        refresh_plot(current_graph)
                    else:
                        sound('error')
                        messagebox.showwarning("Error", "Node not found.")
                except:
                    sound('error')
                    messagebox.showwarning("Error", "Invalid segment information.")
        else:
            sound('error')
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
                sound('delete')
                refresh_plot(current_graph)
            else:
                sound('error')
                messagebox.showwarning('ERROR', 'It doesn\'t exist a segment with that name.')
        else:
            sound('error')
            messagebox.showwarning("Error", "No graph loaded.")
    
    def new_graph():
        nonlocal canvas_widget
        nonlocal current_graph

        current_graph = NewGraph(current_graph)
        sound('niidea')
        refresh_plot(current_graph)

    def superdevelopers():
        popup = Toplevel()
        popup.title("Super Developers")
        popup.configure(bg="white")

        imagen = Image.open("imagenes/Grup 10.png")
        imagen = imagen.resize((800, 400))
        sound('rickroll')
        foto = ImageTk.PhotoImage(imagen)

        label = tk.Label(popup, image=foto, bg="white")
        label.image = foto  # guardar referencia para evitar que se borre
        label.pack(padx=10, pady=10)
    
    # sound functions

    BG = True
    EF = True 
    def sound(sound_name):
        nonlocal BG, EF
        ef = {
            'rickroll' : pygame.mixer.Sound('sonidos/Rick roll.mp3'),
            'create' : pygame.mixer.Sound('sonidos/victory.mp3'),
            'delete' : pygame.mixer.Sound('sonidos/eliminarnodo.mp3'),
            'pestaña' : pygame.mixer.Sound('sonidos/cambiarpestañaa.mp3'),
            'error': pygame.mixer.Sound('sonidos/windows error.mp3'),
            'graf': pygame.mixer.Sound('sonidos/Windows startup.mp3'),
            'niidea': pygame.mixer.Sound('sonidos/G2.mp3'),
            'googleearth': pygame.mixer.Sound('sonidos/outro music free (no copyright).mp3')
        }

        bg = {
            'background': "sonidos/wii.mp3"
        }

        if sound_name == 'background':
            if BG:
                pygame.mixer.music.load(bg[sound_name])
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)  # -1 = bucle infinito
            else:
                pygame.mixer.music.stop()
        else:
            if EF:
                ef[sound_name].play()
    
    def toggle_sound(sound_name = None):
        nonlocal BG, EF
        if sound_name == 'background':
            BG = not BG
            sound(sound_name)
        elif sound_name == None:
            EF = not EF
    
    ### colorinchis ###

    THEMES = {
        "Verdecito": { "bg": "#d7f0f2", "button_bg": "#A3D4C9", "button_fg": "#2E4A62" },
        "Rosita": { "bg": "#FFE4E1", "button_bg": "#FFB6C1", "button_fg": "#8B0000" },
        "Personalizado": {}  # lo rellenaremos con colorchooser
    }
    def apply_theme_to_all_widgets(root, theme: dict):
        bg = theme.get("bg", "#ffffff")
        fg = theme.get("button_fg", "#000000")
        btn_bg = theme.get("button_bg", "#cccccc")
        active_bg = theme.get("active_bg", btn_bg) 

        style = ttk.Style()
        style.theme_use('default')

        # estilos para ttk
        style.configure("TButton", background=btn_bg, foreground=fg,
                        bordercolor=btn_bg, lightcolor=btn_bg, darkcolor=btn_bg) #això ho fico x si de cas que a vegades se le van los flaps con los colores
        style.map("TButton", background=[("active", active_bg), ('pressed', active_bg)], 
                  foreground=[('active', fg), ('pressed', fg)])
        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, foreground=fg)
        style.configure("TCheckbutton", background=bg, foreground=fg)
        style.configure("TOptionMenu", background=btn_bg, foreground=fg)

        #configuracion especial para notebook
        style.configure('TNotebook', background=bg)
        style.configure('TNotebook.Tab', background=btn_bg, foreground=fg, padding=[10, 5])
        style.map('TNotebook.Tab', background=[('selected', bg)], foreground=[('selected', fg)])

        #aqui lo aplicas ya a tk de los normalitos
        root.config(bg=bg)

        # sirve para widgets tk y ttk
        def recursive_apply(widget):
            cls = widget.__class__.__name__

            if cls in ["Button", "Checkbutton", "Label", "Frame", "LabelFrame", "StringVar"]:
                if "bg" in widget.configure():
                    widget.configure(bg=bg)
                if "fg" in widget.configure():
                    widget.configure(fg=fg)

            elif cls == "Canvas":
                widget.configure(bg=bg)
            elif cls == "Entry":
                widget.configure(bg="white", fg=fg)
            
            for child in widget.winfo_children(): #aplicar a todos los hijos que hay dentro de un widget rollo empaquetados en un mismo widget sbs sbs
                try:
                    recursive_apply(child)
                except:
                    continue

        recursive_apply(root)

    def seleccionar_tema_personalizado():
        bg_color = colorchooser.askcolor(title="Interface color")[1]
        btn_color = colorchooser.askcolor(title="Notebook tab color")[1]
        fg_color = colorchooser.askcolor(title="Text color")[1]
        
        if bg_color and btn_color and fg_color:
            THEMES["Personalizado"] = {
                "bg": bg_color,
                "button_bg": btn_color,
                "button_fg": fg_color,
                "active_bg": btn_color
            }
            return THEMES["Personalizado"]
        else:
            return None
        
    def cambiar_tema(nombre_tema, root):
        if nombre_tema == "Personalizado":
            tema = seleccionar_tema_personalizado()
            if not tema:
                print("Color selection cancelled.")
                return
        else:
            tema = THEMES[nombre_tema]

        apply_theme_to_all_widgets(root, tema)
        
    
    ####### base ######
    root = tk.Tk()
    pygame.mixer.init()
    sound('background')
    
    root.geometry('1400x800')
    root.title('Interface')
    root['bg'] = "#d7f0f2"
    
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=9, minsize=1000)

    notebook_frame = ttk.Frame(root)
    notebook_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    
    reset_btn = tk.Button(notebook_frame, text="Reset View", command=lambda: resetview(current_graph))
    reset_btn.pack(pady=5)

    right_frame = tk.LabelFrame(root, text = 'Graph:')
    right_frame.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    right_frame.grid_propagate(False)

    right_frame.columnconfigure(0, weight=1)
    right_frame.rowconfigure(0, weight=1)

    notebook = ttk.Notebook(notebook_frame)
    notebook.pack(expand=True, fill='both')

    #############################################
    ##### Pestaña 1: interfaz con graficos######
    ############################################

    pest1 = ttk.Frame(notebook)
    notebook.add(pest1, text="Graph Interface")

    left_frame_p1 = ttk.Frame(pest1)
    left_frame_p1.pack(expand=True, fill='both')

    left_frame_p1.columnconfigure(0, weight=1)
    left_frame_p1.rowconfigure(0, weight=2)
    left_frame_p1.rowconfigure(1, weight=2)
    left_frame_p1.rowconfigure(2, weight=4)
    left_frame_p1.rowconfigure(3, weight=1)
    
    #EXAMPLE BUTTON
    randomframe = tk.LabelFrame(left_frame_p1)
    randomframe.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    randomframe.rowconfigure(0, weight=1)
    randomframe.columnconfigure(0, weight=1)
    randomframe.columnconfigure(1, weight=1)

    examplebutton = tk.Button(randomframe, text='Example', command=lambda: show_example())
    examplebutton.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    interruptor = tk.Checkbutton(randomframe, text='Reachability Mode', 
                                 indicatoron=False,width=15,height=1, selectcolor="#90BE6D", command=lambda: set_reachability_mode_g())
    interruptor.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    #FILES BUTTONS
    filesframe = tk.LabelFrame(left_frame_p1, text = 'Files')
    filesframe.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    filesframe.rowconfigure(0, weight=1)
    filesframe.columnconfigure(0, weight=1)
    filesframe.columnconfigure(1, weight=1)
    filesframe.columnconfigure(2, weight=1)

    uploadbutton = tk.Button(filesframe, text='Load', command=lambda: load_file())
    uploadbutton.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    savebutton = tk.Button(filesframe, text='Save', command=lambda: save_file())
    savebutton.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    newbutton = tk.Button(filesframe, text='New Graph', command=lambda: new_graph())
    newbutton.grid(row=0, column=2, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    #EDIT BUTTONS
    editframe = tk.LabelFrame(left_frame_p1, text = 'Edit')
    editframe.grid(row=2, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    editframe.columnconfigure(0, weight=1)
    editframe.columnconfigure(1, weight=1)
    editframe.rowconfigure(0, weight=1)
    editframe.rowconfigure(1, weight=1)
    editframe.rowconfigure(2, weight=2)

    addnodebutton = tk.Button(editframe, text='Add Node', command=lambda: add_node_button())
    addnodebutton.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    Tooltip(addnodebutton, "Press to add a node.\nFormat: Name X Y (e.g., A 10 20)")

    delnodebutton = tk.Button(editframe, text='Delete Node', command=lambda: del_node_button())
    delnodebutton.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    Tooltip(delnodebutton, "Press to delete a node.\nFormat: Name (e.g., A)")

    addsegmentbutton = tk.Button(editframe, text='Add Segment', command=lambda: add_segment_button())
    addsegmentbutton.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    Tooltip(addsegmentbutton, "Press to add a segment.\nFormat: Name Node1 Node2 (e.g., AB A B)")

    delsegmentbutton = tk.Button(editframe, text='Delete Segment', command=lambda: del_segment_button())
    delsegmentbutton.grid(row=1, column=1, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    Tooltip(delsegmentbutton, "Press to delete a segment.\nFormat: Name (e.g., AB)")

    entry = tk.Entry(editframe)
    entry.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    #CLIPPY :D
    info_frame = ttk.Frame(left_frame_p1)
    info_frame.grid(row=3, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    texto_var = tk.StringVar()
    texto_var.set("Hiiiii!\nLoad a graph/airspace to get started :D")

    original = Image.open('imagenes/clippy.png')
    resized = original.resize((100, 100), Image.Resampling.LANCZOS)
    clippy = ImageTk.PhotoImage(resized)

    imagen = tk.Label(info_frame, image = clippy)
    imagen.image = clippy
    imagen.pack(side='left', padx = 5)
    texto_label = tk.Label(info_frame, textvariable=texto_var, wraplength=100, anchor = 'w',  font=("Comic Sans MS", 8))
    texto_label.pack(side="left", padx=5, pady=5, fill='both', expand=True)

    
    ######################################################
    ##### Pestaña 2: interfaz con nodos de cat, esp, eu###
    ######################################################

    pest2 = ttk.Frame(notebook)
    notebook.add(pest2, text="Airspace Interface")

    left_frame_p2 = ttk.Frame(pest2)
    left_frame_p2.pack(expand=True, fill='both')

    left_frame_p2.columnconfigure(0, weight=1)
    left_frame_p2.rowconfigure(0, weight=2)
    left_frame_p2.rowconfigure(1, weight=4)
    left_frame_p2.rowconfigure(2, weight=1)

    #Path buttons
    pathframe = tk.LabelFrame(left_frame_p2, text = 'Path')
    pathframe.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    pathframe.rowconfigure(0, weight=1)
    pathframe.columnconfigure(0, weight=1)
    pathframe.columnconfigure(1, weight=1)

    interruptor = tk.Checkbutton(pathframe, text='Reachability Mode', 
                                 indicatoron=False,width=15,height=1, selectcolor="#90BE6D", command=lambda: set_reachability_mode_a())
    interruptor.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    googleEarth = tk.Button(pathframe, text='Save as KML', command=lambda: export_to_kml())
    googleEarth.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    #Files buttons
    filesframe = tk.LabelFrame(left_frame_p2, text = 'Files')
    filesframe.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    
    filesframe.columnconfigure(0, weight=1)
    filesframe.rowconfigure(0, weight=1)
    filesframe.rowconfigure(1, weight=1)
    filesframe.rowconfigure(2, weight=1)

    catbutton = tk.Button(filesframe, text='Load Cat', command=lambda: loadCat())
    catbutton.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    espbutton = tk.Button(filesframe, text='Load Esp', command=lambda: loadEsp())
    espbutton.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    eubutton = tk.Button(filesframe, text='Load Eu', command=lambda: loadEu())
    eubutton.grid(row=2, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    #CLIPPY :D
    info_frame = ttk.Frame(left_frame_p2)
    info_frame.grid(row=3, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    original = Image.open('imagenes/clippy.png')
    resized = original.resize((100, 100), Image.Resampling.LANCZOS)
    clippy = ImageTk.PhotoImage(resized)

    imagen = tk.Label(info_frame, image = clippy)
    imagen.image = clippy
    imagen.pack(side='left', padx = 5)
    texto_label = tk.Label(info_frame, textvariable=texto_var, wraplength=100, anchor = 'w',  font=("Comic Sans MS", 8))
    texto_label.pack(side="left", padx=5, pady=5, fill='both', expand=True)

    #############################
    ##### Pestaña 3: Extras #####
    #############################

    pest3 = ttk.Frame(notebook)
    notebook.add(pest3, text="Extras")
    left_frame_p3 = ttk.Frame(pest3)
    left_frame_p3.pack(expand=True, fill='both')
    left_frame_p3.columnconfigure(0, weight=1)
    left_frame_p3.rowconfigure(0, weight=1)
    left_frame_p3.rowconfigure(1, weight=1)
    left_frame_p3.rowconfigure(2, weight=1)

    #sound frame

    soundframe = tk.LabelFrame(left_frame_p3, text = 'Sound')
    soundframe.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    soundframe.rowconfigure(0, weight=1)
    soundframe.columnconfigure(0, weight=1)
    soundframe.columnconfigure(1, weight=1)

    bgsound = tk.Checkbutton(soundframe, text='Background Sound', 
                                 indicatoron=False,width=15,height=1, selectcolor="#BF1919", command=lambda: toggle_sound(sound_name='background'))
    bgsound.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    efsound = tk.Checkbutton(soundframe, text = 'Effects sound',
                             indicatoron=False, width=15,height=1, selectcolor="#BF1919", command=lambda: toggle_sound())
    efsound.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    #random frame
    random_frame = tk.Frame(left_frame_p3)
    random_frame.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    random_frame.rowconfigure(0, weight=1)
    random_frame.columnconfigure(0, weight=1)
    random_frame.columnconfigure(1, weight=1)

    tema_var = tk.StringVar(value="Verdecito")
    tema_menu = ttk.OptionMenu(random_frame, tema_var,"Verdecito",*THEMES.keys(),command=lambda nombre: cambiar_tema(nombre, root))
    tema_menu.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    boton = tk.Button(random_frame, text="Developers", command=lambda: superdevelopers())
    boton.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)


    #CLIPPY :D
    info_frame = ttk.Frame(left_frame_p3)
    info_frame.grid(row=2, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

    original = Image.open('imagenes/clippy.png')
    resized = original.resize((100, 100), Image.Resampling.LANCZOS)
    clippy = ImageTk.PhotoImage(resized)

    imagen = tk.Label(info_frame, image = clippy)
    imagen.image = clippy
    imagen.pack(side='left', padx = 5)
    texto_label = tk.Label(info_frame, textvariable=texto_var, wraplength=100, anchor = 'w',  font=("Comic Sans MS", 8))
    texto_label.pack(side="left", padx=5, pady=5, fill='both', expand=True)

    cambiar_tema("Verdecito", root)
    root.mainloop()

if __name__ == "__main__":
    InterfaceGraph()