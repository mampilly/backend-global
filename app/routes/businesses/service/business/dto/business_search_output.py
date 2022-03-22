from typing import Optional
from pydantic import BaseModel


class BusinessSearchOutput(BaseModel):
    id: Optional[int] = None
    business_name: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None
    fax: Optional[str] = None
    telephone: Optional[str] = None
    website: Optional[str] = None
    stock_symbol: Optional[str] = None
