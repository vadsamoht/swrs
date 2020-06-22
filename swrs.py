from flask import (Flask, send_file, render_template, request,
                   redirect, make_response, g, url_for, jsonify)
import sqlite3 as lite
app = Flask(__name__)
application = app
app.config['TEMPLATES_AUTO_RELOAD'] = True
DATABASE = './runs_db.sqlite'
debug = False

# Create connection to the DB
con = lite.connect(DATABASE)
cur = con.cursor()

with con:
    cur.execute('SELECT value FROM metadata WHERE field = "last_update";')

    DATESTAMP = cur.fetchall()[0][0]


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
        cur.execute('PRAGMA table_info(players)')
    
    col_names = cur.fetchall()


    col_dates = []
    for i in col_names:
        if '_any' in i[1] or '_gold' in i[1]:
            col_dates.appendi[1][:8]
    print(col_dates)

    '''
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
    '''
    try:
        return render_template('player.html')
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
