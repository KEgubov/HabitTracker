from datetime import datetime, timedelta
from typing import List, Dict
from habit_storage.json_storage import HabitJsonStorage
from models.base import DailyHabit, WeeklyHabit
from schemas.habit_schema import (
    DailyHabitSchema,
    WeeklyHabitSchema,
    GoalDaysHabit,
    AchievementHabit,
    TypeHabit,
)

class HabitService:
    def __init__(self, storage: HabitJsonStorage) -> None:
        self.storage = storage
        self.habits_data: List[Dict] = self.storage.load()

    def _reload(self):
        self.habits_data = self.storage.load()

    def _save(self):
        self.storage.save(self.habits_data)

    def _generate_id(self) -> int:
        self.habits_data = self.storage.load()
        return max(h.get("habit_id", 0) for h in self.habits_data) + 1

    def _streak_increase(self, habit_id: int) -> str:
        today = datetime.now().date()
        today_iso = today.isoformat()
        for habit in self.habits_data:
            if habit["habit_id"] != habit_id:
                continue
            last_iso = habit.get("last_completed")
            if last_iso == today_iso:
                return "The habit has already been completed!"
            if last_iso is None:
                habit["streak"] = 1
            else:
                try:
                    last_date = datetime.fromisoformat(last_iso).date()
                    delta = (today - last_date).days
                    if delta == 1:
                        habit["streak"] += 1
                    elif delta > 1:
                        habit["streak"] = 1
                    else:
                        pass
                except (ValueError, TypeError):
                    habit["streak"] = 1
            habit["last_completed"] = today_iso
            self._update_goal_days(habit)
            self._update_achievements(habit)
            return f"Habit completed! Current streak: {habit['streak']} days."

        return "Habit not found!"

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

    def create_habit(
        self,
        type_habit: TypeHabit,
        daily_schema: DailyHabitSchema,
    ) -> str:
        self._reload()
        if type_habit == TypeHabit.DAILY:
            habit = DailyHabit(
                habit_id=self._generate_id(),
                habit_name=daily_schema.habit_name,
                habit_description=daily_schema.habit_description,
                category=daily_schema.category,
            )
            self.habits_data.append(habit.to_dict())
            self._save()
        return f"Habit - '{daily_schema.habit_name.title()}' added!"

    def create_weekly_habit(
        self,
        type_habit: TypeHabit,
        weekly_schema: WeeklyHabitSchema,
    ) -> str:
        self._reload()
        if type_habit == TypeHabit.WEEKLY:
            habit = WeeklyHabit(
                habit_id=self._generate_id(),
                habit_name=weekly_schema.habit_name,
                habit_description=weekly_schema.habit_description,
                category=weekly_schema.category,
            )
            self.habits_data.append(habit.to_dict())
            self._save()
        return f"Weekly habit - '{weekly_schema.habit_name.title()}' added!"

    def delete_habit(self, habit_id: int) -> str:
        self._reload()
        for i, habit in enumerate(self.habits_data):
            if habit["habit_id"] == habit_id:
                del self.habits_data[i]
                self._save()
                return f"Habit - {habit['habit_name']} removed!"
        return "Habit not found!"

    def delete_all_habits(self):
        return self.storage.clear()

    def complete_habit(self, habit_id: int) -> str:
        self._reload()
        for habit in self.habits_data:
            if habit["habit_id"] == habit_id:
                habit["completed"] = True
                message = self._streak_increase(habit_id)
                self.storage.save(self.habits_data)
                return message
        return "Habit not found!"

    def show_habit(self, habit_id: int) -> str:
        self._reload()
        if not self.habits_data:
            return f"Habits not found!"
        result = "Habit:\n"
        for habit in self.habits_data:
            if habit["type_habit"] == "daily":
                if habit["habit_id"] == habit_id:
                    result += (
                        f"\nID: {habit['habit_id']} | "
                        f"Name: {habit['habit_name'].title()} | "
                        f"Category: {habit['category'].title()} | "
                        f"Streak: {habit['streak']} days | "
                        f"Type: {habit['type_habit'].title()} | "
                    )
            if habit["type_habit"] == "weekly":
                if habit["habit_id"] == habit_id:
                    result += (
                        f"\nID: {habit['habit_id']} | "
                        f"Name: {habit['habit_name'].title()} | "
                        f"Category: {habit['category'].title()} | "
                        f"Streak: {habit['weekly_streak']} weeks | "
                        f"Type: {habit['type_habit'].title()} | "
                    )
        return result

    def show_all_habits(self):
        self._reload()
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
                if habit["type_habit"] == "daily":
                    result += (
                        f"ID: {habit['habit_id']} | "
                        f"Name: {habit['habit_name'].title()} | "
                        f"Streak: {habit['streak']} days |"
                        f" Type: {habit['type_habit'].title()} |\n"
                    )
                if habit["type_habit"] == "weekly":
                    result += (
                        f"ID: {habit['habit_id']} | "
                        f"Name: {habit['habit_name'].title()} | "
                        f"Streak: {habit['weekly_streak']} weeks |"
                        f" Type: {habit['type_habit'].title()} |\n"
                    )
            result += "\n"
        return result.rstrip()

    def show_achievement(self, habit_id: int) -> str | None:
        self._reload()
        if not self.habits_data:
            return f"Habits not found!"
        result = "Achievement:\n"
        for habit in self.habits_data:
            if habit["habit_id"] == habit_id:
                for value in habit["achievement"]:
                    result += f'"{value}"\n'
                return result
        return "Achievement not found!"
