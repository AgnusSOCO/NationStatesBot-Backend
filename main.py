from config import bot
from utilities import display_banner, get_user_input, extract_economy_data
from web_automation import login, answer_dilemma, random_navigation
import discord_bot
import asyncio
import random

async def main() -> None:
    display_banner()
    nation_name: str
    password: str
    nation_name, password = get_user_input()
    login(nation_name, password)
    
    while True:
        try:
            await answer_dilemma()
            extract_economy_data(nation_name)
            await asyncio.sleep(random.randint(10, 25))  # Pause to mimic reading time
            await random_navigation()
        except KeyboardInterrupt:
            await bot.close()
            break

if __name__ == "__main__":
    discord_bot.set_on_ready(main)
    bot_token = 'BOT TOKEN HERE'
    bot.run(bot_token)
