import requests
from bs4 import BeautifulSoup
import re

import sys
sys.path.insert(0, r"C:\Users\user\github\FootballAnalysis\Database")
import InsertTBL

from datetime import datetime



def NationalityDB(PlayerID, Nationality):

    sql = '''INSERT INTO NationalityTBL(PlayerID, Nationality)
            VALUES(?,?)'''
    val = (PlayerID, Nationality)

    InsertTBL.main(sql,val)



def ContractDB(PlayerID, Club, ContractStart, ContractEnd, Notes, Role):

    sql = '''INSERT INTO ContractTBL(PlayerID, Club, ContractStart, ContractEnd, Notes, Role)
            VALUES (?,?,?,?,?,?)'''
    val = (PlayerID, Club, ContractStart, ContractEnd, Notes, Role)

    InsertTBL.main(sql,val)



def PlayerDB(Inital, FirstName, MiddleName, LastName, DateOfBirth, PlaceOfBirth, Height, Position, FootSide, PlayerAgent, WebsiteName):

    sql = '''INSERT INTO PlayerTBL(PlayerID, FirstName, MiddleName, LastName, DOB, PlaceOfBirth, Height, Position, Foot, PlayerAgent, TransferMarkt)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)'''
    val = (Inital, FirstName, MiddleName, LastName, DateOfBirth, PlaceOfBirth, Height, Position, FootSide, PlayerAgent, WebsiteName)

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

def Loader(Website, Role):
    res  = requests.get(Website,headers={'User-Agent': 'Mozilla/5.0'})
    content = BeautifulSoup(res.content, 'lxml')

    #Initalise
    DateOfBirth = None
    PlaceOfBirth = None
    Citizenship1 = None
    Height = None
    Position = None
    FootSide = None
    ContractNotes = ""
    CurrentClub = None
    Agent = None
    MiddleName = None

    ContractDate = None
    ContractExt = None


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



    for HTMLTable in content.find_all("table", class_="auflistung"):
        for HTMLRow in HTMLTable.find_all("tr"):
            for HTMLRowTitle in HTMLRow.find_all("th"):

                RowTitle = str(HTMLRowTitle.string.strip())
                if "Date" in RowTitle:
                    for HTMLRowResult in HTMLRow.find_all("td"):

                        DateOfBirth = HTMLRowResult.string
                        if DateOfBirth is not None:
                            Present = True
                            DateOfBirth = DateOfBirth.replace(",","")
                            DofB_Obj = datetime.strptime(DateOfBirth, '%b %d %Y')
                            year = (datetime.strftime(DofB_Obj,'%Y'))
                            day = (datetime.strftime(DofB_Obj,'%d'))
                            months = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12)
                            month = (months[datetime.strftime(DofB_Obj,'%b')])
                            DateOfBirth = dateConv(DateOfBirth)

                        for HTMLHyperLink in HTMLRowResult.find_all("a"):
                            DateOfBirth = HTMLHyperLink.string
                            Present = True
                            DateOfBirth = DateOfBirth.replace(",","")
                            DofB_Obj = datetime.strptime(DateOfBirth, '%b %d %Y')
                            year = (datetime.strftime(DofB_Obj,'%Y'))
                            day = (datetime.strftime(DofB_Obj,'%d'))
                            months = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12)
                            month = (months[datetime.strftime(DofB_Obj,'%b')])
                            DateOfBirth = dateConv(DateOfBirth)



                if RowTitle == "Name in home country:":
                    for HTMLRowResult in HTMLRow.find_all("td"):
                        FirstName = HTMLRowResult.string.split()[0]
                        FullName = HTMLRowResult.string
                        FullName = FullName.replace(LastName," ")
                        FullName = FullName.replace(FirstName," ")
                        MiddleName = FullName.replace("  ","")



                #Place of birth

                if RowTitle == "Place of birth:":
                    for HTMLRowResult in HTMLRow.find_all("td"):
                        for HTMLSpan in HTMLRowResult.find_all("span"):
                            PlaceOfBirth = HTMLSpan
                            #PlaceOfBirth = PlaceOfBirth.replace("&nbsp;", "")
                            PlaceOfBirth = re.sub('<img.*?>','', str(PlaceOfBirth))
                            PlaceOfBirth = PlaceOfBirth.replace("<span>","")
                            PlaceOfBirth = PlaceOfBirth.replace("</span>","")
                            PlaceOfBirth = PlaceOfBirth.replace(" ","")
                            PlaceOfBirth = PlaceOfBirth.strip("\xa0")

                #Height

                if RowTitle == "Height:":
                    for HTMLRowResult in HTMLRow.find_all("td"):
                        Height = HTMLRowResult.string

                        Height = Height.replace(",", ".")
                        Height = Height.replace("&nbsp;m", "")
                        Height = Height.replace("\xa0","")

                #Position

                if RowTitle == "Position:":
                    for HTMLRowResult in HTMLRow.find_all("td"):
                        Position = HTMLRowResult.string
                        Position = Position.strip('\n')
                        Position = Position.replace("  ","")

                if RowTitle == "Player agent:":
                    for HTMLRowResult in HTMLRow.find_all("a"):
                        Agent = HTMLRowResult.string

                #Foot

                if HTMLRowTitle.string == "Foot:":

                    for  HTMLRowResult in HTMLRow.find_all("td"):
                        FootSide = HTMLRowResult.string

                #Citizenship

                if RowTitle == "Citizenship:":
                    for HTMLRowResult in HTMLRow.find_all("td"):
                        for HTMLImg in HTMLRowResult.find_all("img"):
                            Citizenship1 = HTMLImg.attrs["title"]
                            Citizenship1 = Citizenship1.replace("'","")

                            Inital = FirstName[:2] + LastName[:5]
                            Inital = Inital.replace(" ","")

                            NationalityDB(Inital,Citizenship1)

                if RowTitle == "Current club:":
                    for HTMLRowResult in HTMLRow.find_all("a"):
                        CurrentClub = (HTMLRowResult.string)

                if RowTitle == "Contract expires:":
                    for HTMLRowResult in HTMLRow.find_all("td"):
                        ContractExt = dateConv(HTMLRowResult.string.strip('\n').replace("  ",""))

                if RowTitle == "Contract option:":
                    for HTMLRowResult in HTMLRow.find_all("td"):
                        ContractNotes = ContractNotes + " " + HTMLRowResult.string

                if RowTitle == "Date of last contract extension:" or RowTitle == "Joined:":
                    for HTMLRowResult in HTMLRow.find_all("td"):
                        ContractDate = dateConv(HTMLRowResult.string.strip('\n').replace("  ",""))

                if RowTitle == "On loan":
                    for HTMLRowResult in HTMLRow.find_all("td"):
                        ContractNotes = ContractNotes + " On loan from: " + HTMLRowResult.string
                        LoanFrom = HTMLRowResult.string


                if RowTitle == "Contract there expires":
                    for HTMLRowResult in HTMLRow.find_all("td") :
                        ContractNotes = ContractNotes + " Contract expires on:" + HTMLRowResult.string
                        LoanFromFinishDate = HTMLRowResult.string
                        if InStr(LoanFromFinishDate, "-"):
                            LoanFromFinishDate = "00:00:00"
                        else:
                            LoanFromFinishDate = format(LoanFromFinishDate, "dd/mm/yyyy")
                            LoanFromFinishDate = LoanFromFinishDate.replace(".", "/")

                        OnLoanAt = "On loan at " + CurrentClub

                        ContractDB(Inital, LoanFrom, "00:00:00", LoanFromFinishDate, OnLoanAt)


    if not FirstName:
        FirstName = None

    if not LastName:
        LastName = None

    if not DateOfBirth:
        DateOfBirth = None

    if not PlaceOfBirth:
        PlaceOfBirth = None

    if not Citizenship1:
        Citizenship1 = None

    if not Height:
        Height = None

    if not Position:
        Position = None

    if not FootSide:
        FootSide = None

    Inital = FirstName[:2] + LastName[:5]
    Inital = Inital.replace(" ","")

    #Database adding
    PlayerDB(Inital, FirstName, MiddleName, LastName, DateOfBirth, PlaceOfBirth, Height, Position, FootSide, Agent, Website)
    ContractDB(Inital, CurrentClub, ContractDate, ContractExt, ContractNotes, Role)
