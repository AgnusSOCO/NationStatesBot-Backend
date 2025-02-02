from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class BotStatus(BaseModel):
    version: str = "1.1.2"
    is_running: bool
    last_activity: datetime
    nation_name: Optional[str]

class BotConfig(BaseModel):
    nation_name: str
    password: str
    chrome_path: str
    driver_path: str

class BotLog(BaseModel):
    timestamp: datetime
    message: str
    type: str  # "dilemma", "navigation", "error"
