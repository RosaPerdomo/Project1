from navPoint import NavPoint
from navSegment import NavSegment
from navAirport import NavAirport
from graph import *
from node import *
from segment import *
from path import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math

class AirSpace: 
    def __init__(self):
        self.navpoints = []
        self.navsegments = []
        self.navairports = []

def LoadAirlineData(filenamepoints, filenamesegments, filenameairports):
    airspace = AirSpace()
    def load_navpoints(a, filename=filenamepoints):
        with open(filename, "r") as file: 
            for line in file: 
                parts = line.strip().split()
                if len(parts) >= 4: 
                    number = int(parts[0])
                    name = parts[1]
                    lat = float(parts[2])
                    lon = float(parts[3])
                    a.navpoints.append(NavPoint(number, name, lat, lon))
    def load_navsegments(a, filename=filenamesegments):
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 3:
                    origin = int(parts[0])
                    dest = int(parts[1])
                    a.navsegments.append(NavSegment(origin, dest, float(parts[2])))
    def load_navairports(a, filename=filenameairports): 
        with open(filename, "r") as file: 
            current_airport = None 
            for line in file: 
                line = line.strip()
                if line == "":
                    continue 
                if "." not in line: 
                    if current_airport: 
                        a.navairports.append(current_airport)
                    current_airport = NavAirport(line)
                elif ".D" in line: 
                    current_airport.sids.append(line)
                elif ".A" in line: 
                    current_airport.stars.append(line)
            if current_airport: 
                a.navairports.append(current_airport)
    load_navpoints(airspace)
    load_navsegments(airspace)
    load_navairports(airspace)
    return airspace

def GetGraph(airspace):
    g = Graph()
    
    # crear nodos
    for p in airspace.navpoints:
        AddNode(g, Node(p.name, p.longitude, p.latitude))
    
    # crear segmentos
    for s in airspace.navsegments:
        for p in airspace.navpoints:
            if p.number == s.origin_number:
                origin = p
            if p.number == s.destination_number:
                dest = p
        seg_name = f"{origin.name}-{dest.name}"
        AddSegment(g, seg_name, origin.name, dest.name)
    
    return g