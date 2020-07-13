from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import datetime
import traceback
import numpy as np
import time
from datetime import date

# Driver to open a browser
driver = webdriver.Chrome('/media/subhasish/Professional/git_repos/chat_bot/chromedriver_linux64/chromedriver')

#link to open a site
driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')

#wait buffer
wait5 = WebDriverWait(driver, 5)
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

# fetching old follower(ees) list

file1 = open("../followers_2020-07-08.txt","r") # .txt file containing followers 

followers = file1.readlines()

file1 = open("../following_2020-07-08.txt","r")  # .txt file containing following

following = file1.readlines()

old_list = followers + following

new_list = []
for i in old_list:
    new_list.append(i.split('\n')[0])

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
    #notnow = driver.find_element_by_css_selector(
        #'body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.HoLwm')
    notnow = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')
    notnow.click()
except:
    print("Dheeeeer 1st")
try:
    time.sleep(2)
    #notnow = driver.find_element_by_css_selector(
       # 'body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.HoLwm')
    notnow = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
    notnow.click()
except:
    print("Dheeeeer 2nd")


user_input = 1
print('You are logged in')

liked = []
commented = []

while user_input != 'q':
    print("\n")
    print("Enter 'h' to follow hashtags \n")
    print("Enter 'q' to exit \n")
    
    user_input = input()
    
    if user_input == 'h':
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
            time.sleep(np.random.randint(1,3))
            try:
                #iterate over the first 200 posts in the hashtag
                max_likes = int(input('Enter max likes threshold : '))
                max_iter = int(input('How many posts to scrap : '))
                
                custom = input('Enter c for custom comments : \n')
                if custom == 'c':
                    comm = input('Enter comments separated with space : \n')
                    comment_sample = comm.split(' ')
                else:
                    comment_sample = ['wow !', 'Nice :)', 'awesome', 'amazing !!']
                for x in range(1, max_iter):
                    print("iteration number : ", x)
                    #Get the poster's username
                    time.sleep(3)
                    try :
                        username = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/div/a').text
                        likes_over_limit = False
                        print('\n Got posters username : ', username)
                    except Exception:
                        print('not loading the page maybe : MOVE ON')
                        continue
                    try:
                        #get number of likes and compare it to the maximum number of likes to ignore post
                        time.sleep(4)
                        likes = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[2]/div/div/button/span').text
                        # c'est insta de phoblem :/
                        try:
                            likes = int(likes)
                        except ValueError:
                            try:
                                likes = int(likes.split(',')[0]+likes.split(',')[1])
                            except ValueError:
                                print('\nLike can not be fetched')
                                continue

                        time.sleep(3)
                        print('\n Got likes : ', likes)
                        if likes > max_likes:
                            print(" likes over ", max_likes)
                            likes_over_limit = True
                            #print("\n Detected: {0}".format(username))
                        else:
                            print(" likes below ", max_likes)
                            if username not in new_list:
                                try:
                                    button_like = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button')
                                    button_like.click()
                                    print('\nLiked post\n')
                                    
                                    liked.append(username)
                                    #print('after',liked)
                                    print('Going to sleep ...z..z..z')
                                    time.sleep(int(np.random.uniform(18,25)))
                                    print('\nSlept ...z..z..z.\n')
                                except Exception:
                                    print('Failed to like')
                                    continue
                            else:
                                print('Known User : Found username in list')

                    except Exception:
                        print("Exception in liking loop : MOVE ON")
                        pass


                    # Comments and tracker
                    comm_prob = int(np.random.uniform(1,10))
                    print('{}_{}: {}'.format(hashtag, x,comm_prob))
                    if comm_prob > 5:
                        try:
                            commented.append(username)
                            print('Trying to comment')
                            driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[3]/div/form/textarea').click()
                            comment_box = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[3]/div/form/textarea')
                            print('Comment box located')
                        except Exception:
                            print('Failed to locate comment box')
                            continue

                        num = int(len(comment_sample))
                        index = int(np.random.uniform(0, num))
                        try:
                            comment_box.send_keys(comment_sample[index])
                            time.sleep(1)
                            # Enter to post comment
                            comment_box.send_keys(Keys.ENTER)
                        except Exception:
                            print('Failed to comment')
                            continue
                        print('Sleeping...z...z...')

                        time.sleep(int(np.random.uniform(22,28)))
                    
                    try :    
                        if x == 1:
                            next_button = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/a')
                        else:
                             next_button = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/a[2]')
                        next_button.click()
                    except Exception:
                        print('Not moving to Next')
            
            except Exception:
                print("Exception 2 : Try again")
            
            print('Liked the followings : ', liked)
            print('Commented in : ', commented)

            #writing the newly liked file
            file = open("liked_" + str(date.today()) + ".txt","a")
            for ele in liked:
                file.write(ele + '\n')
            file.close()
            
            #writing the newly commented file
            file = open("commented_" + str(date.today()) + ".txt", "a")
            for ele in commented:
                file.write(ele + '\n')
            file.close()

    elif user_input == 'q':
        
        driver.close()
                        

