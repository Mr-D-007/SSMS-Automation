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
    otp_submission(driver,actions, wait)
    form(driver, actions, wait)
    shutil.rmtree(temp_profile)
    print()

def otp_submission(driver, actions, wait):
    sleep(5)
    otp_element = driver.find_element(By.CSS_SELECTOR, "#txtCOTP")
    resend_button = wait.until(EC.element_to_be_clickable((By.ID, "btnCOTPResend")))
    otp = get_otp()
    if otp:
        otp_element.click()
        actions.send_keys(otp)
    else:
        print('Could not fetch OTP.')
    sleep(2)
    button = driver.find_element(By.XPATH, "//button[@type='button' and contains(text(), 'Submit')]")
    button.click()
    status = check_failure(driver, type='OTP')
    if status == False:
        try:
            sleep(1)
            resend_button.click()
            otp_submission(driver, actions, wait)
        except Exception as e:
            print(e)
            print('Could not get OTP from the API, quitting.')