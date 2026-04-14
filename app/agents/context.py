class AgentContext:
    def __init__(self):
        self.memory = {}
        self.messages = []

    def update(self, key, value):
        self.memory[key] = value

    def get(self, key):
        return self.memory.get(key)

    def send(self, sender, message):
        self.messages.append({"agent": sender, "message": message})

    def get_messages(self):
        return self.messages