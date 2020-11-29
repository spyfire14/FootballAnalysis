import Player_Loader
import Player_History
import Reset
import showTBLxlsx

Website = "https://www.transfermarkt.co.uk/max-watters/profil/spieler/586023"

Reset.main()

#Player_Loader.Loader(Website)
Player_History.HistoryLoader(Website)



showTBLxlsx.main()
