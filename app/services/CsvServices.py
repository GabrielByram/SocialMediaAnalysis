import csv

import sys,os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'utils'))

import CsvUtil
import SentimentUtil

# Creates the csv from the tweets data.
def CreateTweetCSV(tweets, category, hasHeader= True):
    file = open('tweets.csv','a',newline='')
    csvWriter = csv.writer(file, delimiter=',')

    if hasHeader:
        csvWriter.writerow([
        "Tweet Time Shift",
        "Tweet Category",
        "Twitter User Duration",
        "Verified User", 
        "User Tweet Count", 
        "User Followers",
        "Friends Count", 
        "User Listed", 
        "Tweet Word Count",
        "Sentiment Score",
        'Parent Tweet Count',
        'Hash Tags Count',
        'Mentions Count',
        'Media Count',
        "Retweets", 
        "Likes"])

    users = tweets.includes['users']
    data = tweets.data

    for tweet in data:
        has_user_info, user = CsvUtil.getInfoIfUserFound(tweet.author_id, users)

        if has_user_info:
            csvWriter.writerow([
            CsvUtil.getTweetTimeShift(tweet.created_at),
            CsvUtil.getCategoryEnumeration(category), 
            CsvUtil.getDaysSinceJoiningTwitter(user.created_at),
            int(user.verified),
            user.public_metrics['tweet_count'], 
            user.public_metrics['followers_count'],
            user.public_metrics['following_count'], 
            user.public_metrics['listed_count'],
            SentimentUtil.getNumberOfWordsFromText(tweet.text),
            SentimentUtil.getSentimentScore(tweet.text),
            CsvUtil.ReferencedTweetCount(tweet),
            CsvUtil.hashTagsCount(tweet),
            CsvUtil.mentionsCount(tweet),
            CsvUtil.mediaCount(tweet),
            tweet.public_metrics['retweet_count'],
            tweet.public_metrics['like_count']]
            )
        
    file.close()


def CreateTweetUserCSV(tweets, hasHeader= False):
   
    csv_head = [
        "TweetID",
        "AuthorID",
        "AuthorName", 
        "InReplyToUserID",
        "InReplyToUsername",
        "ReferencedTweetID",
        "ReferencedTweetType",
        "MentionsUsername",
        "MentionsID",
        "Verified"
    ]

    data = tweets.data
    users = tweets.includes['users']

    with open('tweets_user.csv', 'a', newline='', encoding='utf-8') as file:
        csvWriter = csv.writer(file, delimiter=',')
        
        if hasHeader: 
            csvWriter.writerow(csv_head)

        if data is not None:  # Fixes the error: TypeError: 'NoneType' object is not iterable
            for tweet in data:
                # Get Author ID INFO
                has_user_info, user = CsvUtil.getInfoIfUserFound(tweet.author_id, users)
                # Get InReplyToUserID
                has_user_info2, inreplytouser = CsvUtil.getInfoIfUserFound(tweet.in_reply_to_user_id, users)
            
                if has_user_info and has_user_info2:
                    if tweet.referenced_tweets is not None:
                        if ('entities' in tweet and ('mentions' in tweet.entities and len(tweet.entities['mentions']) > 0)):
                            
                            for entity in tweet.entities['mentions']:
                                
                                csvWriter.writerow([
                                    "'"+str(tweet.id), #Tweet ID
                                    "'"+str(tweet.author_id), #AuthorID
                                    user.username, #Username - in_reply_to_screen_name
                                    "'"+str(tweet.in_reply_to_user_id), #Tweet_in_reply_to_user_id
                                    inreplytouser.username, #Tweet_in_reply_to_user_name
                                    "'"+str(tweet.referenced_tweets[0]["id"]), #Referrenced Tweet Id
                                    tweet.referenced_tweets[0]["type"], #Referrenced Tweet Type
                                    entity["username"], #Tweet_Entities
                                    "'"+str(entity["id"]), #Tweet_Entities
                                    user.verified #Verified
                                ])