from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
import asyncio
from disaster import DisasterEnvironment


class SensorBehaviour(CyclicBehaviour):
    async def run(self):
        severity = self.agent.environment.generate_event()

        print(f"[SensorAgent] Detected disaster severity level: {severity}")

        # Log to file
        with open("event_log.txt", "a") as f:
            f.write(f"Detected severity: {severity}\n")

        await asyncio.sleep(5)


class SensorAgent(Agent):
    async def setup(self):
        print("SensorAgent started")
        self.environment = DisasterEnvironment()
        self.add_behaviour(SensorBehaviour())


async def main():
    agent = SensorAgent("khemicalsagent@xmpp.jp", "khemical")
    await agent.start()
    await asyncio.sleep(40)
    await agent.stop()


if __name__ == "__main__":
    asyncio.run(main())
