import json
from pathlib import Path

class HabitJsonStorage:
    def __init__(self, filename="habits.json"):
        self.filename = filename
        self.file = Path(filename)

    def load(self):
        if not self.file.exists():
            self.save([])

        try:
            with open(self.file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Failed to load {self.filename}: {e}")


    def save(self, habit):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(habit, f, ensure_ascii=False, indent=4)
