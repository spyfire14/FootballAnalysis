import sqlite3
import pandas as pd
import pathlib
import os






def sql_fetch(con):

    cursorObj = con.cursor()

    cursorObj.execute('SELECT name from sqlite_master where type="table"')

    tables = cursorObj.fetchall()

    for table_name in tables:
        table_name = table_name[0]
        table = pd.read_sql_query("SELECT * from %s" % table_name, con)
        output_file = os.path.join(r'C:\Users\user\github\FootballAnalysis\Database\DatebaseContents',table_name+".xlsx")

        table.to_excel(output_file, index=False)

def main():
    con = sqlite3.connect(r'C:\Users\user\github\FootballAnalysis\Database\pythonsqlite.db')
    sql_fetch(con)

if __name__ == '__main__':
    main()
