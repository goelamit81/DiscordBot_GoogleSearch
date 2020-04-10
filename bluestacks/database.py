import mysql.connector
from datetime import datetime

import environment as env

################################################################################################

# Function to establish mysql db connection
def get_db_connection():
    config = {
        'user': env.MYSQL_DB_USER,
        'password': env.MYSQL_DB_PASSWORD,
        'host': env.MYSQL_DB_HOST,
        'database': env.MYSQL_DB_NAME,
    }

    db_connection = mysql.connector.connect(**config)
    
    return db_connection

################################################################################################

# Function to setup search history table upon bot startup if not already setup
def setup_search_history_table():

    db_connection = get_db_connection()
    cur = db_connection.cursor()

    cur.execute(
        '''
            CREATE TABLE IF NOT EXISTS search_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                created DATETIME,
                search_key VARCHAR(255) NOT NULL UNIQUE
            )
        '''
    )

    try:
        cur.close()
        db_connection.close()
    except:
        pass

################################################################################################

# Function to persist search history in search history table
def create_search_history(search_keyword):

    statement = (
        '''
        REPLACE  INTO search_history
        (search_key, created)
        VALUES (%s, %s)
        '''
    )
    db_connection = get_db_connection()
    data = (search_keyword, datetime.utcnow())
    cur = db_connection.cursor()

    cur.execute(statement, data)

    db_connection.commit()

    try:
        cur.close()
        db_connection.close()
    except:
        pass

################################################################################################

# Function to return related search history based on input search keyword
def get_search_history(search_keyword):

    db_connection = get_db_connection()
    cur = db_connection.cursor()
    cur.execute(
        '''
        SELECT search_key FROM search_history where search_key LIKE '%{}%' 
        ORDER BY created DESC
        '''.format(search_keyword)
    )
    search_results = []
    for result in cur.fetchall():
        search_results.append(result[0])

    try:
        cur.close()
        db_connection.close()
    except:
        pass

    return search_results

################################################################################################