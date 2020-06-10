
import sqlite3 as lite

import sys
import time
import os.path

import srcomapi, srcomapi.datatypes as dt
api = srcomapi.SpeedrunCom(); api.debug = 0


#
#   GLOBALS
#
debug = False
#
#   DATABASE GLOBALS
#
DATABASE = './runs_db.sqlite'  # Uncomment to run locally
DATABASE_VERSION = 'v0.4.2020-6-11'
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

  # Create the tables with necessary rows
  with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE il_runs (" +
                "run_id          integer primary key," +
                "level           text," +
                "category        text," +
                "player          text," +
                "time            integer default 9999," +
                "platform        text," +
                "medal           text," +
                "src_link        text)")

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
  createNewDb()
  return


def get_il_leaderboard(game, category, level):
  # Takes in a GAME being run, a CATEGORY (e.g. X-Wing) and a LEVEL (e.g. AaME) 
  # and returns for each run on the leaderboard:
  #    - Player Name
  #    - Time (in seconds, according to the primary method set on SRC)
  #    - Platform played on
  #    - Variables (TO BE ADDED)

  print(level.name, ":", category.name)

  out = []
  #print("leaderboards/{}/level/{}/{}?embed=variables".format(game.id, level.id, category.id))
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
  #  medal_type]
  
  # Create connection to the DB
  con = lite.connect(DATABASE)
  with con:
    cur = con.cursor()
    cur.execute("INSERT INTO il_runs (level, category, player, time, platform, medal, src_link) " +
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
  #for level in [il_levels[0]]:
  for level in il_levels:
    for category in il_categories:
      # Get a LIST of details for all runs fitting the level/category 
      result = get_il_leaderboard(game, category, level)
      for i in result:
        if debug:
          print("Adding to DB:", i)
        add_il_run_to_db(i)

  return













if os.path.isfile(DATABASE):
    updateDb()
else:
    createNewDb()

get_all_il_runs()