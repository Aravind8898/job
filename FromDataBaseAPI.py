from flask import Flask
import pymongo
from flask import request
from pymongo import MongoClient
import json
from bson import json_util

client = MongoClient('mongodb://127.0.0.1:27017/') #this is the default ip and default port for mongo

mydb = client['mylib']
mycol = mydb['employeeinformation']

app = Flask(__name__)


@app.route("/jobs", methods=["GET"])
def get_jobs():
    all_jobs = list(mycol.find({}))
    return json.dumps(all_jobs,default=json_util.default)



if __name__ =="__main__" :
    app.run(debug=True, port=8000)