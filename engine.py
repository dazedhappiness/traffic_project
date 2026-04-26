class SimulationEngine:
    def __init__(self):
        self.time = 0
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def tick(self):
        self.time += 1
        for component in self.components:
            component.update(self.time)

    def run(self, steps):
        for _ in range(steps):
            self.tick()
