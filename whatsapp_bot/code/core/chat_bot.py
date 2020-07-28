try:
    ## Prerequisit
    import time
    import datetime
    import os, sys, inspect
    from bs4 import BeautifulSoup
    from selenium.webdriver.common.keys import Keys
    # Defining path variables    
    currentdir = os.getcwd()
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)
    ## Utility functions
    import utils.bot as Model
    from utils.get_msg import read_last_msg
    from utils.find_chat import search_chatter
except Exception as e:
    package = str(e).split()[-1]
    print("ERROR")
    print("{} package not found" .format(package))
    print("Please install the module", package)
    
class BotMemory():
    def __init__(self):
        self.storage = {}  ## Storage stores the top 5 users name and last chat time
        
    def updateUser(self, details):
        self.storage[details[0]] = details[1]

    def updateTime(self, user, time):
            self.storage[user] = time
        
    def addAll(self, details):
        for usertime in details:
            self.storage[usertime[0]] = usertime[1]
            
    def exisingUser(self):
        return self.storage.keys()
    
    def chatTime(self, user):
        return self.storage[user]
    
def get_time_tuple(time_str):
    hour = int(time_str.split(':')[0])
    if hour > 12:
        hour -= 12
    minute = int(time_str.split(':')[1])
    #sec = int(time_str.split(':')[2].split(".")[0])
    #return(hour, minute, sec)
    return(hour, minute)

def getUserList(driver, maxNum = 5):
    htmlcode = (driver.page_source).encode('utf-8')
    soup = BeautifulSoup(htmlcode, features="html.parser")
    users = []
    div = soup.find_all('div', class_ = '_3dtfX')
    for i in div:
        user = i.span.text
        isoup = BeautifulSoup((i).encode('utf-8'), features="html.parser")
        timing = isoup.find_all('div', class_ = 'm61XR')[0].text.split()[0]
        if timing.split(":")[0].isdigit():
            users.append([user, timing])
    users = sorted(users, key = lambda x: x[1], reverse = True)
    return users[: maxNum]



## Main function
def activate_bot(driver):
    print("Press Ctrl + C any time to stop bot")
    model = Model.Model()
    activation_time = get_time_tuple(str(datetime.datetime.now().time()))
    memory = BotMemory()
    users = getUserList(driver)
    memory.addAll(users)
    
    try:
        while True:
            usersList = getUserList(driver)
            for details in usersList:
                newuser = False
                user = details[0]
                timing = details[1]
                if user not in memory.exisingUser():
                    memory.update(details)
                    newuser = True
                search_chatter(driver, user)
                time.sleep(2)
                msg = read_last_msg(driver)
                last_chat_owner = msg[0].split("] ")[-1].split(":")[0]
                last_chat_time = msg[0].split(" ")[0].split("[")[-1]
                if (get_time_tuple(last_chat_time) > get_time_tuple(memory.chatTime(user)) and last_chat_owner == user) or newuser or (last_chat_owner == user and get_time_tuple(last_chat_time) > activation_time):
                    
                    print('\nNew chat detected from', user)
                    last_new_msg = msg[-1]
                    reply = model.getReply(last_new_msg)
                    # Selecting Input Box
                    input_box = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
                    # Sending Intro    
                    if newuser:
                        intro = "Hi, this is ABot, a bot created by Aritra Banerjee :). "
                        "\nAritra is not available right now, so I'm here to chat with you "
                        "! Although I'm under development but I can do a few cool stuffs."
                        input_box.send_keys(intro)
                        time.sleep(1)
                        input_box.send_keys(Keys.ENTER)
                        time.sleep(1)
                    # Sending reply
                    input_box.send_keys(reply + Keys.SHIFT + Keys.ENTER)
                    time.sleep(1)
                    input_box.send_keys(Keys.ENTER)
                    memory.updateTime(user, last_chat_time)
    except KeyboardInterrupt:
        print("Exiting")
        sys.exit()
