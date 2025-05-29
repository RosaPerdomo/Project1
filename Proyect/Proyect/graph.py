class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

class Segment:
    def __init__(self, name, origin, destination):
        self.name = name
        self.origin = origin
        self.destination = destination

class Graph:
    def __init__(self):
        self.node = []
        self.segment = []

    def add_node(self, node):
        self.node.append(node)

    def delete_node(self, node_name):
        self.node = [node for node in self.node if node.name != node_name]
        self.segment = [segment for segment in self.segment if segment.origin.name != node_name and segment.destination.name != node_name]

    def add_segment(self, name, origin_name, destination_name):
        origin = next((node for node in self.node if node.name == origin_name), None)
        destination = next((node for node in self.node if node.name == destination_name), None)
        if origin and destination:
            segment = Segment(name, origin, destination)
            self.segment.append(segment)

    def delete_segment(self, segment_name):
        self.segment = [segment for segment in self.segment if segment.name != segment_name]