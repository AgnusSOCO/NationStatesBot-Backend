import platform
import g4f
from g4f.Provider import GetGpt, You
from config import wait, find_chrome_binary, get_browser_version, Config, logger
from typing import Dict, Any, List
from datetime import datetime
from selenium.webdriver.common.by import By

def get_ai_provider():
    """Get the appropriate AI provider based on the platform."""
    if platform.system() == "Windows":
        return You  # Browser-based provider for Windows
    return GetGpt  # Default provider for other platforms
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep
import random

def create_browser(max_retries=3):
    """Create a new browser instance with platform-specific automation."""
    import subprocess
    import psutil
    import socket
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    if platform.system() != "Darwin":
        import undetected_chromedriver as uc
    
    def find_free_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
    
    # Kill any existing browser processes
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if any(name in proc.info['name'].lower() 
                  for name in ['chrome', 'chromium', 'thorium', 'chromedriver']):
                psutil.Process(proc.info['pid']).terminate()
                logger.info(f"Terminated browser process: {proc.info['name']}")
    except Exception as e:
        logger.warning(f"Error cleaning up processes: {e}")
    
    sleep(2)  # Wait for processes to clean up
    
    for attempt in range(max_retries):
        service = None
        browser = None
        try:
            logger.info(f"Browser creation attempt {attempt + 1}/{max_retries}")
            
            binary_path = find_chrome_binary()
            logger.info(f"Using browser binary: {binary_path}")
            
            browser_version = get_browser_version(binary_path)
            major_version = browser_version.split('.')[0]
            logger.info(f"Using browser version {browser_version} (major: {major_version})")
            
            # Use major version for ChromeDriver
            driver_path = ChromeDriverManager(driver_version=major_version).install()
            logger.info(f"Using ChromeDriver from: {driver_path}")
            
            # Configure browser options
            if platform.system() == "Darwin":
                options = webdriver.ChromeOptions()
            else:
                options = uc.ChromeOptions()
                
            options.binary_location = binary_path
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-notifications')
            options.add_argument('--disable-popup-blocking')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--disable-blink-features=AutomationControlled')
            
            # Use a specific port to avoid conflicts
            port = find_free_port()
            service = Service(
                executable_path=driver_path,
                port=port,
                service_args=['--verbose']
            )
            
            if platform.system() == "Darwin":  # macOS
                logger.info("Creating Chrome instance with selenium-stealth...")
                browser = webdriver.Chrome(service=service, options=options)
                from selenium_stealth import stealth
                stealth(
                    browser,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                )
            else:
                logger.info("Creating undetected-chromedriver instance...")
                browser = uc.Chrome(
                    driver_executable_path=driver_path,
                    options=options,
                    version_main=int(major_version),
                    service=service
                )
            
            # Configure timeouts
            browser.set_page_load_timeout(30)
            browser.implicitly_wait(10)
            
            # Test browser connection
            max_test_retries = 3
            for test_attempt in range(max_test_retries):
                try:
                    logger.info(f"Testing browser connection (attempt {test_attempt + 1})...")
                    browser.get('https://www.example.com')
                    # Force a command to verify connection
                    browser.title
                    logger.info("Browser connection verified")
                    return browser
                except Exception as test_e:
                    if test_attempt == max_test_retries - 1:
                        raise
                    logger.warning(f"Browser test failed: {test_e}")
                    sleep(2)
                    
        except Exception as e:
            logger.error(f"Browser creation failed: {e}")
            if browser:
                try:
                    browser.quit()
                except:
                    pass
            if service:
                try:
                    service.stop()
                except:
                    pass
            if attempt == max_retries - 1:
                raise
            sleep(3)
            
            if attempt == max_retries - 1:
                logger.error("All attempts to create browser failed")
                if 'chrome not installed' in str(e).lower():
                    logger.error("Please install Chrome/Chromium browser first")
                raise
            sleep(3)
            continue
            
    raise Exception("Failed to create browser after all retries")

# Initialize browser
try:
    browser = create_browser()
except Exception as e:
    error_msg = f"Failed to initialize ChromeDriver: {str(e)}"
    logger.error(error_msg)  # For local debugging
    if 'chrome not installed' in str(e).lower():
        logger.error("Please install Chrome/Chromium browser first")
    raise Exception(error_msg)
import random
import asyncio
from bs4 import BeautifulSoup
import re 
from time import sleep
from datetime import datetime
from typing import List

# In-memory storage for logs
bot_logs: List[Dict[str, Any]] = []

async def send_log(message: str, type: str = "info") -> None:
    log = {
        "timestamp": datetime.now().isoformat(),
        "message": message,
        "type": type
    }
    bot_logs.append(log)
    if Config.DISCORD_ENABLED:
        from discord_bot import send_message_to_discord
        await send_message_to_discord(message)
    else:
        logger.info(f"[{type}] {message}")

def login(nation_name: str, password: str) -> None:
    try:
        logger.info("Initializing browser session...")
        browser.get("https://www.nationstates.net")
        
        # Wait a bit before navigating to login
        sleep(3)
        
        logger.info("Navigating to login page...")
        browser.get("https://www.nationstates.net/page=login")
        sleep(2)  # Let the page settle
        
        logger.info("Waiting for login form...")
        nation_input = wait.until(EC.presence_of_element_located((By.NAME, "nation")))
        password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        
        # Add random delays between actions
        sleep(random.uniform(0.5, 1.5))
        
        logger.info("Entering credentials...")
        nation_input.send_keys(nation_name)
        sleep(random.uniform(0.3, 0.7))
        password_input.send_keys(password)
        
        logger.info("Attempting login...")
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'][contains(text(), 'Login')]")))
        sleep(random.uniform(0.5, 1.0))
        login_button.click()
        
        logger.info("Verifying login...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "STANDOUT")))
        logger.info("Login successful!")
    except Exception as e:
        print(f"Login failed: {str(e)}")
        print("Current URL:", browser.current_url)
        print("Page title:", browser.title)
        print("Page source:", browser.page_source[:500])
        raise


async def answer_dilemma() -> None:
    try:
        # Navigate to the dilemmas page
        browser.get("https://www.nationstates.net/page=dilemmas")
        dilemmas = browser.find_elements(By.CSS_SELECTOR, "ul.dilemmalist li a")
        if not dilemmas:
            await send_log("No dilemmas found", "info")
            return

        dilemmas[0].click()
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        
        title_elem = soup.select_one(".dpaper4 p")
        desc_elem = soup.select_one(".dilemma h5 + p")
        
        if not title_elem or not desc_elem:
            await send_log("Could not find dilemma content", "error")
            return
            
        issue_title = title_elem.text.strip()
        issue_description = desc_elem.text.strip()
        choices = [choice.text.strip() for choice in soup.select(".diloptions li p") if choice]
        prompt_text = ("Issue Title: " + issue_title + "\n"
                       "Issue Description: " + issue_description + "\n"
                       "Choices:\n" + '\n'.join([f"{i+1}. {choice}" for i, choice in enumerate(choices)]) + "\n"
                       "Based on the information provided, which choice (1, 2, 3, 4, or 5) do you recommend to increase economic growth, military growth, or both? ONLY RESPOND WITH ANSWER e.x 1, 2, 3, 4, 5")

        # Send the user prompt to g4f for processing
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                provider=get_ai_provider(),
                messages=[
                    {"role": "system", "content": "You are an AI advisor for NationStates.net, focused on maximizing economic and military growth. Analyze each dilemma and choose the option that best benefits the economy, military strength, or both. Respond only with a number (1-5) representing the most advantageous choice."},
                    {"role": "user", "content": prompt_text}
                ]
            )
            logger.info(f"Response from g4f: {response}")
        except Exception as e:
            if platform.system() == "Windows":
                logger.error(f"Error with Windows provider: {e}")
                logger.info("Attempting fallback to GetGpt provider...")
                response = g4f.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    provider=GetGpt,
                    messages=[
                        {"role": "system", "content": "You are an AI advisor for NationStates.net, focused on maximizing economic and military growth. Analyze each dilemma and choose the option that best benefits the economy, military strength, or both. Respond only with a number (1-5) representing the most advantageous choice."},
                        {"role": "user", "content": prompt_text}
                    ]
                )
                logger.info(f"Fallback response: {response}")
            else:
                raise

        # Extract the choice from the printed g4f response
        match = re.search(r'\b([1-5])\b', response.strip().lower())
        if match:
            selected_choice_number = match.group(1)
            choice_index = int(selected_choice_number) - 1

            choice_buttons = browser.find_elements(By.CSS_SELECTOR, ".dilemmaaccept button")

            # Check if the choice_index is within the range of available choices
            if 0 <= choice_index < len(choice_buttons):
                choice_buttons[choice_index].click()
                await send_log(f"Dilemma resolved - Choice: {selected_choice_number}", "dilemma")
            else:
                await send_log(f"Invalid choice number: {selected_choice_number}", "error")

    except Exception as e:
        await send_log(f"Error while answering dilemma: {str(e)}", "error")

async def random_navigation() -> None:
    await send_log("Starting random navigation", "navigation")
    random_links = [
        "https://www.nationstates.net/page=world",
        "https://www.nationstates.net/page=dispatches",
        "https://www.nationstates.net/page=activity",
        # Visit nation based on nation_name
        "https://www.nationstates.net/nation=machiavrocia",
        "https://www.nationstates.net/nation=machiavrocia/detail=factbook"
    ]
    
    chosen_link = random.choice(random_links)
    browser.get(chosen_link)
        
    # Randomly scroll up or down
    for _ in range(random.randint(1, 3)):
        action = random.choice([Keys.PAGE_UP, Keys.PAGE_DOWN])
        browser.find_element(By.TAG_NAME, 'body').send_keys(action)
        await asyncio.sleep(random.uniform(0.5, 1.5))  # Use asyncio.sleep for async behavior
    
    await asyncio.sleep(random.randint(10, 25))  # Use asyncio.sleep for async behavior
    
    await answer_dilemma()  # Call the answer_dilemma() function after random navigation
