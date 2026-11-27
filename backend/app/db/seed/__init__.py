import json
from pathlib import Path


def read_exercises() -> list[dict]:
    return json.loads(Path(__file__).with_name("exercises.json").read_text(encoding="utf-8"))
