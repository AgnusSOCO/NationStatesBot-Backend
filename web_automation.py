import g4f
from g4f.Provider import GetGpt
from config import wait, bot
from discord_bot import send_message_to_discord
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from time import sleep
import random

def create_browser(max_retries=3):
    """Create a new browser instance with undetected-chromedriver."""
    import subprocess
    import psutil
    import undetected_chromedriver as uc
    
    for attempt in range(max_retries):
        try:
            print(f"Browser creation attempt {attempt + 1}/{max_retries}")
            
            options = uc.ChromeOptions()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            
            print("Creating undetected-chromedriver instance...")
            browser = uc.Chrome(options=options)
            browser.set_page_load_timeout(15)
            browser.implicitly_wait(5)
            
            print("Testing browser with example.com...")
            browser.get('https://www.example.com')
            print("Browser test successful")
            
            return browser
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            try:
                if 'browser' in locals():
                    browser.quit()
            except:
                pass
            
            if attempt == max_retries - 1:
                print("All attempts to create browser failed")
                if 'chrome not installed' in str(e).lower():
                    print("Please install Chrome/Chromium browser first")
                raise
    
    # Kill any existing Chrome and ChromeDriver processes
    try:
        subprocess.run(['pkill', '-f', 'chrome'], capture_output=True)
        subprocess.run(['pkill', '-f', 'chromedriver'], capture_output=True)
    except Exception as e:
        print(f"Warning: Failed to kill existing processes: {e}")
    sleep(2)
    
    options = uc.ChromeOptions()
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # Enhanced stealth mode
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--start-maximized')
    # Add random user agent
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    options.add_argument(f'--user-agent={random.choice(user_agents)}')
    
    try:
        print("Creating undetected-chromedriver instance...")
        browser = uc.Chrome(options=options)
        browser.set_page_load_timeout(30)
        browser.implicitly_wait(10)
        
        # Add delay to avoid detection
        sleep(random.uniform(2, 4))
        
        # Test browser with a simple page
        browser.get('https://www.example.com')
        print("Browser verified with test page")
        sleep(random.uniform(1, 2))
        
        print("Browser instance created successfully")
        return browser
    except Exception as e:
        print(f"Failed to create browser: {str(e)}")
        if 'chrome not installed' in str(e).lower():
            print("Please install Chrome/Chromium browser first")
        try:
            if 'browser' in locals():
                browser.quit()
        except:
            pass
        raise

# Initialize browser
try:
    browser = create_browser()
except Exception as e:
    error_msg = f"Failed to initialize ChromeDriver: {str(e)}"
    print(error_msg)  # For local debugging
    if 'chrome not installed' in str(e).lower():
        print("Please install Chrome/Chromium browser first")
    raise Exception(error_msg)
import random
import asyncio
from bs4 import BeautifulSoup
import re 
from time import sleep
from datetime import datetime
from typing import List

# In-memory storage for logs
bot_logs: List[dict] = []

async def send_log(message: str, type: str = "info") -> None:
    log = {
        "timestamp": datetime.now().isoformat(),
        "message": message,
        "type": type
    }
    bot_logs.append(log)
    # Still send to Discord for backward compatibility
    await bot.loop.create_task(send_message_to_discord(message))

def login(nation_name: str, password: str) -> None:
    try:
        print("Initializing browser session...")
        browser.get("https://www.nationstates.net")
        
        # Wait a bit before navigating to login
        sleep(3)
        
        print("Navigating to login page...")
        browser.get("https://www.nationstates.net/page=login")
        sleep(2)  # Let the page settle
        
        print("Waiting for login form...")
        nation_input = wait.until(EC.presence_of_element_located((By.NAME, "nation")))
        password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        
        # Add random delays between actions
        sleep(random.uniform(0.5, 1.5))
        
        print("Entering credentials...")
        nation_input.send_keys(nation_name)
        sleep(random.uniform(0.3, 0.7))
        password_input.send_keys(password)
        
        print("Attempting login...")
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'][contains(text(), 'Login')]")))
        sleep(random.uniform(0.5, 1.0))
        login_button.click()
        
        print("Verifying login...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "STANDOUT")))
        print("Login successful!")
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
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            provider=g4f.Provider.GetGpt,
            messages=[
                {"role": "system", "content": "You are an AI advisor for NationStates.net, focused on maximizing economic and military growth. Analyze each dilemma and choose the option that best benefits the economy, military strength, or both. Respond only with a number (1-5) representing the most advantageous choice."},
                {"role": "user", "content": prompt_text}
            ]
        )

        # Print out the response from g4f
        print("Response from g4f:", response)

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
