import json, os

def load_memory():
    if not os.path.exists("storage/memory.json"):
        return {"learning_ids": [], "ta_ids": []}
    return json.load(open("storage/memory.json"))

def save_memory(mem):
    with open("storage/memory.json", "w") as f:
        json.dump(mem, f, indent=2)
