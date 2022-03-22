from pydantic import BaseModel
from fastapi.param_functions import Form, Body
from typing import Optional
import datetime


class BsiTrendOutput(BaseModel):
    business_name: str
    bsi_score: float
    date: str