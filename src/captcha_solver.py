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


def extract_captcha_text(driver, element_id) -> str:
    """
    Extracts and returns uppercase alphanumeric captcha text from a webpage using OCR.
    
    Args:
        driver (WebDriver): Selenium WebDriver instance.
    
    Returns:
        str: Cleaned captcha string (uppercase and alphanumeric), or an empty string if not found.
    """
    try:
        # Locate the captcha image element
        captcha_element = driver.find_element(By.XPATH, f'//*[@id="{element_id}"]')

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


# import io
# import re
# import base64
# from PIL import Image
# from selenium.webdriver.common.by import By
# from selenium.webdriver.remote.webdriver import WebDriver
# import openai

# # Set your API key
# openai.api_key = os.getenv('OPENAI_API_KEY')


# def extract_captcha_text(driver: WebDriver, element_id: str) -> str:
#     """
#     Extracts CAPTCHA text from a webpage using OpenAI's GPT-4o model.
    
#     Args:
#         driver (WebDriver): Selenium WebDriver instance.
#         element_id (str): The HTML ID of the CAPTCHA image.

#     Returns:
#         str: Cleaned CAPTCHA string (uppercase alphanumeric), or empty string if failed.
#     """
#     try:
#         # Locate the CAPTCHA image element
#         captcha_element = driver.find_element(By.ID, element_id)

#         # Capture the CAPTCHA image as PNG
#         captcha_png = captcha_element.screenshot_as_png
#         captcha_base64 = base64.b64encode(captcha_png).decode('utf-8')

#         # Create GPT-4o API prompt
#         response = openai.ChatCompletion.create(
#             model="gpt-4o",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": [
#                         {"type": "text", "text": "Please extract the text from this CAPTCHA image. Only return the exact text, no explanation."},
#                         {
#                             "type": "image_url",
#                             "image_url": {
#                                 "url": f"data:image/png;base64,{captcha_base64}"
#                             }
#                         }
#                     ]
#                 }
#             ],
#             max_tokens=20
#         )

#         # Extract and clean the response
#         raw_text = response['choices'][0]['message']['content'].strip()
#         cleaned_text = re.sub(r'[^A-Z0-9]', '', raw_text.upper())

#         print(f"Extracted CAPTCHA: '{cleaned_text}'")
#         return cleaned_text

#     except Exception as e:
#         print(f"[ERROR] Failed to extract CAPTCHA using GPT-4o: {e}")
#         return ""
