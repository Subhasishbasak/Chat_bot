## Imports pre-requisites

from selenium import webdriver

## Import dependencies

# Utils to be imported here..
from recursive import text_recursively

## Login into WhatsApp Web :

# Driver to open a browser
driver = webdriver.Chrome('/media/subhasish/Professional/git_repos/chat_bot/chromedriver_linux64/chromedriver')

#link to open a site
driver.get("https://web.whatsapp.com/")

input("Scan the QR code and then press Enter")

user_input = 'temp'

while user_input != 'q':
    
    print("\nEnter 'r' for recursive message")
    print("\nEnter 'q' to exit")
    
    user_input = input()
    
    if user_input == 'r':
        
        #importing from recursive module
        text_recursively(driver)
    
    elif user_input == 'q':
     
        driver.quit()
