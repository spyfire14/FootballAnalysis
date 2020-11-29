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
        return conn
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
        print(create_table_sql)


def main():
    database = str(pathlib.Path(__file__).parent.absolute()) +"\pythonsqlite.db"


    sql_create_player_table = '''CREATE TABLE IF NOT EXISTS PlayerTBL(
                                        PlayerID text,
                                        FirstName text NOT NULL,
                                        MiddleName text,
                                        LastName text,
                                        DOB text,
                                        PlaceOfBirth text,
                                        Height real,
                                        Position text,
                                        Foot text,
                                        CoachingBadges text,
                                        PlayerAgent text,
                                        Wikipedia text,
                                        Notes text,
                                        Camera text,
                                        TransferMarkt text,
                                        Field1 text,
                                        Photo text,
                                        Primary KEY (PlayerID),
                                        UNIQUE(PlayerID,FirstName,LastName,DOB,PlaceOfBirth,Height,Position,Foot)
                                    );'''

    sql_create_nationality_table = '''CREATE TABLE IF NOT EXISTS NationalityTBL(
                                    PlayerID text,
                                    Nationality text,
                                    Primary KEY (PlayerID, Nationality),
                                    UNIQUE(PlayerID,Nationality)
                                )'''

    sql_create_contract_table = '''CREATE TABLE IF NOT EXISTS ContractTBL(
                                    PlayerID text,
                                    Club text NOT NULL,
                                    ContractStart text,
                                    ContractEnd text,
                                    Notes text,
                                    Role text,
                                    Primary KEY (PlayerID, Club, ContractStart, ContractEnd),
                                    UNIQUE(PlayerID,Club,ContractStart,ContractEnd,Notes)
                                )'''

    sql_create_history_table = '''CREATE TABLE IF NOT EXISTS HistoryTBL(
                                    PlayerID text,
                                    FromFC text,
                                    ToFC text,
                                    StartDate text,
                                    EndDate text,
                                    Fee text,
                                    Role text,
                                    Notes,
                                    Primary KEY(PlayerID, FromFC, ToFC, StartDate, EndDate),
                                    UNIQUE(PlayerID, FromFC, ToFC, StartDate, EndDate)
                                )'''

    sql_create_transfer_table = '''CREATE TABLE IF NOT EXISTS TransferTBL(
                                    PlayerID text,
                                    DateOfTransfer text,
                                    Left text,
                                    Joined text,
                                    Fee text,
                                    Notes,
                                    Primary KEY(PlayerID, DateOfTransfer, Left, Joined, Fee, Notes),
                                    UNIQUE(PlayerID, DateOfTransfer, Left, Joined, Fee, Notes)
                                )'''

    sql_create_opponent_table = '''CREATE TABLE IF NOT EXISTS OpponentTBL(
                                    Team text,
                                    Primary KEY(Team),
                                    UNIQUE(Team)
                                )'''

    sql_create_Stadium_table = '''CREATE TABLE IF NOT EXISTS StadiumTBL(
                                    Built text,
                                    Capacity integer,
                                    Standing integer,
                                    Seating integer,
                                    Boxes intefer,
                                    BoxSeats integer,
                                    Cost text,
                                    Length integer,
                                    Width integer,
                                    Heating text,
                                    RunningTrack text,
                                    Surface text,
                                    Address text,
                                    Owner text,
                                    Primary KEY(Address)
                                )'''

    sql_create_Stadium_Name_table = '''CREATE TABLE IF NOT EXISTS StadiumNameTBL(
                                    Address text,
                                    Name text,
                                    Start text,
                                    End text,
                                    Primary KEY(Address, Name)
                                )'''



    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create player table
        create_table(conn, sql_create_player_table)

        # create nationality table
        create_table(conn, sql_create_nationality_table)

        # create contract table
        create_table(conn, sql_create_contract_table)

        create_table(conn, sql_create_history_table)

        create_table(conn, sql_create_transfer_table)

        create_table(conn, sql_create_opponent_table)

        create_table(conn, sql_create_Stadium_table)

        create_table(conn, sql_create_Stadium_Name_table)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
