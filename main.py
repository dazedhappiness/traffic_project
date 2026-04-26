from traffic_sim.engine import SimulationEngine
from traffic_sim.roads import Road
from traffic_sim.junctions import Junction
from traffic_sim.vehicles import Vehicle

def main():
    engine = SimulationEngine()
    
    r1 = Road("R1", length=10, capacity=5)
    r2 = Road("R2", length=10, capacity=5)
    
    j1 = Junction("J1")
    j1.add_incoming(r1)
    j1.add_outgoing(r2)
    
    v1 = Vehicle("V1", source="R1", destination="R2")
    r1.add_vehicle(v1)
    
    engine.add_component(r1)
    engine.add_component(r2)
    engine.add_component(j1)
    
    engine.run(steps=5)

if __name__ == "__main__":
    main()
