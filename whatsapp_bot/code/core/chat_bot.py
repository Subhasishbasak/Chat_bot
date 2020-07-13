import os,sys,inspect
currentdir = os.getcwd()
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from selenium.webdriver.common.keys import Keys
import datetime
import time

from utils.find_chat import search_chatter
from utils.get_msg import read_last_msg
import utils.bot as bot

def activate_bot(driver):
    
    model = bot.Model()
    f = 0

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
    
    for i in range(1,10):

        time.sleep(15)
    
        msg = read_last_msg(driver)
        
        m = msg[0].split(' ')
        last_chat_owner = m[3]+' '+m[4].split(':')[0]
        print('\nlast_chat_owner', last_chat_owner)

        last_chat_time = get_time_tuple(m[0].split('[')[1])
        print('\nIteration {}, last chat time {}'.format(i, last_chat_time))
        
        ### Temp
        #print("Activation, Last", [activation_time, last_chat_time])
        #print(last_chat_time > activation_time)
        ########

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
            if f == 0:
                time.sleep(3)
                intro = "Hi, this is JACK :). \nSubhasish is not available rn, so I'm here to chat with u ! Although I'm under development but I can do a few cool stuffs."
                input_box.send_keys(intro)
                time.sleep(2)
                input_box.send_keys(Keys.ENTER)
                time.sleep(4)
                f += 1

            input_box.send_keys(reply)
            time.sleep(2)
            input_box.send_keys(Keys.SHIFT + Keys.ENTER)
            time.sleep(1)
            input_box.send_keys(Keys.ENTER)
            activation_time = last_chat_time



