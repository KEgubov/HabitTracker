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

class GoalDaysHabit(int, Enum):
    ONE_DAY = 1
    ONE_WEEK = 7
    TWO_WEEK = 14
    ONE_MONTH = 30
    SIX_MONTHS = 180
    ONE_YEAR = 365


class DailyHabitSchema(BaseModel):
    habit_name: Annotated[str, Field(min_length=1, max_length=500)]
    habit_description: Annotated[str, Field(min_length=1, max_length=500)]
    category: CategoryHabit
    type_habit: TypeHabit = TypeHabit.DAILY

class WeeklyHabitSchema(DailyHabitSchema):
    type_habit: TypeHabit = TypeHabit.WEEKLY
    weekly_streak: Annotated[int, Field(ge=0)]