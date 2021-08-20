
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split 

import helper



def random_forest_model(df, target_col):
    
    '''
    input is a pandas dataframe
    function instantiates a Random Forest Classifier model 
    returns the fitted model
    '''
    X = df
    y = df.pop(target_col)

    X_train, X_test, y_train, y_test = train_test_split(X,y)

    rf= RandomForestClassifier(class_weight= 'balanced')
    rf.fit(X_train, y_train)

    return rf


if __name__ == '__main__':

    main_df =  pd.read_json('../data/data.json')
    
    df = helper.prep_df(main_df)

    rf = random_forest_model(df, 'Fraud')

    print('Random Forest model created!')





