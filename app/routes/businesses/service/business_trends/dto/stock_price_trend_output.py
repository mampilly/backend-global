from pydantic import BaseModel
from fastapi.param_functions import Form, Body
from typing import Optional
import datetime


class StockPriceTrendOutput(BaseModel):
    date: str
    bsi_score: float
    stock_price: float = None