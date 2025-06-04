import io
import re
from PIL import Image, ImageOps, ImageFilter
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import pytesseract
import easyocr
import numpy as np
import cv2
import os

# Initialize EasyOCR reader once
reader = easyocr.Reader(['en'], gpu=False)

# IMPORTANT: Set the path to your Tesseract executable.
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"


def extract_captcha_text(driver, id) -> str:
    """
    Extracts and returns uppercase alphanumeric captcha text from a webpage using OCR.
    
    Args:
        driver (WebDriver): Selenium WebDriver instance.
    
    Returns:
        str: Cleaned captcha string (uppercase and alphanumeric), or an empty string if not found.
    """
    try:
        # Locate the captcha image element
        captcha_element = driver.find_element(By.XPATH, f'//*[@id="{id}"]')

        # Take a screenshot of the captcha element
        captcha_png = captcha_element.screenshot_as_png
        captcha_image = Image.open(io.BytesIO(captcha_png))

        # --- Preprocessing ---
        gray = ImageOps.grayscale(captcha_image)
        threshold = 150
        binary = gray.point(lambda x: 0 if x < threshold else 255, '1')
        
        # Optional: Save for debug
        binary.save("captcha_processed.png")

        # OCR
        raw_text = pytesseract.image_to_string(binary, config='--psm 8').strip()

        # Filter to uppercase alphanumeric only
        cleaned_text = re.sub(r'[^A-Z0-9]', '', raw_text.upper())

        print("Extracted Captcha:", cleaned_text)
        return cleaned_text

    except Exception as e:
        print(f"Error extracting captcha: {e}")
        return ""

def extract_captcha_text_2():
    reader = easyocr.Reader(['en'])
    result = reader.readtext("captcha_processed.png")
    os.remove("captcha_processed.png")
    return " ".join([res[1] for res in result]).upper()
