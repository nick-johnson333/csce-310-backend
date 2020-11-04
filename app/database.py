import psycopg2

conn = None
def open_db():
    try:
        global conn
        conn = psycopg2.connect(
            host="ec2-52-1-95-247.compute-1.amazonaws.com",
            port="5432",
            database="d89uja0jkmio1h",
            user="ijexgsielqcyxr",
            password="90a3789a8b5ceea5f70502e7905a17f4c8b61fe7b88d856d2823af2d6c80bebd"
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit(-1)

def close_db():
    global conn
    if conn is not None:
        conn.close()

def is_db_open():
    global conn
    return conn is not None

def build_dicts(cursor, rows: list):
    colnames = [desc[0] for desc in cursor.description]
    all_data = []
    for row in rows:
        i = 0
        data = {}
        for col in colnames:
            data[col] = row[i]
            i+=1
        all_data.append(data)
    return all_data

def getAllFromUserSuggestionsTable():
    global conn
    open_db() # HAVE AT START OF ALL FUNCTIONS
    cur = conn.cursor()

    cur.execute('SELECT * from user_suggestions')

    rows = cur.fetchall()
    data = build_dicts(cur,rows)
    cur.close()
    close_db() # HAVE AT END OF ALL FUNCTIONS
    return data

def addUserSuggestionToDatabase(user_name, suggestion):
    global conn
    print('here')
    try:
        open_db()
        cur = conn.cursor()
        print('pre execute')
        cur.execute(f'''insert into user_suggestions (user_name, suggestion) values('{user_name}','{suggestion}');''');
        conn.commit()
        print('post execute')
        cur.close()
        close_db()
        return 'Success'
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        return 'Error'

def removeUserSuggestion(suggestion_id):
    try:
        open_db()
        cur = conn.cursor()
        print('pre execute')
        cur.execute(f'''delete from user_suggestions where id = {suggestion_id}''');
        conn.commit()
        print('post execute')
        cur.close()
        close_db()
        return 'Success'
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        return 'Error'