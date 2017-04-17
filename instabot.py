# requests library imported to make network requests
import requests
# access token is generated from instagram.com/developer
App_Access_token = "4044638267.343cca6.31d4df2da6744c8596b9b20d3f5a1f05"
# base url for all the requests
BASE_URL = "http://api.instagram.com/v1/"
data = requests.get("https://api.github.com/events")

# info_owner function is used to get owner's details


def info_owner():
    url_owner = BASE_URL + 'users/self/?access_token=' + App_Access_token
    owner_info = requests.get(url_owner).json()
    print "\n Details of owner are:"
    print "\n url is:"
    print url_owner
    print "\n information of owner in json format is:"
    print owner_info
    print"\n usename is:", owner_info["data"]["username"]
    print "\n name of user is:", owner_info['data']['full_name']
    print "\n the link to the profile picture of owner is:", owner_info['data']['profile_picture']
    print"\n owner is following:", owner_info['data']['counts']['follows']
    print "\n number of followers are:", owner_info['data']['counts']['followed_by']

# info_owner()

# We use user_by_username function to get the another id on which like,comments oprations are to be performes


def user_by_username(insta_user):
    url = BASE_URL + "users/search?q=" + insta_user + "&access_token=" + App_Access_token
    search_result = requests.get(url).json()
    if len(search_result['data']):
        print"the user id is :\n"
        print search_result
        print search_result['data'][0]['id']
        return search_result['data'][0]['id']
    else:
        print "no such user exist"
    return search_result['data'][0]['id']

# user_by_username('shivtaj21')
# get_user_post function is used to get the user's public posts


def get_user_post(insta_username):
    insta_user_id = user_by_username(insta_username)
    request_url = BASE_URL + 'users/'+insta_user_id+'/media/recent/?access_token=' + App_Access_token
    recent_posts = requests.get(request_url).json()
    x = raw_input("\n press Y to get the id of recent post only:\n press Z to get the id of interestimg post.")
    if x == 'y'or x == 'Y':
        user_input = int(raw_input("\n enter the post number for which you want to get the id \n"))
        if len(recent_posts) > user_input >= 0:
            print recent_posts
            print "the post id is "+str(recent_posts['data'][user_input]['id'])
            print "the link of post id is:"+recent_posts['data'][user_input]['link']
            return recent_posts['data'][user_input]['id']
        else:
            print "you will get the default id because this post is not in recent posts "
            return recent_posts['data'][0]['id']
    else:   # this will execute when u want to get interesting post means with maximum comments or maximum likes
        a = raw_input("\n enter L if u want to get user id with maximum likes\n enter C if u want to get user id with maximum comments")
        if a == 'l'or a == 'L':
            print recent_posts
            if len(recent_posts['data']):
                x = []
                print"\n on posts number of likes are:"
                for i in (range(len(recent_posts['data']))):
                    x.append(recent_posts['data'][i]['likes']['count'])
                    print recent_posts['data'][i]['likes']['count']
                print x
                m = max(x)  # this max is used to get the post having max. likes, that value store in m
                n = x.index(m)
                print "\n maximum number of likes are " + str(m) + " on post no." + str(n)
                d = n
                return recent_posts['data'][d]['id']
        elif a == 'c' or a == 'C':
            print recent_posts
            if len(recent_posts['data']):
                x = []
                print"\n on posts number of comments are:"
                for i in (range(len(recent_posts['data']))):
                    x.append(recent_posts['data'][i]['comments']['count'])
                    print recent_posts['data'][i]['comments']['count']
                    print x
                    m = max(x)  # this max is used to get the post having max. comments, that value store in m
                    n = x.index(m)
                    print "\n maximum number of comments are " + str(m) + " on post no." + str(n)
                    d = n
                    return recent_posts['data'][d]['id']
            else:
                return recent_posts['data'][0]['id']

get_user_post('api_17790')


