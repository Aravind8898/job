import pandas as pd
from pymongo import MongoClient
from flask import Flask
from flask import Flask, Response
import requests
from flask import request
import csv


client = MongoClient('mongodb://127.0.0.1:27017/')
mydb = client['mylib']
mycol = mydb['employeeinformation']



app = Flask(__name__)

@app.route('/adddata', methods=["POST","GET"])
def csv_to_json():
    filename = request.args['filename']
    data = pd.read_csv(filename)
    mycol.insert_many(data.to_dict('records'))
    return("action completed successfully")

if __name__ =="__main__" :
    app.run(debug=True, port=8000)
