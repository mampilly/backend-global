from pydantic import BaseModel


class UserDetailsOutput(BaseModel):
    first_name: str
    username: str
    account_name: str
