import math

class Waypoint:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon
        
def distance (wp1, wp2):
        R = 6371
        lat1=math.radians(wp1.lat)
        lon1=math.radians(wp1.lon)
        lat2=math.radians(wp2.lat)
        lon2=math.radians(wp2.lon)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
        c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
        dist = R*c
        return dist

def ShowWaypoint(waypoint):
    print(f'Nombre:{waypoint.name}, lat:{waypoint.lat}, lon:{waypoint.lon}')