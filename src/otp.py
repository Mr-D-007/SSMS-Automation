from datetime import datetime
from time import sleep
import requests
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

    # Sort messages by 'receivedAt' (latest first)
    messages_list.sort(key=lambda x: datetime.fromisoformat(x['receivedAt'].replace('Z', '+00:00')), reverse=True)

    # Extract OTP from the most recent message containing one
    otp = None
    for msg in messages_list:
        match = re.search(r'\b([A-Z0-9]{6})\b', msg['message'])
        if match:
            otp = match.group(1)
            break

    return otp

