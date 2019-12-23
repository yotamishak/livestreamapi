from flask import Flask, request,make_response
from get1 import get_sport,get_now, get_league
from flask_cors import CORS
from flask_caching import Cache
from datetime import datetime
from pytz import timezone
import pandas as pd
from apscheduler.schedulers.blocking import BlockingScheduler



app = Flask(__name__)

CORS(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


@app.route("/football")
@cache.cached(timeout=1500)
def nfl():
    df = pd.read_csv('streams.csv')

    resp=make_response(get_sport("American Football",df))
    resp.headers['Link']='<http://www.freebets.co.uk/live-nfl-streaming>; rel="cannonical"'
    return resp


@app.route("/now")
def now():
    df = pd.read_csv('streams.csv')
    resp=make_response(get_now(df))
    resp.headers['Link'] = '<http://www.freebets.co.uk/live-sports-streaming>; rel="cannonical"'
    return resp


@app.route("/darts")
@cache.cached(timeout=1500)
def darts():
    df = pd.read_csv('streams.csv')
    resp = make_response(get_sport("Darts",df))
    resp.headers['Link'] = '<http://www.freebets.co.uk/live-darts-streaming>; rel="cannonical"'

    return resp


@app.route("/snooker")
@cache.cached(timeout=1500)
def snooker():
    df = pd.read_csv('streams.csv')
    resp = make_response(get_sport("Snooker",df))
    resp.headers['Link'] = '<http://www.freebets.co.uk/live-snooker-streaming>; rel="cannonical"'

    return resp


@app.route("/basketball")
@cache.cached(timeout=1500)
def basketball():
    df = pd.read_csv('streams.csv')
    resp = make_response(get_sport("Basketball",df))
    resp.headers['Link'] = '<http://www.freebets.co.uk/football-live-streaming>; rel="cannonical"'

    return resp


@app.route("/tennis")
@cache.cached(timeout=1500)
def tennis():
    df = pd.read_csv('streams.csv')
    resp = make_response(get_sport("Tennis",df))
    resp.headers['Link'] = '<http://www.freebets.co.uk/live-tennis-streaming>; rel="cannonical"'

    return resp

@app.route("/horse-racing")
@cache.cached(timeout=1500)
def horse_racing():
    df = pd.read_csv('streams.csv')
    resp = make_response(get_sport("Horse Racing",df))
    resp.headers['Link'] = '<http://www.freebets.co.uk/live-horse-racing-streaming>; rel="cannonical"'

    return resp

@app.route("/soccer")
@cache.cached(timeout=1500)
def soccer():
    df = pd.read_csv('streams.csv')
    resp = make_response(get_sport("Soccer",df))
    resp.headers['Link'] = '<http://www.freebets.co.uk/football-live-streaming>; rel="cannonical"'

    return resp


@app.route("/cricket")
@cache.cached(timeout=1500)
def cricket():
    df = pd.read_csv('streams.csv')
    resp = make_response(get_sport("Cricket",df))
    resp.headers['Link'] = '<http://www.freebets.co.uk/live-cricket-streaming>; rel="cannonical"'

    return resp


@app.route("/badminton")
@cache.cached(timeout=1500)
def badminton():
    df = pd.read_csv('streams.csv')
    resp = make_response(get_sport("Badminton",df))
    resp.headers['Link'] = '<http://www.freebets.com/live-streaming-sports/badminton>; rel="cannonical"'

    return resp


@app.route("/golf")
@cache.cached(timeout=1500)
def golf():
    df = pd.read_csv('streams.csv')
    table = get_sport("Golf",df)

    return table


@app.route("/league")
def league():
    df = pd.read_csv('streams.csv')
    l=request.args.get('name')
    table = get_league(l,df)

    return table

@app.route("/greyhounds")
def greyhound():
    df = pd.read_csv('streams.csv')
    table = get_sport("Greyhounds racing",df)

    return table
    
if __name__ == '__main__':
    app.run()