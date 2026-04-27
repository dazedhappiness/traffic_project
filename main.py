import matplotlib.pyplot as plt
import matplotlib.animation as animation
from traffic_sim.engine import SimulationEngine
from traffic_sim.roads import Road
from traffic_sim.junctions import Junction
from traffic_sim.vehicles import Vehicle

def compute_path(source, dest):
    graph = {
        "J1": {"J2": "R1"},
        "J2": {"J3": "R2"},
        "J3": {}
    }

    path = []
    current = source

    while current != dest:
        next_node = list(graph[current].keys())[0]
        path.append(graph[current][next_node])
        current = next_node

    return path

class Source:
    def __init__(self, road, rate):
        self.road = road
        self.rate = rate

    def generate(self, step):
        if step % self.rate == 0 and len(self.road.vehicles) < self.road.capacity:
            return True
        return False

class Sink:
    def __init__(self):
        self.completed = 0

    def record(self, vehicle):
        self.completed += 1

def main():
    total_spawned = 0
    engine = SimulationEngine()
    
    j1 = Junction("J1", 0, 5)
    j2 = Junction("J2", 5, 5)
    j3 = Junction("J3", 10, 5)
    
    junctions = {"J1": j1, "J2": j2, "J3": j3}
    for j in junctions.values():
        engine.add_component(j)
    
    r1 = Road("R1", "J1", "J2", length=10, capacity=5)
    r2 = Road("R2", "J2", "J3", length=10, capacity=5)
    
    roads = {"R1": r1, "R2": r2}
    for r in roads.values():
        engine.add_component(r)
        
    j1.add_outgoing(r1)
    j2.add_incoming(r1)
    j2.add_outgoing(r2)
    j3.add_incoming(r2)

    source = Source(r1, rate=3)
    sink = Sink()
    
    fig, ax = plt.subplots(figsize=(8, 4))
    frames_data = []
    total_steps = 30
    completed_ids = set()
    
    for step in range(total_steps):
        if source.generate(step):
            vid = f"V{step}"
            path = compute_path("J1", "J3")[1:]
            v = Vehicle(vid, source="J1", destination="J3", path=path, speed=2)
            r1.add_vehicle(v)
            total_spawned += 1
        
        engine.tick()
        
        current_frame_vehicles = []
        for r in roads.values():
            start_j = junctions[r.start_node]
            end_j = junctions[r.end_node]
            
            for v in r.vehicles:
                progress = v.position_on_road / r.length
                x = start_j.x + (end_j.x - start_j.x) * progress
                y = start_j.y + (end_j.y - start_j.y) * progress
                current_frame_vehicles.append((x, y, v.color))
                
        frames_data.append(current_frame_vehicles)

        for v in r2.vehicles:
            if v.position_on_road >= r2.length and not v.path:
                if v.vid not in completed_ids:
                    sink.record(v)
                    completed_ids.add(v.vid)

    def update(frame_idx):
        ax.clear()
        ax.set_title(f"Time Step: {frame_idx}")
        ax.set_xlim(-1, 11)
        ax.set_ylim(0, 10)
        
        for r in roads.values():
            start_j = junctions[r.start_node]
            end_j = junctions[r.end_node]
            ax.plot([start_j.x, end_j.x], [start_j.y, end_j.y], 'gray', linewidth=4, zorder=1)
            
        for j in junctions.values():
            ax.plot(j.x, j.y, 'ko', markersize=10, zorder=2)
            ax.text(j.x, j.y + 0.5, j.name, ha='center')
            
        frame_vehicles = frames_data[frame_idx]
        for x, y, color in frame_vehicles:
            ax.plot(x, y, marker='s', color=color, markersize=8, zorder=3)
            
    ani = animation.FuncAnimation(fig, update, frames=total_steps, interval=200)
    ani.save('simulation_output.gif', writer='pillow')

    arrived_vehicles = sink.completed

    print(f"Throughput: {arrived_vehicles} vehicles")
    print(f"Spawned: {total_spawned} vehicles")
    print(f"Completion Rate: {arrived_vehicles/total_spawned:.2f}")


if __name__ == "__main__":
    main()
