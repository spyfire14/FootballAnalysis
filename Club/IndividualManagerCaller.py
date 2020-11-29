import sys
sys.path.insert(0, r"C:\Users\user\github\FootballAnalysis\Database")

import Reset
import showTBLxlsx
import Manager

Website = "https://www.transfermarkt.co.uk/john-yems/profil/trainer/76935"

Reset.main()

Manager.main(Website,"manager")



showTBLxlsx.main()
