import sqlite3 as lite
import time
from datetime import date

debug = False

prorated_maxima = [25, 35, 44, 52, 59, 65, 70, 75, 79, 83, 87, 90, 93, 95, 97, 98, 99, 100]
prorated_maxima2 = [25, 40, 50, 59, 67, 74, 80, 85, 89, 92, 95, 97, 99, 100]

fastest_level_multiplier = 3

DATABASE = './runs_db.sqlite'
DATESTAMP = date.today().strftime("%Y%m%d")


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



q_platform = "N64"
q_level = "The Death Star Trench Run"
q_category = "Y-Wing"
q_medal = "Any Medal"

scoreboard = generate_scores(q_platform, q_level, q_category, q_medal)
for i in scoreboard:
	print(i)