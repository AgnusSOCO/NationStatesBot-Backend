import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Path to Ungoogled-Chromium on OSX
binary_location = '/Applications/Chromium.app/Contents/MacOS/Chromium'

# Path to the Chromium WebDriver
driver_path = '/Users/null/Desktop/nsb-bot/chromedriver_mac_arm64/chromedriver'  # Replace with your path to the chromedriver

# Set up ChromeOptions
chrome_options = Options()
chrome_options.binary_location = binary_location

# Initialize the browser with the specified options
browser = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
channel_id = 1141581196745257010  # Replace with your Discord channel ID

# Initialize WebDriverWait
wait = WebDriverWait(browser, 10)
