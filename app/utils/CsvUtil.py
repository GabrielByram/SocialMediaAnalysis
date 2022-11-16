
from datetime import datetime, timezone

categories = {
    "food": 1,
    "tech": 2,
    "music": 3,
    "movies":4,
    "politics": 5,
    "sports": 6
}

def getCategoryEnumeration(category_name):
    return categories[category_name.lower()]


# Checks if the tweet has media files attached to it.
def hasAttachment(tweetInfo):
    return 'attachments' in tweetInfo and ( 'mdeia_keys' in tweetInfo.attachments and len(tweetInfo.attachments['media_keys']) > 0)

def hasTags(tweetInfo):
    return 'entities' in tweetInfo and (('hashtags' in tweetInfo.entities and len(tweetInfo.entities['hashtags'])>0) 
        or ('mentions' in tweetInfo.entities and len(tweetInfo.entities['mentions'])>0))

# Checks if the tweet is parent tweet.
def isParentTweet(tweetInfo):
    return 'referenced_tweets' in tweetInfo and len(tweetInfo.referenced_tweets) > 0

# Reads the iso date string and returns enumerate value for morning, afternoon and evening as 1 ,2 and 3.
def getTweetTimeShift(isoDate):
    [date,time] = str(isoDate).split(' ')

    hour = int(time.split(':')[0])

    if(hour < 12):
        return 1
  
    if(hour >= 12 and hour < 18):
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
