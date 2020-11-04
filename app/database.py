import psycopg2
from app.DatabaseException import DatabaseException

conn = None
def open_db():
    global conn
    conn = psycopg2.connect(
        host="ec2-52-1-95-247.compute-1.amazonaws.com",
        port="5432",
        database="d89uja0jkmio1h",
        user="ijexgsielqcyxr",
        password="90a3789a8b5ceea5f70502e7905a17f4c8b61fe7b88d856d2823af2d6c80bebd"
    )

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

def executeQuery(query_string):
    try:
        open_db()
        cur = conn.cursor()
        cur.execute(query_string)
        conn.commit()
        if 'select' in query_string.lower():
            rows = cur.fetchall()
            data = build_dicts(cur, rows)
            cur.close()
            close_db()
            return data
        return 'Success'
    except(Exception, psycopg2.DatabaseError) as error:
        raise DatabaseException(error)