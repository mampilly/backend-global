from pydantic import BaseModel
from fastapi.param_functions import Form, Body
from typing import Optional
import datetime


class AverageSentimentTrendOutput(BaseModel):
    date: str
    sentiment_score_percentage: str