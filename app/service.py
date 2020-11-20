from app.database import executeQuery, select, insert, delete
from app.BlankException import BlankException
from app.position_mappings import POSITION_MAPPINGS


def convert_to_int(**kwargs):
    converted_args = []
    for (key, val) in kwargs.items():
        if key == 'limit' and val is None:
            converted_args.append(default_limit(val))
            continue
        if val is None:
            converted_args.append(None)
            continue
        try:
            converted_args.append(int(val))
        except ValueError as _:
            raise BlankException(f'''The arg [{key}] cannot be converted to an int''', code=400)
    return tuple(converted_args)


def convert_to_float(**kwargs):
    converted_args = []
    for (key, val) in kwargs.items():
        if key == 'limit' and val is None:
            converted_args.append(default_limit(val))
            continue
        if val is None:
            converted_args.append(None)
            continue
        try:
            converted_args.append(float(val))
        except ValueError as _:
            raise BlankException(f'''The arg [{key}] cannot be converted to a float''', code=400)
    return tuple(converted_args)


def default_limit(limit):
    if limit is None:
        return 20
    return limit


def execute_query(query: str):
    return executeQuery(query)


def get_null_stats():
    return {'type': 'None Available',
            'numbers': {}
            }


def get_passing_stats(name):
    data = select('player_passing', name=name, limit=1)
    if len(data) == 0:
        return get_null_stats()
    data = data[0]
    numbers = {
        'games': data['games'],
        'games_starting': data['games_starting'],
        'completed_passes': data['completed_passes'],
        'attempted_passes': data['attempted_passes'],
        'completion_percent': data['completion_percent'],
        'yards': data['yards'],
        'touchdowns': data['touchdowns'],
        'touchdown_percent': data['touchdown_percent'],
        'interceptions': data['interceptions'],
        'interception_percent': data['interception_percent']
    }
    return {
        'type': 'passing',
        'numbers': numbers
    }


def get_rushing_stats(name):
    data = select('player_rushing', name=name, limit=1)
    if len(data) == 0:
        return get_null_stats()
    data = data[0]
    numbers = {
        'games': data['games'],
        'rushes_attempted': data['rushes_attempted'],
        'yards': data['yards'],
        'avg_yards': data['avg_yards'],
        'yards_per_game': data['yards_per_game'],
        'touchdowns': data['touchdowns']
    }
    return {
        'type': 'rushing',
        'numbers': numbers
    }


def get_defense_stats(name):
    data = select('player_defense', name=name, limit=1)
    if len(data) == 0:
        return get_null_stats()
    data = data[0]
    numbers = {
        'games': data['games_played'],
        'interceptions': data['interceptions'],
        'tackles': data['tackles'],
        'sacks': data['sacks']
    }
    return {
        'type': 'defense',
        'numbers': numbers
    }


def get_kicking_stats(name):
    data = select('player_kicking', name=name, limit=1)
    if len(data) == 0:
        return get_null_stats()
    data = data[0]
    numbers = {
        'games': data['games_played'],
        'fg_attempted': data['fg_attempted'],
        'fg_made': data['fg_made'],
        'fg_percentage': int(data['fg_percentage']*100),
        'xp_attempted': data['xp_attempted'],
        'xp_made': data['xp_made'],
        'xp_percentage': int(data['xp_percentage']*100),
        'kickoffs': data['kickoffs'],
        'kickoff_yards': data['kickoff_yards'],
        'kickoff_avg': data['kickoff_avg'],
        'punts': data['punts'],
        'punt_yards': data['punt_yards'],
        'yards_per_punt': data['yards_per_punt']
    }
    return {
        'type': 'kicking',
        'numbers': numbers
    }


def get_receiving_stats(name):
    data = select('player_receiving', name=name, limit=1)
    if len(data) == 0:
        return get_null_stats()
    data = data[0]
    numbers = {
        'games': data['games'],
        'games_starting': data['games_starting'],
        'receptions': data['receptions'],
        'reception_percent': int(data['catch_percent']*100),
        'receptions_per_game': data['catches_per_game'],
        'yards': data['yards'],
        'yards_per_catch': data['yards_per_catch'],
        'yards_per_game': data['yards_per_game'],
        'touchdowns': data['touchdowns'],
        'fumbles': data['fumbles']
    }
    return {
        'type': 'receiving',
        'numbers': numbers
    }


def get_player_stats(name, position):
    try:
        stat_type = POSITION_MAPPINGS[position]
    except KeyError as _:
        stat_type = None

    name = name.replace("'","''")
    if stat_type is "rushing":
        return get_rushing_stats(name)
    elif stat_type is "passing":
        return get_passing_stats(name)
    elif stat_type is "receiving":
        return get_receiving_stats(name)
    elif stat_type is "kicking":
        return get_kicking_stats(name)
    elif stat_type is "defense":
        return get_defense_stats(name)
    else:
        return get_null_stats()


def get_players(position, team, height, weight, limit):
    (weight, limit) = convert_to_int(weight=weight, limit=limit)

    raw_players = select('players', limit, position=position, team=team, height=height, weight=weight)
    players = []
    for raw_player in raw_players:
        player = {'name': raw_player['name'],
                  'team': raw_player['team'],
                  'number': raw_player['number'],
                  'weight': int(raw_player['weight']),
                  'height': raw_player['height'],
                  'age': raw_player['age'],
                  'birthday': str(raw_player['birthday']),
                  'university': raw_player['university'],
                  'position': raw_player['position'],
                  'stats': get_player_stats(raw_player['name'], raw_player['position'])}
        players.append(player)
    return players


def get_games(team_a, team_b, limit):
    limit = convert_to_int(limit=limit)[0]
    teams = []
    if team_a is not None:
        teams.append(team_a)
    if team_b is not None:
        teams.append(team_b)

    if len(teams) == 0:
        raw_games = select('games', limit)
    elif len(teams) == 1:
        raw_games = select('games', limit, home_team=teams[0])
        raw_games += select('games', limit, away_team=teams[0])
    else:
        raw_games = select('games', limit, home_team=teams[0], away_team=teams[1])
        raw_games += select('games', limit, away_team=teams[0], home_team=teams[1])

    games = []
    i = 0
    for raw_game in raw_games:
        if i == limit:
            break
        if raw_game['away_score'] > raw_game['home_score']:
            winner = raw_game['away_team']
        elif raw_game['away_score'] < raw_game['home_score']:
            winner = raw_game['home_team']
        else:
            winner = 'tie'

        games.append({
            'date':str(raw_game['date']),
            'away_team': raw_game['away_team'],
            'home_team': raw_game['home_team'],
            'away_score': raw_game['away_score'],
            'home_score': raw_game['home_score'],
            'winner': winner
        })
        i += 1
    return games


def get_season(team):
    if team is None:
        raise BlankException(f'''The parameter [team] is required''', 400)

    data = select('season', 1, team_name=team)
    if len(data) == 0:
        raise BlankException(f'''There is no season for the team [{team}]''', 404)

    data = data[0]
    return {
        'name': data['team_name'],
        'wins': data['wins'],
        'losses': data['losses'],
        'ties': data['ties'],
        'playoffs': data['playoffs'],
        'superbowl_champ': data['superbowl_champ'],
    }


def get_team(name):
    if name is None:
        raise BlankException(f'''The parameter [name] is required''', 400)

    data = select('teams', 1, team_name=name)
    if len(data) == 0:
        raise BlankException(f'''There is no season for the team [{name}]''', 404)

    data = data[0]
    return {
        'name': data['team_name'],
        'state': data['state'],
        'division': data['division'],
        'conference': data['conference']
    }


def get_suggestions(limit):
    limit = convert_to_int(limit=limit)[0]
    raw_suggestions = select('user_suggestions', limit)

    suggestions = []
    for suggestion in raw_suggestions:
        suggestions.append({
            'id': suggestion['id'],
            'user_name': suggestion['user_name'],
            'suggestion': suggestion['suggestion'],
        })
    return suggestions


def post_user_suggestion(request_data):
    try:
        user_name = request_data['user_name']
    except KeyError as _:
        raise BlankException(f'''There is no field [user_name] in the request body''')
    try:
        suggestion = request_data['suggestion']
    except KeyError as _:
        raise BlankException(f'''There is no field [suggestion] in the request body''')

    return insert('user_suggestions', user_name=user_name, suggestion=suggestion)


def delete_suggestion(suggestion_id):
    if suggestion_id is None:
        raise BlankException(f'''The parameter [id] is required''')
    suggestion_id = convert_to_int(id=suggestion_id)[0]
    return delete('user_suggestions', id=suggestion_id)
