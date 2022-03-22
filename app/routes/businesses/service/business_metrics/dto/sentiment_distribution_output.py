from pydantic import BaseModel


class SentimentDistributionOutput(BaseModel):
    sentiment_label: str
    sentiment_score: float
    count: int
    date: str
