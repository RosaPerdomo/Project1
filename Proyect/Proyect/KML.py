def export_graph_to_kml(graph, filename):
    kml_header = '<?xml version="1.0" encoding="UTF-8"?>\n'
    kml_header += '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
    kml_header += '<Document>\n'

    for node in graph.node:
        kml_header += f'  <Placemark>\n'
        kml_header += f'    <name>{node.name}</name>\n'
        kml_header += f'    <Point>\n'
        kml_header += f'      <coordinates>{node.x},{node.y},0</coordinates>\n'
        kml_header += f'    </Point>\n'
        kml_header += f'  </Placemark>\n'

    for segment in graph.segment:
        kml_header += f'  <Placemark>\n'
        kml_header += f'    <name>{segment.name}</name>\n'
        kml_header += f'    <LineString>\n'
        kml_header += f'      <coordinates>\n'
        kml_header += f'        {segment.origin.x},{segment.origin.y},0\n'
        kml_header += f'        {segment.destination.x},{segment.destination.y},0\n'
        kml_header += f'      </coordinates>\n'
        kml_header += f'    </LineString>\n'
        kml_header += f'  </Placemark>\n'

    kml_footer = '</Document>\n'
    kml_footer += '</kml>'

    with open(filename, 'w') as kml_file:
        kml_file.write(kml_header + kml_footer)