import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import tempfile
import os
import platform
from pathlib import Path

def find_chrome_binary():
    """Find Chrome or Chromium binary path based on platform."""
    system = platform.system()
    chrome_paths = {
        'Darwin': [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '/Applications/Chromium.app/Contents/MacOS/Chromium',
            '/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta'
        ],
        'Windows': [
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        ],
        'Linux': [
            '/usr/bin/google-chrome',
            '/usr/bin/chromium-browser'
        ]
    }
    
    for path in chrome_paths.get(system, []):
        if Path(path).exists():
            return path
            
    raise RuntimeError(f"Could not find Chrome/Chromium binary on {system}. Please install Chrome or Chromium browser.")

def create_browser():
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    try:
        binary_path = find_chrome_binary()
        chrome_options.binary_location = binary_path
        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=chrome_options)
        return browser
    except Exception as e:
        logging.error(f"Error setting up ChromeDriver: {e}")
        if 'chrome not installed' in str(e).lower():
            logging.error("Please install Chrome/Chromium browser first")
        raise

browser = create_browser()

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
channel_id = 1141581196745257010  # Replace with your Discord channel ID

# Initialize WebDriverWait
wait = WebDriverWait(browser, 10)
