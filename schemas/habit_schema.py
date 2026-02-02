from pydantic import BaseModel, Field
from typing import Annotated
from enum import Enum

class TypeHabit(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"

class CategoryHabit(str, Enum):
    HEALTH = "health"
    PRODUCTIVITY = "productivity"
    SPORTS = "sports"
    SELF_DEVELOPMENT = "self development"
    FINANCE = "finance"
    OTHER = "other"

class GoalDaysHabit(int, Enum):
    ONE_DAY = 1
    ONE_WEEK = 7
    THREE_WEEKS = 21
    ONE_MONTH = 30
    TWO_MONTHS = 60
    SIX_MONTHS = 180
    ONE_YEAR = 365

class GoalWeeklyHabit(int, Enum):
    ONE_WEEK = 1
    ONE_MONTH = 4
    TWO_MONTHS = 8
    SIX_MONTHS = 24
    ONE_YEAR = 52

class AchievementHabit(str, Enum):
    ONE_DAY = "I started – and this is a victory!"
    ONE_WEEK = "Willpower Week"
    THREE_WEEKS = "21 days - the habit has taken root!"
    ONE_MONTH = "30 days – I can do more!"
    TWO_MONTHS = "Two months without failures is discipline!"
    SIX_MONTHS = "180 Days of Power"
    ONE_YEAR = "365 days – I did it!"

class AchievementWeeklyHabit(str, Enum):
    ONE_WEEK = "A week in action, you're in the game!"
    ONE_MONTH = "A month without breakdowns - you are no longer what you were"
    TWO_MONTHS = "Two months without failures is discipline!"
    SIX_MONTHS = "Six months - you are not a hero on a schedule, you are a hero on life"
    ONE_YEAR = "A Year Without Stops – You've Created a Legend from Your Discipline"

class DailyHabitSchema(BaseModel):
    habit_name: Annotated[str, Field(min_length=1, max_length=500)]
    habit_description: Annotated[str, Field(min_length=1, max_length=500)]
    category: CategoryHabit
    type_habit: TypeHabit = TypeHabit.DAILY

class WeeklyHabitSchema(DailyHabitSchema):
    type_habit: TypeHabit = TypeHabit.WEEKLY