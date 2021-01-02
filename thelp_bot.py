import sys
import tweepy
import time
from keys import client_key, client_secret

consumer_key=client_key
consumer_secret=client_secret
access_token=sys.argv[1]
access_token_secret=sys.argv[2]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)



def get_status_text(input_text):
   return " test" 

last_replied_status_id=api.mentions_timeline()[0].id


while(True):
    print("checking for mentions...")
    mentions=api.mentions_timeline(last_replied_status_id)
    for mention in mentions:
        print("replying to a tweet...")
        api.update_status("@" + mention.user.screen_name + get_status_text(mention.text),mention.id)
        last_replied_status_id=mention.id
        print("replied")
    time.sleep(3)