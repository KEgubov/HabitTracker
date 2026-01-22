from datetime import datetime
from habit_storage.json_storage import HabitJsonStorage
from models.base import DailyHabit
from schemas.habit_schema import (
    DailyHabitSchema,
    GoalDaysHabit,
    AchievementHabit,
)


class HabitService:
    def __init__(self, storage: HabitJsonStorage) -> None:
        self.storage = storage
        self.habits_data = storage.load()

    def _increase_streak(self, habit_id: int) -> str:
        """
        Method:
        Checks the validity of the series.
        Increases the streak by 1.
        Refreshes the target.
        """
        for habit in self.habits_data:
            if habit["habit_id"] == habit_id and habit["completed"]:
                if self._check_streak_validity():
                    habit["streak"] += 1

                    messages = []
                    message_achievement = self._update_achievements(habit)
                    if message_achievement:
                        messages.append(message_achievement)

                    message_goal_days = self._update_goal_days(habit)
                    if message_goal_days:
                        messages.append(message_goal_days)

                    habit["last_completed"] = datetime.now().isoformat(
                        timespec="seconds"
                    )
                    habit["completed"] = False
                    if messages:
                        return "\n".join(messages)
        return ""

    def _check_streak_validity(self) -> bool:
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
                habit["streak"] = 0
                return False
        return True

    def _update_goal_days(self, habit: dict) -> str:
        goal_map = {
            1: GoalDaysHabit.ONE_WEEK,
            7: GoalDaysHabit.THREE_WEEKS,
            21: GoalDaysHabit.ONE_MONTH,
            30: GoalDaysHabit.TWO_MONTHS,
            60: GoalDaysHabit.SIX_MONTHS,
            180: GoalDaysHabit.ONE_YEAR,
        }
        for days, goal in goal_map.items():
            if habit["streak"] == days:
                habit["current_goal_days"] = goal
                return (
                    f"Congratulations! You've reached your goal! "
                    f"New target - {goal.value} days!"
                )
        return f"Current streak - {habit['streak']} days"

    def _update_achievements(self, habit: dict) -> str | None:
        achievement_map = {
            1: AchievementHabit.ONE_DAY,
            7: AchievementHabit.ONE_WEEK,
            21: AchievementHabit.THREE_WEEKS,
            30: AchievementHabit.ONE_MONTH,
            60: AchievementHabit.TWO_MONTHS,
            180: AchievementHabit.SIX_MONTHS,
            365: AchievementHabit.ONE_YEAR,
        }
        for days, achievement in achievement_map.items():
            if habit["streak"] == days:
                habit["achievement"].append(achievement)
                return f"You have received a new achievement - {achievement.value}!"
        return None

    def generate_id(self) -> int:
        if self.habits_data:
            try:
                max_id = max(habit.get("habit_id", 0) for habit in self.habits_data)
                next_id = max_id + 1
            except (ValueError, KeyError):
                next_id = 1
        else:
            next_id = 1
        return next_id

    def create_habit(self, habit_schema: DailyHabitSchema) -> str:
        habit = DailyHabit(
            habit_id=self.generate_id(),
            habit_name=habit_schema.habit_name,
            habit_description=habit_schema.habit_description,
            category=habit_schema.category,
        )
        self.habits_data.append(habit.to_dict())
        self.storage.save(self.habits_data)
        return f"Habit - '{habit_schema.habit_name.title()}' added!"

    def delete_habit(self, habit_id: int) -> str:
        for i, habit in enumerate(self.habits_data):
            if habit["habit_id"] == habit_id:
                del self.habits_data[i]
                self.storage.save(self.habits_data)
                return f"Habit - {habit['habit_name']} removed!"
        return "Habit not found!"

    def delete_all_habits(self):
        return self.storage.clear()

    def complete_habit(self, habit_id: int) -> str:
        for habit in self.habits_data:
            if habit["habit_id"] == habit_id:
                habit["completed"] = True
                message = self._increase_streak(habit_id)
                self.storage.save(self.habits_data)
                if message:
                    return f"Habit - '{habit['habit_name']}' Completed!\n{message}"
                else:
                    return f"Habit - '{habit['habit_name']}' Completed!"

        return "Habit not found!"

    def show_habit(self, habit_id: int) -> str:
        if not self.habits_data:
            return f"Habits not found!"
        result = "Habit:\n"
        for habit in self.habits_data:
            if habit["habit_id"] == habit_id:
                result += (
                    f"\nID: {habit['habit_id']} | "
                    f"Name: {habit['habit_name']} | "
                    f"Category: {habit['category']} | "
                    f"Streak: {habit['streak']} days"
                )
        return result

    def show_all_habits(self):
        category = {}
        for habit in self.habits_data:
            cat = habit["category"]
            if cat not in category:
                category[cat] = []
            category[cat].append(habit)

        result = ""
        for cat, habits in category.items():
            result += f"Category: {cat.title()}\n"
            for habit in habits:
                result += (
                    f"  ID: {habit['habit_id']} | "
                    f"Name: {habit['habit_name']} | "
                    f"Streak: {habit['streak']} days\n"
                )
            result += "\n"
        return result.rstrip()

    def show_achievement(self, habit_id: int) -> str:
        if not self.habits_data:
            return f"Habits not found!"
        result = "Achievement:\n"
        for habit in self.habits_data:
            if habit["habit_id"] == habit_id:
                for value in habit["achievement"]:
                    result += f'"{value}"\n'
                return result
        return "Achievement not found!"
