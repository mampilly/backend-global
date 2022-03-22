from pydantic import BaseModel
from fastapi.param_functions import Form, Body
from typing import Optional
import datetime


class RedflagTrendOutput(BaseModel):
    business_name: str
    date: str
    redflags: dict