import numpy as np
import pandas as pd

from sklearn.utils import class_weight
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

import sys,os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'utils'))

import ModelUtil

def main(dataset, shuffle):
    # Random shuffling of the data.
    shuffled_data = dataset

    for i in range(shuffle):
        shuffled_data = shuffled_data.sample(frac = 1, random_state = 1)

    # Normalizing and preprocessing the data.
    normalized_data = ModelUtil.normalizeAndSetValues(shuffled_data,['User Tweet Count', 'User Followers','Friends Count'])
    normalized_data['Twitter User Duration'] = ModelUtil.getInYears(normalized_data['Twitter User Duration'])
    processed_data =  ModelUtil.addViralityInTheData(normalized_data)

    # Preparing out x values and y values data so that we can generate training and testing out of it.
    y_values = processed_data['Virality']
    x_values = normalized_data.drop(['Retweets','Likes','Virality'], axis = 1)
    
    # Splits the data into training and testing.
    x_train,x_test,y_train,y_test=train_test_split(x_values,y_values ,test_size=0.20)

    weights = class_weight.compute_class_weight(class_weight='balanced',classes= np.unique(y_train), y= y_train)
    class_weights = dict(zip(np.unique(y_train), weights))

    # Implementing the Logistic Regression Model
    model_lg = LogisticRegression(multi_class='ovr',solver='liblinear', class_weight=class_weights, max_iter= 10000)
    model_lg.fit(x_train,y_train)

    predicted_labels_lg = model_lg.predict(x_test)
    correct_count_lg , accuracy_lg = ModelUtil.getAccuracy(predicted_labels_lg,np.array(y_test))

    print("Logisitic Regression Model")
    print(correct_count_lg,accuracy_lg)
    print("\n")

    # Implementing the SVM model
    model_rf = RandomForestClassifier(class_weight = "balanced", random_state= 0 )
    model_rf.fit(x_train,y_train)

    predicted_labels_rf = model_rf.predict(x_test)
    correct_count_rf , accuracy_rf = ModelUtil.getAccuracy(predicted_labels_rf,np.array(y_test))

    print("Random Forest Ensembles Classofier")
    print(correct_count_rf,accuracy_rf)
    print("\n")

    print("Class Weights in the dataset")
    print(class_weights)

dataset = pd.read_csv("Collection.csv")
main(dataset, 5)
