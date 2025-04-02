from flightplan import *
option = -1
while option != 0:
   print ('Estas son las opciones del menu:')
   print ('\t1: \tCargar plan de vuelo desde fichero')
   print ('\t2: \tPlot del plan de vuelo')
   print ('\t3: \tAñadir waypoint')
   print ('\t4: \tEliminar waypoint')
   print ('\t5: \tEncontrar waypoint')
   print ('\t6: \tMostrar plan de vuelo actual')
   print ('\t0: \tSalir')
   option = eval(input ('Elije una opción: '))
   if option == 1:
      fileName = str(input('Escribe el nombre del fichero: '))
      fp = LoadFlightPlan(fileName)
   if option == 2:
      PlotFlightPlan(fp)
   if option == 3:
      wp = Waypoint()
      linea=input('Ingresa el nombre, la latitud y la longitud del waypoint: ')
      trozos = linea.strip().split(', ')
      wp.name = trozos[0]
      wp.lat = trozos[1]
      wp.lon = trozos[2]
      add_waypoint(fp, wp)
   if option == 4:
      name = input('Escribe el nombre del waypoint: ')
      RemoveWaypoint(fp, name)
   if option == 5:
      name=input('Ingresa el nombre del waypoint: ')
      FindWaypoint(fp, name)
   if option == 6:
      ShowFlightPlan(fp)
   if option == 0:
      print ('Gracias por usar nuestro programa')