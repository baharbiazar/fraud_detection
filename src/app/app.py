
import os
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from flask import Flask, render_template, request

import helper
import pandas as pd
from pymongo import MongoClient
from api_client import EventAPIClient

import pickle

print(os.listdir(path = "."))
# exit()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def predict():
    upload_file = request.files['user_csv']
    user_df = pd.read_csv(upload_file)
    preds = helper.predictions(user_df)
    user_df['risk'] = preds
    predicts = user_df
    print(predicts)
    #display predicts
    return render_template('table.html', predicts = predicts)


@app.route('/live')
def live():
    mongo_client = MongoClient('0.0.0.0', 27017)
    db = mongo_client['fraud']
    records = db['records']
    result = list(records.find({}))
    predictions = []
    for i in result:
        predictions.append((i['object_id'], i['prediction']))

    return render_template('live.html',predicts = predictions)


if __name__ == '__main__':
    
        
    app.run(host='0.0.0.0', port=8080, debug=True)