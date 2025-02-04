import asyncio
import datetime
import g4f
import logging
import os
import platform
import psutil
import random
import re
import signal
import socket
import subprocess
import sys
import time
import types
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from g4f.Provider import GetGpt, You
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing import Dict, Any, List
from webdriver_manager.chrome import ChromeDriverManager

from config import wait, find_chrome_binary, get_browser_version, Config

# Configure logging once at module level
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('browser_debug.log')
    ]
)

# Get logger for this module
logger = logging.getLogger(__name__)

# Configure logging once at module level
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('browser_debug.log')
    ]
)

# Get logger for this module
logger = logging.getLogger(__name__)

# Configure selenium loggers
for logger_name in ['selenium', 'undetected_chromedriver']:
    selenium_logger = logging.getLogger(logger_name)
    selenium_logger.setLevel(logging.WARNING)
    if not selenium_logger.handlers:
        selenium_logger.addHandler(logging.StreamHandler(sys.stdout))

# Configure logging once at module level
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('browser_debug.log')
    ]
)

def get_ai_provider():
    """Get the appropriate AI provider based on the platform."""
    if platform.system() == "Windows":
        return You  # Browser-based provider for Windows
    return GetGpt  # Default provider for other platforms

class VisibleChrome(uc.Chrome):
    def __init__(self, *args, **kwargs):
        logger = logging.getLogger(__name__)
        logger.info("Initializing VisibleChrome...")
        
        # Create options with minimal settings
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-headless')
        options.add_argument('--disable-headless')
        options.add_argument('--headless=0')
        
        kwargs.update({
            'options': options,
            'headless': False,
            'use_subprocess': True,
            'version_main': 132,
            'browser_executable_path': '/usr/bin/google-chrome'
        })
        
        logger.info("Starting Chrome with non-headless configuration...")
        super().__init__(*args, **kwargs)
        
        # Force window to be visible
        self.maximize_window()
        self.set_window_position(0, 0)
        self.set_window_size(1920, 1080)
        self.execute_script("window.focus()")

def create_browser(max_retries=3):
    """Create a new browser instance with platform-specific automation."""
    global os
    logger = logging.getLogger(__name__)
    
    # Configure environment for visibility
    os.environ.pop('UC_HEADLESS', None)
    os.environ.pop('HEADLESS', None)
    os.environ['DISPLAY'] = ':0'
    
    # Configure Chrome options for visibility
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-headless')
    options.add_argument('--disable-headless')
    options.add_argument('--headless=0')
    
    # Create browser instance with retries
    for attempt in range(max_retries):
        try:
            logger.info(f"Browser creation attempt {attempt + 1}/{max_retries}")
            browser = VisibleChrome(
                options=options,
                headless=False,
                use_subprocess=True,
                version_main=132
            )
            
            # Test browser connection
            logger.info(f"Testing browser connection (attempt {attempt + 1})...")
            browser.get('about:blank')
            browser.current_url
            logger.info("Browser connection verified")
            return browser
            
        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
            if 'browser' in locals():
                try:
                    browser.quit()
                except:
                    pass
            if attempt == max_retries - 1:
                raise
            time.sleep(2)
    
    raise Exception("Failed to create browser after all retries")
    
    # Configure Chrome options for visibility
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--remote-debugging-port=0')
    options.add_argument('--disable-gpu')
    options.add_argument('--enable-logging')
    options.add_argument('--v=1')
    options.add_argument('--no-headless')
    options.add_argument('--disable-headless')
    options.add_argument('--headless=0')
    options.add_argument('--force-device-scale-factor=1')
    options.add_argument('--force-color-profile=srgb')
    options.add_argument('--disable-background-networking')
    options.add_argument('--disable-features=IsolateOrigins,site-per-process')
    options.add_argument('--disable-site-isolation-trials')
    
    # Configure Chrome options for visibility
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-headless')
    options.add_argument('--disable-headless')
    options.add_argument('--headless=0')
    
    # Create browser instance with retries
    for attempt in range(max_retries):
        try:
            logger.info(f"Browser creation attempt {attempt + 1}/{max_retries}")
            browser = uc.Chrome(
                options=options,
                headless=False,
                use_subprocess=True,
                version_main=132
            )
            
            # Configure window and ensure visibility
            browser.maximize_window()
            browser.set_window_position(0, 0)
            browser.set_window_size(1920, 1080)
            browser.execute_script("window.focus()")
            browser.execute_cdp_cmd('Page.bringToFront', {})
            
            # Test browser connection
            browser.get('about:blank')
            browser.current_url
            logger.info("Browser connection verified")
            return browser
            
        except Exception as e:
            logger.error(f"Browser creation attempt {attempt + 1} failed: {e}")
            if 'browser' in locals():
                try:
                    browser.quit()
                except:
                    pass
            if attempt == max_retries - 1:
                raise
            time.sleep(2)
    
    def find_free_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
    
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
            
            # Configure browser for visible mode and Cloudflare handling
            logger.info("Running in visible mode for Cloudflare handling")
            
            # Basic window configuration
            options.add_argument('--start-maximized')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            # Set a random user agent
            options.add_argument(f'user-agent={random.choice(Config.BROWSER_USER_AGENTS)}')
            
            # Use a specific port to avoid conflicts
            port = find_free_port()
            service = Service(
                executable_path=driver_path,
                port=port,
                service_args=['--verbose']
            )
            
            if platform.system() == "Darwin":  # macOS
                logger.info(f"Creating Chrome instance with selenium-stealth (headless: {Config.HEADLESS_MODE})...")
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
                logger.info("Creating undetected-chromedriver instance in visible mode...")
                # Initialize Chrome with visibility settings
                # Clean up any existing Chrome processes
                def kill_chrome_processes():
                    """Kill any existing Chrome processes."""
                    # Get module logger
                    logger = logging.getLogger(__name__)
                    
                    # First try graceful termination
                    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                        try:
                            if any(x in proc.info['name'].lower() for x in ['chrome', 'chromedriver']):
                                psutil.Process(proc.info['pid']).terminate()
                                logger.info(f"Terminated browser process: {proc.info['name']}")
                        except (psutil.NoSuchProcess, psutil.AccessDenied, ProcessLookupError):
                            pass
                    
                    # Wait for processes to terminate
                    time.sleep(2)
                    
                    # Force kill any remaining processes
                    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                        try:
                            if any(x in proc.info['name'].lower() for x in ['chrome', 'chromedriver']):
                                os.kill(proc.info['pid'], signal.SIGKILL)
                                logger.info(f"Force killed browser process: {proc.info['name']}")
                        except (psutil.NoSuchProcess, psutil.AccessDenied, ProcessLookupError):
                            pass
                    
                    # Final check and cleanup
                    time.sleep(1)
                    remaining = []
                    for proc in psutil.process_iter(['pid', 'name']):
                        try:
                            if any(x in proc.info['name'].lower() for x in ['chrome', 'chromedriver']):
                                remaining.append(proc.info['name'])
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
                    if remaining:
                        logger.warning(f"Some processes could not be terminated: {remaining}")
                    else:
                        logger.info("All Chrome processes successfully terminated")
                
                kill_chrome_processes()
                
                # Environment variables are handled at module level
                
                # Configure Chrome options for visible mode
                logger = logging.getLogger(__name__)
                logger.info("Creating browser with forced visible mode for Cloudflare handling...")
                
                # Configure undetected-chromedriver logging
                for logger_name in ['undetected_chromedriver', 'selenium.webdriver.remote.remote_connection']:
                    uc_logger = logging.getLogger(logger_name)
                    uc_logger.setLevel(logging.WARNING)
                    if not uc_logger.handlers:
                        uc_logger.addHandler(logging.StreamHandler(sys.stdout))
                
                # Patch undetected-chromedriver to prevent headless mode
                def patch_uc():
                    try:
                        import undetected_chromedriver.patcher as patcher
                        import types
                        
                        def noop(*args, **kwargs): pass
                        
                        # Create a modified patch method that skips headless configuration
                        def modified_patch(self, *args, **kwargs):
                            self.options.add_argument('--no-headless')
                            self.options.add_argument('--disable-headless')
                            self.options.add_argument('--headless=0')
                            return self.options
                        
                        # Patch Patcher class methods
                        setattr(patcher.Patcher, 'patch', types.MethodType(modified_patch, patcher.Patcher))
                        setattr(patcher.Patcher, 'set_headless', noop)
                        setattr(patcher.Patcher, '_configure_headless', noop)
                        
                        # Patch logging
                        patcher.logger.info = noop
                        
                        logger.info("Successfully patched undetected-chromedriver")
                    except Exception as e:
                        logger.warning(f"Failed to patch undetected-chromedriver: {e}")
                patch_uc()
                
                # Patch undetected-chromedriver's patcher module
                def patch_patcher():
                    """Patch the undetected-chromedriver patcher to prevent headless mode."""
                    try:
                        import undetected_chromedriver.patcher as patcher
                        import types
                        
                        # Create a no-op function
                        def noop(*args, **kwargs):
                            pass
                        
                        # Create a modified patch function that skips headless configuration
                        def modified_patch(self, *args, **kwargs):
                            self.options.add_argument('--no-headless')
                            self.options.add_argument('--disable-headless')
                            self.options.add_argument('--headless=0')
                            self.options.add_argument('--start-maximized')
                            self.options.add_argument('--window-size=1920,1080')
                            return self.options
                        
                        # Create a modified log function that skips headless messages
                        def modified_log(self, *args, **kwargs):
                            if any(x in str(args) for x in ['headless', 'setting properties']):
                                return
                            if hasattr(self, '_orig_log'):
                                self._orig_log(*args, **kwargs)
                        
                        # Save original methods
                        if not hasattr(patcher.Patcher, '_orig_patch'):
                            patcher.Patcher._orig_patch = patcher.Patcher.patch
                        if not hasattr(patcher.Patcher, '_orig_log'):
                            patcher.Patcher._orig_log = getattr(patcher.Patcher, 'log', noop)
                        
                        # Patch Patcher class methods
                        setattr(patcher.Patcher, 'patch', types.MethodType(modified_patch, patcher.Patcher))
                        setattr(patcher.Patcher, 'log', types.MethodType(modified_log, patcher.Patcher))
                        setattr(patcher.Patcher, 'set_headless', noop)
                        setattr(patcher.Patcher, '_configure_headless', noop)
                        
                        logger.info("Successfully patched patcher module")
                    except Exception as e:
                        logger.warning(f"Failed to patch patcher module: {e}")
                patch_patcher()
                
                # Initialize Chrome with minimal settings
                try:
                    # Kill any existing Chrome processes
                    kill_chrome_processes()
                    time.sleep(2)  # Give processes time to terminate
                    
                    # Create Chrome class with overridden headless configuration
                    class VisibleChrome(uc.Chrome):
                        def __init__(self, *args, **kwargs):
                            logger.info("Initializing VisibleChrome with non-headless configuration...")
                            # Create options first
                            options = self._create_options()
                            
                            # Initialize with non-headless configuration
                            kwargs.update({
                                'options': options,
                                'headless': False,
                                'use_subprocess': True,
                                'suppress_welcome': True,
                                'no_sandbox': True,
                                'version_main': int(kwargs.get('version_main', 0))
                            })
                            
                            super().__init__(*args, **kwargs)
                            
                            # Configure window visibility
                            self.maximize_window()
                            self.set_window_position(0, 0)
                            self.set_window_size(1920, 1080)
                            self.execute_script("window.focus()")
                            
                            # Inject minimal anti-detection script
                            self.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                                'source': '''
                                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                                    window.chrome = {app: {isInstalled: false}, runtime: {}};
                                '''
                            })
                            
                        def _create_options(self):
                            options = uc.ChromeOptions()
                            
                            # Basic options
                            options.add_argument('--start-maximized')
                            options.add_argument('--window-size=1920,1080')
                            options.add_argument('--no-sandbox')
                            options.add_argument('--disable-dev-shm-usage')
                            options.add_argument('--disable-blink-features=AutomationControlled')
                            options.add_argument('--disable-extensions')
                            options.add_argument('--disable-gpu')
                            options.add_argument('--no-headless')
                            options.add_argument('--force-renderer-accessibility')
                            options.add_argument('--disable-software-rasterizer')
                            options.add_argument('--disable-setuid-sandbox')
                            options.add_argument('--window-position=0,0')
                            options.add_argument('--remote-debugging-port=0')
                            
                            # Disable automation flags
                            options.add_experimental_option('useAutomationExtension', False)
                            options.add_experimental_option('excludeSwitches', ['enable-automation'])
                            
                            # Set headless property directly
                            options.headless = False
                            
                            return options
                            
                        def _configure_headless(self):
                            """Prevent headless mode configuration."""
                            pass
                            
                        def start_session(self, *args, **kwargs):
                            """Initialize browser session with minimal configuration."""
                            try:
                                # Initialize with parent class's start_session
                                super(uc.Chrome, self).start_session(*args, **kwargs)
                                
                                # Basic window configuration
                                self.maximize_window()
                                self.set_window_position(0, 0)
                                self.set_window_size(1920, 1080)
                                
                                # Ensure window is active
                                self.execute_script("window.focus()")
                            except Exception as e:
                                logger.error(f"Failed to start browser session: {e}")
                                raise
                    
                    # Kill any existing Chrome processes
                    kill_chrome_processes()
                    time.sleep(2)
                    
                    # Configure Chrome options
                    options = uc.ChromeOptions()
                    options.add_argument('--no-sandbox')
                    options.add_argument('--disable-dev-shm-usage')
                    options.add_argument('--disable-blink-features=AutomationControlled')
                    options.add_argument('--start-maximized')
                    options.add_argument('--window-size=1920,1080')
                    options.headless = False
                    
                    # Create browser instance
                    logger.info("Creating browser instance in visible mode...")
                    browser = uc.Chrome(
                        options=options,
                        headless=False,
                        use_subprocess=True,
                        version_main=132,
                        browser_executable_path='/usr/bin/google-chrome',
                        driver_executable_path=None,
                        suppress_welcome=True,
                        service_creationflags=0
                    )
                    
                    # Configure window and ensure visibility
                    browser.maximize_window()
                    browser.set_window_position(0, 0)
                    browser.set_window_size(1920, 1080)
                    browser.execute_script("window.focus()")
                    browser.execute_cdp_cmd('Page.bringToFront', {})
                    
                    # Test browser visibility
                    browser.get('about:blank')
                    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, "html")))
                    
                    # Configure download behavior
                    browser.execute_cdp_cmd('Page.setDownloadBehavior', {
                        'behavior': 'allow',
                        'downloadPath': os.getcwd()
                    })
                    
                    logger.info("Successfully created visible browser instance")
                    return browser
                    
                    # Test browser visibility and ensure window is active
                    browser.get('about:blank')
                    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, "html")))
                    
                    # Configure timeouts and test connection
                    browser.set_page_load_timeout(30)
                    browser.implicitly_wait(10)
                    
                    # Test browser connection
                    max_test_retries = 3
                    for test_attempt in range(max_test_retries):
                        try:
                            logger.info(f"Testing browser connection (attempt {test_attempt + 1})...")
                            browser.get('https://www.example.com')
                            browser.title
                            logger.info("Browser connection verified")
                            return browser
                        except Exception as test_e:
                            if test_attempt == max_test_retries - 1:
                                raise
                            logger.warning(f"Browser test failed: {test_e}")
                            time.sleep(2)
                    
                    raise Exception("Failed to verify browser connection")
                except Exception as e:
                    logger.error(f"Browser creation failed: {e}")
                    if 'browser' in locals():
                        try:
                            browser.quit()
                        except:
                            pass
                    raise
                    
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
            time.sleep(3)
            
            if attempt == max_retries - 1:
                logger.error("All attempts to create browser failed")
                if 'chrome not installed' in str(e).lower():
                    logger.error("Please install Chrome/Chromium browser first")
                raise
            time.sleep(3)
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
# In-memory storage for logs
bot_logs: List[Dict[str, Any]] = []

async def send_log(message: str, type: str = "info") -> None:
    log = {
        "timestamp": datetime.datetime.now().isoformat(),
        "message": message,
        "type": type
    }
    bot_logs.append(log)
    if Config.DISCORD_ENABLED:
        from discord_bot import send_message_to_discord
        await send_message_to_discord(message)
    else:
        logger.info(f"[{type}] {message}")

def wait_for_cloudflare(browser, timeout: int = Config.CLOUDFLARE_TIMEOUT) -> bool:
    """Wait for user to solve Cloudflare challenge."""
    start_time = time.time()
    
    # Force window to be visible and focused
    browser.maximize_window()
    browser.set_window_position(0, 0)
    browser.set_window_size(1920, 1080)
    browser.execute_script("window.focus()")
    browser.execute_cdp_cmd('Page.bringToFront', {})
    browser.execute_script("document.body.style.zoom='100%'")
    
    # List of Cloudflare challenge indicators
    challenge_selectors = [
        '[id="challenge-running"]',
        '[class*="cf-"]',
        '#challenge-stage',
        '#cf-wrapper',
        '.ray-id',
        'iframe[title*="challenge"]',
        '[data-testid="challenge"]',
        '.challenge-container',
        '#challenge-error-title',
        '[aria-label*="Challenge"]',
        '#challenge-form',
        '#challenge-response-field',
        '#challenge-spinner',
        '#challenge-success',
        '#challenge-error',
        '#challenge-body-text',
        '#challenge-running',
        '#challenge-content',
        '#challenge-title'
    ]
    
    while time.time() - start_time < timeout:
        try:
            # Ensure browser remains visible
            browser.maximize_window()
            browser.set_window_position(0, 0)
            browser.set_window_size(1920, 1080)
            browser.execute_script("window.focus()")
            
            # Check for any Cloudflare challenge elements
            challenge_present = False
            for selector in challenge_selectors:
                try:
                    element = WebDriverWait(browser, 1).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    challenge_present = True
                    logger.info(f"Cloudflare challenge still active (detected: {selector})")
                    break
                except:
                    continue
            
            if not challenge_present:
                logger.info("Cloudflare challenge completed successfully")
                return True
                
            time.sleep(1)
            
        except Exception as e:
            logger.error(f"Error checking Cloudflare status: {e}")
            continue
    
    logger.error(f"Cloudflare challenge timed out after {timeout} seconds")
    return False

def handle_cloudflare(browser) -> bool:
    """Handle Cloudflare challenge detection and bypass."""
    try:
        # Force window to be visible and focused
        browser.maximize_window()
        browser.set_window_position(0, 0)
        browser.set_window_size(1920, 1080)
        browser.execute_script("window.focus()")
        browser.execute_cdp_cmd('Page.bringToFront', {})
        browser.execute_script("document.body.style.zoom='100%'")
        
        # Check for Cloudflare challenge using multiple selectors
        selectors = [
            '[id="challenge-running"]',
            '[class*="cf-"]',
            '#challenge-stage',
            '#cf-wrapper',
            '.ray-id',
            'iframe[title*="challenge"]',
            '[data-testid="challenge"]',
            '.challenge-container',
            '#challenge-error-title',
            '[aria-label*="Challenge"]',
            '#challenge-form',
            '#challenge-response-field',
            '#challenge-spinner',
            '#challenge-success',
            '#challenge-error',
            '#challenge-body-text',
            '#challenge-running',
            '#challenge-content',
            '#challenge-title'
        ]
        
        for selector in selectors:
            try:
                element = WebDriverWait(browser, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                logger.warning(f"Cloudflare challenge detected with selector: {selector}")
                logger.info("Waiting for user to complete Cloudflare challenge...")
                
                # Ensure browser is visible
                browser.maximize_window()
                browser.set_window_position(0, 0)
                browser.set_window_size(1920, 1080)
                browser.execute_script("window.focus()")
                browser.execute_cdp_cmd('Page.bringToFront', {})
                
                # Wait for challenge completion
                if not wait_for_cloudflare(browser):
                    raise Exception("Cloudflare challenge timeout - please complete the challenge in the visible browser window")
                
                logger.info("Cloudflare challenge completed successfully")
                return True
            except:
                continue
                
    except Exception as e:
        logger.error(f"Error handling Cloudflare challenge: {e}")
        raise
    return False

def login(nation_name: str, password: str) -> None:
    try:
        logger.info("Initializing browser session...")
        browser.get("https://example.com")  # Initial test page
        time.sleep(random.uniform(2, 4))
        
        logger.info("Navigating to NationStates...")
        browser.get("https://www.nationstates.net")
        
        if handle_cloudflare(browser):
            # Re-navigate after Cloudflare challenge
            browser.get("https://www.nationstates.net")
            time.sleep(random.uniform(1, 2))
        
        logger.info("Navigating to login page...")
        browser.get("https://www.nationstates.net/page=login")
        time.sleep(random.uniform(2, 3))  # Random delay to appear more human-like
        
        logger.info("Waiting for login form...")
        nation_input = wait.until(EC.presence_of_element_located((By.NAME, "nation")))
        password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        
        # Add random delays between actions
        time.sleep(random.uniform(0.5, 1.5))
        
        logger.info("Entering credentials...")
        nation_input.send_keys(nation_name)
        time.sleep(random.uniform(0.3, 0.7))
        password_input.send_keys(password)
        
        logger.info("Attempting login...")
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'][contains(text(), 'Login')]")))
        time.sleep(random.uniform(0.5, 1.0))
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
