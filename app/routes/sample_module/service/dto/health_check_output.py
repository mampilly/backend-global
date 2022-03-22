from pydantic import BaseModel
from fastapi.param_functions import Form, Body


class HealthCheckOutput(BaseModel):
    message: str
