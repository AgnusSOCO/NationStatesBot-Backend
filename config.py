import logging
from typing import Optional
import os

__all__ = ['wait', 'find_chrome_binary', 'get_browser_version', 'Config', 'logger']

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Config:
    DISCORD_ENABLED: bool = False
    DISCORD_TOKEN: Optional[str] = None
    DISCORD_CHANNEL_ID: Optional[int] = None
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

def get_browser_version(binary_path: str) -> str:
    import subprocess
    import re
    import psutil
    
    VERSION_PATTERN = r'Version (\d+\.\d+\.\d+\.\d+)|(\d+\.\d+\.\d+\.\d+)'
    
    # Kill any existing browser processes
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if any(browser in proc.info['name'].lower() 
                  for browser in ['thorium', 'chrome', 'chromium']):
                psutil.Process(proc.info['pid']).terminate()
                logging.info(f"Terminated browser process: {proc.info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            logging.debug(f"Process handling error: {e}")
            
    def extract_version(output: str) -> str:
        match = re.search(VERSION_PATTERN, output)
        if match:
            # Return the first non-None group (either with or without "Version" prefix)
            return next(g for g in match.groups() if g is not None)
        return ""
            
    try:
        # Capture both stdout and stderr
        result = subprocess.run(
            [binary_path, '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # Log the complete output for debugging
        logging.debug(f"Version command output - stdout: {result.stdout}")
        logging.debug(f"Version command output - stderr: {result.stderr}")
        
        # Check stdout first, then stderr
        version = extract_version(result.stdout)
        if not version:
            version = extract_version(result.stderr)
            
        if version:
            logging.info(f"Detected browser version: {version}")
            return version
            
        raise RuntimeError(f"Could not parse version from output: {result.stdout}\n{result.stderr}")
            
    except subprocess.TimeoutExpired:
        logging.error("Timeout while getting browser version")
        raise RuntimeError("Browser version check timed out")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to get browser version: {e}")
        raise RuntimeError(f"Failed to execute browser version check: {e}")
    except Exception as e:
        logging.error(f"Unexpected error getting browser version: {e}")
        raise RuntimeError(f"Unexpected error during version check: {e}")

def create_browser() -> webdriver.Chrome:
    """Create browser instance with improved error handling."""
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    try:
        binary_path = find_chrome_binary()
        chrome_options.binary_location = binary_path
        logging.info(f"Using browser binary at: {binary_path}")
        
        browser_version = get_browser_version(binary_path)
        major_version = browser_version.split('.')[0]
        logging.info(f"Using browser version {browser_version} (major: {major_version})")
        
        # Download and install ChromeDriver matching the browser version
        driver_path = ChromeDriverManager(driver_version=major_version).install()
        logging.info(f"Using ChromeDriver from: {driver_path}")
        
        service = Service(driver_path)
        
        if platform.system() == "Darwin":  # macOS
            browser = webdriver.Chrome(service=service, options=chrome_options)
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
        else:  # Other platforms
            import undetected_chromedriver as uc
            browser = uc.Chrome(
                driver_executable_path=driver_path,
                options=chrome_options,
                version_main=int(major_version)
            )
            
        return browser
        
    except Exception as e:
        logging.error(f"Browser setup failed: {e}")
        if platform.system() == "Darwin":
            logging.error("On macOS, using selenium-stealth for automation")
        raise

browser = create_browser()

# Initialize WebDriverWait
wait = WebDriverWait(browser, 10)

# Load Discord configuration if enabled
if os.getenv('DISCORD_TOKEN'):
    Config.DISCORD_ENABLED = True
    Config.DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    Config.DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID', '0'))
    logger.info("Discord integration enabled")
