import random
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from traffic_sim.engine import SimulationEngine
from traffic_sim.roads import Road
from traffic_sim.junctions import Junction
from traffic_sim.vehicles import Vehicle


class Source:
    def __init__(self, road, source_node, rate):
        self.road = road
        self.source_node = source_node
        self.rate = rate

    def generate(self, step):
        return random.random() < self.rate and len(self.road.vehicles) < self.road.capacity


class Sink:
    def __init__(self, name):
        self.name = name
        self.completed = 0

    def record(self):
        self.completed += 1


def compute_path(graph, source, dest):
    queue = deque([(source, [])])
    visited = set()

    while queue:
        current, path = queue.popleft()

        if current == dest:
            return path

        if current in visited:
            continue

        visited.add(current)

        for neighbor, road_name in graph[current].items():
            queue.append((neighbor, path + [road_name]))

    return []


def main():
    engine = SimulationEngine()

    junction_positions = {
        "J1": (0, 10),
        "J2": (10, 10),
        "J3": (0, 5),
        "J4": (10, 5),
        "J5": (0, 0),
        "J6": (10, 0),
    }

    junctions = {}

    for name, (x, y) in junction_positions.items():
        j = Junction(name, x, y)
        junctions[name] = j
        engine.add_component(j)

    road_definitions = [
        ("R1", "J1", "J2"),
        ("R2", "J2", "J1"),

        ("R3", "J3", "J4"),
        ("R4", "J4", "J3"),

        ("R5", "J5", "J6"),
        ("R6", "J6", "J5"),

        ("R7", "J1", "J3"),
        ("R8", "J3", "J1"),

        ("R9", "J3", "J5"),
        ("R10", "J5", "J3"),

        ("R11", "J2", "J4"),
        ("R12", "J4", "J2"),

        ("R13", "J4", "J6"),
        ("R14", "J6", "J4"),
    ]

    roads = {}

    for name, start, end in road_definitions:
        r = Road(name, start, end, length=10, capacity=10)
        roads[name] = r
        engine.add_component(r)

        junctions[start].add_outgoing(r)
        junctions[end].add_incoming(r)

    graph = {
        "J1": {"J2": "R1", "J3": "R7"},
        "J2": {"J1": "R2", "J4": "R11"},
        "J3": {"J4": "R3", "J1": "R8", "J5": "R9"},
        "J4": {"J3": "R4", "J2": "R12", "J6": "R13"},
        "J5": {"J6": "R5", "J3": "R10"},
        "J6": {"J5": "R6", "J4": "R14"},
    }

    sources = [
        Source(roads["R1"], "J1", 0.4),
        Source(roads["R3"], "J3", 0.4),
        Source(roads["R5"], "J5", 0.4),
    ]

    sink_nodes = {
        "K1": "J6",
        "K2": "J2",
        "K3": "J5",
        "K4": "J5",
        "K5": "J6"
    }

    sinks = {
        "K1": Sink("K1"),
        "K2": Sink("K2"),
        "K3": Sink("K3"),
        "K4": Sink("K4"),
        "K5": Sink("K5"),
    }

    fig, ax = plt.subplots(figsize=(10, 8))

    frames_data = []

    total_steps = 100
    total_spawned = 0
    completed_ids = set()

    vehicle_counter = 0

    for step in range(total_steps):

        for source in sources:

            if source.generate(step):

                destination = random.choice(list(sink_nodes.keys()))

                target_junction = sink_nodes[destination]

                path = compute_path(
                    graph,
                    source.source_node,
                    target_junction
                )

                if len(path) > 0:

                    first_road = roads[path[0]]

                    vehicle = Vehicle(
                        f"V{vehicle_counter}",
                        source.source_node,
                        destination,
                        path[1:],
                        speed=1
                    )

                    added = first_road.add_vehicle(vehicle)

                    if added:
                        total_spawned += 1
                        vehicle_counter += 1

        engine.tick()

        frame_vehicles = []

        for road in roads.values():

            start_j = junctions[road.start_node]
            end_j = junctions[road.end_node]

            for vehicle in road.vehicles:

                progress = vehicle.position_on_road / road.length

                x = start_j.x + (end_j.x - start_j.x) * progress
                y = start_j.y + (end_j.y - start_j.y) * progress

                frame_vehicles.append((x, y, vehicle.color))

                if (
                    vehicle.position_on_road >= road.length
                    and not vehicle.path
                    and vehicle.vid not in completed_ids
                ):

                    sinks[vehicle.destination].record()
                    completed_ids.add(vehicle.vid)

        frames_data.append(frame_vehicles)

    def update(frame_idx):

        ax.clear()

        ax.set_title(f"Time Step: {frame_idx}")

        ax.set_xlim(-3, 13)
        ax.set_ylim(-3, 13)

        for road in roads.values():

            start_j = junctions[road.start_node]
            end_j = junctions[road.end_node]

            ax.plot(
                [start_j.x, end_j.x],
                [start_j.y, end_j.y],
                color="gray",
                linewidth=2
            )

        for junction in junctions.values():

            ax.plot(
                junction.x,
                junction.y,
                "ko",
                markersize=12
            )

        for x, y, color in frames_data[frame_idx]:

            ax.plot(
                x,
                y,
                marker="s",
                color=color,
                markersize=6
            )

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=total_steps,
        interval=100
    )

    ani.save("simulation_output.gif", writer="pillow")

    total_completed = sum(s.completed for s in sinks.values())

    max_queue = max(len(r.vehicles) for r in roads.values())

    print(f"Throughput: {total_completed} vehicles")
    print(f"Spawned: {total_spawned} vehicles")
    print(f"Completion Rate: {total_completed / total_spawned:.2f}")
    print(f"Maximum Queue Length: {max_queue}")


if __name__ == "__main__":
    main()
