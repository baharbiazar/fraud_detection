import os
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import geopandas as gpd
import pickle

from mpl_toolkits.mplot3d import Axes3D

import sklearn.preprocessing
import sklearn.decomposition
import sklearn


from termcolor import colored as cl # text customization
import itertools # advanced tools

from sklearn.preprocessing import StandardScaler # data normalization
from sklearn.model_selection import train_test_split # data split
from sklearn.tree import DecisionTreeClassifier # Decision tree algorithm
from sklearn.neighbors import KNeighborsClassifier # KNN algorithm
from sklearn.linear_model import LogisticRegression # Logistic regression algorithm
from sklearn.svm import SVC # SVM algorithm
from sklearn.ensemble import RandomForestClassifier # Random forest tree algorithm
from xgboost import XGBClassifier # XGBoost algorithm

from sklearn.metrics import confusion_matrix # evaluation metric
from sklearn.metrics import accuracy_score # evaluation metric
from sklearn.metrics import f1_score, recall_score # evaluation metric



def fraud(string): 
    word = 'fraud'
    if string == 'premium':
        return 0
    
    elif word in string:
        return 2
    else:
        return 1

def vectorizeCol(df, col):
    df = df.copy()
    df[col] = pd.Categorical(df[col])
    df[col] = df[col].cat.codes
    return df

def vectorizeAllCategoricalColumns(df):
    df = df.copy()
    cols = ['country','currency', 'email_domain','org_name',
            'payee_name','venue_address','venue_country','venue_name',
            'venue_state', 'payout_type']
    for col in cols:
        df = vectorizeCol(df, col)
    return df

def prep_df(main_df):
    
    # make a copy of the main df:
    df = main_df.copy()
    
    # vectorize selected columns:
    df = vectorizeAllCategoricalColumns(df)
    
    # number of previous payouts
    df['prev_payout_count'] = df['previous_payouts'].apply(lambda x: len(x))
    
    #create Fraud(target) column:
    df['Fraud'] = df['acct_type'].apply(lambda x: fraud(x))
    
    
    # drop unwanted columns
    df.drop(columns=['acct_type','description', 'ticket_types', 
                  'org_desc', 'name', 'previous_payouts','listed'], inplace= True)
    
    # replace NaN values:
    df.fillna(-1, inplace= True)

    return df


def split_df(df, target_col):
    '''
    input: clean dataframe with target column
    input: name of the target column
    function splits the data into X_train, x_test, y_train, y_test
    '''

    X = df.copy()
    y = X.pop(target_col)

    X_train, X_test, y_train, y_test = train_test_split(X,y, random_state= 10)

    return X_train, X_test, y_train, y_test


def show_pca_df(df):
    x = df[df.columns[0:-1]].to_numpy()
    y = df[df.columns[-1]].to_numpy()

    x = sklearn.preprocessing.MinMaxScaler().fit_transform(x)
    pca = sklearn.decomposition.PCA(n_components=3)
    pca_result = pca.fit_transform(x)
    print(pca.explained_variance_ratio_)

    pca_df = pd.DataFrame(data=pca_result, columns=['pc_1', 'pc_2', 'pc_3'])
    pca_df = pd.concat([pca_df, pd.DataFrame({'label': y})], axis=1)
    print(pca_df)

    ax = Axes3D(plt.figure(figsize=(8, 8)))
    ax.scatter(xs=pca_df['pc_1'], ys=pca_df['pc_2'], zs=pca_df['pc_3'], c=pca_df['label'], s=25)
    ax.set_xlabel("pc_1")
    ax.set_ylabel("pc_2")
    ax.set_zlabel("pc_3")
    #plt.legend()
    plt.show()

def predictions(input_file):

    '''
    returns a list of predictions
    '''
    preds =[]
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)

    predictions = model.predict(input_file).tolist()
    for i in predictions:
        if i == 0:
            preds.append('Low Risk Transaction')
        elif i ==1:
            preds.append('Suspicious Transaction')
        else:
            preds.append('Fraud Transaction')

    return preds   


def clean_client_data(row):
    client_df = pd.DataFrame.from_dict(row, orient='index').T
    
    df = client_df[['object_id','previous_payouts','sale_duration','user_age','user_created','user_type']]  
    print(df.columns)
    # number of previous payouts
    df['prev_payout_count'] = df.iloc[:,1].apply(lambda x: len(x))
    
    # drop unwanted columns
    df2= df.drop(columns=['previous_payouts'])
    print(df2)

    # replace NaN values:
    df2.fillna(-1, inplace= True)

    return df2







    





    




    