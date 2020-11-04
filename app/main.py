from flask import Flask, request
import json
from flask_cors import CORS
from app import database

app = Flask(__name__)
CORS(app)
GET = ['GET']
POST = ['POST']
PUT = ['PUT']
DELETE = ['DELETE']

@app.route('/')
def hello():
    return 'Hello, World 2'

@app.route('/user_suggestions', methods=['GET','POST'])
def get_user_messages():
    if request.method == 'GET':
        data = {}
        data['data']  = database.getAllFromUserSuggestionsTable()
        return json.dumps(data)
    elif request.method == 'POST':
        request_data = json.loads(request.data)
        data = {}
        data['result'] = database.addUserSuggestionToDatabase(request_data["user_name"],request_data["suggestion"])
        return json.dumps(data)
    elif request.method == 'DELETE':
        request_data = json

@app.route('/user_suggestions/<int:suggestion_id>',methods=['DELETE'])
def delete_suggestion(suggestion_id):
    data = {}
    data['result'] = database.removeUserSuggestion(suggestion_id)
    return json.dumps(data)

