from .driver import initialize_driver, By
from .login import login, sleep
from .form_filling import form
from .utils import check_failure

def run():
    driver, actions, wait = initialize_driver()
    login(driver, actions)
    otp_submission(driver,actions)
    form(driver, actions, wait)    
    print()

def otp_submission(driver, actions):
    sleep(5)
    otp_element = driver.find_element(By.CSS_SELECTOR, "#txtCOTP")
    otp = input('Enter OTP: ')
    otp_element.send_keys(otp)
    sleep(2)
    button = driver.find_element(By.XPATH, "//button[@type='button' and contains(text(), 'Submit')]")
    button.click()
    check_failure(driver, actions, button, otp_element, type='OTP')