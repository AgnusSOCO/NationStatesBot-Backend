from config import Config, logger
from utilities import display_banner, get_user_input, extract_economy_data
from web_automation import login, answer_dilemma, random_navigation
import asyncio
import random
import os

async def main() -> None:
    display_banner()
    nation_name, password = get_user_input()
    login(nation_name, password)
    
    while True:
        try:
            await answer_dilemma()
            extract_economy_data(nation_name)
            await asyncio.sleep(random.randint(10, 25))
            await random_navigation()
        except KeyboardInterrupt:
            if Config.DISCORD_ENABLED:
                from config import bot
                await bot.close()
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            break

if __name__ == "__main__":
    try:
        if os.getenv('DISCORD_TOKEN'):
            Config.DISCORD_ENABLED = True
            Config.DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
            import discord_bot
            from config import bot
            discord_bot.set_on_ready(main)
            bot.run(Config.DISCORD_TOKEN)
        else:
            logger.info("Running without Discord integration")
            asyncio.run(main())
    except Exception as e:
        logger.error(f"Error: {e}")
        raise
