from datetime import datetime
from typing import Optional
from habit_storage.json_storage import HabitJsonStorage
from models.base import DailyHabit, CategoryHabit
from schemas.habit_schema import DailyHabitSchema, GoalDaysHabit
# Проверить работает ли валидация

class HabitService:
    def __init__(self, storage: HabitJsonStorage):
        self.storage = storage
        self.habits_data = storage.load()

    def increase_streak(self) -> str:
        """
        Method:
        Checks the validity of the series.
        Increases the streak by 1.
        Refreshes the target.
        """
        for habit in self.habits_data:
            if habit["completed"]:
                self.check_streak_validity()
                habit["streak"] += 1
                self.update_goal_days()
                habit["last_completed"] = datetime.now().isoformat(timespec="seconds")
                habit["completed"] = False
            return f"Current streak - {habit["streak"]} days"
        return f"Current streak - no streak"

    def check_streak_validity(self) -> bool:
        """
        Series Verification
        """
        for habit in self.habits_data:
            if not habit["last_completed"]:
                return True

            if isinstance(habit["last_completed"], str):
                last_completed_dt = datetime.fromisoformat(habit["last_completed"])
            else:
                last_completed_dt = habit["last_completed"]

            days_since_last = (datetime.now() - last_completed_dt).days
            if days_since_last > 1:
                habit.streak = 0
                return False
        return True

    # Добавить оповещение пользователя о новой цели
    def update_goal_days(self) -> Optional[str]:
        """
        Refreshes the target when a specific streak is reached
        """
        for habit in self.habits_data:
            if habit["streak"] == 1:
                habit["goal_days"] = GoalDaysHabit.ONE_WEEK
            elif habit["streak"] == 7:
                habit["goal_days"] = GoalDaysHabit.TWO_WEEK
            elif habit["streak"] == 14:
                habit["goal_days"] = GoalDaysHabit.ONE_MONTH
            elif habit["streak"] == 30:
                habit["goal_days"] = GoalDaysHabit.SIX_MONTHS
            elif habit["streak"] == 180:
                habit["goal_days"] = GoalDaysHabit.ONE_YEAR
            elif habit["streak"] == 365:
                return (
                    f"Hey there!\n\n"
                    f"Imagine this: exactly one year ago, you took your first step.\n"
                    f"\tBack then, 365 days felt like an eternity.\n"
                    f"\tYou had no idea if you’d make it to the end.\n"
                    f"\tBut you decided to give it a shot — and you started walking.\n\n"
                    f"\tDay after day, you kept going.\n"
                    f"\tThere were moments when you wanted to quit.\n"
                    f"\tTimes when it felt like you weren’t making any progress.\n"
                    f"\tInstances when fatigue whispered, «Take a break, it’s not urgent.»\n"
                    f"\tBut you kept pushing forward. Every single day. No exceptions.\n\n"
                    f"\tAnd now — you’re on the home stretch.\n\n"
                    f"Look at what you’ve achieved:\n"
                    f"\t-- You proved to yourself that you can keep your word;\n"
                    f"\t-- You forged ironclad discipline;\n"
                    f"\t-- You turned action into habit, and habit into a way of life.\n\n"
                    f"This year isn’t just a mark on the calendar.\n"
                    f"\tIt’s your personal victory.\n"
                    f"\tA victory over laziness, doubts, and the habit of postponing things.\n"
                    f"\tYou’ve shown what you’re capable of when you go all the way.\n\n"
                    f"One final push. You’re almost there. Take a deep breath — and take those last steps.\n"
                    f"\tYou’ve earned the right to say:\n"
                    f"\t«I completed the entire journey.»\n\n"
                    f"You’re doing great. I believe in you.\n"
                    f"It’s time to finish what you started. Go for it!"
                )
        return None

    def generate_id(self):
        if self.habits_data:
            try:
                max_id = max(habit.get("habit_id", 0) for habit in self.habits_data)
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
        self.habits_data.append(habit.to_dict())
        self.storage.save(self.habits_data)
        return f"Habit - '{habit_schema.habit_name.title()}' added!"

    def remove_habit(self, habit_id: int):
        for i, habit in enumerate(self.habits_data):
            if habit["habit_id"] == habit_id:
                del self.habits_data[i]
                self.storage.save(self.habits_data)
                return f"Habit - {habit["habit_name"]} removed!"
        return "Habit not found!"

    def complete_habit(self, habit_id: int):
        for i, habit in enumerate(self.habits_data):
            if habit["habit_id"] == habit_id:
                habit["completed"] = True
                message = self.increase_streak()
                self.storage.save(self.habits_data)
                return (f"Habit - '{habit["habit_name"]}' Completed!"
                        f"\n{message}")
        return "Habit not found!"


hs = HabitService(HabitJsonStorage())
# print(hs.create_habit(DailyHabitSchema(habit_name="test",
#                                        habit_description="test",
#                                        category=CategoryHabit.HEALTH)))
print(hs.complete_habit(1))
# print(hs.remove_habit(1))
