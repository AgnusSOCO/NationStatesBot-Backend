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
    """Find Thorium, Chrome or Chromium binary path based on platform."""
    system = platform.system()
    logging.info(f"Detecting browser binary on {system}")
    
    # Thorium paths - checked first since it's the preferred browser
    thorium_paths = {
        'Darwin': [
            '/Applications/Thorium.app/Contents/MacOS/Thorium',
            '~/Applications/Thorium.app/Contents/MacOS/Thorium',
            '/Users/*/Applications/Thorium.app/Contents/MacOS/Thorium'
        ],
        'Windows': [
            r'%LOCALAPPDATA%\Thorium\Application\thorium.exe',
            r'%PROGRAMFILES%\Thorium\Application\thorium.exe',
            r'%PROGRAMFILES(X86)%\Thorium\Application\thorium.exe',
            r'C:\Program Files\Thorium\Application\thorium.exe',
            r'C:\Program Files (x86)\Thorium\Application\thorium.exe'
        ],
        'Linux': [
            '/usr/bin/thorium-browser',
            '/usr/local/bin/thorium-browser',
            '~/.local/bin/thorium-browser'
        ]
    }
    
    # Chrome/Chromium paths as fallback
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
    
    # Try Thorium paths first
    for path in thorium_paths.get(system, []):
        expanded_path = os.path.expanduser(os.path.expandvars(path))
        # Handle glob patterns for user directories
        if '*' in expanded_path:
            import glob
            potential_paths = glob.glob(expanded_path)
            for p in potential_paths:
                logging.debug(f"Checking Thorium path: {p}")
                if Path(p).exists():
                    logging.info(f"Found Thorium binary at: {p}")
                    return p
        else:
            logging.debug(f"Checking Thorium path: {expanded_path}")
            if Path(expanded_path).exists():
                logging.info(f"Found Thorium binary at: {expanded_path}")
                return expanded_path
    
    logging.info("Thorium not found, checking Chrome/Chromium paths")
    
    # Fallback to Chrome/Chromium paths
    for path in chrome_paths.get(system, []):
        expanded_path = os.path.expanduser(os.path.expandvars(path))
        logging.debug(f"Checking Chrome/Chromium path: {expanded_path}")
        if Path(expanded_path).exists():
            logging.info(f"Found Chrome/Chromium binary at: {expanded_path}")
            return expanded_path
            
    error_msg = (
        f"Could not find any supported browser on {system}.\n"
        "Please install one of:\n"
        "- Thorium (preferred): https://thorium.rocks/\n"
        "- Google Chrome: https://www.google.com/chrome/\n"
        "- Chromium: https://www.chromium.org/getting-involved/download-chromium"
    )
    logging.error(error_msg)
    raise RuntimeError(error_msg)

def get_browser_version(binary_path):
    import subprocess
    import re
    
    try:
        result = subprocess.check_output([binary_path, '--product-version'], 
                                      stderr=subprocess.STDOUT,
                                      timeout=5)
        version = result.decode('utf-8').strip()
        if version:
            return version
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        try:
            result = subprocess.check_output([binary_path, '--version'], 
                                          stderr=subprocess.STDOUT,
                                          timeout=5)
            version = result.decode('utf-8')
            match = re.search(r'(\d+\.\d+\.\d+\.\d+)', version)
            if match:
                return match.group(1)
        except Exception:
            pass
    return None

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
        
        browser_version = get_browser_version(binary_path)
        if not browser_version:
            raise RuntimeError("Could not determine browser version")
            
        major_version = browser_version.split('.')[0]
        logging.info(f"Detected browser version: {browser_version}")
        
        # Use driver_version parameter to match ChromeDriver with browser version
        service = Service(ChromeDriverManager(driver_version=major_version).install())
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
