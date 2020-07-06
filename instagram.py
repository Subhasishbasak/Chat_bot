from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import datetime
import traceback
import numpy
import time

# Driver to open a browser
driver = webdriver.Chrome('/media/subhasish/Professional/git_repos/chat_bot/chromedriver_linux64/chromedriver')

#link to open a site
driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')

#sleep for 3 seconds to prevent issues with the server
time.sleep(3)
#Find username and password fields and set their input using our constants
username = driver.find_element_by_name('username')
username_input = input('Enter Username : ')
username.send_keys(str(username_input))
password = driver.find_element_by_name('password')
password_input = input('Enter password : ')
password.send_keys(str(password_input))
#Get the login button
print('Credentials successfully entered')
try:
    print('Tring to log-in')
    button_login = driver.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button')
except:
    button_login = driver.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[6]/button/div')
#sleep again
time.sleep(2)
#click login
button_login.click()
time.sleep(3)
#In case you get a popup after logging in, press not now.
#If not, then just return
try:
    notnow = driver.find_element_by_css_selector(
        'body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.HoLwm')
    notnow.click()
except:
    print("Pop-up issue")

user_input = 1
print('You are logged in')
while user_input != 'q':
    print("\n")
    print("Enter 'h' to follow hashtags \n")
    print("Enter 'in' to know list of followers \n")
    print("Enter 'out' to know list of follwings \n")
    print("Enter 'q' to exit \n")
    
    user_input = input()
    
    if user_input == 'in':

        # Load account page
        driver.get("https://www.instagram.com/{0}/".format(username_input))

        driver.find_element_by_partial_link_text("follower").click()

        # Wait for the followers modal to load
        xpath = "//div[@style='position: relative; z-index: 1;']/div/div[2]/div/div[1]"
        #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

        #Find the followers page
        dialog = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]')
        #find number of followers
        allfoll=int(driver.find_element_by_xpath("//li[2]/a/span").text) 
        #scroll down the page
        for i in range(int(allfoll/2)):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
            time.sleep(random.randint(500,1000)/1000)
            print("Extract friends %",round((i/(allfoll/2)*100),2),"from","%100")

        # Finally, scrape the followers
        xpath = "//div[@style='position: relative; z-index: 1;']//ul/li/div/div/div/div/a"
        followers_elems = driver.find_elements_by_xpath(xpath)

        print("The second one")  
        print([e.text for e in followers_elems])


    if user_input == 'h':
        print("Hello")
        h = input("Enter hashtag (without #) : ")
        hashtag = str(h)
        if h == 'abort':
            pass
        else:
            driver.get('https://www.instagram.com/explore/tags/' + hashtag+ '/')

            time.sleep(5)

            #Get the first post thumbnail and click on it
            first_thumbnail = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')

            first_thumbnail.click()
            time.sleep(numpy.random.randint(1,3))
            try:
                #iterate over the first 200 posts in the hashtag
                for x in range(1,5):
                    print("iteration number : ", x)
                    t_start = datetime.datetime.now()
                    #Get the poster's username
                    username = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div[1]/h2/a').text
                    likes_over_limit = False
                    try:
                        #get number of likes and compare it to the maximum number of likes to ignore post
                        likes = int(driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/section[2]/div/div/button/span').text)
                        if likes > 50:
                            print("likes over 50")
                            likes_over_limit = True
                            print("Detected: {0}".format(username))
                        else:
                            print("likes below 50")
                    except Exception:
                        print("like not found")
            except Exception:
                print("# not found")
        
    elif user_input == 'q':
        
        driver.close()
                        

