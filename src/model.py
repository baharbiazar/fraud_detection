
import pickle

import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split 

import helper


def random_forest_model(X_train, y_train):
    
    '''
    returns the fitted model
    '''
    
    rf= RandomForestClassifier(class_weight= 'balanced')
    rf.fit(X_train, y_train)

    return rf


if __name__ == '__main__':

    main_df =  pd.read_json('../data/data.json')
    df = helper.prep_df(main_df)
    X_train, X_test, y_train, y_test = helper.split_df(df, 'Fraud') 
    model = random_forest_model(X_train, y_train)
    print('Random Forest model created!')

    with open('model.pkl', 'wb') as f:
        # Write the model to a file.
        pickle.dump(model, f)

