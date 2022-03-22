from pydantic import BaseModel


class AverageSenetimentOutput(BaseModel):
    sentiment_score: float
    date: str
