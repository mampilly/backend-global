import datetime
from typing import List
from pydantic import BaseModel


class MediaTopicsOutput(BaseModel):
    platform: str
    date: datetime.date
    media_topics: List[str]
