from pydantic import BaseModel


class BusinessDetailsOutput(BaseModel):
    business_name: str
    business_alias_name: str
    address_line_1: str 
    address_line_2: str = None
    city: str = None
    state: str = None
    zip: str = None
    country: str = None
    telephone: str = None
    website: str = None
    stock_symbol: str = None
    year_founded: str = None
    industry: str = None
    contact_name: str = None
    bsi_score: float = None
    twitter_handle: str = None
