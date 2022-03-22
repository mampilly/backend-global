import datetime
from typing import List, Optional
from pydantic import BaseModel
    
class EntityDetailsOutput(BaseModel):
    entity_name: str
    entity_alias_name: str
    address_line_1: str
    address_line_2: Optional[str]
    city: Optional[str] = None
    state: Optional[str]
    zip: Optional[str]
    country: Optional[str]
    telephone: Optional[str]
    website: str
    stock_symbol: Optional[str]
    year_founded: Optional[str]
    industry: Optional[str]
    contact_name: Optional[str]
    bsi_score: float
    twitter_handle: Optional[str]