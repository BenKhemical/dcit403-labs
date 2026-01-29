import random


class DisasterEnvironment:
    def __init__(self):
        self.severity = 0

    def generate_event(self):
        # severity from 1 to 10
        self.severity = random.randint(1, 10)
        return self.severity
