from pydantic import BaseModel
import datetime

class AlertsOutput(BaseModel):
    business_name: str
    date: datetime.date
    title: str
    priority: str
    alert_description: str