from datetime import datetime, timedelta


class BaseHabit:
    def __init__(self, habit_name: str, habit_description: str, category: str,
                 completed=False) -> None:
        self.habit_name = habit_name
        self.habit_description = habit_description
        self.category = category
        self.completed = completed


# self.completed по умолчанию False, как только user отмечает привычку выполненной
# в self.streak значение меняется с 0 на 1. if self.completed == True, self.streak += 1


class DailyHabit(BaseHabit):
    def __init__(
        self,
        habit_id: int,
        habit_name: str,
        habit_description: str,
        category: str,
        goal_days: int,
    ):
        super().__init__(habit_name, habit_description, category)
        self.habit_id = habit_id
        self.streak = 0
        # в self.goal_days тоже можно сделать разделение через Enum
        # например: 7дн, 14дн, 30дн и т.д, возможно цель будет ставиться автоматически
        # например при достижении 7 дней, цель становится сразу 14 дней и т.д
        # например: если стрик равен 7, то self.goal_days == 14
        # можно добавить систему ачивок при достижении цели (self.goal_days)
        self.goal_days = goal_days
        self.created_at = datetime.now()


class WeeklyHabit(BaseHabit):
    def __init__(
        self, habit_id: int, habit_name: str, habit_description: str, category: str
    ) -> None:
        super().__init__(habit_name, habit_description, category)
        self.habit_id = habit_id
        self.weekly_streak = 0
        self.created_at = datetime.now()
        self.deadline = self.created_at + timedelta(weeks=1)
