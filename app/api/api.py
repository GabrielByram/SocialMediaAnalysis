from index import *

import sys,os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'services'))

import CsvServices

Client = getClient()

def getRecentTweets():
   tweets = Client.search_recent_tweets(query='"twitter data" (elon musk)',
   expansions= ['author_id'],
   tweet_fields = ['created_at','public_metrics','possibly_sensitive','attachments','referenced_tweets'], 
   user_fields = ['id','public_metrics','verified', 'created_at'], max_results = 100 )

   return tweets


tweets = getRecentTweets()
CsvServices.CreateTweetCSV(tweets, 'sports')



