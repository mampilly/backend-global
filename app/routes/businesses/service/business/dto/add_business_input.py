from pydantic import BaseModel
from fastapi.param_functions import Body
from typing import Optional

class AddBusinessInput(BaseModel):
        business_name: str = None
        website: str
        type: str = Body(..., enum=["Public" , "Private"])
        year_founded:  Optional[int]
        industry: Optional[str]
        stock_symbol: Optional[str]
        address_line_1: str 
        address_line_2: Optional[str] 
        city: Optional[str]
        state: Optional[str]
        zip: Optional[int] 
        country: Optional[str] 
        contact_name: Optional[str] 
        telephone: Optional[str] 
        twitter_handle: Optional[str] 
        business_alias_name : Optional[str] 
        additional_notes: Optional[str] 