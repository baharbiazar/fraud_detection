"""Realtime Events API Client for DSI Fraud Detection Case Study"""
import os
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import time
import requests
from pymongo import MongoClient
from helper import clean_client_data

import pickle


class EventAPIClient:
    """Realtime Events API Client"""

    def __init__(self, first_sequence_number=0,
                 api_url='https://hxobin8em5.execute-api.us-west-2.amazonaws.com/api/',
                 api_key='vYm9mTUuspeyAWH1v-acfoTlck-tCxwTw9YfCynC',
                 db=None,
                 model=None,
                 interval=30):
        """Initialize the API client."""
        self.next_sequence_number = first_sequence_number
        self.api_url = api_url
        self.api_key = api_key
        self.db = db
        self.model = model
        self.interval = 30
        

    def save_to_database(self, row):

        """Save a data row to the database."""
        if self.model:
            clean_data = clean_client_data(row)
            preds = self.model.predict(clean_data)
            print(preds)
        for i in preds:
            if i == 0:
                row['prediction']= 'Low Risk Transaction'
            elif i ==1:
                row['prediction'] = 'Suspicious Transaction'
            else:
                row['prediction']= 'Fraud Transaction'
        row = {k: v if v else '(None)' for k, v in row.items()}
        self.db.insert_one(row)
        

    def get_data(self):
        """Fetch data from the API."""
        payload = {'api_key': self.api_key,
                   'sequence_number': self.next_sequence_number}
        response = requests.post(self.api_url, json=payload)
        data = response.json()
        self.next_sequence_number = data['_next_sequence_number']
        return data['data']

    def collect(self, interval=30):
        """Check for new data from the API periodically."""
        while True:
            print("Requesting data...")
            data = self.get_data()
            if data:
                print("Saving...")
                for row in data:
                    self.save_to_database(row)
                    
            else:
                print("No new data received.")
            print(f"Waiting {interval} seconds...")
            time.sleep(interval)




if __name__ == "__main__":

    mongo_client = MongoClient('0.0.0.0', 27017)
    db = mongo_client['fraud']
    records = db['records']

    with open('src/app/model2.pkl', 'rb') as f:
        model = pickle.load(f)

    client = EventAPIClient(db=records, model=model)
    client.collect()
    
