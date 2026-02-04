import json
from pathlib import Path


class HabitJsonStorage:
    """JSON file-based storage for habits."""

    def __init__(self, filename="habits.json") -> None:
        self.filename = filename
        self.file = Path(filename)

    def load(self):
        """
        Load habits from JSON file.

        Returns:
            List[Dict]: List of habit dictionaries. Returns empty list if file missing.
        """
        if not self.file.exists():
            self.save([])

        try:
            with open(self.file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Failed to load {self.filename}: {e}")

    def save(self, habit):
        """
        Save habits list to JSON file.

        Args:
            habits (List[Dict]): Habits data to persist
        """
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(habit, f, ensure_ascii=False, indent=4)

    def clear(self) -> str:
        """
        Remove all habits by overwriting file with empty list.

        Returns:
            str: Confirmation message
        """
        self.save([])
        return f"All Habits cleared!"
