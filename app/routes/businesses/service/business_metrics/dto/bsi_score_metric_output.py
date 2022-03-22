from pydantic import BaseModel
import datetime


class BsiScoreMetricOutput(BaseModel):
    bsi_score: float
    date: datetime.date = datetime.date.today()
