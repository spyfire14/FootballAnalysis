import requests
from bs4 import BeautifulSoup
import re

import sys
sys.path.insert(0, r"C:\Users\user\github\FootballAnalysis\Database")
import InsertTBL

from datetime import datetime


def ContractLoan(Inital,Club, ContractStart, ContractEnd, Notes):

    sql = '''INSERT INTO ContractTBL(PlayerID, Club, ContractStart, ContractEnd, Notes)
            VALUES (?,?,?,?,?)'''
    val = (Inital, club, ContractStart, ContractEnd, Notes)

    InsertTBL.main(sql,val)

def PlayerHistorySQL(PlayerID, FromFC, ToFC, StartDate, EndDate, Fee, Notes, Role):

    sql = '''INSERT INTO HistoryTBL(PlayerID, FromFC, ToFC, StartDate, EndDate, Fee, Notes, Role)
            VALUES (?,?,?,?,?,?,?,?)'''
    val = (PlayerID, FromFC, ToFC, StartDate, EndDate, Fee, Notes, Role)
    InsertTBL.main(sql,val)

def PlayerTransferSQL(PlayerID, DateOfTransfer, Left, Joined, Fee, Notes):

    sql = '''INSERT INTO TransferTBL(PlayerID, DateOfTransfer, Left, Joined, Fee, Notes)
            VALUES (?,?,?,?,?,?)'''
    val = (PlayerID, DateOfTransfer, Left, Joined, Fee, Notes)

    InsertTBL.main(sql,val)

def OpponentSQL(Team):

    sql = '''INSERT INTO OpponentTBL(Team)
            VALUES(?)'''
    val = (Team,)

    InsertTBL.main(sql,val)


def dateConv(date):
    if date == None:
        return None
    elif "/" in date:
        RealDate = date
    else:
        try:
            date = date.replace(",","")
            Date_Obj = datetime.strptime(date, '%b %d %Y')
            year = (datetime.strftime(Date_Obj,'%Y'))
            day = (datetime.strftime(Date_Obj,'%d'))
            months = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12)
            month = (months[datetime.strftime(Date_Obj,'%b')])
            RealDate = str(day)+"/"+str(month)+"/"+str(year)
            return RealDate
        except:
            return date



def HistoryLoader(Website, role):

    StartDateFC = None
    TransferNotes = None
    Inital = None


    res  = requests.get(Website,headers={'User-Agent': 'Mozilla/5.0'})
    content = BeautifulSoup(res.content, 'lxml')

    #Name gather
    for HTMLDiv in content.find_all(class_="dataName"):
        for HTMLH1Span in HTMLDiv.find_all("span"):
            Number = HTMLH1Span.string
            Number = Number.replace("#","")

        for  HTMLH1 in HTMLDiv.find_all("h1"):
            if HTMLH1.attrs["itemprop"] == "name":
                FirstName = HTMLH1.getText()
                FirstName = str(FirstName).replace("'","")

                for  HTMLB in HTMLH1.find_all("b"):
                    LastName = (HTMLB.string).replace("'","")
                    FirstName = FirstName.replace("<B>","")
                    FirstName = FirstName.replace("</B>","")
                    FirstName = FirstName.replace(LastName,"")
                    FirstName = FirstName.replace(" ","")
                    Inital = FirstName[:2] + LastName[:5]
                    Inital = Inital.replace(" ","")
        #table

        for HTMLTable in content.find_all("table", class_="auflistung"):

            for HTMLRow in HTMLTable.find_all("tr"):
                for HTMLRowTitle in HTMLRow.find_all("th"):


                    RowTitle = str(HTMLRowTitle.string.strip())
                    if RowTitle == "Name in home country:":
                        for HTMLRowResult in HTMLRow.find_all("td"):
                            FirstName = HTMLRowResult.string.split()[0]
                            FullName = HTMLRowResult.string
                            FullName = FullName.replace(LastName," ")
                            FullName = FullName.replace(FirstName," ")
                            MiddleName = FullName.replace("  ","")
                            Inital = FirstName[:2] + LastName[:5]
                            Inital = Inital.replace(" ","")

    #Info gather

    for HTMLDiv in content.find_all("div",class_="box transferhistorie viewport-tracking"):
            for HTMLTBody in HTMLDiv.find_all("tbody"):
                CountDate = 1
                RowCount = 1
                Dates = [None] * 100

                for HTMLTr in HTMLTBody.find_all("tr", class_="zeile-transfer"):
                    PlayerHistoryArray = [None] *10
                    RowCount = RowCount + 1
                    TDCount = 0
                    CountDate = CountDate + 1
                    EndDateFC = StartDateFC
                    TransferNotes = ""
                    for HTMLTD in HTMLTr.find_all("td"):
                        TDCount = TDCount + 1

                        if TDCount == 2:
                            PlayerHistoryArray[1] == dateConv(HTMLTD.innerText)
                            if not "<A" in HTMLTD.string:
                                DateFC = HTMLTD.string
                                StartDateFC = dateConv(DateFC)

                        if TDCount == 6:
                            for  HTMLTDA in HTMLTD.find_all("a"):
                                PlayerHistoryArray[2] = str(HTMLTDA.string).replace("'", "")

                        if TDCount == 10:
                            for HTMLTDA in HTMLTD.find_all("a"):
                                PlayerHistoryArray[3] = str(HTMLTDA.string).replace("'", "")

                        if TDCount == 12:
                            Fee = str(HTMLTD.string).lower()

                            if "free" in str(Fee):
                                Fee = 0
                            else:
                                if "loan fee:" in str(Fee):
                                    Fee = Fee.replace("Loan fee:", "")

                                if "£" in str(Fee):
                                    Fee = Fee.replace("£", "")

                                if "-" in str(Fee):
                                    Fee = 0

                                if "th" in str(Fee):
                                    Fee = Fee.replace("th.", "")
                                    Fee = str(int(Fee) * 1000)

                                if "k" in str(Fee):
                                    Fee = Fee.replace("k", "")
                                    Fee = str(int(Fee) * 1000)

                                if "m" in str(Fee):
                                    Fee = Fee.replace("m", "")
                                    Fee = str(int(Fee * 1000000))

                                if "?" in str(Fee):
                                    Fee = 0
                                    TransferNotes = "Not sure on fee"

                                if "end of loan" in str(Fee):
                                    Fee = 0
                                    TransferNotes = "End of loan"

                                if "loan" in str(Fee):
                                    Fee = 0
                                    TransferNotes = "Beginning of loan"

                            PlayerHistoryArray[4] = Fee
                            PlayerHistoryArray[5] = TransferNotes


                        Dates[CountDate] = StartDateFC

                    if "Crawley Town" in str(PlayerHistoryArray[2]):
                        if "Beginning of loan" in str(PlayerHistoryArray[5]):
                            past = datetime.strptime(Dates[CountDate], "%d/%m/%Y")
                            present = datetime.now()
                            if past.date() <= present.date():
                                past = datetime.strptime(Dates[CountDate - 1], "%d/%m/%Y")
                                present = datetime.now()
                                if past.date() >= present.date():
                                    OnLoanAt = "On loan from " + PlayerHistoryArray[2]
                                    ContractLoan(Inital, PlayerHistoryArray[3], dateConv(Dates[CountDate]),dateConv(Dates[CountDate-1]), OnLoanAt)



                    if PlayerHistoryArray[3] == "Retired":
                        DateEndClub = "00:00:00"
                    else:
                        DateEndClub = Dates[CountDate - 1]

                    PlayerHistorySQL(Inital, PlayerHistoryArray[2], PlayerHistoryArray[3], Dates[CountDate], DateEndClub, PlayerHistoryArray[4], PlayerHistoryArray[5], role)
                    PlayerTransferSQL(Inital, Dates[CountDate], PlayerHistoryArray[2], PlayerHistoryArray[3], PlayerHistoryArray[4], PlayerHistoryArray[5])

                    OpponentSQL(PlayerHistoryArray[2])
