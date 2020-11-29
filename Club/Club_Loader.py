import requests
from bs4 import BeautifulSoup
import re

import Stadium
import Manager

def main(website):
    res = requests.get(Website, headers={'User-Agent': 'Mozilla/5.0'})
    content = BeautifulSoup(res.content, 'lxml')

    #Team Name#

    for HTMLDiv in content.find_all(class_="dataName"):
        for HTMLH1 in HTMLDiv.find_all("h1"):
            if HTMLH1.attrs["itemprop"] == "name":
                for HTMLSpan in HTMLH1.find_all("span"):
                    TeamName = HTMLSpan.string

    for HTMLDiv in content.find_all(class_="dataZusatzDaten"):
        for HTMLSpan in HTMLDiv.find_all("span", class_="hauptpunkt"):
            for HTMLA in HTMLSpan.find_all("a"):
                TeamLeague = HTMLA.string.strip()

    for HTMLDiv in content.find_all(class_="dataBottom"):
        dataDaten = 0
        for HtMLDaten in content.find_all(class_="dataDaten"):
            dataDaten = dataDaten + 1
            if dataDaten == 2:
                HTMLPCount = 0
                for HTMLP in HtMLDaten.find_all("p"):
                    HTMLPCount = HTMLPCount + 1
                    if HTMLPCount == 2:
                        for HTMLSpan in HTMLP.find_all("span", class_="dataValue"):
                            for HTMLAStadium in HTMLSpan.find_all("a"):
                                StadiumName = HTMLAStadium.string.replace("'", "")
                                StadiumWebsite = HTMLAStadium.attrs["href"]
                                StadiumWebsite = "https://www.transfermarkt.co.uk" + StadiumWebsite
                                Stadium.stadium(StadiumWebsite)

    for HTMLDiv in content.find_all(class_="container-hauptinfo"):
        for HTMLDivA in HTMLDiv.find_all("a"):
            ManagerWebsite = HTMLDivA.attrs["href"]
            ManagerWebsite = "https://www.transfermarkt.co.uk" + ManagerWebsite
            Manager.main(ManagerWebsite,"manager")


if __name__ == '__main__':
    Website = "https://www.transfermarkt.co.uk/crawley-town/transfers/verein/3537/saison_id/2020"
    main(Website)
