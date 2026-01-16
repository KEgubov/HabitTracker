from datetime import datetime
from typing import Optional
from habit_storage.json_storage import HabitJsonStorage
from models.base import DailyHabit, CategoryHabit
from schemas.habit_schema import DailyHabitSchema, GoalDaysHabit


class HabitService:
    def __init__(self, storage: HabitJsonStorage):
        self.storage = storage
        self.habits_data = storage.load()

    def increase_streak(self, habit_id: int) -> str:
        """
        Method:
        Checks the validity of the series.
        Increases the streak by 1.
        Refreshes the target.
        """
        for habit in self.habits_data:
            if habit["habit_id"] == habit_id and habit["completed"]:
                if self.check_streak_validity():
                    habit["streak"] += 1
                    message = self.update_goal_days(habit)
                    habit["last_completed"] = datetime.now().isoformat(
                        timespec="seconds"
                    )
                    habit["completed"] = False
                    return f"\n{message}"
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

    def update_goal_days(self, habit) -> Optional[str]:
        goal_map = {
            1: GoalDaysHabit.ONE_WEEK,
            7: GoalDaysHabit.TWO_WEEK,
            14: GoalDaysHabit.ONE_MONTH,
            30: GoalDaysHabit.SIX_MONTHS,
            180: GoalDaysHabit.ONE_YEAR,
        }
        for days, goal in goal_map.items():
            if habit["streak"] == days:
                habit["goal_days"] = goal
                return f"Congratulations! You've reached your goal! New target - {goal.value} days!"
        return f"Current streak - {habit["streak"]} days"

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

    def remove_all_habits(self):
        return self.storage.clear()

    def complete_habit(self, habit_id: int):
        for habit in self.habits_data:
            if habit["habit_id"] == habit_id:
                habit["completed"] = True
                message = self.increase_streak(habit_id)
                self.storage.save(self.habits_data)
                return f"Habit - '{habit["habit_name"]}' Completed!" f"{message}"
        return "Habit not found!"

    def show_habit(self, habit_id: int):
        for habit in self.habits_data:
            if habit["habit_id"] == habit_id:
                return (
                    f"Habit Information: "
                    f"\nHabit - '{habit["habit_name"]}'"
                    f"\nDescription - '{habit['habit_description']}'"
                    f"\nStreak - {habit['streak']} days"
                    f"\nGoal - {habit['goal_days']} days"
                )
        return result

    def show_all_habits(self):
        if not self.habits_data:
            return f"Habits not found!"
        result = "All Habits:\n"
        for habit in self.habits_data:
            result += (
                f"\nID: {habit['habit_id']} | "
                f"Name: {habit['habit_name']} | "
                f"Category: {habit['category']} | "
                f"Streak: {habit['streak']} days"
            )
        return result
    
    # ДОБАВИТЬ ГРУППИРОВКУ ПО ПРИВЫЧКАМ


hs = HabitService(HabitJsonStorage())
# print(hs.create_habit(DailyHabitSchema(habit_name="test",
#                                        habit_description="test",
#                                        category=CategoryHabit.HEALTH)))
# print(hs.complete_habit(1))
# print(hs.remove_habit(1))
# print(hs.show_habit(1))
