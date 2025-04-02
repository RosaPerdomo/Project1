from waypoint import*

wp1 = Waypoint ('Nou Camp', 41.381623923229995, 2.122853541678448)
wp2 = Waypoint ('Santiago Bernabeu', 40.453030507454244, -3.6883551609249308)
wp3 = Waypoint ('Balaidos', 42.211904178262195, -8.739772189675971 )
wp4 = Waypoint ('Sanchez Pizjuan', 37.38276157689335, -5.971691936532935)
ShowWaypoint(wp1)
ShowWaypoint(wp2)
ShowWaypoint(wp3)
ShowWaypoint(wp4)

print(f"La distancia entre {wp1.name} y {wp2.name} es de {distance(wp1,wp2)} km")
print(f"La distancia entre {wp2.name} y {wp3.name} es de {distance(wp2,wp3)} km")
print(f"La distancia entre {wp3.name} y {wp4.name} es de {distance(wp3,wp4)} km")