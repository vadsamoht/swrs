
import sqlite3 as lite
import sys
import time
import os.path
from datetime import date

import srcomapi, srcomapi.datatypes as dt
api = srcomapi.SpeedrunCom(); api.debug = 0

class textcol:
    INFO = '\033[93m' # yellow
    BODY = '\033[0m' # white
    WARN = '\033[91m' # red
    OK = '\033[92m' # green

#...
#   GLOBALS
#
debug = True
short_run = False
#
#   DATABASE GLOBALS
#
DATABASE = './runs_db.sqlite'
DATABASE_VERSION = 'v0.6.2020-6-12'
DATESTAMP = date.today().strftime("%Y%m%d")
#
#   GAME/SRC GLOBALS
#
game_id = "rogue1"
il_platform_names = ["Nintendo 64",
                    "PC"]
il_category_names = ["X-Wing",
                    "Y-Wing",
                    "A-Wing",
                    "V-Wing",
                    "Speeder",
                    "Millennium Falcon",
                    "TIE Interceptor",
                    "Naboo Starfighter"]
il_level_names = ["Ambush at Mos Eisley",
                  "The Search for the Nonnah",
                  "Defection at Corellia",
                  "Liberation of Gerrard V",
                  "The Jade Moon",
                  "Imperial Construction Yards",
                  "Assault on Kile II",
                  "Rescue on Kessel",
                  "Prisons of Kessel",
                  "Battle Above Taloraan",
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
                       ["Escape from Fest", "X-Wing"],
                       ["Escape from Fest", "A-Wing"],
                       ["Escape from Fest", "Millennium Falcon"],
                       ["Escape from Fest", "TIE Interceptor"],
                       ["Escape from Fest", "Y-Wing"],
                       ["Escape from Fest", "V-Wing"],
                       ["Escape from Fest", "Naboo Starfighter"],
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
                       ["The Battle of Hoth", "Naboo Starfighter"],]

def createNewDb():
  if debug:
    print("Creating database from scratch\n")

  # Remove old DB if present
  try:
    os.remove(DATABASE)
  except OSError:
    pass

  # Create connection to the DB
  con = lite.connect(DATABASE)

  # Create basic metadata table
  with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE metadata (" +
                "field          text primary key," +
                "value          text)")

  # Add database version to metadata
  with con:
    cur = con.cursor()
    cur.execute("INSERT INTO metadata (field, value) " +
                "VALUES (?, ?)",
                ['db_version', DATABASE_VERSION])
  return


def updateDb():
  if debug:
    print("Updating existing", DATABASE, "\n")

  # Create connection to the DB
  con = lite.connect(DATABASE)

  # Create the tables with necessary rows
  with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS il_runs_" + DATESTAMP + " (" +
                "run_id          integer primary key," +
                "level           text," +
                "category        text," +
                "player          text," +
                "time            integer default 9999," +
                "platform        text," +
                "medal           text," +
                "src_link        text)")
  
  # Add database version to metadata
  with con:
    cur = con.cursor()
    cur.execute("REPLACE INTO metadata (field, value) " +
                "VALUES (?, ?)",
                ['last_update', DATESTAMP])

  return


def get_il_leaderboard(game, category, level):
  # Takes in a GAME being run, a CATEGORY (e.g. X-Wing) and a LEVEL (e.g. AaME) 
  # and returns for each run on the leaderboard:
  #    - Player Name
  #    - Time (in seconds, according to the primary method set on SRC)
  #    - Platform played on
  #    - Variables (TO BE ADDED)

  if(debug):
    print("Scraping", textcol.INFO +level.name, ":", category.name + textcol.BODY, "...")

  out = []
  if (debug):
    print("http://speedrun.com/api/v1/leaderboards/{}/level/{}/{}?embed=variables".format(game.id, level.id, category.id))
  il_board = dt.Leaderboard(api, data=api.get("leaderboards/{}/level/{}/{}?embed=variables".format(game.id, level.id, category.id)))

  #print(il_board)
  #print(il_board.runs)
  if il_board.runs != []:
    for il_run in il_board.runs:
      player_name = il_run["run"].players[0].name
      run_time = il_run["run"].times["primary_t"]

      # get platform hash
      platform_id = il_variable_ids[il_run["run"].values["onvvdwnm"]]
      #platform_id = il_run["run"].system["platform"] #Don't use this - use the one from variables instead

      # get medal hash
      medal_type = il_variable_ids[il_run["run"].values["78966vq8"]]

      # get SRC link
      weblink = il_run["run"].weblink

      out.append([level.name, category.name, player_name, run_time, platform_id, medal_type, weblink])
  else:
    if(debug):
      print("                NO ENTRIES            ")
    pass

  return(out)


def add_il_run_to_db(run_data):
  # [level.name, 
  #  category.name,
  #  player_name,
  #  run_time, 
  #  platform_id,
  #  medal_type,
  #  src_link]
  
  # Create connection to the DB
  con = lite.connect(DATABASE)
  with con:
    cur = con.cursor()
    cur.execute("INSERT INTO il_runs_" + DATESTAMP + " (level, category, player, time, platform, medal, src_link) " +
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                [run_data[0], run_data[1], run_data[2], run_data[3], run_data[4], run_data[5], run_data[6]])


def get_all_il_runs():
  # Get the game instance
  game = api.get_game(game_id)

  # Get the platform instances for all with a name in il_platform_names
  all_platforms = game.platforms
  il_platforms = []
  for plat in all_platforms:
    if plat.name in il_platform_names:
      il_platforms.append(plat)

  # Get the Category instances for all cats names in il_category_names
  all_categories = game.categories
  il_categories = []
  for cat in all_categories:
    if cat.name in il_category_names:
      il_categories.append(cat)

  # Get the Level instances
  all_levels = game.levels
  il_levels = []
  for lev in all_levels:
    if lev.name in il_level_names:
      il_levels.append(lev)
   
  # Get all (PB-time) runs from SRC
  if short_run:
    # run limited version of scrape for debug purposes
    runs_to_test = [il_levels[0]]
  else:
    # scrape all levels
    runs_to_test = il_levels

  for level in runs_to_test:
  #for level in il_levels:
    for category in il_categories:
      # Check for IL level/category combinations that can't be run at all
      bad_il_combo = False
      for combo in bad_il_combinations:
        if level.name == combo[0] and category.name == combo[1]:
          bad_il_combo = True

      if bad_il_combo:
        if(debug):
          print(textcol.WARN + "Ignoring level:", level.name, ":", category.name + textcol.BODY)
        pass
      else:
        # Get a LIST of details for all runs fitting the level/category 
        result = get_il_leaderboard(game, category, level)
        for i in result:
          if debug:
            print("Adding to DB:", i)
          add_il_run_to_db(i)

  return












if (debug):
  # Start a counter to see how long this takes
  start_time = time.time()

if not os.path.isfile(DATABASE):
    createNewDb()

updateDb()
get_all_il_runs()

if (debug):
  # Print out timed completion message
  total_time = time.time() - start_time
  timetaken = ""

  if total_time >= 3600:
      timetaken += (textcol.WARN +
                    str(int((total_time - (total_time % 3600))/3600)) +
                    textcol.BODY +
                    " hrs, ")
      total_time = total_time % 3600

  if total_time >= 60:
      timetaken += (textcol.INFO +
                    str(int((total_time - (total_time % 60))/60)) +
                    textcol.BODY +
                    " mins, ")
      total_time = total_time % 60

  timetaken += (textcol.OK +
                str(int(total_time)) +
                textcol.BODY +
                " secs.")

  print("Leaderboards scrape complete in " + timetaken + ".")