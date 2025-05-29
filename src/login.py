from .captcha_solver import extract_captcha
from .utils import check_failure
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
        sleep(2)
        driver.refresh()
        sleep(2)
        form_element = driver.find_element(By.ID, 'divd')
        user_element = form_element.find_element(By.XPATH, './input')
        user_element.click()
        sleep(1)
        actions.send_keys(os.getenv("USERID")).perform()
        sleep(1)
        actions.send_keys(Keys.TAB).perform()
        sleep(1)
        actions.send_keys(os.getenv("PASSWORD")).perform()
        sleep(1)
        captcha_element = driver.find_element(By.ID, 'txtEnterCode')
        captcha_element.click()
        sleep(1)
        captcha_text = extract_captcha(driver)
        actions.send_keys(captcha_text).perform()
        sleep(10)
        login_button = driver.find_element(By.ID, "btnLogin")
        login_button.click()
        sleep(2)
        status = check_failure(driver, actions, login_button, captcha_element, type='captcha')
        already_logged_in = driver.find_elements(By.CSS_SELECTOR, "#tblLogOut")
        if already_logged_in[0].text:
            already_logged_in[0].find_element(By.XPATH, ".//button").click()
            print('User was already logged in.')
        if status == True:
            print('Login Success.')
    except Exception as e:
        print(f"Exception during login: {e}")
        driver.quit()
        return None