import numpy as np

import pandas as pd

from sklearn.utils import class_weight
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

import sys,os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'utils'))

import ModelUtil

def main(dataset):
    # Random shuffling of the data.
    shuffled_data = dataset.sample(frac = 1, random_state = 1)

    # Normalizing and preprocessing the data.
    normalized_data = ModelUtil.normalizeAndSetValues(shuffled_data,['User Tweet Count', 'User Followers','Friends Count'])
    normalized_data['Twitter User Duration'] = ModelUtil.getInYears(normalized_data['Twitter User Duration'])
    processed_data =  ModelUtil.addViralityInTheData(normalized_data)

    # Preparing out x values and y values data so that we can generate training and testing out of it.
    y_values = processed_data['Virality']
    x_values = normalized_data.drop(['Retweets','Likes','Virality', 'Tweet Category', 'Verified User'], axis = 1)
    
    # Splits the data into training and testing.
    x_train,x_test,y_train,y_test=train_test_split(x_values,y_values ,test_size=0.2)

    # Finding weights of the virality class as they are imbalanced. Has more classes with lesser virality.
    weights = class_weight.compute_class_weight(class_weight='balanced',classes= np.unique(y_train), y= y_train)
    class_weights = dict(zip(np.unique(y_train), weights))

    # Implementing the Logistic Regression Model
    model = LogisticRegression(multi_class='ovr', class_weight= class_weights ,solver='liblinear')
    model.fit(x_train,y_train)

    # Prediction Outcome
    predicted_labels = model.predict(x_test)
    correct_count , accuracy = ModelUtil.getAccuracy(predicted_labels,np.array(y_test))

    print(correct_count,accuracy)
    print('here')

dataset = pd.read_csv("DataSet.csv")
main(dataset)
