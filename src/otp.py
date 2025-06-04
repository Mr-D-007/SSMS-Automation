from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime, timezone
from time import sleep
import requests
import json
import os
import re

def get_otp():
    sleep(5)
    response = requests.request("GET", os.getenv("OTP_URL"), headers={}, data={})
    otp = extract_recent_otp_tsmdcl(response.json()['messages'])
    return otp

def extract_recent_otp_tsmdcl(messages_list):
    """
    Extracts the most recent One-Time Password (OTP) from messages sent by TSMDCL.

    The function assumes the `messages_list` is ordered from most recent to oldest.
    It searches for common OTP patterns like "OTP XXXXXX" or "XXXXXX is your One Time Password".

    Args:
        messages_list (list): A list of dictionaries, where each dictionary represents
                              a message and contains 'sender' and 'message' keys.

    Returns:
        str or None: The extracted most recent OTP string if found, otherwise None.
    """
    # This regex pattern is designed to capture 5 or 6 alphanumeric characters
    # that appear in common OTP message formats:
    # 1. After "OTP " or "OTP" (e.g., "Use OTP C6C26", "Your SSMMS Login OTP E4425C")
    # 2. Before " is your One Time Password" (e.g., "F29EA is your One Time Password")
    otp_pattern = re.compile(r'(?:OTP\s|OTP)([A-Z0-9]{5,6})|([A-Z0-9]{5,6})\s+is your One Time Password', re.IGNORECASE)

    for message_data in messages_list:
        sender = message_data.get('sender', '')
        message_text = message_data.get('message', '')

        # Check if 'TSMDCL' is present in the sender's name (case-insensitive)
        if 'TSMDCL' in sender.upper():
            match = otp_pattern.search(message_text)
            if match:
                # Group 1 captures OTPs from "OTP XXXX" patterns
                # Group 2 captures OTPs from "XXXX is your One Time Password" patterns
                if match.group(1):
                    return match.group(1)
                elif match.group(2):
                    return match.group(2)
    return None

