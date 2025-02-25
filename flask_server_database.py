from flask import Flask, jsonify, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
from bson import json_util

uri = "mongodb+srv://brillian-wahyu:UpKraYoOCtRmYJaO@rpl-maalma-3-cluster.puv7c.mongodb.net/?retryWrites=true&w=majority&appName=RPL-MAALMA-3-Cluster"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client["sensor_database"]
collections = db["sensor_data_collections"]

app = Flask(__name__)

@app.route("/")
def main():
    return "ABOUT:BLANK"

@app.route("/v1/com_database", methods =["POST", "GET", "DELETE"])
def com_database():
    if(request.method == "POST"):
        body = request.get_json()
        if(not body): return "Error 404 - No Body Found"
        print(body)
        collections.insert_one(body)
        return "OK 200 - Data Successfully Inserted"
    if(request.method == "GET"):
        data_database = collections.find()
        data_tosend = json.loads(json_util.dumps(data_database))
        print("Get Data Successfully")
        return jsonify({"message": "OK 200", "data": data_tosend})
    if(request.method == "DELETE"):
        collections.delete_many({})
        return "OK 200 - All Datas Succesfully Deleted"
    
if(__name__ == "__main__"):
    app.run(debug=True, host="0.0.0.0")

