import pandas as pd
import numpy as np
from api_client import EventAPIClient
from helper import clean_client_data
import pickle

new_data = EventAPIClient()

data = new_data.get_data()

print('/n', '/n',data, type(data))

clean= clean_client_data(data[0])   

with open('model2.pkl', 'rb') as f:
        model = pickle.load(f)


predictions = model.predict(clean)
print(predictions)

preds=[]
for i in predictions:
        if i == 0:
            preds.append('Low Risk Transaction')
        elif i ==1:
            preds.append('Suspicious Transaction')
        else:
            preds.append('Fraud Transaction')
print(preds)