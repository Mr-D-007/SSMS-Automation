from .driver import initialize_driver, By, EC
from .login import login, sleep
from .form_filling import form
from .utils import check_failure
from .otp import get_otp
import shutil

def run():
    driver, actions, wait, temp_profile = initialize_driver()
    login_status = login(driver, actions)
    if login_status == False:
        login(driver, actions)
    resend_button = wait.until(EC.element_to_be_clickable((By.ID, "btnCOTPResend")))
    otp_submission(driver,actions, wait, resend_button, element="txtCOTP")
    form(driver, actions, wait)
    otp_submission(driver,actions, wait, resend_button, element="ccMain_txtCOTP")
    shutil.rmtree(temp_profile)
    input()

def otp_submission(driver, actions, wait, resend_button, element):
    sleep(5)
    otp = get_otp()
    otp_element = driver.find_element(By.CSS_SELECTOR, f"#{element}")
    if otp:
        otp_element.click()
        actions.send_keys(otp).perform()
    else:
        print('Could not fetch OTP.')
    sleep(2)
    button = driver.find_element(By.XPATH, "//button[@type='button' and contains(text(), 'Submit')]")
    button.click()
    sleep(2)
    status = check_failure(driver, type='OTP')
    if status == False:
        try:
            sleep(1)
            resend_button.click()
            otp_element.click()
            otp_element.clear()
            otp_submission(driver, actions, wait, element)
        except Exception as e:
            print(e)
            print('Could not get OTP from the API, quitting.')