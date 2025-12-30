import json
import os

CACHE_DIR = "data"
os.makedirs(CACHE_DIR, exist_ok=True)

def _get_path(name):
    return os.path.join(CACHE_DIR, f"{name}.json")


def load_cache(name, default=None):
    path = _get_path(name)
    if not os.path.exists(path):
        return default if default is not None else []

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default if default is not None else []


def save_cache(name, data):
    path = _get_path(name)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
