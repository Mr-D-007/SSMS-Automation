from .driver import By, Keys, Select, EC, os
from .captcha_solver import extract_captcha_text
from time import sleep
import json

def form(driver, actions, wait):
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "NEW BOOKING"))).click()
    new_window = driver.window_handles[-1]
    driver.switch_to.window(new_window)
    sleep(1)
    # Find the select element by its ID
    select_element = driver.find_element(By.CLASS_NAME, "Dropdown")
    # Create a Select object
    select = Select(select_element)
    # Select by value
    select.select_by_value("24")
    print("Selected 'BHADRADRI KOTHAGUDEM' by value.")
    sleep(1)
    # Wait for the table to be present and visible
    table = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "MasterpageLayout"))
    )
    sleep(2)
    # Find the first radio button input within the table
    # We use find_element (singular) because we only want the first one
    first_radio_button = table.find_element(By.XPATH, ".//input[@type='radio']")
    # Scroll into view if necessary (optional, but good practice for interaction)
    driver.execute_script("arguments[0].scrollIntoView(true);", first_radio_button)
    sleep(0.5) # Small pause for scrolling animation
    # Click the radio button
    first_radio_button.click()
    sleep(1)
    driver.find_element(By.XPATH, "//*[@class='GridviewScrollItem']//td//input").click()
    sleep(1)
    driver.find_element(By.XPATH, "//tr[th[contains(text(), 'Customer GSTIN')]]/td/input").click()
    # sleep(1)
    # actions.send_keys(os.getenv("GSTIN")).perform()
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
    captcha_text = extract_captcha_text(driver, id="ccMain_imgCaptcha")
    captcha_element = driver.find_element(By.ID, "ccMain_txtCECode")
    captcha_element.click()
    sleep(1)
    actions.send_keys(captcha_text)
    radio_button_xpath = "//input[@type='radio' and @value='PAYU']"

    # Wait until the element is clickable
    payu_radio_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, radio_button_xpath))
    )

    # Click the radio button
    payu_radio_button.click()
    print("Clicked the radio button with value 'PAYU' using XPath.")
    input()