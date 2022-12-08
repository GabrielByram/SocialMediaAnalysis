
from datetime import datetime, timezone

categories = {
    "food": 1,
    "tech": 2,
    "music": 3,
    "movies":4,
    "politics": 5,
    "sports": 6
}

# Enumerating the category of the data.
def getCategoryEnumeration(category_name):
    return categories[category_name.lower()]


# Counts the number of media in the tweet.
def mediaCount(tweetInfo):
    if ('attachments' in tweetInfo and ( 'media_keys' in tweetInfo.attachments and len(tweetInfo.attachments['media_keys']) > 0)):
        return len(tweetInfo.attachments['media_keys'])
    return 0

# Gives the hashtags count.
def hashTagsCount(tweetInfo):
    if ( 'entities' in tweetInfo and ('hashtags' in tweetInfo.entities and len(tweetInfo.entities['hashtags'])>0)):
        return len(tweetInfo.entities['hashtags'])
    return 0

# Gives the hashtags count.
def mentionsCount(tweetInfo):
    if ( 'entities' in tweetInfo and ('mentions' in tweetInfo.entities and len(tweetInfo.entities['mentions'])>0)):
        return len(tweetInfo.entities['mentions'])
    return 0
        
# Counts the referenced tweets.
def ReferencedTweetCount(tweetInfo):
    if ('referenced_tweets' in tweetInfo and len(tweetInfo.referenced_tweets) > 0):
        return len(tweetInfo.referenced_tweets)
    return  0

# Reads the iso date string and returns enumerate value for morning, afternoon and evening as 1 ,2 and 3.
def getTweetTimeShift(isoDate):
    [date,time] = str(isoDate).split(' ')

    hour = int(time.split(':')[0])

    if(hour < 6):
        return 1

    if(hour >=6 and hour < 12):
        return 2
  
    if(hour >= 12 and hour < 18):
        return 3
    
    return 4

# Converts user joined date into time elapsed in days since joining Twitter
def getDaysSinceJoiningTwitter(userJoinDate):
    return (datetime.now(timezone.utc) - userJoinDate).days

# Returns the user info if the user of given id is found.
def getInfoIfUserFound(user_id, users):
    user_info = []

    for user in users:
        if user.id == user_id:
            user_info.append(user)

    if len(user_info) > 0:
        return True, user_info[0]

    return False,{} 
