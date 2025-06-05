from .driver import By, Keys, Select, EC, os
from .captcha_solver import extract_captcha_text
from time import sleep
from .utils import check_timer

def form(driver, actions, wait):
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "NEW BOOKING"))).click()
    new_window = driver.window_handles[-1]
    driver.switch_to.window(new_window)
    sleep(1)
    select_element = driver.find_element(By.CLASS_NAME, "Dropdown")
    select = Select(select_element)
    select.select_by_value("24")
    print("Selected 'BHADRADRI KOTHAGUDEM' by value.")
    sleep(1)
    table = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "MasterpageLayout"))
    )
    sleep(2)
    first_radio_button = table.find_element(By.XPATH, ".//input[@type='radio']")
    driver.execute_script("arguments[0].scrollIntoView(true);", first_radio_button)
    sleep(0.5) # Small pause for scrolling animation
    first_radio_button.click()
    sleep(1)
    driver.find_element(By.XPATH, "//*[@class='GridviewScrollItem']//td//input").click()
    sleep(1)
    driver.find_element(By.XPATH, "//tr[th[contains(text(), 'Customer GSTIN')]]/td/input").click()
    sleep(1)
    actions.send_keys(Keys.TAB).perform()
    sleep(1)
    select_element = wait.until(EC.presence_of_element_located((By.ID, "ccMain_ddlsandpurpose")))
    sleep(1)
    dropdown = Select(select_element)
    dropdown.select_by_visible_text("Commercial")
    sleep(1)
    actions.send_keys(Keys.TAB).perform()
    sleep(1)
    actions.send_keys(os.getenv("VEHICLE_NUMBER")).perform()
    sleep(1)
    actions.send_keys(Keys.TAB).perform()
    sleep(1)
    district_select = driver.find_element(By.XPATH, "//tr[th[contains(., 'District')]]/td[1]/select")
    sleep(1)
    district_dropdown = Select(district_select)
    sleep(1)
    district_dropdown.select_by_visible_text(os.getenv("DISCTRICT_NAME").upper())
    sleep(1)
    mandal_dropdown = wait.until(EC.presence_of_element_located((By.ID, "ccMain_ddldelMandal")))
    select = Select(mandal_dropdown)
    select.select_by_visible_text(os.getenv("MANDAL").upper())
    sleep(1)
    village_dropdown = wait.until(EC.presence_of_element_located((By.ID, "ccMain_ddldelvillage")))
    select_village = Select(village_dropdown)
    select_village.select_by_visible_text(os.getenv("VILLAGE").upper())
    sleep(1)
    delivery_slot = driver.find_elements(By.ID, "ccMain_ddlDeliverySlot")
    if delivery_slot:
        select = Select(delivery_slot[0])
        options = select.options
        if len(options) > 1:
            select.select_by_index(1)
            print(f"Selected: {select.first_selected_option.text}")
        else:
            print("No selectable options found in the dropdown besides '--Select--'.")
    radio_button_xpath = "//input[@type='radio' and @value='PAYU']"
    payu_radio_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, radio_button_xpath))
    )
    payu_radio_button.click()
    sleep(2)
    print("Clicked the radio button with value 'PAYU' using XPath.")
    captcha_filler(driver, actions)
    check_timer(driver, By)
    try:
        error = driver.switch_to.alert.text
        if 'captcha' in error:
            print('Can not fill captcha.')
            driver.quit()
    except Exception as e:
        print()
    register_button = driver.find_element(By.ID, "btnRegister")
    register_button.click()
    check_timer(driver, By)

def captcha_filler(driver, actions):
    captcha_text = extract_captcha_text(driver, element_id="ccMain_imgCaptcha")
    captcha_element = driver.find_element(By.ID, "ccMain_txtCECode")
    captcha_element.click()
    sleep(1)
    actions.send_keys(captcha_text).perform()