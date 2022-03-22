from pydantic import BaseModel
from fastapi.param_functions import Form, Body
from typing import Optional
import datetime


class WatchLevelTrendOutput(BaseModel):
    business_name: str
    watch_level: Optional[str]
    date: str