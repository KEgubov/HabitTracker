from datetime import datetime, timedelta
from schemas.habit_schema import GoalDaysHabit, TypeHabit, CategoryHabit
from typing import Optional


class BaseHabit:
    def __init__(
        self,
        habit_name: str,
        habit_description: str,
        category: CategoryHabit,
        type_habit: TypeHabit,
        completed=False,
    ) -> None:

        self.habit_name = habit_name
        self.habit_description = habit_description
        self.category = category
        self.type_habit = type_habit
        self.completed = completed
        self.created_at = datetime.now()
        self.last_completed: Optional[datetime] = None


class DailyHabit(BaseHabit):
    def __init__(
        self,
        habit_id: int,
        habit_name: str,
        habit_description: str,
        category: CategoryHabit,
    ):
        super().__init__(
            habit_name, habit_description, category, type_habit=TypeHabit.DAILY
        )
        self.habit_id = habit_id
        self.streak = 0
        self.goal_days: GoalDaysHabit = GoalDaysHabit.ONE_DAY

    def increase_streak(self):
        """
        Method:
        Checks the validity of the series.
        Increases the streak by 1.
        Refreshes the target.
        """
        if self.completed:
            self.check_streak_validity()
            self.streak += 1
            self.update_goal_days()
            self.last_completed = datetime.now()
            self.completed = False
        return f"Congratulations! Current streak - {self.streak} days"

    def check_streak_validity(self) -> bool:
        """
        Series Verification
        """
        if not self.last_completed:
            return True

        days_since_last = (datetime.now() - self.last_completed).days
        if days_since_last > 1:
            self.streak = 0
            return False
        return True

    def update_goal_days(self):
        """
        Refreshes the target when a specific streak is reached
        """
        if self.streak == 1:
            self.goal_days = GoalDaysHabit.ONE_WEEK
        elif self.streak == 7:
            self.goal_days = GoalDaysHabit.TWO_WEEK
        elif self.streak == 14:
            self.goal_days = GoalDaysHabit.ONE_MONTH
        elif self.streak == 30:
            self.goal_days = GoalDaysHabit.SIX_MONTHS
        elif self.streak == 180:
            self.goal_days = GoalDaysHabit.ONE_YEAR
        elif self.streak == 365:
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

#  IN DEVELOPMENT
class WeeklyHabit(BaseHabit):
    def __init__(
        self,
        habit_id: int,
        habit_name: str,
        habit_description: str,
        category: CategoryHabit,
    ) -> None:
        super().__init__(
            habit_name, habit_description, category, type_habit=TypeHabit.WEEKLY
        )
        self.habit_id = habit_id
        self.weekly_streak = 0
        self.deadline = self.created_at + timedelta(weeks=1)