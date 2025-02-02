from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List, Optional
from .models import BotStatus, BotConfig, BotLog, EconomyData, DilemmaStatistics, BotSettings

app = FastAPI()

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# In-memory storage
bot_status = BotStatus(
    is_running=False,
    last_activity=datetime.now(),
    nation_name=None
)
bot_logs: List[BotLog] = []
bot_config: Optional[BotConfig] = None

@app.get("/api/status")
async def get_status():
    return bot_status

@app.post("/api/start")
async def start_bot():
    global bot_status
    bot_status.is_running = True
    bot_status.last_activity = datetime.now()
    bot_logs.append(BotLog(
        timestamp=datetime.now(),
        message="Bot started",
        type="navigation"
    ))
    return bot_status

@app.post("/api/stop")
async def stop_bot():
    global bot_status
    bot_status.is_running = False
    bot_status.last_activity = datetime.now()
    bot_logs.append(BotLog(
        timestamp=datetime.now(),
        message="Bot stopped",
        type="navigation"
    ))
    return bot_status

@app.get("/api/logs")
async def get_logs():
    return bot_logs

@app.post("/api/config")
async def update_config(config: BotConfig):
    global bot_config, bot_status
    bot_config = config
    bot_status.nation_name = config.nation_name
    return bot_config

@app.get("/api/economy")
async def get_economy_data():
    data = []
    try:
        with open("economy_data.txt", "r") as file:
            for line in file:
                nation, value = line.strip().split(": ")
                data.append(EconomyData(
                    timestamp=datetime.now(),
                    value=float(value)
                ))
    except FileNotFoundError:
        pass
    return data

@app.get("/api/settings")
async def get_settings():
    return BotSettings()

@app.post("/api/settings")
async def update_settings(settings: BotSettings):
    return settings

@app.get("/api/dilemma-stats")
async def get_dilemma_stats():
    dilemma_logs = [log for log in bot_logs if log.type == "dilemma"]
    total = len(dilemma_logs)
    
    choices: Dict[str, int] = {}
    categories: Dict[str, int] = {}
    
    for log in dilemma_logs:
        if match := re.search(r'Choice: (\d+)', log.message):
            choice = match.group(1)
            choices[choice] = choices.get(choice, 0) + 1
            
        if match := re.search(r'Category: (\w+)', log.message):
            category = match.group(1)
            categories[category] = categories.get(category, 0) + 1
    
    return DilemmaStatistics(
        total=total,
        choices=choices,
        categories=categories
    )

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
