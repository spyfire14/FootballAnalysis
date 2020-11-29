import requests
from bs4 import BeautifulSoup
import re

import sys
sys.path.insert(0, r"C:\Users\user\github\FootballAnalysis\Squad")
import Player_Loader

from datetime import datetime

def main(Website, Role):
    Player_Loader.Loader(Website, "Manager")
    managerHistory(Website,"Manager")

def managerHistory(Website,Role):
    res = requests.get(Website, headers={'User-Agent': 'Mozilla/5.0'})
    content = BeautifulSoup(res.content, 'lxml')

    #Team Name#

    for HTMLTable in content.find_all("table",class_="items"):
        for HTMLTBody in HTMLTable.find_all("tbody"):
            for HTMLTr in HTMLTBody.find_all("tr"):
                HTMLTDCount = 1
                for HTMLTD in HTMLTr.find_all("td"):
                    HTMLTDCount = HTMLTDCount + 1
                    if HTMLTDCount == 3:
                        for HTMLa in HTMLTD.find_all("a"):
                            TeamName = HTMLTa.string
                    if HTMLTDCount == 4:
                        JoinDate = HTMLTD.string
                        JoinDate = JoinDate.split("(")[1]
                        JoinDate = JoinDate.split(")")[0]
                    if HTMLTDCount == 5:
                        FinishDateCorrect = HTMLTD.string
                        if "expected" in FinishDateCorrect:
                            FinishDate = ""
                        else:
                            FinishDate = FinishDateCorrect.split("(")[1]
                            FinishDate = FinishDate.split(")")[0]
                    if HTMLTDCount == 5:
                        JobPosition = HTMLTD.innerText
