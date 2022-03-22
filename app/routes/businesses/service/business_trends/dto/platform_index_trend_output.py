from pydantic import BaseModel
from fastapi.param_functions import Form, Body
from typing import Optional
import datetime


class PlatformIndexTrendOutput(BaseModel):
    google_news_platform_index: float
    date: str