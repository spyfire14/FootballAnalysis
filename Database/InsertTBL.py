import sqlite3
from sqlite3 import Error
import pathlib

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(sql,values)
        print(e)

    return conn


def intoDB(conn, sql, values):
    cur = conn.cursor()
    if sql == None or values == None:
        return
    else:
        try:
            cur.execute(sql, values)
            conn.commit()
        except Error as e:
            if not "UNIQUE" or "NULL" in str(e):
                print(sql,values)
                print(e)

        return cur.lastrowid

def main(sql, values):
    database = str(pathlib.Path(__file__).parent.absolute()) +"\pythonsqlite.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        intoDB(conn, sql, values)
