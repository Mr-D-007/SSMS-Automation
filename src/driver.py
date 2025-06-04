from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from selenium import webdriver
import tempfile
import os

load_dotenv()


def initialize_driver():
    """Initializes and returns a Selenium WebDriver with desired options."""
    temp_profile = tempfile.mkdtemp()
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(f"--user-data-dir={temp_profile}")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    service = Service(executable_path=os.getenv("CHROMEDRIVER_PATH"))
    driver = webdriver.Chrome(service=service, options=options)
    driver.delete_all_cookies() 
    actions = ActionChains(driver=driver)
    wait = WebDriverWait(driver, 30)
    return driver, actions, wait, temp_profile

