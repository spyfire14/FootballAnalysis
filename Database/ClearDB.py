import sqlite3
from sqlite3 import Error


def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def delete_all_DB(conn,db):
    """
    Delete all rows in the tasks table
    :param conn: Connection to the SQLite database
    :return:
    """
    sql = 'DELETE FROM ' + db
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def main():
    database = r"C:\Users\user\github\FootballAnalysis\Database\pythonsqlite.db"

    # create a database connection
    conn = create_connection(database)

    dbs = ["PlayerTBL","NationalityTBL","ContractTBL"]

    for db in dbs:
        with conn:
            delete_all_DB(conn,db);


if __name__ == '__main__':
    main()
