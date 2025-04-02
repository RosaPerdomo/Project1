from flightplan import*
from test_waypoint import*

myPlan = FlightPlan('myPlan')
add_waypoint(myPlan, wp1)
add_waypoint(myPlan, wp2)
add_waypoint(myPlan, wp3)
add_waypoint(myPlan, wp4)

ShowFlightPlan(myPlan)

PlotFlightPlan(myPlan)

#Test del FindWaypoint
if FindWaypoint (myPlan, 'Balaidos'):
    print('Waypoint encontrado')
else: 
    print('Waypoint no encontrado')
#Test del RemoveWaypoint
RemoveWaypoint (myPlan, 'Balaidos')
print(myPlan.waypoint)
#Test del FlightPlanLength
distanciatotal=FlightPlanLength(myPlan)
print(f'La distancia total es de {distanciatotal}')

#Test de LoadFlightPlan y SaveFlightPlan
file = str('Integration exercice\waypoints_file.txt')
LoadFlightPlan(file)
SaveFlightPlan(LoadFlightPlan(file), file)