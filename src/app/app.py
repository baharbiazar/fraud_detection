
import os
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from flask import Flask, render_template, request

import helper
import pandas as pd
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
    upload_file = request.files['user_csv']
    raw_data = pd.read_json(upload_file)
    print(raw_data.head(2))
    if upload_file.filename:
        
        pass


      
        
        #display predicts



    return render_template('table.html')


if __name__ == '__main__':
    
        
    app.run(host='0.0.0.0', port=8080, debug=True)