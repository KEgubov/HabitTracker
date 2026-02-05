from datetime import datetime, timedelta, date
from typing import List, Dict
from habit_storage.json_storage import HabitJsonStorage
from models.base import DailyHabit, WeeklyHabit
from schemas.habit_schema import (
    DailyHabitSchema,
    WeeklyHabitSchema,
    GoalDaysHabit,
    AchievementHabit,
    TypeHabit,
    AchievementWeeklyHabit,
    GoalWeeklyHabit,
)


class HabitService:
    """Service class for managing habits: creation, deletion, completion, and display."""

    def __init__(self, storage: HabitJsonStorage) -> None:
        """
        Initialize the HabitService with a storage backend.

        Args:
            storage (HabitJsonStorage): Storage instance used to persist habits.
        """
        self.storage = storage
        self.habits_data: List[Dict] = self.storage.load()

    def _reload(self) -> None:
        """Reload habits data from storage."""
        self.habits_data = self.storage.load()

    def _save(self) -> None:
        """Save current habits data to storage."""
        self.storage.save(self.habits_data)

    def _generate_id(self) -> int:
        """
        Generate a new unique habit ID.

        Returns:
            int: The next available habit ID (starts from 1 if empty).
        """
        self.habits_data = self.storage.load()
        if not self.habits_data:
            return 1
        return max(h.get("habit_id", 0) for h in self.habits_data) + 1

    def _streak_increase(self, habit_id: int) -> str | None:
        """
        Increase the streak for a daily habit if completed today.

        Handles streak logic, goal updates, and achievement unlocking.

        Args:
            habit_id (int): ID of the habit to update.

        Returns:
            str | None: Success message with streak/goal/achievement info,
                        or error message, or None if habit not found.
        """
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
            messages = []

            update_goal_message = self._update_goal_days(habit)
            if update_goal_message:
                messages.append(update_goal_message)

            update_achievement_message = self._update_achievements(habit)
            if update_achievement_message:
                messages.append(update_achievement_message)

            if messages:
                return "\n".join(messages)
            else:
                return f"Habit completed! Current streak - {habit['streak']} days"
        return None

    def _check_weekly_deadline(self, habit: dict, today: date) -> tuple[int, str]:
        """
        Check if the weekly deadline has passed and determine new streak value.

        Args:
            habit (dict): Habit data dictionary.
            today (date): Current date.

        Returns:
            tuple[int, str]: (new_streak_value, message)
        """
        deadline_iso = habit.get("deadline")

        if not deadline_iso:
            return 1, "Weekly streak started!"

        try:
            deadline_date = datetime.fromisoformat(deadline_iso).date()

            if today > deadline_date:
                return 1, "Weekly streak reset - missed the deadline!"
            else:
                return (
                    habit.get("weekly_streak", 0) + 1,
                    f"Weekly streak increased to {habit.get('weekly_streak', 0) + 1}!",
                )

        except (ValueError, TypeError):
            return 1, "Data parsing error. Weekly streak reset to 1."

    def _weekly_streak_increase(self, habit_id: int) -> str | None:
        """
        Increase the weekly streak and update deadline for a weekly habit.

        Also handles goal and achievement updates.

        Args:
            habit_id (int): ID of the weekly habit.

        Returns:
            str | None: Message about streak update, new deadline, goals/achievements,
                        or error message, or None if not found.
        """
        today = datetime.now().date()
        today_iso = today.isoformat()

        for habit in self.habits_data:
            if habit["habit_id"] != habit_id:
                continue

            if habit.get("last_completed") == today_iso:
                return "The habit has already been completed today!"

            new_streak, streak_message = self._check_weekly_deadline(habit, today)
            habit["weekly_streak"] = new_streak

            new_deadline = today + timedelta(weeks=1)
            habit["deadline"] = new_deadline.isoformat()

            habit["last_completed"] = today_iso

            messages = [
                streak_message,
                f"New deadline: {new_deadline.strftime('%Y-%m-%d')}",
            ]

            if goal_msg := self._update_weekly_goal_days(habit):
                messages.append(goal_msg)

            if achievement_msg := self._update_weekly_achievements(habit):
                messages.append(achievement_msg)

            return "\n".join(messages)

        return None

    def _update_goal_days(self, habit: dict) -> str | None:
        """
        Check if current daily streak matches any goal milestone and update it.

        Args:
            habit (dict): Habit data dictionary.

        Returns:
            str | None: Congratulation message if a new goal was reached, else None.
        """
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
        return None

    def _update_weekly_goal_days(self, habit: dict) -> str | None:
        """
        Check if current weekly streak matches any weekly goal milestone.

        Args:
            habit (dict): Habit data dictionary.

        Returns:
            str | None: Congratulation message if a new goal was reached, else None.
        """
        goal_map = {
            1: GoalWeeklyHabit.ONE_MONTH,
            4: GoalWeeklyHabit.TWO_MONTHS,
            8: GoalWeeklyHabit.SIX_MONTHS,
            45: GoalWeeklyHabit.ONE_YEAR,
        }
        for weeks, goal in goal_map.items():
            if habit["weekly_streak"] == weeks:
                habit["current_goal_weeks"] = goal
                return (
                    f"Congratulations! You've reached your goal! "
                    f"New target - {goal.value} weeks!"
                )
        return None

    def _update_achievements(self, habit: dict) -> str | None:
        """
        Check and award new daily achievements based on current streak.

        Args:
            habit (dict): Habit data dictionary.

        Returns:
            str | None: Message about new achievement, or None if none awarded.
        """
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
                if achievement in habit["achievement"]:
                    return None
                habit["achievement"].append(achievement.value)
                return f"You have received a new achievement - {achievement.value}!"
        return None

    def _update_weekly_achievements(self, habit: dict) -> str | None:
        """
        Check and award new weekly achievements based on current weekly streak.

        Args:
            habit (dict): Habit data dictionary.

        Returns:
            str | None: Message about new weekly achievement, or None if none.
        """
        achievement_map = {
            1: AchievementWeeklyHabit.ONE_WEEK,
            4: AchievementWeeklyHabit.ONE_MONTH,
            8: AchievementWeeklyHabit.TWO_MONTHS,
            45: AchievementWeeklyHabit.SIX_MONTHS,
            91: AchievementWeeklyHabit.ONE_YEAR,
        }
        for days, achievement in achievement_map.items():
            if habit["weekly_streak"] == days:
                if achievement in habit["achievement"]:
                    return None
                habit["achievement"].append(achievement.value)
                return (
                    f"You have received a new weekly achievement - {achievement.value}!"
                )
        return None

    def create_habit(
        self,
        type_habit: TypeHabit,
        daily_schema: DailyHabitSchema,
    ) -> str:
        """
        Create a new daily habit.

        Args:
            type_habit (TypeHabit): Must be TypeHabit.DAILY
            daily_schema (DailyHabitSchema): Validated habit input data

        Returns:
            str: Success message with habit name
        """
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
        """
        Create a new weekly habit.

        Args:
            type_habit (TypeHabit): Must be TypeHabit.WEEKLY
            weekly_schema (WeeklyHabitSchema): Validated habit input data

        Returns:
            str: Success message with habit name
        """
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
        """
        Delete a habit by its ID.

        Args:
            habit_id (int): ID of the habit to delete

        Returns:
            str: Success message or "Habit not found!"
        """
        self._reload()
        for i, habit in enumerate(self.habits_data):
            if habit["habit_id"] == habit_id:
                del self.habits_data[i]
                self._save()
                return f"Habit - {habit['habit_name']} removed!"
        return "Habit not found!"

    def delete_all_habits(self):
        """
        Delete all habits from storage.

        Returns:
            str: Confirmation message from storage
        """
        return self.storage.clear()

    def complete_habit(self, habit_id: int) -> str:
        """
        Mark a habit as completed for today and update streak/goals/achievements.

        Args:
            habit_id (int): ID of the habit to complete

        Returns:
            str: Result message (streak info, achievements, errors, etc.)
        """
        self._reload()
        for habit in self.habits_data:
            if habit["type_habit"] == "daily":
                if habit["habit_id"] == habit_id:
                    habit["completed"] = True
                    message = self._streak_increase(habit_id)
                    self.storage.save(self.habits_data)
                    return message
            if habit["type_habit"] == "weekly":
                if habit["habit_id"] == habit_id:
                    habit["completed"] = True
                    message = self._weekly_streak_increase(habit_id)
                    self.storage.save(self.habits_data)
                    return message
        return "Habit not found!"

    def show_habit(self, habit_id: int) -> str:
        """
        Return formatted string with details of a single habit.

        Args:
            habit_id (int): ID of the habit to display

        Returns:
            str: Formatted habit info or "Habit not found!"
        """
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

    def show_all_habits(self) -> str:
        """
        Return formatted string with all habits grouped by category.

        Returns:
            str: Multi-line string with categorized habits
        """
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
        """
        Return all achievements earned for a specific habit.

        Args:
            habit_id (int): ID of the habit

        Returns:
            str: List of achievements or error message
        """
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

    def show_all_achievements(self):
        """
        Return a list of all achievements earned across all habits.

        Returns:
            str: Formatted string with all unique achievements
        """
        self._reload()
        if not self.habits_data:
            return f"Habits not found!"
        result = "All achievements:\n"
        achievement = []
        for habit in self.habits_data:
            if habit.get("achievement"):
                achievement.extend(habit.get("achievement"))
        for element in achievement:
            result += f'\n"{element}"'
        return result