from pydantic import BaseModel, Field
from typing import Annotated
from enum import Enum

class CategoryHabit(Enum):
    HEALTH = "health"
    PRODUCTIVITY = "productivity"
    SPORTS = "sports"
    SELF_DEVELOPMENT = "self development"
    FINANCE = "finance"

class GoalDaysHabit(Enum):
    ONE_DAY = 1
    ONE_WEEK = 7
    TWO_WEEK = 14
    ONE_MONTH = 30
    SIX_MONTHS = 180
    ONE_YEAR = 365

class DailyHabitSchema(BaseModel):
    habit_id: Annotated[int, Field(ge=0)]
    streak: Annotated[int, Field(ge=0)]
    habit_name: Annotated[str, Field(min_length=1, max_length=500)]
    habit_description: Annotated[str, Field(min_length=1, max_length=500)]
    category: Annotated[CategoryHabit, Field(min_length=1, max_length=500)]
    goal_days: Annotated[GoalDaysHabit, Field(min_length=1, max_length=500)]

class WeeklyHabitSchema(DailyHabitSchema):
    weekly_streak: Annotated[int, Field(ge=0)]