
import sqlite3 as lite
import sys
import time
import os.path
import shutil
from datetime import date
from os import path, system

import srcomapi, srcomapi.datatypes as dt # pip3 install srcomapi
api = srcomapi.SpeedrunCom(); api.debug = 0


from globalvariables import *
#...
#   GLOBALS
#
debug = 1 # 0=no output, 1=limited, 2=detailed
short_run = False


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

  # Add creation date to metadata
  with con:
    cur = con.cursor()
    cur.execute("REPLACE INTO metadata (field, value) " +
                "VALUES (?, ?)",
                ['db_created', DATESTAMP])

  # Create table for runs
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
                "src_link        text," +
                "rank            integer default 0)")

  # Create table for players, without score_date cols (added to updateDB()) due 
  # to lack of IF NOT EXISTS on ALTER TABLE commands.
  with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS players (" +
                "player_id       integer primary key," +
                "name            text," +
                "src_link        text," +
                "n64_total       integer," +
                "pc_total        integer," +
                "UNIQUE(name))")

  return


def updateDb():
  if debug >= 1:
    print("Updating existing", DATABASE, "\n")

  # Create connection to the DB
  con = lite.connect(DATABASE)

  # Drop old table for date if present
  with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS il_runs_" + DATESTAMP)


  # Create table for today's runs
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
                "src_link        text," +
                "rank            integer default 0)")

  with con:
    cur = con.cursor()
    try:
      cur.execute("ALTER TABLE players ADD COLUMN '" + DATESTAMP + "_pc_gold' integer default 0")
    except:
      pass
    try:
      cur.execute("ALTER TABLE players ADD COLUMN '" + DATESTAMP + "_pc_any' integer default 0")
    except:
      pass
    try:
      cur.execute("ALTER TABLE players ADD COLUMN '" + DATESTAMP + "_n64_gold' integer default 0")
    except:
      pass
    try:
      cur.execute("ALTER TABLE players ADD COLUMN '" + DATESTAMP + "_n64_any' integer default 0")
    except:
      pass
    
    
  # Add update date to metadata
  with con:
    cur = con.cursor()
    cur.execute("REPLACE INTO metadata (field, value) " +
                "VALUES (?, ?)",
                ['last_update', DATESTAMP])

  return


def get_il_leaderboard(game, category, level, medal_type='NONE'):
  # Takes in a GAME being run, a CATEGORY (e.g. X-Wing) and a LEVEL (e.g. AaME) 
  # and returns for each run on the leaderboard:
  #    - Player Name
  #    - Time (in seconds, according to the primary method set on SRC)
  #    - Platform played on
  #    - Variables (TO BE ADDED)


  if medal_type == "z197emjl":
    medal_name = "Any"
  elif medal_type == "p123jdvl":
    medal_name = "Gold"
  else:
    medal_name = "Unknown"

  medal_hash = medal_type

  if debug >= 1:
    print("Requesting", textcol.INFO + level.name+":", category.name+"," , medal_name, "Medal" + textcol.BODY, "...")


  out = []
  req = "leaderboards/{}/level/{}/{}?var-78966vq8={}&embed=variables".format(game.id, level.id, category.id, medal_hash)
  if debug >= 2:
    print("http://speedrun.com/api/v1/" + req)
  il_board = dt.Leaderboard(api, data=api.get(req))

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
    if debug >= 2:
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
  # Start a counter to see how long this takes
  if debug >= 1:
    start_time = time.time()

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

  # set variables for medals
  il_medals = il_medal_types

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
          if debug >= 1:
            print(textcol.WARN + "Ignoring level:", level.name, ":", category.name + textcol.BODY)
          pass
        else:
          for medal in il_medals:
            # Get a LIST of details for all runs fitting the level/category 
            result = get_il_leaderboard(game, category, level, medal)
            for i in result:
              if debug >= 2:
                print("Adding to DB:", i)
              add_il_run_to_db(i)

  if debug >= 1:
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

  return

def updatePlayers():
  # Get a list of all of the players  for updating into the 'players' table
  if debug >= 1:
    print("updating player master list...")

  # Create connection to the DB
  con = lite.connect(DATABASE)

  with con:
    cur = con.cursor()

    # get Players from all runs in DB
    cur.execute('SELECT player FROM il_runs_' + DATESTAMP)

    # create curated_player_list with all players and duplicates removed
    full_player_list = cur.fetchall()
    curated_player_list = []
    for i in full_player_list:
      if i[0] not in curated_player_list: # and i[0] is not "Jörmungandr":
        curated_player_list.append(i[0])

  # Insert each of those players into the 'players' table if not already present
  for i in curated_player_list:
    if debug >= 2:
      print("Inserting player:", i)
      pass

    with con:
      cur = con.cursor()
      cur.execute('INSERT OR IGNORE INTO players(name) VALUES ("' + i + '")')

  return


def copyFromTo(file_from, file_to):
    # Attempts to copy file IFF file_from exists
    if debug >= 2:
        print('Copying file from', file_from, 'to', file_to + '...')

    if path.exists(file_from):
        shutil.copyfile(file_from, file_to)
    else:
        # do nothing
        pass

def trimDB():
    # Removes un-needed tables from DB for uploading to server

    # Create connection to the DB
    con = lite.connect(DATABASE)

    with con:
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        results = cur.fetchall()

    tables_list = []
    latest_table = 'il_runs_'+DATESTAMP
    keep_tables = ['metadata', 'players', 'update_datestamps', latest_table]
    for i in results:
        if i[0] not in keep_tables:
          tables_list.append(i[0])

    print(tables_list)


    for i in tables_list:
        with con:
            cur.execute('DROP TABLE ' + i + ';');
    
    with con:
        cur.execute('VACUUM');

    if debug >= 2:
        print("Trim complete")





# Copy over full_db.sqlite if exists
if debug >= 1:
    print("duplicating full_db...")
copyFromTo(FULL_DATABASE, DATABASE)

# Create new DB if none copied over
if not os.path.isfile(DATABASE):
    createNewDb()

# Run the 'scrape'
updateDb()
get_all_il_runs()
updatePlayers()

# Run the player-scoring script
if debug >= 1:
    print("Scoring players...")
os.system('python3 rescore.py')

# Copy DB back to full_db.sqlite, overwriting if necessary
if debug >= 1:
    print("Backing up full_db...")
copyFromTo(DATABASE, FULL_DATABASE)

# Remove all unnecessary tables from runs_db.sqlite (keep latest runs info, scoring, metadata)
if debug >= 1:
    print('Trimming wokring DB...')
trimDB()


