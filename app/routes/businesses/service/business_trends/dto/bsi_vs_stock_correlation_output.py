from pydantic import BaseModel
from fastapi.param_functions import Form, Body
from typing import Optional
import datetime


class CorrelationTrendOutput(BaseModel):
    same_day_correlation: float = None
    next_day_correlation: float = None
    seven_day_correlation: float = None
    fourteen_day_correlation: float = None
    thirty_day_correlation: float = None