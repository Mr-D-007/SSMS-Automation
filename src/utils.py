from io import BytesIO
from PIL import Image
import easyocr
import os


def check_failure(driver, type):
    try:
        error = driver.switch_to.alert.text
        if type in error:
            driver.switch_to.alert.accept()
            print(f'Bot failed to submit {type}.')
            return False
        elif 'Session' in error:
            print('Your session has been timed out please re-start the Login.')
            driver.quit()
    except Exception as e:
        print('{type} filled correctly.')
        return True
    
def check_timer(driver, By):
    # Wait until the timer hits 0
    while True:
        time_label = driver.find_element(By.ID, "lbltime")
        timer_text = time_label.text.strip().replace("Timer :", "").strip()
        try:
            time_left = int(timer_text)
            print(f"Time left: {time_left}")
            if time_left <= 0:
                break
        except ValueError:
            return True
    return True