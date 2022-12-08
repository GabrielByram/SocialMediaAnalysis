import sys, os
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'api'))

import index

# Get list of users by community
def getCommunities(userDict, numOfCommunities):
    communityList = []
    for num in range(0, numOfCommunities):
        communityList.append([])
    
    for user in userDict:
        communityList[userDict[user]].append(user)

    return communityList

# Make csv of the users with regression info and community info
def getUserInfo(communityList, communityNumber):
    Client = index.getClient()

    userInfo = Client.get_users(
        ids=communityList[communityNumber],
        user_fields = ['id','public_metrics','verified', 'created_at']
    )

    return userInfo

def findAverageOfField(userInfoList, fieldNum):
    sumOfField = 0
    for userInfoTuple in userInfoList:
        sumOfField += int(userInfoTuple[fieldNum])

    avgOfField = sumOfField / len(userInfoList)
    return avgOfField

def normalizeValues(values):
    min_value = min(values)
    max_value = max(values)

    normalized_values = [ (value - min_value)/(max_value - min_value) for value in values]

    return normalized_values



def displayCommunityCharts(numOfCommunities,colors):
    data = dict()
    fields = ['Avg. Time since Creating Account', "Avg. Number of Tweets", "Avg. Number of followers"]
    labels = [{'x_label' : "Communities" , "y_label": "Duration in Days"} , {'x_label': "Communities" , 'y_label': 'Tweets Count'},{'x_label': 'Communities', 'y_label': 'Followers Count'}]

    with open('users_in_graph.csv', 'r') as f:
        index = 0
        for line in f.readlines():
            # skip header
            if index != 0:
                userDuration, verified, tweetCount, followers, community = line.split(',')

                community = int(community.strip('\n'))
                if community not in data:
                    data[community] = []
                data[community].append((userDuration, tweetCount, followers, verified))

            index += 1

    for fieldNum in range(0, len(fields)):
        fieldData = dict()

        for communityNum in range(0, numOfCommunities):
            fieldData[str(communityNum)] = findAverageOfField(data[communityNum], fieldNum)

        #plt.xticks(fontsize=10)
        plt.title(fields[fieldNum])
        plt.xlabel(labels[fieldNum]['x_label'])
        plt.ylabel(labels[fieldNum]['y_label'])
        plt.bar(fieldData.keys(), fieldData.values(), color = colors)
        plt.show()