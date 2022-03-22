from pydantic import BaseModel
import datetime


class NewsOutput(BaseModel):
    business_name: str
    news_url: str
    sentiment_score: float
    sentiment_label: str
    published_date: datetime.datetime
