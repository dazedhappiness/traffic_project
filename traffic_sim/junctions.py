class Junction:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.incoming_roads = []
        self.outgoing_roads = []

    def add_incoming(self, road):
        self.incoming_roads.append(road)

    def add_outgoing(self, road):
        self.outgoing_roads.append(road)

    def update(self, current_time):
        for in_road in self.incoming_roads:
            if not in_road.vehicles:
                continue
            
            first_vehicle = in_road.vehicles[0]
            if first_vehicle.position_on_road >= in_road.length:
                if first_vehicle.path:
                    next_road_name = first_vehicle.path[0]
                    next_road = next((r for r in self.outgoing_roads if r.name == next_road_name), None)
                    
                    if next_road and len(next_road.vehicles) < next_road.capacity:
                        in_road.remove_vehicle(first_vehicle)
                        next_road.add_vehicle(first_vehicle)
                        first_vehicle.path.pop(0)
                else:
                    in_road.remove_vehicle(first_vehicle)
