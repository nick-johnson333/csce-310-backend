from flask import Flask
import json
import database

app = Flask(__name__)
GET = ['GET']
POST = ['POST']
PUT = ['PUT']
DELETE = ['DELETE']

@app.route('/')
def hello():
    return 'Hello, World 2'

@app.route('/user_suggestions', methods=GET)
def get_user_messages():
    data = {}
    data['data']  = database.getAllFromUserSuggestionsTable()
    return json.dumps(data)


