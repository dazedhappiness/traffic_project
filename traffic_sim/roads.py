class Road:
    def __init__(self, name, length, capacity):
        self.name = name
        self.length = length
        self.capacity = capacity
        self.vehicles = []

    def add_vehicle(self, vehicle):
        if len(self.vehicles) < self.capacity:
            self.vehicles.append(vehicle)
            vehicle.current_road = self
            vehicle.position_on_road = 0
            return True
        return False

    def remove_vehicle(self, vehicle):
        if vehicle in self.vehicles:
            self.vehicles.remove(vehicle)
            vehicle.current_road = None

    def update(self, current_time):
        for vehicle in self.vehicles:
            vehicle.move()
            if vehicle.position_on_road >= self.length:
                vehicle.position_on_road = self.length
