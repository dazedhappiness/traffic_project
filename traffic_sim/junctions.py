class Junction:
    def __init__(self, name):
        self.name = name
        self.incoming_roads = []
        self.outgoing_roads = []

    def add_incoming(self, road):
        self.incoming_roads.append(road)

    def add_outgoing(self, road):
        self.outgoing_roads.append(road)

    def update(self, current_time):
        pass
