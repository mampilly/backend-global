from pydantic import BaseModel
import datetime


class PlatformIndexOutput(BaseModel):
    google_news_platform_index: float
    twitter_platform_index: float
    date: datetime.date
