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
            comm = input('Enter comments separated ? : \n')
            msg = comm.split('?')
            
            # to use our 100% tested convincing-text un-comment below:

            #msg = msg + 'Bol ? Please? Please? Please?Arr kotokkhon? MAaf karo humko? please?please?please?rply?rply?rply?rply?please?please?please?arre bhagwan se toh daaro? please? bhagwan se daro?Ki re? ei tuku oo doya maya nei? EKTU DOYA MAYA NEI? Please? please? rr koto ? ebar ami more jabo kintu? bol na? accha bolis na rply toh de? rply oo dibi na? please? please? Pleassseee? Please? Bole dey? Bolle Dey? Please?please?Please?pplease?why r u doin this to me? please? ki hobe bolle?? rply toh de atleast? Please?please? Bol na? please? bol? please? please rply? rply? Block kore dili naki? please?rply toh de? please? esob thik na? please bol? please? please? Bol? please? bol naaaa? please rply? rply? please? please? rply toh de? please?please? Please? bol? rply? ARREYY KI HOLO? AREY KII HOOLO? BOL?PLEASE? RPLY? RplY? BOl? PLEAse? plEase?PlEase? Please? KI HOLO RE?'.split('?')

            if comm == 'abort':
                pass
            else:
                r = input('How many times to iterate ? ')

                for i in range(int(r)):
                    num = int(len(msg))
                    index = int(np.random.uniform(0, num))
                    input_box.send_keys(msg[index] + Keys.SHIFT + Keys.ENTER) 
                    print('typed msg : ', msg[index])
                    
                    #time.sleep(len(msg)//6) # Call it a pro gamer move !
                    time.sleep(np.round(np.random.uniform(1,2)))
                    
                    input_box.send_keys(Keys.ENTER)
                
                print("Successfully Send Message to : "+ target + '\n')
                time.sleep(0.5)

        except:
            # If target Not found Add it to the failed List
            print("Cannot find Target: " + target)
            pass

