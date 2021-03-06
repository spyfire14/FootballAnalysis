import sqlite3
from sqlite3 import Error
import pathlib

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    CurrentFolder = str(pathlib.Path(__file__).parent.absolute()) +"\pythonsqlite.db"
    print(CurrentFolder)
    create_connection(CurrentFolder)
