from .captcha_solver import extract_captcha_text, extract_captcha_text_2
from .utils import check_failure, check_timer
from .driver import Keys, By
from time import sleep
import os

def login(driver, actions):
    """
    Performs login for a single instance.
    Returns:
        WebDriver if successful, else None
    """
    try:
        driver.get(os.getenv("BASE_URL"))
        # sleep(2)
        # driver.refresh()
        sleep(2)
        form_element = driver.find_element(By.ID, 'divd')
        user_element = form_element.find_element(By.XPATH, './input')
        user_element.click()
        sleep(2)
        actions.send_keys(os.getenv("USERID")).perform()
        sleep(2)
        actions.send_keys(Keys.TAB).perform()
        sleep(2)
        actions.send_keys(os.getenv("PASSWORD")).perform()
        sleep(2)
        captcha_element = driver.find_element(By.ID, 'txtEnterCode')
        # captcha_element.click()
        sleep(2)
        captcha_text = extract_captcha_text(driver, id="imgCaptcha")
        print(f'Captcha Text: {captcha_text}')
        captcha_element.send_keys(captcha_text)
        # error = driver.find_elements(By.ID, "RequiredFieldValidator2")
        # if error:
        #     print('Error while entering Captcha.')
        #     login(driver, actions)
        sleep(2)
        check_timer(driver, By)
        login_button = driver.find_element(By.ID, "btnLogin")
        login_button.click()
        sleep(2)
        status = check_failure(driver, type='captcha')
        if status == False:
            login(driver, actions)
        print('Login Success.')
        already_logged_in = driver.find_elements(By.CSS_SELECTOR, "#tblLogOut")
        if already_logged_in[0].text:
            already_logged_in[0].find_element(By.XPATH, ".//button").click()
            print('User was already logged in.')
            login(driver, actions)
    except Exception as e:
        print(f"Exception during login: {e}")
        driver.quit()
        return None