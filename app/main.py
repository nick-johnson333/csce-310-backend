from flask import Flask, request, Response
import json
from flask_cors import CORS
from app import database, DatabaseException

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def get_user_messages():
    request_data = json.loads(request.data)
    query_string = request_data['query']
    data = {}
    data['result'] = database.executeQuery(query_string)
    return Response(json.dumps(data), status=201, mimetype='application/json')

@app.errorhandler(DatabaseException.DatabaseException)
def handle_sql_exception(e):
    return Response(json.dumps({
        "error_type": e.error_type,
        "description": e.message
    }), status=e.code, mimetype='application/json')

