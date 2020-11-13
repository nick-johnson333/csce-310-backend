from flask import Flask, request, Response
import json
from flask_cors import CORS
from app import service, BlankException

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def run_query():
    request_data = json.loads(request.data)
    query_string = request_data['query']
    return Response(
        json.dumps({'result': service.execute_query(query_string)}),
        status=201,
        mimetype='application/json')


@app.route('/players', methods=['GET'])
@app.route('/players/', methods=['GET'])
def get_players():
    return Response(
        json.dumps({'result': service.get_players(position=request.args.get('position'),
                                                  team=request.args.get('team'),
                                                  height=request.args.get('height'),
                                                  weight=request.args.get('weight'),
                                                  limit=request.args.get('limit')
                                                  )}),
        status=200,
        mimetype='application/json')


@app.route('/games', methods=['GET'])
@app.route('/games/', methods=['GET'])
def get_games():
    return Response(
        json.dumps({'result': service.get_games(team_a=request.args.get('team_a'),
                                                team_b=request.args.get('team_b'),
                                                limit=request.args.get('limit')
                                                )}),
        status=200,
        mimetype='application/json')


@app.route('/seasons', methods=['GET'])
@app.route('/seasons/', methods=['GET'])
def get_season():
    return Response(
        json.dumps({'result': service.get_season(team=request.args.get('team')
                                                )}),
        status=200,
        mimetype='application/json')


@app.route('/teams', methods=['GET'])
@app.route('/teams/', methods=['GET'])
def get_team():
    return Response(
        json.dumps({'result': service.get_team(name=request.args.get('name')
                                                )}),
        status=200,
        mimetype='application/json')


@app.route('/user_suggestions',methods=['GET'])
@app.route('/user_suggestions/',methods=['GET'])
def get_user_suggestions():
    return Response(
        json.dumps({'result': service.get_suggestions(limit=request.args.get('limit')
                                                )}),
        status=200,
        mimetype='application/json')


@app.route('/user_suggestions',methods=['POST'])
@app.route('/user_suggestions/',methods=['POST'])
def post_user_suggestion():
    request_data = json.loads(request.data)
    return Response(
        json.dumps({'result': service.post_user_suggestion(request_data)}),
        status=201,
        mimetype='application/json')


@app.route('/user_suggestions',methods=['DELETE'])
@app.route('/user_suggestions/',methods=['DELETE'])
def delete_user_suggestion():
    return Response(
        json.dumps({'result': service.delete_suggestion(suggestion_id=request.args.get('id')
                                                      )}),
        status=200,
        mimetype='application/json')


@app.errorhandler(BlankException.BlankException)
def handle_sql_exception(e):
    return Response(json.dumps({
        "result": e.message
    }), status=e.code, mimetype='application/json')

