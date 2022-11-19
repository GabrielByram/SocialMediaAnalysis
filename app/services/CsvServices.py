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
