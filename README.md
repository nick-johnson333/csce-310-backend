# Kicker's Almanac Backend

## Endpoints that this app provides:

### Post Your Own Query
Endpoint: [POST] `/`

Body: 
```
{
    "query":<string>
}
```

Description: The body and all parts of it are *required*.

This endpoint will allow you to run your own query directly on the DB if you don't want to use the other endpoints.

The return will be whatever your query requests. 
If your query is a "select", then the return will contain a list of the results.
Otherwise, it will just contain 'Success' 

Possible Errors:
* 400 if body is malformed or fields are missing

Sample Return: 

```
{ 
    "result": <'Success' or whatever your query result is>
}
```

### Get Players
Endpoint: [GET] `/players?position=<string>&team=<string>&height=<string>&weight=<int>&limit=<int>`

Description: The params are not required on the backend, but if you'd like to provide them they will be used in the query. 
This endpoint will return players that fulfill the requirements. 

The returned players' statistics will also be returned within a field called "stats".
This field will be a JSON body saying the type of stats which will be of value "kicking","passing","defense","receiving","rushing", "None Available" depending on the position of the player.
For offensive lineman, the stats field will be null.
The stats field will also have a "numbers" child which will hold the specific statistics of that position, as shown below in the "statistics-body" example.

The default limit will be 20 but can be changed in the params.

Possible Errors:
* 400 if params are mistyped (ex. if you enter a string for limit)

Sample Return: 

```
{ 
    "result":[
        {
            "name":<string>, 
            "team":<string>, 
            "number":<int>, 
            "weight":<int>, 
            "height":<string>, 
            "age":<int>, 
            "birthday":<string>, 
            "university":<string>, 
            "position":<string>,
            "stats": <statistics-body, shown below>
        }
    ]
}
```

Sample Statistics Bodies:
```
{
    "type":"rushing",
    "numbers": {
        "games":<int>,
        "rushes_attempted":<int>,
        "yards":<int>,
        "avg_yards":<float>,
        "yards_per_game":<float>,
        "touchdowns":<int>
    }
}

{
    "type":"defense",
    "numbers": {
        "games":<int>,
        "interceptions":<int>,
        "tackles":<int>,
        "sacks":<int>
    }
}

{
    "type":"kicking",
    "numbers": {
        "games":<int>,
        "fg_attempted":<int>,
        "fg_made":<int>,
        "fg_percentage":<int: between 0 and 100>,
        "xp_attempted":<int>,
        "xp_made":<int>,
        "xp_percentage":<int: between 0 and 100>,
        "kickoffs":<int>,
        "kickoff_yards":<int>,
        "kickoff_avg":<float>,
        "punts":<int>,
        "punt_yards":<int>,
        "yards_per_punt":<float>
    }
}

{
    "type":"passing",
    "numbers": {
        "games":<int>,
        "games_starting":<int>,
        "completed_passes":<int>,
        "attempted_passes":<int>,
        "completion_percent":<int: between 0 and 100>,
        "yards":<int>,
        "touchdowns":<int>,
        "touchdown_percent":<int: between 0 and 100>,
        "interceptions":<int>,
        "interception_percent":<int: between 0 and 100>
    }
}

{
    "type":"receiving",
    "numbers": {
        "games":<int>,
        "games_starting":<int>,
        "receptions":<int>,
        "reception_percent":<int: between 0 and 100>,
        "receptions_per_game":<float>,
        "yards":<int>,
        "yards_per_catch":<float>,
        "yards_per_game":<float>,
        "touchdowns":<int>,
        "fumbles":<int>
    }
}

{
    "type": "None Available",
    "numbers": {}
}
```



### Get Game
Endpoint: [GET] `/games?team_a=<string>&team_b=<string>&limit=<int>`

Description: The params are not required on the backend, but if you'd like to provide them they will be used in the query. 
This endpoint will return games that fulfill the requirements of being in the selected season, and containing the teams given. 

The teams are interchangeable, meaning that it doesn't matter to the api which team is in which position.

The default limit will be 20 but can be changed in the params.

Possible Errors:
* 400 if params are mistyped (ex. if you enter a string for limit)

Sample Return: 

```
{ 
    "result": [
        {
            "date":<string>, 
            "away_team":<string>, 
            "home_team":<string>, 
            "away_score":<int>, 
            "home_score":<int>, 
            "winner":<string>
        }
    ]
}
```

### Get Season
Endpoint: [GET] `/seasons?team=<string>`

Description: The params are *required*.

This endpoint will return season information of the team being inputted.

Possible Errors:
* Error Code 404 if the team does not exist
* Error Code 400 if the param is missing

Sample Return: 

```
{ 
    "result": {
        "name":<string>, 
        "wins":<int>, 
        "losses":<int>, 
        "ties": <int>,
        "playoffs":<string: either Yes or No>, 
        "superbowl_champ":<string: either Yes or No>
    }
}
```


### Get Team
Endpoint: [GET] `/teams?name=<string>`

Description: The params are *required*.

This endpoint will return information on the inputted team.

Possible Errors:
* 404 if team is missing
* 400 if param is not found

Sample Return: 

```
{ 
    "result": {
        "name":<string>, 
        "state":<string>, 
        "division":<string>,
        "conference":<string>
    }
}
```


### Get User Suggestions
Endpoint: [GET] `/user_suggestions?limit=<int>`

Description: The params are optional. 

This endpoint will return as many user suggestions as are specified by the limit. 
If there are less than the limit returned, then that is all that are in the database.

The default limit is 20.

Possible Errors:
* 400 if params are mistyped (ex. if you enter a string for limit)

Sample Return: 

```
{ 
    "result": [
        {
            "suggestion_id":<int>,
            "user_name":<string>, 
            "suggestion":<string>
        }
    ]
}
```


### Post User Suggestion
Endpoint: [POST] `/user_suggestions`

Body: 
```
{
    "user_name":<string>,
    "suggestion":<string>
}
```

Description: The body and all parts of it are *required*.

This endpoint will add the suggestion to the database.

Possible Errors:
* 400 if body is malformed or fields are missing

Sample Return: 

```
{ 
    "result": 'Success'
}
```

## To Run Locally:

`python wsgi.py`

Or if that doesn't work:

### for Windows:

`venv\Scripts\activate`

`set FLASK_APP=main.py`

`flask run`

After you kill your flask app, end the virtual environment with 

`deactivate`

### for Other:

`venv/bin/activate`

`export FLASK_APP=main.py`

`flask run`

After you kill your flask app, end the virtual environment with 

`deactivate`
