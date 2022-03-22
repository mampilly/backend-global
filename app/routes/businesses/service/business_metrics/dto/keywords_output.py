from pydantic import BaseModel
from typing import List
import datetime


class KeywordsOutput(BaseModel):
    platform: str
    date: datetime.date = datetime.date.today()
    keywords: List[str]
