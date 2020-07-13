## Imports pre-requisites

from selenium import webdriver

## Import dependencies

# Utils to be imported here..
from core.recursive import text_recursively
from core.chat_bot import activate_bot
from core.clone_chat_bot import activate_clone_bot

## Login into WhatsApp Web :

# Driver to open a browser
try:
    driver = webdriver.Chrome('/media/subhasish/Professional/git_repos/chat_bot/chromedriver_linux64/chromedriver')
    print("Using Chrome as default browser")
except:
    driver = webdriver.Firefox(executable_path = '/media/subhasish/Professional/git_repos/chat_bot/Firefox/geckodriver/geckodriver.exe')
    print("Using Firefox as default browser")
    
#link to open a site
driver.get("https://web.whatsapp.com/")

input("Scan the QR code and then press Enter")

user_input = 'temp'

while user_input != 'q':
    
    print("\nEnter 'r' for recursive message")
    print("\nEnter 'm' for activaing bot")
    print("\nEnter 'c' for clone bot")
    print("\nEnter 'q' to exit")
    
    user_input = input()
    
    if user_input == 'r':
        
        text_recursively(driver)

    elif user_input == 'm':

        activate_bot(driver)
    
    elif user_input == 'c':

        activate_clone_bot(driver)

    elif user_input == 'q':
     
        driver.quit()
