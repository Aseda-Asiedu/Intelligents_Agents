import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

# 1. Separating the logic into a specialized monitoring class
class DisasterMonitor(CyclicBehaviour):
    async def run(self):
        # Changed the output format to look more like a system log
        print(f"| SYSTEM LOG | Node: {self.agent.jid} | Status: OPERATIONAL")
        await asyncio.sleep(5)

class ReliefCoordinator(Agent):
    async def setup(self):
        # Professional-style initialization message
        print(f"--- Initializing Coordinator Node: {self.jid} ---")
        
        # Adding the monitoring heartbeat
        self.add_behaviour(DisasterMonitor())

async def boot_platform():
    """
    Main entry point to initialize the XMPP agent platform.
    Uses the 'agents' password for the agent1 user on localhost.
    """
    node_id = "agent1@localhost"
    node_key = "agents"

    print(">>> Establishing secure connection to Prosody XMPP Server...")
    
    # Initialize our custom coordinator class
    coordinator = ReliefCoordinator(node_id, node_key)
    
    # Disable SSL verification for the local environment
    coordinator.verify_security = False 

    try:
        # 2. Refactored the 'Injection' logic to be more compact
        # We launch the connection and immediately intercept the client object
        connection_task = asyncio.create_task(coordinator.start(auto_register=True))
        
        # Wait for the backend client to materialize
        while not hasattr(coordinator, "client") or coordinator.client is None:
            await asyncio.sleep(0.02)
        
        # SECURITY OVERRIDE: Force plain auth over local unencrypted stream
        coordinator.client.allow_insecure_auth = True
        
        await connection_task
        
        print(f"--- Node {node_id} successfully synchronized with server ---")

        # Keep the process alive while the coordinator is active
        while coordinator.is_alive():
            await asyncio.sleep(1)

    except Exception as failure:
        print(f"FATAL: Coordination Node failed to join the network: {failure}")
    finally:
        if coordinator.is_alive():
            await coordinator.stop()
        print(">>> Node decommissioned.")

if __name__ == "__main__":
    try:
        # Using a renamed runner function
        asyncio.run(boot_platform())
    except KeyboardInterrupt:
        print("\n[!] Emergency Stop: User interrupted process.")