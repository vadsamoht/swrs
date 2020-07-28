# SWRS

Scored leaderboards website for Star Wars: Rogue Squadron using the Speedrun.com API.

Made with:
- Python 3
- Flask 1.1.2
- Sqlite 3.31.1

## scrape.py

Run this to fetch new runs from the API (it's not actually a scrape). Should take about 12 minutes to complete - some of this is due to the API response time, but could probably still be made much more efficient.

Updates both `runs_db.sqlite` and `full_db.sqlite` with each run.

## rescore.py

Run this to generate scores for the latest runs and write those back to the DB. Removes any previous data for 'today' (i.e. the lastest date runs have been added) before update.

**Note:** this is now called automatically as part of `scrape.py`, but can still be done manually if needed for testing.

## swrs.py

Can be run locally as a default flask server for local testing on `127.0.0.1:5000`

## runs_db.sqlite

The working DB that the website reads from. Contains the historical total scores for each player-category, but only the IL leaderboard from the last time `scrape.py` was successfully run.

## full_db.sqlite

A DB that includes the full run-leaderboard from each date the DB is updated in case this is valuable for the future - likely to be a MUCH larger file than `runs_db.sqlite`.