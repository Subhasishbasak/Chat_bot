# clicks on the perticular chat

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import time

def search_chatter(driver, name):
    """
    Function that search the specified user and activates his chat
    """
    wait = WebDriverWait(driver, 10)
    wait5 = WebDriverWait(driver, 5)
    # Select the target
    name = "\"" + str(name) + "\""
    x_arg = '//span[contains(@title,' + name + ')]'
    try:
        #print('Trying to find the contact')
        wait5.until(EC.presence_of_element_located((
            By.XPATH, x_arg
        )))
    except:
        print('Cant find contact')
        # If contact not found, then search for it
        searBoxPath = '//*[@id="input-chatlist-search"]'
        wait5.until(EC.presence_of_element_located((
            By.ID, "input-chatlist-search"
        )))
        inputSearchBox = driver.find_element_by_id("input-chatlist-search")
        time.sleep(0.5)
        # click the search button
        driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[2]/div/button').click()
        time.sleep(1)
        inputSearchBox.clear()
        inputSearchBox.send_keys(target[1:len(target) - 1])
        #print('Target Searched')
        # Increase the time if searching a contact is taking a long time
        time.sleep(4)

    # Select the target
    driver.find_element_by_xpath(x_arg).click()
    print("Target Successfully Selected")
    time.sleep(2)



