from pydantic import BaseModel
from typing import Optional


class WatchLevelOutput(BaseModel):
    watch_level:  Optional[str]
