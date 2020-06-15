import sqlite3 as lite
import time
from datetime import date

debug = False

prorated_maxima = [25, 35, 44, 52, 59, 65, 70, 75, 79, 83, 87, 90, 93, 95, 97, 98, 99, 100]
prorated_maxima2 = [25, 40, 50, 59, 67, 74, 80, 85, 89, 92, 95, 97, 99, 100]

fastest_level_multiplier = 3

DATABASE = './runs_db.sqlite'
DATESTAMP = date.today().strftime("%Y%m%d")

il_platform_names = ["N64",
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
                  "Escapt from Fest",
                  "Blockade on Chandrila",
                  "Raid on Sullust",
                  "Moff Seerdon's Revenge",
                  "The Battle of Calamari",
                  "Beggar's Canyon",
                  "The Death Star Trench Run",
                  "The Battle of Hoth"]

def calc_score(position, maximum):
	if position == 1:
		return maximum
	elif position == 2:
		return maximum-3
	elif position == 3:
		return maximum-5
	else:
		return maximum-(position+2)

def generate_scores(q_platform, q_level, q_category, q_medal):
	# Create connection to the DB
	con = lite.connect(DATABASE)

	with con:
		cur = con.cursor()
		cur.execute('SELECT player, time FROM il_runs_' + DATESTAMP +
		                ' WHERE platform="' + q_platform + '"' +
		                ' AND level="' + q_level + '"' +
		                ' AND category="' + q_category + '"' +
		                ' AND medal="' + q_medal + '"' +
		                ' ORDER BY time ASC')

	il_leaderboard = cur.fetchall()
	for i in range(len(il_leaderboard)):
		il_leaderboard[i] = list(il_leaderboard[i])
		if debug:
			print(il_leaderboard[i])

	number_players = len(il_leaderboard)
	if number_players > len(prorated_maxima):
		maximum_points = prorated_maxima[-1]
	else:
		maximum_points = prorated_maxima[number_players-1]

	if debug:
		print("Number of players:", number_players)
		print("Maximum score:", maximum_points)

	for i in range(len(il_leaderboard)):
		if debug:
			print("Working on", il_leaderboard[i])
		if i == 0 or il_leaderboard[i][1] != il_leaderboard[i-1][1]:
			il_leaderboard[i].append(i+1)
		else:
			il_leaderboard[i].append(il_leaderboard[i-1][2])

		il_leaderboard[i].append(calc_score(il_leaderboard[i][2], maximum_points))

	return il_leaderboard

def set_db_column(table, col_name, value):
	#UPDATE table SET column=0
	# Create connection to the DB
	con = lite.connect(DATABASE)

	cmd = 'UPDATE ' + table + ' SET "' + col_name + '"=' + value + ';'
	print(cmd)

	with con:	
		cur = con.cursor()
		cur.execute(cmd)

# Set values of all players in today's column to 0
set_db_column('players', DATESTAMP+"_n64_any", '0')
set_db_column('players', DATESTAMP+"_n64_gold", '0')
set_db_column('players', DATESTAMP+"_pc_any", '0')
set_db_column('players', DATESTAMP+"_pc_gold", '0')

for q_platform in il_platform_names:
	if q_platform == 'N64':
		platform_tag = '_n64'
	elif q_platform == 'PC':
		platform_tag = '_pc'
	else:
		platform_tag = "_PLATFORM"

	for q_medal in il_medal_names:
		if q_medal == 'Gold Medal':
			medal_tag = '_gold'
		elif q_medal == 'Any Medal':
			medal_tag = '_any'
		else:
			medal_tag = "_MEDAL"

		column_tag = DATESTAMP + platform_tag + medal_tag

		#for q_level in ["Ambush at Mos Eisley"]:
		for q_level in il_level_names:
			#q_category = "Y-Wing"
			level_master_list = []
			for q_category in il_category_names:

				#print(q_level, ":", q_category, "("+q_platform+", "+q_medal+")")
				scoreboard = generate_scores(q_platform, q_level, q_category, q_medal)

				level_master_list.append(scoreboard)
				
			fastest_time = 9999
			fastest_idx = 0
			fastest_unique = False
			for i in range(len(level_master_list)):
				if level_master_list[i]:
					#print(level_master_list[i][0][1])
					if level_master_list[i][0][1] < fastest_time:
						fastest_time = level_master_list[i][0][1]
						fastest_idx = i
						fastest_unique = True
					elif level_master_list[i][0][1] == fastest_time:
						fastest_unique = False
			if fastest_unique:
				for i in level_master_list[fastest_idx]:
					#print("WOO", i, i[3])
					i[3] = i[3] * fastest_level_multiplier

			if debug:
				print("\n" + q_level + ": (" + q_platform + ", " + q_medal + ")")
				for i in level_master_list:
					print(i)

			for i in level_master_list:
				for j in i:
					print(j, column_tag)

					# Create connection to the DB
					con = lite.connect(DATABASE)
					with con:
						cur = con.cursor()
						cur.execute('UPDATE players SET "' + column_tag + '"="' + column_tag + '"+' + str(j[3]) + ' WHERE name = "' + j[0] + '";')