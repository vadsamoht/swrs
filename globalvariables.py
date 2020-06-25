from datetime import date

#
#   DATABASE GLOBALS
#
DATABASE = './runs_db.sqlite'

DATABASE_VERSION = 'v0.9.2020-6-23'

DATESTAMP = date.today().strftime("%Y%m%d")

#
#   GAME/SRC GLOBALS
#
game_id = "rogue1"

il_platform_names = ["Nintendo 64",
                     "PC"]

il_medal_names = ["Any Medal",
                  "Gold Medal"]

il_category_names = ["X-Wing",
                     "Y-Wing",
                     "A-Wing",
                     "V-Wing",
                     "Speeder",
                     "Millennium Falcon",
                     "TIE Interceptor",
                     "Naboo Starfighter",
                     "T-16 Skyhopper"]

il_level_names = ["Ambush at Mos Eisley",
                  "Rendezvous on Barkhesh",
                  "The Search for the Nonnah",
                  "Defection at Corellia",
                  "Liberation of Gerrard V",
                  "The Jade Moon",
                  "Imperial Construction Yards",
                  "Assault on Kile II",
                  "Rescue on Kessel",
                  "Prisons of Kessel",
                  "Battle Above Taloraan",
                  "Escape From Fest",
                  "Blockade on Chandrila",
                  "Raid on Sullust",
                  "Moff Seerdon's Revenge",
                  "The Battle of Calamari",
                  "Beggar's Canyon",
                  "The Death Star Trench Run",
                  "The Battle of Hoth"]

il_variable_ids = {"onvvdwnm":"Platform",
                   "zqoe7gly":"PC",
                   "rqv2n516":"N64",
                   "jq63o9vq":"EMU",
                   "78966vq8":"Medal Awarded",
                   "z197emjl":"Any Medal",
                   "p123jdvl":"Gold Medal"}

bad_il_combinations = [["Defection at Corellia", "X-Wing"],
                       ["Defection at Corellia", "A-Wing"],
                       ["Defection at Corellia", "Millennium Falcon"],
                       ["Defection at Corellia", "TIE Interceptor"],
                       ["Defection at Corellia", "Y-Wing"],
                       ["Defection at Corellia", "V-Wing"],
                       ["Defection at Corellia", "Naboo Starfighter"],
                       ["Imperial Construction Yards", "X-Wing"],
                       ["Imperial Construction Yards", "A-Wing"],
                       ["Imperial Construction Yards", "Millennium Falcon"],
                       ["Imperial Construction Yards", "TIE Interceptor"],
                       ["Imperial Construction Yards", "Y-Wing"],
                       ["Imperial Construction Yards", "V-Wing"],
                       ["Imperial Construction Yards", "Naboo Starfighter"],
                       ["Rescue on Kessel", "A-Wing"],
                       ["Rescue on Kessel", "Speeder"],
                       ["Rescue on Kessel", "Millennium Falcon"],
                       ["Rescue on Kessel", "TIE Interceptor"],
                       ["Rescue on Kessel", "V-Wing"],
                       ["Rescue on Kessel", "Naboo Starfighter"],
                       ["Escape From Fest", "X-Wing"],
                       ["Escape From Fest", "A-Wing"],
                       ["Escape From Fest", "Millennium Falcon"],
                       ["Escape From Fest", "TIE Interceptor"],
                       ["Escape From Fest", "Y-Wing"],
                       ["Escape From Fest", "V-Wing"],
                       ["Escape From Fest", "Naboo Starfighter"],
                       ["Beggar's Canyon", "X-Wing"],
                       ["Beggar's Canyon", "A-Wing"],
                       ["Beggar's Canyon", "Speeder"],
                       ["Beggar's Canyon", "Millennium Falcon"],
                       ["Beggar's Canyon", "TIE Interceptor"],
                       ["Beggar's Canyon", "Y-Wing"],
                       ["Beggar's Canyon", "V-Wing"],
                       ["Beggar's Canyon", "Naboo Starfighter"],
                       ["The Death Star Trench Run", "A-Wing"],
                       ["The Death Star Trench Run", "Speeder"],
                       ["The Death Star Trench Run", "Millennium Falcon"],
                       ["The Death Star Trench Run", "TIE Interceptor"],
                       ["The Death Star Trench Run", "Y-Wing"],
                       ["The Death Star Trench Run", "V-Wing"],
                       ["The Battle of Hoth", "X-Wing"],
                       ["The Battle of Hoth", "A-Wing"],
                       ["The Battle of Hoth", "Millennium Falcon"],
                       ["The Battle of Hoth", "TIE Interceptor"],
                       ["The Battle of Hoth", "Y-Wing"],
                       ["The Battle of Hoth", "V-Wing"],
                       ["The Battle of Hoth", "Naboo Starfighter"],
                       ["Ambush at Mos Eisley", "T-16 Skyhopper"],
                       ["Rendezvous on Barkhesh", "T-16 Skyhopper"],
                       ["The Search for the Nonnah", "T-16 Skyhopper"],
                       ["Defection at Corellia", "T-16 Skyhopper"],
                       ["Liberation of Gerrard V", "T-16 Skyhopper"],
                       ["The Jade Moon", "T-16 Skyhopper"],
                       ["Imperial Construction Yards", "T-16 Skyhopper"],
                       ["Assault on Kile II", "T-16 Skyhopper"],
                       ["Rescue on Kessel", "T-16 Skyhopper"],
                       ["Prisons of Kessel", "T-16 Skyhopper"],
                       ["Battle Above Taloraan", "T-16 Skyhopper"],
                       ["Escape From Fest", "T-16 Skyhopper"],
                       ["Blockade on Chandrila", "T-16 Skyhopper"],
                       ["Raid on Sullust", "T-16 Skyhopper"],
                       ["Moff Seerdon's Revenge", "T-16 Skyhopper"],
                       ["The Battle of Calamari", "T-16 Skyhopper"],
                       ["Beggar's Canyon", "T-16 Skyhopper"],
                       ["The Death Star Trench Run", "T-16 Skyhopper"],
                       ["The Battle of Hoth", "T-16 Skyhopper"]]

class textcol:
   INFO = '\033[93m' # yellow
   BODY = '\033[0m' # white
   WARN = '\033[91m' # red
   OK = '\033[92m' # green
