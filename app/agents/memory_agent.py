import json
import os

MEMORY_FILE = "memory.json"

def save_memory(data):
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)
    else:
        memory = []

    memory.append(data)

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []