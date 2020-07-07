import instaloader
from datetime import date

L = instaloader.Instaloader()

username = input('Enter Username : ')
password = input('Enter Password : ')

# Login or load session
L.login(username, password)        # (login)

profile_name = input('Enter Profile name : ')
# Obtain profile metadata
profile = instaloader.Profile.from_username(L.context, str(profile_name))

# Print list of followees

follower_list = []
following_list = []
count_follower = 0
count_following = 0

for follower in profile.get_followers():
    follower_list.append(follower.username)
    count_follower += 1

for following in profile.get_followees():
    following_list.append(following.username)
    count_following += 1

print(follower_list)
file = open("followers_" + str(date.today()) + ".txt","w")
for ele in follower_list:
    file.write(ele + '\n')
file.close()
print('Total followers: ', count_follower)

print(following_list)
file = open("following_" + str(date.today()) + ".txt","w")
for ele in following_list:
    file.write(ele + '\n')
file.close()
print('Total following: ', count_following)
