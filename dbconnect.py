import sqlite3
from sqlite3 import Error


import os
basedir = os.path.abspath(os.path.dirname(__file__))


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_cities(conn):

    records = [(1,'Tashkent','41.2995','69.2401'),
               (2, 'Los Angeles', '34.0522', '118.2437'),
               (3, 'New York', '40.7128', '74.0060'),
               (4, 'London', '51.5074', '0.1278'),
               (5, 'Paris', '0.1278', '2.3522'),
               (6, 'Milan', '45.4642', '9.1900')]

    try:
        c = conn.cursor()
        c.executemany( 'INSERT INTO cities(id, name, lat, lon) VALUES(?,?,?,?);', records)
    except Error as e:
        print(e)


def insert_weather(conn, query):
    time =0
    try:
        c = conn.cursor()
        c.execute('SELECT time FROM weather WHERE city_id={id} ORDER BY time DESC LIMIT 1'.format(id=query[6]))
        time = c.fetchone()
        if time:
            time = int(time[0])
    except Error as e:
        print(e)

    try:
        if not time:
            c = conn.cursor()
            c.execute( 'INSERT INTO weather(time, summary, windSpeed, temperature, uvIndex, visibility, city_id) VALUES(?,?,?,?,?,?,?);', query)

        elif time<=query[0]-60:
            c = conn.cursor()
            c.execute( 'INSERT INTO weather(time, summary, windSpeed, temperature, uvIndex, visibility, city_id) VALUES(?,?,?,?,?,?,?);', query)
    except Error as e:
        print(e)


def select_all_cities(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM cities")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def select_weather_by_city(conn, city_id):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """

    cur = conn.cursor()
    cur.execute("SELECT * FROM weather WHERE city_id={my_id}".\
        format(my_id=city_id))

    rows = cur.fetchall()

    for row in rows:
        print(row)

def select_weather_all(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """

    cur = conn.cursor()
    cur.execute("SELECT * FROM weather")

    rows = cur.fetchall()

    return rows



def select_city_by_id(city_id):
    database = os.path.join(basedir, 'data.db')

    # create a database connection
    conn = create_connection(database)

    if conn is not None:
        cur = conn.cursor()
        cur.execute("SELECT * FROM cities WHERE id={my_id}".\
            format(my_id=city_id))

        id_exists = cur.fetchone()
        if id_exists:
            return id_exists
        else:
            print('{} does not exist'.format(city_id))
    

def main():
    database = os.path.join(basedir, 'data.db')

    # create a database connection
    conn = create_connection(database)

    sql_create_cities_table = """ CREATE TABLE IF NOT EXISTS cities (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        lat text,
                                        lon text
                                    ); """

    sql_create_weather_table = """ CREATE TABLE IF NOT EXISTS weather (
                                        
                                        time integer,
                                        summary text,
                                        windSpeed text,
                                        temperature text,
                                        uvIndex integer,
                                        visibility integer,
                                        city_id 
                                    ); """

    # create tables
    if conn is not None:
        # create city table
        create_table(conn, sql_create_cities_table)

        insert_cities(conn)

        # create weather table
        create_table(conn, sql_create_weather_table)



    else:
        print("Error! cannot create the database connection.")

    with conn:

        print("Query all cities")
        select_all_cities(conn)


if __name__ == '__main__':
    main()
