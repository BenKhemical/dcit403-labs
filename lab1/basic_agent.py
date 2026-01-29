from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
import asyncio


class HelloBehaviour(CyclicBehaviour):
    async def run(self):
        print("Hello! Agent is running...")
        await asyncio.sleep(5)


class MyAgent(Agent):
    async def setup(self):
        print("Agent started")
        self.add_behaviour(HelloBehaviour())


async def main():
    agent = MyAgent("khemicalsagent@xmpp.jp", "khemical")
    await agent.start()
    await asyncio.sleep(30)
    await agent.stop()


if __name__ == "__main__":
    asyncio.run(main())
