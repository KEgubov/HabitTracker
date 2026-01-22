from datetime import datetime, timedelta
from schemas.habit_schema import GoalDaysHabit, TypeHabit, CategoryHabit


class BaseHabit:
    def __init__(
        self,
        habit_name: str,
        habit_description: str,
        category: CategoryHabit,
        type_habit: TypeHabit,
        completed: bool = False,
    ) -> None:
        self.habit_name = habit_name
        self.habit_description = habit_description
        self.category = category
        self.type_habit = type_habit
        self.completed = completed
        self.created_at = datetime.now()
        self.last_completed = None  # FIX ME


class DailyHabit(BaseHabit):
    def __init__(
        self,
        habit_id: int,
        habit_name: str,
        habit_description: str,
        category: CategoryHabit,
        streak: int = 0,
        current_goal_days: GoalDaysHabit = GoalDaysHabit.ONE_DAY,
    ) -> None:
        super().__init__(
            habit_name,
            habit_description,
            category,
            type_habit=TypeHabit.DAILY,
        )
        self.habit_id = habit_id
        self.streak = streak
        self.current_goal_days = current_goal_days
        self.achievement = []

    def to_dict(self) -> dict:
        return {
            "habit_id": self.habit_id,
            "habit_name": self.habit_name,
            "habit_description": self.habit_description,
            "category": self.category,
            "type_habit": self.type_habit,
            "completed": self.completed,
            "streak": self.streak,
            "current_goal_days": self.current_goal_days,
            "created_at": self.created_at.isoformat(timespec="seconds"),
            "last_completed": self.last_completed,  # FIX ME
            "achievement": self.achievement,
        }


#  IN DEVELOPMENT
class WeeklyHabit(BaseHabit):
    def __init__(
        self,
        habit_id: int,
        habit_name: str,
        habit_description: str,
        category: CategoryHabit,
        weekly_streak: int = 0,
    ) -> None:
        super().__init__(
            habit_name,
            habit_description,
            category,
            type_habit=TypeHabit.WEEKLY,
        )
        self.habit_id = habit_id
        self.weekly_streak = weekly_streak
        self.deadline = self.created_at + timedelta(weeks=1)
