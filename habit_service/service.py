from models.base import DailyHabit
from schemas.habit_schema import DailyHabitSchema
from habit_storage.json_storage import HabitJsonStorage


class HabitService:
    def __init__(self, storage: HabitJsonStorage):
        self.storage = storage
        self.habits = storage.load()

    def generate_id(self):
        if self.habits:
            try:
                max_id = max(habit.get("habit_id", 0) for habit in self.habits)
                next_id = max_id + 1
            except (ValueError, KeyError):
                next_id = 1
        else:
            next_id = 1
        return next_id

    def create_habit(self, habit_schema: DailyHabitSchema):
        habit = DailyHabit(
            habit_id=self.generate_id(),
            habit_name=habit_schema.habit_name,
            habit_description=habit_schema.habit_description,
            category=habit_schema.category,
        )
        self.habits.append(habit.to_dict())
        self.storage.save(self.habits)
        return f"Habit - '{habit_schema.habit_name.title()}' added!"

    def remove_habit(self, habit_id: int):
        for habit in self.habits:
            if habit["habit_id"] == habit_id:
                self.habits.remove(habit)
                self.storage.save(self.habits)
                return f"Habit removed!"
        return f"Habit not found!"

    def complete_habit(self, habit_id: int):
        for habit in self.habits:
            if habit["habit_id"] == habit_id:
                habit["complete"] = True
                self.storage.save(self.habits)
                return f"Habit complete!"
        return f"Habit not found!"


hs = HabitService(HabitJsonStorage())
# print(hs.create_habit(DailyHabitSchema(habit_name="test",
#                                        habit_description="test",
#                                        category=CategoryHabit.HEALTH)))
print(hs.complete_habit(1))
# print(hs.remove_habit(2))
