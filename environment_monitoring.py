import asyncio
import random
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour


SEVERITY_LEVELS = ["Low", "Moderate", "High", "Critical"]

class EnvironmentMonitor(PeriodicBehaviour):
    async def run(self):
        
        current_severity = random.choice(SEVERITY_LEVELS)
        
        
        print(f"| SENSOR DATA | Node: {self.agent.jid} | Perceived Severity: {current_severity}")
        
        # Logic to handle critical events
        if current_severity == "Critical":
            print(f"!!!  ALERT: Critical disaster level detected at {self.agent.jid}!")

class SensorNode(Agent):
    async def setup(self):
        print(f"--- Sensor Node {self.jid} Initializing Monitoring Behaviors ---")
        
        # Set to monitor the environment every 10 seconds 
        monitor_behaviour = EnvironmentMonitor(period=10)
        self.add_behaviour(monitor_behaviour)

async def boot_sensor_system():
    node_id = "agent1@localhost"
    node_key = "agents"

    print(">>> Launching Disaster Perception Module...")
    sensor_agent = SensorNode(node_id, node_key)
    
    
    sensor_agent.verify_security = False 

    try:
        connection_task = asyncio.create_task(sensor_agent.start(auto_register=True))
        
        while not hasattr(sensor_agent, "client") or sensor_agent.client is None:
            await asyncio.sleep(0.02)
        
        sensor_agent.client.allow_insecure_auth = True
        await connection_task
        
        print(f"--- Node {node_id} successfully sensing environment ---")

        while sensor_agent.is_alive():
            await asyncio.sleep(1)

    except Exception as e:
        print(f"FATAL: Sensor failed to initialize perception: {e}")
    finally:
        await sensor_agent.stop()

if __name__ == "__main__":
    try:
        asyncio.run(boot_sensor_system())
    except KeyboardInterrupt:
        print("\n[!] Sensor Node deactivated.")