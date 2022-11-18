# Get category for the volume.
def getVolumeCategory(volume):
    if(volume >= 0 and volume<=100):
        return 1
    elif(volume >100 and volume <=1000):
        return 2
    elif(volume > 1000 and volume <= 5000):
        return 3
    elif(volume > 5000 and volume <= 25000):
        return 4
    else:
        return 5
    

# Normalized the given column in the data frame.
def getNormalizedValue(dataset, column):
    column_values = dataset[column]

    categories = []

    for value in column_values:
        categories.append(getVolumeCategory(value))
        
    return categories

# Normalizing the values based on the volumes.
def normalizeAndSetValues(dataset,col_names):
    for name in col_names:
        dataset[name] = getNormalizedValue(dataset,name)
    
    return dataset

# Change retweets to the virality class and add new column 'Virality' to the data frame.
def addViralityInTheData(dataset):
    virality = []

    for retweet_count in dataset['Retweets']:
        virality.append(getVolumeCategory(retweet_count))

    dataset['Virality'] = virality

    return dataset

# Finds the accuracy of the model.
def getAccuracy(predicted_labels, actual_labels):
    correct = 0

    for index, label in enumerate(predicted_labels):
        if label == actual_labels[index] :
            correct+=1
        
        
    return correct , correct / len(predicted_labels)

# Convert the day to years as an integer.
def getInYears(days_count):
    years = []

    for days in days_count:
        years.append(int(days/ 365))

    return years
