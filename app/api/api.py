from index import *

import sys,os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'services'))

import CsvServices

Client = getClient()

def getRecentTweets():
   tweets = Client.search_recent_tweets(query='((Harry Styles songs))  has:media',
   expansions= ['author_id', 'referenced_tweets.id'],
   tweet_fields = ['created_at','public_metrics','possibly_sensitive','attachments','referenced_tweets','entities'], 
   user_fields = ['id','public_metrics','verified', 'created_at'], max_results = 100 )

   return tweets


tweets = getRecentTweets()
CsvServices.CreateTweetCSV(tweets, 'music',False)



