from pydantic import BaseModel


class PublicPerceptionOutput(BaseModel):
    Joy: str
    Anger: str
    Disgust: str
    Fear: str
    Sadness: str
