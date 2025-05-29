from .utils import extract_captcha_text
from time import sleep
from .driver import By
from PIL import Image
from io import BytesIO
import easyocr

reader = easyocr.Reader(['en'], gpu=False)

def extract_captcha(driver):
    """
    Crops and returns CAPTCHA text using OCR from the webpage.
    Args:
        driver: Selenium WebDriver
    Returns:
        str: OCR-decoded CAPTCHA text
    """
    captcha_element = driver.find_element(By.ID, 'txtEnterCode')
    captcha_element.click()
    sleep(2)
    text = extract_captcha_text(driver)
    return text
