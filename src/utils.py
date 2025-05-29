from io import BytesIO
from PIL import Image
from time import sleep
from .driver import Keys
import easyocr

def extract_captcha_text(driver, x=851, y=482, width=250, height=120) -> str:
    png = driver.get_screenshot_as_png()
    image = Image.open(BytesIO(png))
    cropped = image.crop((x, y, x + width, y + height))
    cropped.save("captcha_cropped.png")

    reader = easyocr.Reader(['en'])
    result = reader.readtext("captcha_cropped.png")
    return " ".join([res[1] for res in result]).upper()

def check_failure(driver, actions, submit_button, element, type):
    try:
        error = driver.switch_to.alert.text
        if type in error:
            driver.switch_to.alert.accept()
            print('Bot failed to submit {type}.')
            entered_text = input('Please enter the correct {type}: ')
            element.click()
            sleep(1)
            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
            actions.send_keys(entered_text).perform()
            sleep(2)
            submit_button.click()
        elif 'Session' in error:
            print('Your session has been timed out please re-start the Login.')
            driver.quit()
    except Exception as e:
        print('{type} filled correctly.')
        return True
    