
from typing import List
from pydantic import BaseModel
import datetime


class RedFlagOutput(BaseModel):
    business_name: str
    redflags: List[str]
    date: datetime.datetime
