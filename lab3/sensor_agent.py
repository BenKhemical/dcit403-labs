import asyncio
import random
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message

SENSOR_JID = "khemicalsagent@xmpp.jp"   
SENSOR_PASSWORD = "khemical"            

RESCUE_JID = "khemicalsrescue@xmpp.jp"
VERIFY_SECURITY = False               


class SensorAgent(Agent):
    class MonitorBehaviour(PeriodicBehaviour):
        async def run(self):
            event, severity = self.generate_disaster_event()

            if event == "No Event":
                print("[Sensor] No disaster detected.")
                return

            print(f"[Sensor] Disaster detected -> Type={event}, Severity={severity}")

            msg = Message(to=RESCUE_JID)
            msg.set_metadata("performative", "inform")
            msg.set_metadata("ontology", "disaster-report")
            msg.body = f"{event}|{severity}"

            await self.send(msg)
            print(f"[Sensor] Report sent to {RESCUE_JID}\n")

        def generate_disaster_event(self):
            events = ["Flood", "Fire", "Earthquake", "No Event"]
            severities = ["Low", "Medium", "High"]
            event = random.choice(events)
            severity = random.choice(severities) if event != "No Event" else None
            return event, severity

    async def setup(self):
        print(f"[Sensor] Starting: {self.jid}")
        self.add_behaviour(self.MonitorBehaviour(period=5))
        print("[Sensor] Monitoring started (every 5 seconds).\n")


async def main():
    print("[Boot] Creating SensorAgent...")
    agent = SensorAgent(SENSOR_JID, SENSOR_PASSWORD, verify_security=VERIFY_SECURITY)

    print("[Boot] Connecting to XMPP server (xmpp.jp)...")
    await agent.start()

    print("[Boot] SensorAgent is running. Press CTRL+C to stop.")
    try:
        while agent.is_alive():
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n[Boot] Stopping SensorAgent...")
    finally:
        await agent.stop()


if __name__ == "__main__":
    asyncio.run(main())