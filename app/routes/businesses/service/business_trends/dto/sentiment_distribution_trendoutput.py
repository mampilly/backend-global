from pydantic import BaseModel
from fastapi.param_functions import Form, Body
from typing import Optional
import datetime


class SentimentDistributionTrendOutput(BaseModel):
    date: str
    sentiment_distribution_percentage: str
    article_count: int
    total_articles: int