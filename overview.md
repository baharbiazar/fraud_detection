# Content

- [Content](#content)
  - [Overview](#overview)
    - [The Data](#the-data)
    - [Deliverables](#deliverables)
  - [EDA](#EDA)
  - [Model](#model)
    - [Model description and code](#model-description-and-code)
    - [Prediction script](#prediction-script)
  - [Database](#database)
    - [Web App](#web-app)
    - [Get "live" data](#get-live-data)
 

This study was done as part of Galvanize cohort in collaboration with two other peers. The objective is to help a new e-commerce site to try to weed out fraudsters. Deliverables include but are not limited to exploratory data analysis, build  proper machine learning models and presenting the solution as well as building a sustainable software project that can be hand off to the companies engineers by deploying the final model in the cloud.  


## Overview
### The Data
The data is confidential and can not be shared outside of Galvanize. The training data has 14337 rows and 44 features. The second part of the data comes from a live API that is utalized for predictions and is saved in the data base.


### Deliverables 
* EDA
* Classification model building
* Flask app with documented API
    * Query live data from server 
* Web based front-end to enable quick triage of potential fraud
    * Triage importance of transactions (low risk, medium risk, high risk)


### EDA
- Step 1:
Loaded the data with pandas. Added a 'Fraud' column that contains numeric values 0,1,2 depending on if the event is fraud. If `acct_type` field contains the word `fraud`, that point is considered 'High Risk' or 2, if the field is `premium`, the label is 'Low Risk' or 0 and everything else is considered 'Medium Risk' or 1.

<img src="images/transactions.png" width="700" />

- Step 2:
Using latitude and longitude to visualize the data distribution. 

3. Look at the features. Make note of ones you think will be particularly useful to you.

4. Do any data visualization that helps you understand the data.


#### [Deliverable]: Scoping the problem
Before you get cranking on your model, think of how to approach the problem.

1. What preprocessing might you want to do? How will you build your feature matrix? What different ideas do you have?

2. What models do you want to try?

3. **What metric will you use to determine success?**


### Model
The model will be used only the first step in the fraud identification process. You do not use the model to declare a ground truth about fraud or not fraud, but simply to flag which transactions need further manual review.  You will be building a triage model of what are the most pressing (and costly) transactions you have seen. It may also be useful to display what factors contribute to a given case being flagged as fraudulent by your model.  

#### Comparing models
Start building your potential models.

**Notes for writing code:**
* As you write your code, **always be committing** (ABC) to Github!
* Write **clean and modular code**.
* Include **comments** on every method.

*Make sure to get a working model first before you try all of your fancy ideas!*

1. If you have complicated ideas, implement the simplest one first! Get a baseline built so that you can compare more complicated models to that one.

2. Experiment with using different features in your feature matrix. Use different featurization techniques like stemming, lemmatization, tf-idf, part of speech tagging, etc.

3. Experiment with different models like SVM, Logistic Regression, Decision Trees, kNN, etc. You might end up with a final model that is a combination of multiple classification models.

4. Compare their results. Pick a good metric; don't just use accuracy!

#### [Deliverable]: Model description and code
After all this experimentation, you should end up with a model you are happy with.

1. Create a file called `model.py` which builds the model based on the training data.

    * Feel free to use any library to get the job done.
    * Again, make sure your code is **clean**, **modular** and **well-commented**! The general rule of thumb: if you looked at your code in a couple months, would you be able to understand it?

2. In a file called `report.md`, describe your project findings including:
    * An overview of a chosen "optimal" modeling technique, with:
        * process flow
        * preprocessing
        * accuracy metrics selected
        * validation and testing methodology
        * parameter tuning involved in generating the model
        * further steps you might have taken if you were to continue the project.


#### [Deliverable]: Pickled model

1. Use `pickle` to serialize your trained model and store it in a file. This is going to allow you to use the model without retraining it for every prediction, which would be ridiculous.

### Step 3: Prediction script

Take a few raw examples and store them in json or csv format in a file called `test_script_examples`.


#### [Deliverable]: Prediction script

1. Write a script `predict.py` that reads in a single example from `test_script_examples`, vectorizes it, unpickles the model, predicts the label, and outputs the label probability (print to standard out is fine).

    This script will serve as a sort of conceptual and code bridge to the web app you're about to build.

    Each time you run the script, it will predict on one example, just like a web app request. You may be thinking that unpickling the model every time is quite inefficient and you'd be right; we'll remove that inefficiency in the web app.


### Step 4: Database

#### [Deliverable]: Prediction script backed by a database

You'll want to store each prediction the model makes on new examples, which means you'll need a database.

1. Set up a Postgres or MongoDB database that will store each example that the script runs on. You should create a database schema that reflects the form of the raw example data and add a column for the predicted probability of fraud.

2. Write a function in your script that takes the example data and the prediction as arguments and inserts the data into the database.

    Now, each time you run your script, one row should be added to the `predictions` table with a predicted probability of fraud.




### Web App


### Step 6: Get "live" data

We've set up a service for you that will send out "live" data so that you can see that your app is really working.

To use this service, you will need to make a request to our secure server. It gives a maximum of the 10 most recent datapoints, ordered by `sequence_number`. New datapoints come in every few minutes.

*Warning: you will need to implement the save_to_database method.*


1. Write a function that periodically fetches new data, generates a predicted fraud probability, and saves it to your database (after verifying that the data hasn't been seen before).

**Make sure your app is adding the examples to the database with predicted fraud probabilities.**
