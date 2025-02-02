import os
import discord
from discord.ext import commands
from config import Config, logger

# Initialize Discord bot only if enabled
if Config.DISCORD_ENABLED:
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)
    channel_id = int(os.getenv('DISCORD_CHANNEL_ID', '0'))
else:
    bot = None
    channel_id = None

on_ready_callback = None

async def send_updates():
    if not Config.DISCORD_ENABLED:
        return
    channel = bot.get_channel(channel_id)
    if not channel:
        logger.error(f"Discord channel {channel_id} not found")
        return
    
    banner = """
       🌎 **NationStatesBot**
       
       *Not Affiliated With NationStates.Net™️*
       ~~~~~
       👨‍💻 Version: 1.1.2
       ~~~~~
       📝 Author: https://github.com/elalfa1

       Searching For Dilemmas To Solve...🔎
    """
    
    await channel.send(banner)

if Config.DISCORD_ENABLED:
    @bot.event
    async def on_ready():
        logger.info(f'Logged in as {bot.user.name} ({bot.user.id})')
        await send_updates()
        if on_ready_callback:
            await on_ready_callback()

async def send_message_to_discord(content: str) -> None:
    if not Config.DISCORD_ENABLED:
        logger.info(f"Discord disabled, message not sent: {content}")
        return
    channel = bot.get_channel(channel_id)
    if not channel:
        logger.error(f"Discord channel {channel_id} not found")
        return
    await channel.send(content)

def set_on_ready(callback):
    if not Config.DISCORD_ENABLED:
        callback()
        return
    global on_ready_callback
    on_ready_callback = callback
