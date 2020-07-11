# Import Pre-requisites

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import numpy as np
import datetime
import time


def text_recursively(driver):

    wait = WebDriverWait(driver, 10)
    wait5 = WebDriverWait(driver, 5)

    t = input("Enter contact name : ")
    target = "\"" + str(t) + "\""
    if t == 'abort':
        pass
    else:
        try:
            # Select the target
            x_arg = '//span[contains(@title,' + target + ')]'
            try:
                print('Trying to find the contact')
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
                print('Target Searched')
                # Increase the time if searching a contact is taking a long time
                time.sleep(4)

            # Select the target
            driver.find_element_by_xpath(x_arg).click()
            print("Target Successfully Selected")
            time.sleep(2)

            # Select the Input Box
            time.sleep(1)
            input_box = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
            
            # Send message
            msg = input("Type message : \n")
            if msg == 'abort':
                pass
            else:
                r = input('How many times to iterate ? ')

                for i in range(int(r)):
                    input_box.send_keys(msg + Keys.SHIFT + Keys.ENTER) 
                    print('typed msg : ', msg)
                    
                    #time.sleep(len(msg)//6) # Call it a pro gamer move !
                    time.sleep(np.round(np.random.uniform(1,5)))
                    
                    input_box.send_keys(Keys.ENTER)
                
                print("Successfully Send Message to : "+ target + '\n')
                time.sleep(0.5)

        except:
            # If target Not found Add it to the failed List
            print("Cannot find Target: " + target)
            pass

