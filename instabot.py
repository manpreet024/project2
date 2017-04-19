import requests
# Generate an access token from instagram.com/developer.
App_Access_token = "4044638267.a002815.c56a3624a857455cac0169eec86ecb5b"  # make global variable
# Make a global variable for the base url for all the requests
BASE_URL = "https://api.instagram.com/v1/"

# Make a function  to fetch owner details.


def owner_info():  # https://api.instagram.com/v1/users/self/?access_token=ACCESS-TOKEN
    owner_url = BASE_URL + "users/self/?access_token=" + App_Access_token
    owner_info = requests.get(owner_url).json()   # Get information about the owner of the access_token
    print ("information of owner is")
    print("Name                    : ", owner_info['data']['full_name'])
    print("Username                : ", owner_info['data']['username'])
    print("Link to Profile Picture : ", owner_info['data']['profile_picture'])
    print("number of posts are     : ", owner_info['data']['counts']['media'])
    print("Followed By             : ", owner_info['data']['counts']['followed_by'])
    print("Followers are           : ", owner_info['data']['counts']['follows'])
    if owner_info['data']['website'] != '':
        print("Website                 : ", owner_info['data']['website'])
    else:
        print("Website                 :  No Website Available")
    if owner_info['data']['bio'] != '':
        print("Bio                     : ", owner_info['data']['bio'])
    else:
        print("Bio                     :  No Info Available")


def user_search_by_username(username):
    user_url = BASE_URL+"users/search?q="+ username +"&access_token="+App_Access_token
    user_info=requests.get(user_url).json()
    if user_info['data'] == []:
           print("sorry given user does not exist")
           return 0
    else:
        user_id = user_info['data'][0]['id']
        return user_id


def info_of_user(username):
    user_id = user_search_by_username(username)
    user_url = BASE_URL+"users/"+user_id+"/?access_token="+App_Access_token
    user_info = requests.get(user_url).json()
    if user_info['data'] == []:
        print("sorry!!!!User with given username doesn't exist")
        return 0
    else:
        print("Information of user is")
        print("Name                    : ", user_info['data']['full_name'])
        print("Username                : ", user_info['data']['username'])
        print("Link to Profile Picture : ", user_info['data']['profile_picture'])
        print("number os posts         : ", user_info['data']['counts']['media'])
        print("Followed By             : ", user_info['data']['counts']['followed_by'])
        print("Followers               : ", user_info['data']['counts']['follows'])
        if user_info['data']['website'] != '':
            print("Website                 : ", user_info['data']['website'])
        else:
            print("Website                 :  No Website Available")
        if user_info['data']['bio'] != '':
            print("Bio                     : ", user_info['data']['bio'])
        else:
            print("Bio                     :  No Info Available")


def get_user_post_id(username):
    if username not in ['manpreet287', 'api_17790', 'bajwa_jugnu', 'gabaishu7596']:
        print"you can't perform operation on this...plz enter the valid username"
        return
    else:
     insta_user_id = user_search_by_username(username)
      # https://api.instagram.com/v1/users/{user-id}/media/recent/?access_token=ACCESS-TOKEN
     request_url = BASE_URL+"users/"+insta_user_id+"/media/recent/?access_token="+App_Access_token
     request_to_get_all_post = requests.get(request_url).json()
     if len(request_to_get_all_post["data"])== 0:
        print("\n No Post Found for this User !")
     else :
         posts = len(request_to_get_all_post["data"])
         total_posts = str(posts)
         print(" The " + username + " have " + total_posts + " total posts.")
         post_ids = []
         post_likes = []
         post_comments = []
         post_links = []
         for media in (request_to_get_all_post['data']):
             post_ids.append(media['id'])
             post_likes.append(media['likes']['count'])
             post_comments.append(media['comments']['count'])
             post_links.append(media['link'])
         print("\nWhich Recent Post you want to select ?")
         print("1. The post having maximum likes.")
         print("2. The post having minimum likes.")
         print("3. The post having minimum comments.")
         print("4. just want the recent post by giving the post number.")
         print("\n Enter your choice by press 1 or 2 or 3 or 4\n")
     choice = raw_input()
     if int(choice) == 1:
         dictionary = dict(zip(post_ids, post_likes))
         dictionary = sorted(dictionary, key=dictionary.__getitem__)
         max_likes = max(post_likes)
         return dictionary[max_likes], post_links[max_likes]
     elif int(choice) == 2:
         dictionary = dict(zip(post_ids, post_likes))
         dictionary = sorted(dictionary, key=dictionary.__getitem__)
         min_likes = min(post_likes)
         return dictionary[min_likes], post_links[min_likes]
     elif int(choice) == 3:
         dictionary = dict(zip(post_ids, post_comments))
         dictionary = sorted(dictionary, key=dictionary.__getitem__)
         min_comments = min(post_comments)
         return dictionary[min_comments], post_links[min_comments]
     elif int(choice) == 4:
         user_input = int(raw_input("\n enter the post number for which you want to get the id \n"))
         if len(request_to_get_all_post) > user_input >= 0:
             return request_to_get_all_post['data'][user_input]['id'],request_to_get_all_post['data'][user_input]['link']
         else:
             print "you will get the default id because this post is not in recent posts "
             return request_to_get_all_post['data'][0]['id'],request_to_get_all_post['data'][0]['link']
     else:
             print("you did not chose input from given no.")
             print "you will get the default id that is most recent post of the user "
             return request_to_get_all_post['data'][0]['id'], request_to_get_all_post['data'][0]['link']


def like_on_user_post_id(username):
    post_id,post_links = get_user_post_id(username)
    Access_token = {'access_token':App_Access_token}
    url_post_like = BASE_URL + "media/" + str(post_id) + "/likes"    #To like a user_post
    data = requests.post(url_post_like,Access_token).json()  #to post a like
    if data['meta']['code'] == 200:
        print("The post has been liked.")
    else:
        print("post has not been liked! Try Again.")


def comment_on_user_id(username):
    post_id,post_link = get_user_post_id(username)
    url_post_comment = BASE_URL + "media/" +post_id+ "/comments"
    print ("enter the commant u want to post.\nNOTE THAT\nThe total length of the comment cannot exceed 300 characters.\nThe comment cannot contain more than 4 hashtags.\nThe comment cannot contain more than 1 URL\nThe comment cannot consist of all capital letters.\n")
    text = raw_input()
    text = str(text)
    Access_token_Plus_comment = {'access_token': App_Access_token, 'text': text}
    data = requests.post(url_post_comment, Access_token_Plus_comment).json()
    if data['meta']['code'] == 200:
        print("\nYour comment has been Posted.")
    else:
        print("\nSome error occurred! Try Again.")

# for searching a paricular comment from post id of given user username
def search_comment_on_id(username):
    post_id,post_link=get_user_post_id(username)
    print ("Enter the word you want to search in comments : ")
    search = raw_input()
    word_to_be_searched = str(search)
    url = BASE_URL + "media/" + str(post_id) + "/comments/?access_token=" +App_Access_token
    request_comments = requests.get(url).json()
    list_of_comments = []
    comments_id = []
    user = []
    for comment in request_comments["data"]:
        list_of_comments.append(comment["text"])
        comments_id.append(comment["id"])
        user.append(comment["from"]["username"])
    comments_found = []
    comments_id_found = []
    user_found = []
    for i in range(0,len(list_of_comments),1):       #loop on the comments
        if word_to_be_searched in list_of_comments[i]:
            comments_found.append(list_of_comments[i])
            comments_id_found.append(comments_id[i])
            user_found.append(user[i])
    if len(comments_found) == 0:
        print("no comment have found that have this word \'%s\'" % word_to_be_searched)
        return False, post_id, False, False
    else:
        print("Following comments contains the word \'%s\'" % word_to_be_searched)
        for i in range(len(comments_found)):
            print(str(i+1) + ". " + comments_found[i])
        return comments_id_found, post_id, comments_found, user_found


def delete_comment(username):
    comments_id_found,post_id,comments_found,user_found = search_comment_on_id(username)
    if(comments_found == 0):
      print("Can't delete because there is no such comment present in post_id= \'%s' " %  post_id)
      return False, post_id, False, False
    else:
      for i in range(len(comments_id_found)):
        url = BASE_URL + "media/" + str(post_id) + "/comments/" + str(comments_id_found[i]) + "/?access_token=" + App_Access_token
        data = requests.delete(url).json()
        if data['meta']['code'] == 200:
           print("%s --> Deleted." % comments_found[i])
           break
        elif data['meta']['error_code'] == "You cannot delete this comment":
            print("%s --> %s as it is made by %s." % (comments_found[i], data['meta']['error_code'], user_found[i]))
        else:
            print("Some error occurred. Try Again !!")

#Make a function that prints the average number of words per comment...It should take the post's id as input parameter


def avg_words_per_comment(post_id):
    url = BASE_URL + "media/" + str(post_id) + "/comments/?access_token=" + App_Access_token
    print post_id
    data = requests.get(url).json()
    if len(data['data']) == 0:
        print("There are no comments on this post...")
    else:
        list_of_comments = []
        total_no_of_words = 0
        comments_id = []
        for comment in data['data']:
            list_of_comments.append(comment['text'])
            total_no_of_words += len(comment['text'].split())
            comments_id.append(comment['id'])
        average_words = float(total_no_of_words)/len(list_of_comments)
        print("\nAverage no. of words per comment in most interesting post = %.2f" % average_words)


def average_words_per_comment(username):
    user_id = user_search_by_username(username)
    if user_id:
        post_id, post_link = get_user_post_id(username)
        avg_words_per_comment(post_id)

def end_it():
    print("\nTHANKS FOR USING INSTABOT\nhope you enjoy the services")

print("\nHello User! Welcome to the Instabot Environment.")
owner_info()
Input = "y" or "Y"
while Input == 'y'or Input == 'Y':
    print("Choose the username from following \n  manpreet287  \n api_17790  \n bajwa_jugnu  \n gabaishu7579 " )     # The bot should ask the username for which you want to perform any of the action
    username = raw_input()
    if username not in ['manpreet287', 'api_17790' ,'bajwa_jugnu' ,'gabaishu7579']:
        print"you enter wrong username"
        print("please!!Choose the username from following \n manpreet287 \n api_17790 \n bajwa_jugnu \n gabaishu7579 ")
    else :
     print("\nWhat do you want to do using the bot?")                           #The bot should ask the user of what they want to do for the username already provided
     print("\n1. Get the Details of the owner.")
     print("\n2. Get the UserId of the User.")
     print("\n3. Get Information about the User.")
     print("\n4. Get the post_id and post_links of the User on the basis of given criteria.")
     print("\n5. Like a post of the User.")
     print("\n6. Comment on post of the User.")
     print("\n7. search the comment containing a particular word.")
     print("\n8. Delete the comment containing a particular word.")
     print("\n9. Get the average no. of words per comment in specified post.")
     print("\n10. Exit.\n\n")
     choice=raw_input()
     if choice in ['1', '2', '3', '4', '5', '6', '7', '8','9','10']:
       if choice == "1":
         owner_info()
       elif choice == "2":
          user_id = user_search_by_username(username)
          print("UserId   : %s" % user_id)
       elif choice == "3":
        info_of_user(username)
       elif choice == '4':
         post_id, post_link = get_user_post_id(username)
         if post_id and post_link:
             print("\nPost Id : %s" % post_id)
             print("Post Link : %s" % post_link)
       elif choice == '5':
           like_on_user_post_id(username)
       elif choice == '6':
          comment_on_user_id(username)
       elif choice == '7':
          search_comment_on_id(username)
       elif choice == '8':
           delete_comment(username)
       elif choice =='9':
            average_words_per_comment(username)
       elif choice =='10':
            end_it()
     else:
         print("You entered the wrong choice. Please choose from given options.")
         choice = input("\nEnter your choice (1 or 2 or 3 or 4 or 5 or 6 or 7 or 8 or 9 or 10) : ")
    print ("\npress 'Y' or 'y' to continue or press any key to exit \n")
    Input = raw_input()
else:
   print("...........hope you enjoyed this app :)...................")
   print("...................THANK YOU :)...........................")


