from config import bot, channel_id

on_ready_callback = None
@bot.event
async def send_updates():
    channel = bot.get_channel(channel_id)
    
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

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    await send_updates()  # Call the send_updates function directly
    if on_ready_callback:
        await on_ready_callback()

async def send_message_to_discord(content):
    channel = bot.get_channel(channel_id)
    await channel.send(content)

def set_on_ready(callback):
    global on_ready_callback
    on_ready_callback = callback