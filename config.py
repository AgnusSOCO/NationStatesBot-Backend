import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import tempfile
import os

def create_browser():
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    try:
        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=chrome_options)
        return browser
    except Exception as e:
        print(f"Error setting up ChromeDriver: {e}")
        if 'chrome not installed' in str(e).lower():
            print("Please install Chrome/Chromium browser first")
        raise

browser = create_browser()

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
channel_id = 1141581196745257010  # Replace with your Discord channel ID

# Initialize WebDriverWait
wait = WebDriverWait(browser, 10)
