from graph import *
from node import *
from segment import *
from path import *
import os

def GraphToKMLFAIL(g, filename='Graph.kml'):
    with open(filename, 'w') as X:
        X.write("<kml xmlns='http://www.opengis.net/kml/2.2'>\n")
        X.write('<Document>\n')
        for n in g.node:
            X.write(f'<Placemark> <name>{n.name}</name>\n')
            X.write('<Point>\n')
            X.write('<coordinates>\n')
            X.write(f'{n.x},{n.y}\n')
            X.write('</coordinates>\n')
            X.write('</Point>\n')
            X.write('</Placemark>\n')
        
        for s in g.segment:
            X.write('<Placemark>\n')
            X.write(f'<name>Route {s.name}</name>\n')
            X.write('<LineString>\n')
            X.write('<altitudeMode>clampToGround</altitudeMode>\n')
            X.write('<extrude>1</extrude>\n')
            X.write('<tessellate>1</tessellate>\n')
            X.write('<coordinates>\n')
            X.write(f'{s.origin.x},{s.origin.y}\n')
            X.write(f'{s.destination.x},{s.destination.y}\n')
            X.write('</coordinates>\n')
            X.write('</LineString>\n')
            X.write('</Placemark>\n')
        X.write('</Document>\n')
        X.write('</kml>')
    try:
            os.startfile(os.path.abspath(filename))
    except Exception as e:
        print('Error!')


def PathToKML(g,p,filename='Path.kml'):
    with open(filename, 'w') as X:
        X.write("<kml xmlns='http://www.opengis.net/kml/2.2'>\n")
        X.write('<Document>\n')
        for n in g.node:
            if n in p.nodes:
                X.write(f'<Placemark> <name>{n.name}</name>\n')
                X.write('<Point>\n')
                X.write('<coordinates>\n')
                X.write(f'{n.x},{n.y}\n')
                X.write('</coordinates>\n')
                X.write('</Point>\n')
                X.write('</Placemark>\n')
        for i in range(len(p.nodes)-1):
            origin = p.nodes[i]
            destination = p.nodes[i+1]
            segment = None
            for s in g.segment:
                if (s.origin == origin and s.destination == destination) or \
                (s.origin == destination and s.destination == origin):
                    segment = s
                    break
            if segment:
                X.write('<Placemark>\n')
                X.write(f'<name>Route {segment.name}</name>\n')
                X.write('<LineString>\n')
                X.write('<altitudeMode>clampToGround</altitudeMode>\n')
                X.write('<extrude>1</extrude>\n')
                X.write('<tessellate>1</tessellate>\n')
                X.write('<coordinates>\n')
                X.write(f'{origin.x},{origin.y}\n')
                X.write(f'{destination.x},{destination.y}\n')
                X.write('</coordinates>\n')
                X.write('</LineString>\n')
                X.write('</Placemark>\n')
        X.write('</Document>\n')
        X.write('</kml>')
    try:
        os.startfile(os.path.abspath(filename))
    except Exception as e:
        print('Error!')

def GraphToKML(gnodes, gsegments, filename='Graph.kml'):
    with open(filename, 'w') as X:
        X.write("<kml xmlns='http://www.opengis.net/kml/2.2'>\n")
        X.write('<Document>\n')
        for n in gnodes:
            X.write(f'<Placemark> <name>{n.name}</name>\n')
            X.write('<Point>\n')
            X.write('<coordinates>\n')
            X.write(f'{n.x},{n.y}\n')
            X.write('</coordinates>\n')
            X.write('</Point>\n')
            X.write('</Placemark>\n')

        for s in gsegments:
            X.write('<Placemark>\n')
            X.write(f'<name>Route {s.name}</name>\n')
            X.write('<LineString>\n')
            X.write('<altitudeMode>clampToGround</altitudeMode>\n')
            X.write('<extrude>1</extrude>\n')
            X.write('<tessellate>1</tessellate>\n')
            X.write('<coordinates>\n')
            X.write(f'{s.origin.x},{s.origin.y}\n')
            X.write(f'{s.destination.x},{s.destination.y}\n')
            X.write('</coordinates>\n')
            X.write('</LineString>\n')
            X.write('</Placemark>\n')
        X.write('</Document>\n')
        X.write('</kml>')