file1 = open("followers_2020-07-08.txt","r") # .txt file containing followers 

followers = file1.readlines() 

file1 = open("following_2020-07-08.txt","r")  # .txt file containing following

following = file1.readlines() 


non_followers = []

for i in following:
    if i not in followers:
        non_followers.append(i.split('\n')[0])

not_following = []

for i in followers:
    if i not in following:
        not_following.append(i.split('\n')[0])

print('\n')
print('Users do not follow back : \n',non_followers)       
print('\n')
print('U do not follow back : \n',not_following)
