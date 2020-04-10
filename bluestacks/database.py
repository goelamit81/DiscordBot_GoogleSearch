import psycopg2
from datetime import datetime

import environment as env

################################################################################################

# Function to establish postgre db connection
def get_db_connection():

    psql_conn = psycopg2.connect(host=env.PSQL_DB_HOST,
    port=env.PSQL_DB_PORT,
    user=env.PSQL_DB_USER,
    password=env.PSQL_DB_PASSWORD,
    database=env.PSQL_DB_NAME,
    sslmode='require')

    return psql_conn

################################################################################################

# Function to setup search history table upon bot startup if not already setup
def setup_search_history_table():

    db_connection = get_db_connection()
    sql_cursor = db_connection.cursor()

    sql_cursor.execute("create table if not exists public.search_history (user_id varchar(300), search_key varchar(300), created_timestamp timestamp, primary key(user_id, search_key))")
    
    db_connection.commit()

    try:
        sql_cursor.close()
        db_connection.close()
    except:
        pass

################################################################################################

# Function to persist search history in search history table with input user id and search keyword
def create_search_history(user_id, search_keyword):
    db_connection = get_db_connection()
    sql_cursor = db_connection.cursor()

    sql_cursor.execute("insert into public.search_history(user_id, search_key, created_timestamp) Values('{}', '{}', '{}') on conflict (user_id, search_key) do update set created_timestamp = '{}'".format(
        user_id, search_keyword, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    db_connection.commit()

    try:
        sql_cursor.close()
        db_connection.close()
    except:
        pass

################################################################################################

# Function to return related search history based on input user id and search keyword
def get_search_history(user_id, search_keyword):
    db_connection = get_db_connection()
    sql_cursor = db_connection.cursor()
    sql_cursor.execute("select search_key from public.search_history where user_id = '{}' and search_key like '%{}%'".format(user_id, search_keyword))

    results = sql_cursor.fetchall()

    try:
        sql_cursor.close()
        db_connection.close()
    except:
        pass

    return results
    
################################################################################################