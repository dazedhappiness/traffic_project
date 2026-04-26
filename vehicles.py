class Vehicle:
    def __init__(self, vid, source, destination, speed=1):
        self.vid = vid
        self.source = source
        self.destination = destination
        self.speed = speed
        self.current_road = None
        self.position_on_road = 0 
        self.path = []

    def move(self):
        if self.current_road:
            self.position_on_road += self.speed
