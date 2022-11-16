import csv

import sys,os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'utils'))

import CsvUtil

# Creates the csv from the tweets data.
def CreateTweetCSV(tweets, category, hasHeader= True):
    file = open('tweets.csv','a',newline='')
    csvWriter = csv.writer(file, delimiter=',')

    if hasHeader:
        csvWriter.writerow(["Tweet Time Shift","Tweet Category","Twitter User Duration",
                    "Verified User", "User Tweet Count", "User Followers", "Sensitive Tweet",'Parent Tweet','Has Tags','Has Media',"Retweets", "Likes"])

    users = tweets.includes['users']
    data = tweets.data

    for tweet in data:
        has_user_info, user = CsvUtil.getInfoIfUserFound(tweet.author_id, users)

        if has_user_info:
            csvWriter.writerow([CsvUtil.getTweetTimeShift(tweet.created_at),CsvUtil.getCategoryEnumeration(category), CsvUtil.getDaysSinceJoiningTwitter(user.created_at),
            int(user.verified),user.public_metrics['tweet_count'], 
            user.public_metrics['followers_count'],int(tweet.possibly_sensitive),
            int(CsvUtil.isParentTweet(tweet)),
            int(CsvUtil.hasTags(tweet)),int(CsvUtil.hasAttachment(tweet)),tweet.public_metrics['retweet_count'],tweet.public_metrics['like_count']]
            )
        
    file.close()
