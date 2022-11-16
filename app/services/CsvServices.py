import csv
from datetime import datetime, timezone

# Checks if the tweet has media files attached to it.
def hasAttachment(tweetInfo):
    return 'attachments' in tweetInfo and len(tweetInfo.attachments['media_keys']) > 0

# Checks if the tweet is parent tweet.
def isParentTweet(tweetInfo):
    return 'referenced_tweets' in tweetInfo and len(tweetInfo.referenced_tweets) > 0

# Reads the iso date string and returns enumerate value for morning, afternoon and evening as 1 ,2 and 3.
def getTweetTimeShift(isoDate):
    [date,time] = str(isoDate).split(' ')

    hour = int(time.split(':')[0])

    if(hour < 12):
        return 1
  
    if(hour > 12 and hour < 18):
        return 2

    return 3

# Converts user joined date into time elapsed in days since joining Twitter
def getDaysSinceJoiningTwitter(userJoinDate):
    return (datetime.now(timezone.utc) - userJoinDate).days

def getInfoIfUserFound(user_id, users):
    user_info = []

    for user in users:
        if user.id == user_id:
            user_info.append(user)

    if len(user_info) > 0:
        return True, user_info[0]

    return False,{} 

# Creates the csv from the tweets data.
def CreateTweetCSV(tweets, category, hasHeader= True):
    file = open('tweets.csv','a')
    csvWriter = csv.writer(file, delimiter=',')

    if hasHeader:
        csvWriter.writerow(["Tweet Time Shift","Tweet Category","Twitter User Duration",
                    "Verified User", "User Tweet Count", "User Followers", "Sensitive Tweet",'Parent Tweet','Has Media',"Retweets", "Likes"])

    users = tweets.includes['users']
    data = tweets.data

    for tweet in data:
        has_user_info, user = getInfoIfUserFound(tweet.author_id, users)

        if has_user_info:
            csvWriter.writerow([getTweetTimeShift(tweet.created_at),category, getDaysSinceJoiningTwitter(user.created_at),
            user.verified,user.public_metrics['tweet_count'], 
            user.public_metrics['followers_count'],tweet.possibly_sensitive,
            isParentTweet(tweet),
            hasAttachment(tweet),tweet.public_metrics['retweet_count'],tweet.public_metrics['like_count']]
            )
        
    file.close()
