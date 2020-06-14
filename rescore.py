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
                     "Naboo Starfighter"]
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



for q_platform in il_platform_names:
	for q_medal in il_medal_names:
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

			if True:
				print("\n" + q_level + ": (" + q_platform + ", " + q_medal + ")")
				for i in level_master_list:
					print(i)