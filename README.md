# swrs

Leaderboards for Star Wars: Rogue Squadron using the Speedrun.com API.

Made with:
- Python 3
- Flask 1.1.2
- Sqlite 3.31.1

## scrape.py

Run this to fetch new runs from the API (it's not actually a scrape). Should take about 10 minutes to complete - some of this is due to the API response time, but could probably still be made much more efficient.

## rescore.py

Run this after `scrape.py` to generate scores for the latest runs and write those back to the DB.

## swrs.py

Can be run locally as a default flask server for local testing on 127.0.0.1:5000

