class Segment:
    def __init__(self, name, origin, destination):
        self.name = name
        self.origin = origin  # This should be a reference to a Node object
        self.destination = destination  # This should be a reference to a Node object

    def __repr__(self):
        return f"Segment({self.name}, {self.origin.name} -> {self.destination.name})"