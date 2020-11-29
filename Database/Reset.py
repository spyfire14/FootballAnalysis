import ClearExcel
import CreateDB
import os
import CreateTBL


def main():

    ClearExcel.main()

    os.remove(r"C:\Users\user\github\FootballAnalysis\Database\pythonsqlite.db")

    CreateDB.main()

    CreateTBL.main()


if __name__ == '__main__':
    main()
