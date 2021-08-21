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
    df = main_df[['acct_type','object_id','previous_payouts','sale_duration','user_age','user_created','user_type']]
    print(1)

    # number of previous payouts
    df['prev_payout_count'] = df['previous_payouts'].apply(lambda x: len(x))

    print(2)

    #create Fraud(target) column:
    df['Fraud'] = df['acct_type'].apply(lambda x: helper.fraud(x))
    
    # drop unwanted columns
    df.drop(columns=['previous_payouts','acct_type'], inplace= True)


    # replace NaN values:
    df.fillna(-1, inplace= True)

    X_train, X_test, y_train, y_test = helper.split_df(df, 'Fraud') 
    
    model2 = random_forest_model(X_train, y_train)
    print('Random Forest model2 created!')
    print(X_train.shape)

    with open('model2.pkl', 'wb') as f:
        # Write the model to a file.
        pickle.dump(model2, f)