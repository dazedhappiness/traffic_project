class Vehicle:
    def __init__(self, vid, source, destination, path, speed=1):
        self.vid = vid
        self.source = source
        self.destination = destination
        self.speed = speed
        self.current_road = None
        self.position_on_road = 0
        self.path = path

        colors = {
            "K1": "red",
            "K2": "blue",
            "K3": "green",
            "K4": "orange",
            "K5": "purple"
        }

        self.color = colors.get(destination, "black")

    def move(self):
        if self.current_road:
            self.position_on_road += self.speed
