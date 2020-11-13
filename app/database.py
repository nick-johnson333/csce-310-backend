import psycopg2
from app.BlankException import BlankException

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
    print("QUERY:",query_string)
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
        raise BlankException(error)


def build_where_clause(**kwargs):
    any_not_none = False
    clause = ' where '
    for(key,val) in kwargs.items():
        if val is None:
            continue
        clause += f'''{key} = '{val}' and '''
        any_not_none = True
    if any_not_none is False:
        return ''
    return clause[:-4]


def build_insert_clause(**kwargs):
    columns = ''
    values = ''
    for (key, val) in kwargs.items():
        val = val.replace("'","''")
        columns += (key + ',')
        values += ("'" + str(val) + "',")
    columns = columns[:-1]
    values = values[:-1]
    return f'''({columns}) values ({values})'''


def select(table_name, limit, **kwargs):
    query_string = f'''select * from {table_name} '''
    query_string += build_where_clause(**kwargs)
    query_string += f'''limit {limit};'''
    return executeQuery(query_string)


def insert(table_name, **kwargs):
    query_string = f'''insert into {table_name}'''
    query_string += build_insert_clause(**kwargs)
    query_string += ';'
    return executeQuery(query_string)


def delete(table_name, **kwargs):
    query_string = f'''delete from {table_name}'''
    query_string += build_where_clause(**kwargs)
    query_string += ';'
    return executeQuery(query_string)
