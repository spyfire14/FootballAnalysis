import requests
from bs4 import BeautifulSoup
import re
import sys

sys.path.append(r'C:\Users\user\github\FootballAnalysis\Database')

import Stadium
import InsertTBL


def StadiumTable(Built, Capacity, Standing, Seating, Boxes, BoxSeats, Cost, Length, Width, Heating, RunningTrack, Surface, Address, Owner):

    sql = '''INSERT INTO StadiumTBL(Built, Capacity, Standing, Seating, Boxes, BoxSeats, Cost, Length, Width, Heating, RunningTrack, Surface, Address, Owner)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
    val = (Built, Capacity, Standing, Seating, Boxes, BoxSeats, Cost, Length, Width, Heating, RunningTrack, Surface, Address, Owner)

    InsertTBL.main(sql,val)

def StadiumNameTBL(Address, Name, Start, End):
    sql = '''INSERT INTO StadiumNameTBL(Address, Name, Start, End)
            VALUES (?,?,?,?)'''
    val = (Address, Name, Start, End)

    InsertTBL.main(sql,val)


def stadium(website):
    res = requests.get(website, headers={'User-Agent': 'Mozilla/5.0'})
    content = BeautifulSoup(res.content, 'lxml')
    count = 0
    StadiumFormerlyOne = None
    StadiumFormerlyTwo = None
    StadiumFormerlyThree = None
    StadiumFormerlyOneDates = None
    StadiumFormerlyTwoDates= None
    StadiumFormerlyThreeDates = None

    ZentriertCount = 0
    StadiumAddress = ""

    FormerlyBegin = ""
    FormerlyEnd = ""

    StadiumCost = None
    StadiumOwner = None

    StadiumNamingRights = None
    StadiumNamingRightsYear = None


    for HTMLDiv in content.find_all(class_="content zentriert"):
        ZentriertCount = ZentriertCount + 1
        if ZentriertCount == 1:
            for HTMLTable in HTMLDiv.find_all("table",class_="profilheader"):
                StadiumAddress = ""
                AddressCount = 0
                for HTMLTableTd in HTMLTable.find_all("td"):
                    if AddressCount == 0:
                        StadiumAddress = HTMLTableTd.string
                        AddressCount = 1

                for HTMLTableTd in HTMLTable.find_all("td"):
                    StadiumAddress = StadiumAddress + ", " + HTMLTableTd.string
                    StadiumAddress = StadiumAddress.strip()
                    StadiumAddress = StadiumAddress.replace("'","")

    for HTMLDiv in content.find_all(class_="large-8 columns"):
        count = count + 1
        if count == 1:
            for HTMLTable in HTMLDiv.find_all("table"):
                for HTMLTr in HTMLTable.find_all("tr"):
                    for HTMLTh in HTMLTr.find_all("th"):
                        if "Name" in str(HTMLTh.string):
                            for HTMLTd in HTMLTr.find_all("td"):
                                StadiumName = HTMLTd.string
                                StadiumName = StadiumName.replace("'", "")
                                StadiumName = StadiumName.replace(", ", "")

                        if "capacity" in str(HTMLTh.string):
                            for HTMLTd in HTMLTr.find_all("td"):
                                StadiumCapacity = HTMLTd.string
                                StadiumCapacity = StadiumCapacity.replace(".", "")

                        if "Standing room" in str(HTMLTh.string):
                            for HTMLTd in HTMLTr.find_all("td"):
                                Standingroom = HTMLTd.string
                                Standingroom = Standingroom.replace(".", "")

                        if "Seats" in str(HTMLTh.string):
                            for HTMLTd in HTMLTr.find_all("td"):
                                StadiumSeats = HTMLTd.string
                                StadiumSeats = StadiumSeats.replace(".", "")

                        if "Boxes" in str(HTMLTh.string):
                            for HTMLTd in HTMLTr.find_all("td"):
                                StadiumBoxes = HTMLTd.string
                                StadiumBoxes = StadiumBoxes.replace(".", "")

                        if "Box seats" in str(HTMLTh.string):
                            for HTMLTd in HTMLTr.find_all("td"):
                                StadiumBoxSeats = HTMLTd.string
                                StadiumBoxSeats = StadiumBoxSeats.replace(".", "")

                        if "Built" in str(HTMLTh.string):
                            for HTMLTd in HTMLTr.find_all("td"):
                                StadiumBuilt = HTMLTd.string

                        if "Construction costs" in str(HTMLTh.string):
                            for HTMLTd in HTMLTr.find_all("td"):
                                StadiumCost = HTMLTD.string

                        if "Formerly" in str(HTMLTh.string):
                            for HTMLTd in HTMLTr.find_all("td"):
                                StadiumFormerlyName = HTMLTd.string
                                StadiumNameList = list(StadiumFormerlyName.split(","))
                                for stadium in StadiumNameList:
                                    FormerlyStadium = stadium.replace("'", "").strip()
                                    if "(" in FormerlyStadium:
                                        FormerlyDate = FormerlyStadium.split("(")[1]
                                        FormerlyDate = FormerlyDate.split(")")[0]
                                        FormerlyBegin = FormerlyDate.split("-")[0]
                                        FormerlyEnd = FormerlyDate.split("-")[1]
                                    FormerlyStadium = FormerlyStadium.split(" (")[0]
                                    StadiumNameTBL(StadiumAddress, FormerlyStadium, FormerlyBegin, FormerlyEnd)

                        if "Undersoil heating" in str(HTMLTh.string):
                            for HTMLTd in HTMLTr.find_all("td"):
                                Undersoilheating = HTMLTd.string

                        if "Running track" in str(HTMLTh.string):
                            for HTMLTd in HTMLTr.find_all("td"):
                                Runningtrack = HTMLTd.string

                        if "Surface" in str(HTMLTh.string):
                            for HTMLTd in HTMLTr.find_all("td"):
                                Surface = HTMLTd.string.strip()

                        if "Pitch size" in str(HTMLTh.string):
                            for HTMLTd in HTMLTr.find_all("td"):
                                PitchSize = HTMLTd.string
                                print(PitchSize)
                                PitchLength = PitchSize.split(" x ")[0]
                                PitchWidth = PitchSize.split(" x ")[1]
                                PitchLength = PitchLength.replace("m","").strip()
                                PitchWidth = PitchWidth.replace("m","").strip()

        ZentriertCount = 0

        for HTMLDiv in content.find_all(class_="content zentriert"):
            ZentriertCount = ZentriertCount + 1
            if ZentriertCount == 1:
                for HTMLTable in HTMLDiv.find_all("table",class_="profilheader"):
                    StadiumAddress = ""
                    AddressCount = 0
                    for HTMLTableTd in HTMLTable.find_all("td"):
                        if AddressCount == 0:
                            StadiumAddress = HTMLTableTd.string
                            AddressCount = 1

                    for HTMLTableTd in HTMLTable.find_all("td"):
                        StadiumAddress = StadiumAddress + ", " + HTMLTableTd.string
                        StadiumAddress = StadiumAddress.strip()
                        StadiumAddress = StadiumAddress.replace("'","")

            if ZentriertCount == 3:
                for HTMLTable in HTMLDiv.find_all("table",class_="profilheader"):
                    HTMLTDCount = 0
                    for HTMLTableTd in HTMLTable.find_all("td"):
                        HTMLTDCount = HTMLTDCount + 1
                        if HTMLTDCount == 1:
                            StadiumOwner = HTMLTableTd.string
                            StadiumOwner = StadiumOwner.replace("'","")
                        if HTMLTDCount == 2:
                            StadiumNamingRights  = HTMLTableTd.string
                            StadiumNamingRights  = StadiumNamingRights.replace("'","")
                        if HTMLTDCount == 3:
                            StadiumNamingRightsYear = HTMLTableTd.string

    StadiumTable(StadiumBuilt, StadiumCapacity, Standingroom, StadiumSeats, StadiumBoxes, StadiumBoxSeats, StadiumCost, PitchLength, PitchWidth, Undersoilheating, Runningtrack, Surface, StadiumAddress, StadiumOwner)
    StadiumNameTBL(StadiumAddress, StadiumNamingRights, "N/A", StadiumNamingRightsYear)
