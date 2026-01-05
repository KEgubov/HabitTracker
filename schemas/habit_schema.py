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
    ONE_DAY = "one-day"
    SEVEN_DAYS = "7 days"
    TWO_WEEK = "2 weeks"
    ONE_MONTH = "1 month"
    SIX_MONTHS = "6 months"
    ONE_YEAR = "1 year"
