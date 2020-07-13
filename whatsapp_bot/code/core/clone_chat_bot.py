import os,sys,inspect
currentdir = os.getcwd()
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from selenium.webdriver.common.keys import Keys
import numpy as np
import datetime
import time

from utils.find_chat import search_chatter
from utils.get_msg import read_last_msg
import utils.bot as bot

def activate_clone_bot(driver):
    
    # N.T the secondary mobile number should be used for scanning the QR code
    model = bot.Model()

    def get_time_tuple(time_str):
        hour = int(time_str.split(':')[0])
        if hour > 12:
            hour -= 12
        minute = int(time_str.split(':')[1])
        return(hour, minute)

    activation_time = get_time_tuple(str(datetime.datetime.now().time()))

    user = input('\nEnter user name : \n')
    print('Bot activated for {} at {} hr & {} min'.format(user, activation_time[0], activation_time[1]))
    
    search_chatter(driver, user)

    t = (int(input('Enter duration (in minutes) : '))*60)//15
    
    for i in range(1,t+2):

        time.sleep(10)
        time.sleep(int(np.random.uniform(1, 8)))
    
        msg = read_last_msg(driver)
        
        m = msg[0].split(' ')
        last_chat_owner = m[3]+' '+m[4].split(':')[0]
        print('\nlast_chat_owner', last_chat_owner)

        last_chat_time = get_time_tuple(m[0].split('[')[1])
        print('\nIteration {}, last chat time {}'.format(i, last_chat_time))
        
        if last_chat_time > activation_time:
            print('\nNew chat detected at {} hr {} min'.format(last_chat_time[0], last_chat_time[1]))
            last_new_msg = msg[-1]
            print('\nDetected last new msg : ', last_new_msg)

            reply = str(model.getReply(last_new_msg))
            print(reply)

            # Select the Input Box
            time.sleep(2)
            input_box = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
            print('Input box selected')
            
            time.sleep(3)
            input_box.send_keys(reply + Keys.SHIFT + Keys.ENTER)
            time.sleep(int(np.random.uniform(1,8)))
            input_box.send_keys(Keys.ENTER)
            activation_time = last_chat_time




