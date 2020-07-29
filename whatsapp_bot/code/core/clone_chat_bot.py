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

    user = input('\nEnter user name (your name as in the bot account) : \n')
    print('Bot activated for {} at {} hr & {} min'.format(user, activation_time[0], activation_time[1]))
    
    search_chatter(driver, user)
    otp = 0

    try:
        
        while True:    

            time.sleep(int(np.random.uniform(1, 8)))
        
            msg = read_last_msg(driver)
            
            m = msg[0].split(' ')
            last_chat_owner = m[3]+' '+m[4].split(':')[0]
            last_chat_owner = last_chat_owner.split(':')[0]

            last_chat_time = get_time_tuple(m[0].split('[')[1])
            print('\nlast chat time {} from {}'.format(last_chat_time, last_chat_owner))
                
            #print('act time : {} || last time : {} || otp : {} || condition : {}'.format(activation_time, last_chat_time, otp,  last_chat_time > activation_time))
            #print('last_chat owner : {} || user : {} || condition1 : {} || condition2 : {} || condition : {}'.format(last_chat_owner, user, last_chat_owner==user, otp>0, (last_chat_owner==user) and (otp>0)))

            if (last_chat_time > activation_time) or ((last_chat_owner==user) and (otp > 0)):
                otp += 1
                print('\nNew chat detected at {} hr {} min, from {}'.format(last_chat_time[0], last_chat_time[1], last_chat_owner))
                last_new_msg = msg[-1]
                print('\nReplying to last new msg : ', last_new_msg)

                reply = str(model.getReply(last_new_msg))
                #print(reply)

                # Select the Input Box
                time.sleep(1)
                input_box = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
                print('Input box selected')
                
                time.sleep(2)
                input_box.send_keys(reply + Keys.SHIFT + Keys.ENTER)
                time.sleep(int(np.random.uniform(1,4)))
                input_box.send_keys(Keys.ENTER)
                activation_time = last_chat_time

    except KeyboardInterrupt:
        print("Exiting")
        sys.exit()





