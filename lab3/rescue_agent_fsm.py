import asyncio
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State

# -----------------------------
# CONFIG (EDIT THESE)
# -----------------------------
RESCUE_JID = "khemicalsrescue@xmpp.jp"   # <-- create this xmpp.jp account
RESCUE_PASSWORD = "khemical"            # <-- password for rescue account
VERIFY_SECURITY = False                 # recommended for lab environments


STATE_IDLE = "IDLE"
STATE_DISPATCHED = "DISPATCHED"
STATE_RESCUING = "RESCUING"
STATE_DONE = "DONE"


class RescueFSM(FSMBehaviour):
    async def on_start(self):
        print("[RescueFSM] Starting FSM...")

    async def on_end(self):
        print("[RescueFSM] FSM finished.")


class IdleState(State):
    async def run(self):
        print("[Rescue] State=IDLE | Waiting for disaster report...")

        msg = await self.receive(timeout=10)
        if not msg:
            print("[Rescue] No report yet. Staying IDLE.\n")
            self.set_next_state(STATE_IDLE)
            return

        ontology = msg.get_metadata("ontology")
        if ontology == "disaster-report":
            try:
                event_type, severity = msg.body.split("|")
            except ValueError:
                print(f"[Rescue] Bad report format: {msg.body}")
                self.set_next_state(STATE_IDLE)
                return

            # Event trigger
            self.agent.current_event = event_type
            self.agent.current_severity = severity

            print(f"[Rescue] EVENT: Received sensor report -> {event_type} (Severity={severity})")
            self.set_next_state(STATE_DISPATCHED)
        else:
            print(f"[Rescue] Unknown ontology '{ontology}'. Ignoring.\n")
            self.set_next_state(STATE_IDLE)


class DispatchedState(State):
    async def run(self):
        event_type = self.agent.current_event
        severity = self.agent.current_severity

        # Goal
        print(f"[Rescue] State=DISPATCHED | Goal: Respond to {event_type} (Severity={severity})")
        print("[Rescue] Dispatching rescue team...")
        await asyncio.sleep(2)

        print("[Rescue] Arrived at location.")
        self.set_next_state(STATE_RESCUING)


class RescuingState(State):
    async def run(self):
        event_type = self.agent.current_event
        severity = self.agent.current_severity

        print(f"[Rescue] State=RESCUING | Performing rescue operations for {event_type}...")

        # simulate operation time based on severity
        op_time = {"Low": 2, "Medium": 4, "High": 6}.get(severity, 3)
        await asyncio.sleep(op_time)

        # Simple outcome rule
        success = severity in ["Low", "Medium"]

        if success:
            self.agent.last_outcome = "COMPLETE"
            print("[Rescue] Rescue SUCCESS.")
        else:
            self.agent.last_outcome = "FAILED"
            print("[Rescue] Rescue FAILED (needs reinforcement).")

        self.set_next_state(STATE_DONE)


class DoneState(State):
    async def run(self):
        print(f"[Rescue] State=DONE | Outcome={self.agent.last_outcome}")
        print("[Rescue] Resetting to IDLE...\n")

        self.agent.current_event = None
        self.agent.current_severity = None
        await asyncio.sleep(1)

        self.set_next_state(STATE_IDLE)


class RescueAgent(Agent):
    async def setup(self):
        print(f"[Rescue] Starting: {self.jid}")

        self.current_event = None
        self.current_severity = None
        self.last_outcome = None

        fsm = RescueFSM()
        fsm.add_state(name=STATE_IDLE, state=IdleState(), initial=True)
        fsm.add_state(name=STATE_DISPATCHED, state=DispatchedState())
        fsm.add_state(name=STATE_RESCUING, state=RescuingState())
        fsm.add_state(name=STATE_DONE, state=DoneState())

        fsm.add_transition(source=STATE_IDLE, dest=STATE_IDLE)
        fsm.add_transition(source=STATE_IDLE, dest=STATE_DISPATCHED)
        fsm.add_transition(source=STATE_DISPATCHED, dest=STATE_RESCUING)
        fsm.add_transition(source=STATE_RESCUING, dest=STATE_DONE)
        fsm.add_transition(source=STATE_DONE, dest=STATE_IDLE)

        self.add_behaviour(fsm)
        print("[Rescue] FSM loaded. Waiting for sensor reports...\n")


async def main():
    print("[Boot] Creating RescueAgent...")
    agent = RescueAgent(RESCUE_JID, RESCUE_PASSWORD, verify_security=VERIFY_SECURITY)

    print("[Boot] Connecting to XMPP server (xmpp.jp)...")
    await agent.start()

    print("[Boot] RescueAgent is running. Press CTRL+C to stop.")
    try:
        while agent.is_alive():
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n[Boot] Stopping RescueAgent...")
    finally:
        await agent.stop()


if __name__ == "__main__":
    asyncio.run(main())