import datetime
from typing import List, Optional
from pydantic import BaseModel

class Sentiment(BaseModel):
    label :  Optional[str]
    mixed :  Optional[str]
    score :  Optional[float]
    
class Entities(BaseModel):
    text: Optional[str]
    relevance: Optional[float]
    sentiment: Optional[Sentiment]
    
class EntityDetailsOutput(BaseModel):
    platform : str
    entities : List[Optional[Entities]]
    date :  datetime.date = datetime.date.today()
