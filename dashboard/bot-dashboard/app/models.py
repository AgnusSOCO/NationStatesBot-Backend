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

class EconomyData(BaseModel):
    timestamp: datetime
    value: float

class BotSettings(BaseModel):
    auto_answer_dilemmas: bool = True
    navigation_interval: int = 15  # minutes
    max_dilemmas_per_day: int = 10
    preferred_categories: List[str] = ["economy", "military"]
