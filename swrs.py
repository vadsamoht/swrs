from flask import (Flask, send_file, render_template, request,
                   redirect, make_response, g, url_for, jsonify)
import sqlite3 as lite
app = Flask(__name__)
application = app
app.config['TEMPLATES_AUTO_RELOAD'] = True

from globalvariables import *

debug = False



# Create connection to the DB
con = lite.connect(DATABASE)
cur = con.cursor()

with con:
    cur.execute('SELECT value FROM metadata WHERE field = "last_update";')

    DATESTAMP = cur.fetchall()[0][0]

def convert_seconds(in_time):
    #print(in_time)
    out_time = 'ERR'
    secs = in_time % 60
    mins = int((in_time - secs) // 60)


    if secs < 10:
        secs = '0' + str(secs)

    out_time = str(mins) + ':' + str(secs)

    return out_time


@app.route('/player')
@app.route('/')
def home():
    # Main page - show Player Search page

    all_leaderboards = []
    board_titles = []

    # query lists from DB
    for q_console in ['pc', 'n64']:
        for q_medal in ['any', 'gold']:
            q_col = DATESTAMP+'_'+q_console+'_'+q_medal

            # Create connection to the DB
            con = lite.connect(DATABASE)
            cur = con.cursor()
            with con:
                cur.execute('SELECT name, "' + q_col +
                            '" FROM players' +
                            ' WHERE name != "_max_possible"' +
                            ' ORDER BY "' + q_col + '" DESC,' +
                            ' name COLLATE NOCASE ASC')

            il_leaderboard = cur.fetchall()

            all_leaderboards.append(il_leaderboard)
            title = q_console.upper() + ' ' + q_medal.capitalize() + ' Medal'
            board_titles.append(title)

    #print(all_leaderboards)

    try:
        return render_template('main.html',
                               titles = board_titles,
                               all_boards=all_leaderboards,
                               last_date = DATESTAMP)
    except Exception as e:
        return str(e)


@app.route('/faq')
def faq():
    # FAQ page
    try:
        return render_template('faq.html')
    except Exception as e:
        return str(e)


@app.route('/player/<player_id>')
def player(player_id):
    # Player profile page
    if debug:
        print(player_id)


            
    # Create connection to the DB
    con = lite.connect(DATABASE)
    cur = con.cursor()
    with con:
        cur.execute('SELECT date FROM update_datestamps')
    
    col_names = cur.fetchall()
    
    up_dates = []
    for i in col_names:
        if i[0] not in up_dates and i[0] != None:
            up_dates.append(i[0])
    #print(up_dates)

    scoredata = []
    scoredata.append(up_dates)
    latest_scores = []

    for q_console in ['pc', 'n64']:
        for q_medal in ['any', 'gold']:
            current_list = []

            for date in up_dates:
                q_col = date+'_'+q_console+'_'+q_medal
                #print(q_col)
                
                # Create connection to the DB
                con = lite.connect(DATABASE)
                cur = con.cursor()
                with con:
                    cur.execute('SELECT "' + q_col + '"' +
                                ' FROM players' +
                                ' WHERE name="' + player_id + '";')
                score_result = cur.fetchall()
                
                current_list.append(score_result[0][0])

            scoredata.append(current_list)

    #print(scoredata)

    for i in scoredata:
        latest_scores.append(i[-1])

    try:
        return render_template('player.html',
                               score_history=scoredata,
                               name=player_id,
                               scores=latest_scores,
                               columns=["Date",
                                        "PC Any Medal",
                                        "PC Gold Medal",
                                        "N64 Any Medal",
                                        "N64 Gold Medal"])
    except Exception as e:
        return str(e)


@app.route('/player/<player_id>/<category>')
def player_cat(player_id, category):
    # Player category (e.g. PC,Gold) page

    # Create connection to the DB
    con = lite.connect(DATABASE)

    # Add update date to metadata
    with con:
        cur = con.cursor()
        cur.execute('SELECT value FROM metadata ' +
                    'WHERE field = "last_update"')
    last_up = cur.fetchall()[0][0]

    # parse category id to variables
    tag = last_up + '_' + category
    
    if category[0:2] == 'pc':
        console = "PC"
    elif category[0:3] == 'n64':
        console = 'N64'
    else:
        console = 'CONSOLE?'

    if category[-3:] == 'any':
        medal_type = "Any Medal"
    elif category[-4:] == 'gold':
        medal_type = 'Gold Medal'
    else:
        medal_type = 'MEDAL?'

    runs = []
    bests = []
    for lev in il_level_names:
        level_array = []
        bests_level = []

        for ship in il_category_names:
            # Get all runs matching the criteria
            cur = con.cursor()
            with con:
                cur.execute('SELECT level, category, time, rank, "src_link" ' +
                            'FROM il_runs_' + last_up + ' ' +
                            'WHERE player = "' + player_id + '" AND ' +
                            'platform = "' + console + '" AND ' +
                            'level = "' + lev + '" AND ' +
                            'category = "' + ship + '" AND ' +
                            'medal = "' + medal_type + '";')    
            run = cur.fetchall()
            #print(run)

            player_best = 0
            if run:
                run = list(run[0])
                #print(run)
                player_best = run[2]
                run[2] = convert_seconds(player_best)
            level_array.append(run)

            # get the best time for comparison
            with con:
                cur.execute('SELECT time ' +
                            'FROM il_runs_' + last_up + ' ' +
                            'WHERE rank = 1 AND ' +
                            'platform = "' + console + '" AND ' +
                            'level = "' + lev + '" AND ' +
                            'category = "' + ship + '" AND ' +
                            'medal = "' + medal_type + '";')    
            best_run = cur.fetchall()
            if best_run:
                best_run = list(best_run[0])[0]
                #print(run)
                # set best_run to difference between the best & current player's
                print(player_best, best_run)
                best_run = player_best - best_run
                print(best_run)
                best_run = convert_seconds(best_run)
            bests_level.append(best_run)

        runs.append(level_array)
        bests.append(bests_level)


    #print(runs)

    '''
    for i in runs:
        print(i)
        #print(i, convert_seconds(i[2]))
    '''

    try:
        return render_template('player-category.html',
                               name=player_id,
                               medal=medal_type,
                               platform=console,
                               runs=runs,
                               best_times=bests,
                               last_update=DATESTAMP)
    except Exception as e:
        return str(e)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))
    print(error)
    return 500

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True, host='192.168.1.200')
