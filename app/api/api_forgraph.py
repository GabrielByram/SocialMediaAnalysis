from index import *

from dotenv import load_dotenv

import sys,os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'services'))

import CsvServices

load_dotenv('.env')

'''
Task is to get User Id and its Follower ID (one to many) from Twitter tweets and save it into CSV file

'''

bearer_token = os.environ['AUTH_BEARER_TOKEN']

Client = getClient()

# A query that is used to get random tweets in Twitter
query = 'lang:en -the the'

def getTweets():
    tweets = Client.search_recent_tweets(query=query,
        expansions= ['author_id','entities.mentions.username','in_reply_to_user_id','referenced_tweets.id'],
        tweet_fields = ['in_reply_to_user_id','entities'],
        user_fields = ['id','username','entities','verified'], max_results = 100 )

    return tweets

tweets = getTweets()
CsvServices.CreateTweetUserCSV(tweets, False)


                







