import requests
from bs4 import BeautifulSoup

import Player_Loader
import Player_History

if __name__ == "__main__":
    url = 'https://www.transfermarkt.co.uk/crawley-town/kader/verein/3537/plus/0/galerie/0?saison_id=2020'
    res  = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
    content = BeautifulSoup(res.content, 'lxml')

    for HTMLTable in content.find_all('table', class_="items"):
        for HTMLBody in HTMLTable.find_all("tbody"):
            for HTMLRow in HTMLBody.find_all("tr"):
                for HTMLTd in HTMLRow.find_all("td", class_="hauptlink"):
                    for HTMLSpan in HTMLTd.find_all("span", class_="hide-for-small"):
                        for HTMLHyp in HTMLSpan.find_all("a"):
                            Website = "https://www.transfermarkt.co.uk" + HTMLHyp.attrs['href']
                            Player_Loader.Loader(Website, "player")
                            Player_History.HistoryLoader(Website, "player")
