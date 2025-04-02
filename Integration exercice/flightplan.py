from waypoint import*
import matplotlib.pyplot as plt 
import numpy as np

class FlightPlan:
	def __init__ (self, name):
		self.name = name
		self.waypoint = []	
		
def add_waypoint(myPlan, waypoint):
	myPlan.waypoint.append(waypoint)

def ShowFlightPlan(flightplan):
	print(f'Nombre del FlightPlan:{flightplan.name}')
	print('Waypoints:')
	for waypoint in flightplan.waypoint:
		ShowWaypoint(waypoint)

def FindWaypoint (fp, name):
	for waypoint in fp.waypoint:
		if waypoint.name == name:
			return waypoint
		else:
			return None

def RemoveWaypoint (fp, name):
	newwaypoints = []
	len_inicial=len(fp.waypoint)
	for wp in fp.waypoint:
		if wp.name != name:
			newwaypoints.append(wp)
	fp.waypoint = newwaypoints
	if len(fp.waypoint) < len_inicial:
		print(f"Se ha eliminado el waypoint '{name}'")
	else:
		print(f"No se ha encontrado el waypoint '{name}' en el flightplan")

def FlightPlanLength (fp):
	totaldist = 0.0
	i=0
	while i<(len(fp.waypoint)-1):
		wp1=fp.waypoint[i]
		wp2=fp.waypoint[i+1]
		totaldist += distance(wp1,wp2)
		i+=1
	return totaldist

def PlotFlightPlan (fp):
    for wp in fp.waypoint:
        plt.plot(wp.lon,wp.lat, 'o', color='red', markersize=5)
        plt.text( wp.lon + 0.5, wp.lat + 0.5, wp.name,
            color='green', weight='bold',
            fontsize=6)
            
    i = 0
    while i < len(fp.waypoint) - 1:
        wp1 = fp.waypoint[i]
        wp2 = fp.waypoint[i + 1]
        plt.arrow(wp1.lon, wp1.lat, wp2.lon - wp1.lon, wp2.lat - wp1.lat, head_width=0.2, head_length=0.3, fc='blue', ec='blue', linewidth=1)
        mid_lon = (wp1.lon + wp2.lon) / 2
        mid_lat = (wp1.lat + wp2.lat) / 2
        distancia = distance(wp1, wp2)
        plt.text(mid_lon, mid_lat, f'{distancia:.2f} km', fontsize=7, weight='bold')
        i += 1
    
	
    latNW = 43.62481631158062
    lonNW = -8.902207838560653
    latSE = 35.98754955400314
    lonSE = 3.8847514743561953

    plt.axis([lonNW, lonSE, latSE, latNW])
    plt.grid(color='red', linestyle='dashed', linewidth=0.5)
    plt.title('Tu plan de vuelo: '+ fp.name)
    plt.show()

def LoadFlightPlan (fileName):
	X = open(fileName, 'r')
	lines = X.readlines()
	fpname = lines[0]
	fp = FlightPlan(fpname)
	for line in lines[1:]:
		line=line.strip()
		if line:
			trozo=line.split(', ')
			name = trozo[0]
			lat = trozo[1]
			lon = trozo[2]
			wp = Waypoint (name, float(lat), float(lon))
			add_waypoint(fp, wp)
	return fp

def SaveFlightPlan (fp, fileName):
	X = open(fileName, 'w')
	X.write(f'{fp.name}\n')
	for wp in fp.waypoint:
		X.write(f'{wp.name}, {wp.lat}, {wp.lon}\n')
	print(f'Se ha guardado el FlightPlan en {fileName}.')