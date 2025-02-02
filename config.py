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
    logging.info(f"Detecting browser binary on {system}")
    chrome_paths = {
        'Darwin': [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '/Applications/Chromium.app/Contents/MacOS/Chromium',
            '/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta',
            '/Applications/Thorium.app/Contents/MacOS/Thorium'
        ],
        'Windows': [
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files\Thorium\Application\thorium.exe',
            r'C:\Program Files (x86)\Thorium\Application\thorium.exe'
        ],
        'Linux': [
            '/usr/bin/google-chrome',
            '/usr/bin/chromium-browser',
            '/usr/bin/thorium-browser'
        ]
    }
    
    for path in chrome_paths.get(system, []):
        logging.debug(f"Checking browser path: {path}")
        if Path(path).exists():
            logging.info(f"Found browser binary at: {path}")
            return path
            
    supported_browsers = "Chrome, Chromium, or Thorium"
    error_msg = f"Could not find {supported_browsers} binary on {system}. Please install one of: {supported_browsers}"
    logging.error(error_msg)
    raise RuntimeError(error_msg)

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
