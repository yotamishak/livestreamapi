from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pytz import timezone
import calendar

import pandas as pd

bet365_button = '<a id="bet365button" href="/links/bet365-live-stream" />'
betfair_button = '<a id="betfairbutton" href="/links/betfair-live-stream" />'

stylesheet = "<style>#livestream{text-align:center;}#eventName{width:70%}#buttonContainer{display: " \
             "flex;min-width:80px;flex-wrap: wrap;flex: 1;justify-content: space-around;align-items: " \
             "center;}" \
             "#bet365button{width:35px;height:35px;background:url('data:image/jpeg;base64," \
             "/9j/4AAQSkZJRgABAQAAAQABAAD" \
             "/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH" \
             "/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH" \
             "/wAARCAAjACMDAREAAhEBAxEB/8QAHAAAAQUAAwAAAAAAAAAAAAAABwIECAkKAQUG" \
             "/8QALxAAAQQCAgAEBAYCAwAAAAAAAQIDBAUGBwgRAAkSIRMUIjEVFjIzQVEkYVJxkf" \
             "/EAB4BAAAGAwEBAAAAAAAAAAAAAAIFBgcICQABAwQK" \
             "/8QAMREAAgEDAwQABQIFBQAAAAAAAQIDBAURBgcSABMhMQgiQVFhI8EUcYGh8AkVFjKR" \
             "/9oADAMBAAIRAxEAPwDrOHXlo2PLXjDvHknH2yzhbOmbjMat7Fn8Yct13n5VwGhzgvptUXkBNf8AOIuxXBBhSy0qP8cKc" \
             "+IGkHMjJADErfI/s4JBxgjx+Dj7" \
             "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')}#betfairbutton{width:35px;height:35px;background:url('data:image/jpeg;base64,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')}</style> "


def get_sport(s, df):
    tables_string = ''

    games_in_sport = df.loc[df['sport'] == s].sort_values(by='date/time')

    if not games_in_sport.empty:
        if s == 'Soccer':
            return soccer_tables(games_in_sport)
        leagues = games_in_sport.league.unique()

        for l in leagues:
            table_string = ''
            games_in_league = games_in_sport.loc[games_in_sport['league'] == l]
            table_string += '<table class="table table-hover table-responsive" id="livestream">'
            table_string += '<th colspan="3">' + l + '</th><tbody>\n'

            for _, ge in games_in_league.iterrows():

                table_string += '<tr>'
                dt = ge['date/time'].split(' ')
                date = dt[0].split('-')
                time = dt[1].split(':')

                if date[2][0] == '0':
                    date[2] = date[2][1:]
                table_string += '<td>' + calendar.month_abbr[int(date[1])] + ' ' + date[2] + ' ' + time[0] + ':' + time[
                    1] + '</td>'
                table_string += '<td id="eventName">' + ge[
                    'match'] + '</td>' + '<td><div id="buttonContainer">'

                if ge['bet365']:
                    table_string += bet365_button
                if ge['betfair']:
                    table_string += betfair_button

                table_string += '</div></td></tr>\n'
            table_string += '</tbody>'
            table_string += '</table>\n'
            tables_string += table_string + stylesheet

    return tables_string + stylesheet


def get_league(l, df):
    table_string = ''
    games_in_league = df.loc[df['league'] == l]
    table_string += '<table class="table table-hover table-responsive" id="livestream">'

    for _, ge in games_in_league.iterrows():

        table_string += '<th colspan="3">' + ge['league'] + '</th><tbody>\n'

        table_string += '<tr>'
        dt = ge['date/time'].split(' ')
        date = dt[0].split('-')
        time = dt[1].split(':')

        if date[2][0] == '0':
            date[2] = date[2][1:]
        table_string += '<td>' + calendar.month_abbr[int(date[1])] + ' ' + date[2] + ' ' + time[0] + ':' + time[
            1] + '</td>'
        table_string += '<td id="eventName">' + ge[
            'match'] + '</td>' + '<td ><div id=buttonContainer>'


        if ge['bet365']:
            table_string += bet365_button
        if ge['betfair']:
            table_string += betfair_button

        table_string += '</div></td></tr>\n'

    table_string += '</tbody>'
    table_string += '</table>\n'

    return table_string + stylesheet


def get_now(df):
    tz = timezone('Europe/London')
    now = datetime.now(tz)
    table_string = ''
    now.replace(tzinfo=None)

    res = []

    for i, row in df.iterrows():

        t2 = datetime.fromisoformat(row['date/time'])
        t2 = t2.replace(tzinfo=tz)
        if abs(now - t2) < timedelta(seconds=600):
            res.append(row)
    happening = pd.DataFrame(res)

    if not happening.empty:
        happening=happening.sort_values(by='date/time')
        table_string = '<table class="table table-hover table-responsive" id="livestream"><thead><th>Date/ Time</th><th>Match</th><th>League/ Sport</th><th>Watch</th></thead>\n<tbody><tr>'
        for _, h in happening.iterrows():
            event = h['league']
            sport = h['sport']
            dt = h['date/time'].split(' ')
            date = dt[0].split('-')
            time = dt[1].split(':')

            if date[2][0] == '0':
                date[2] = date[2][1:]
            table_string += '<tr><td>' + calendar.month_abbr[int(date[1])] + ' ' + date[2] + ' ' + time[0] + ':' + \
                            time[1] + '</td><td>' + h[
                                'match'] + '</td><td><strong>' + event + '</strong><br/> ' + sport + '</td><td><div id="buttonContainer">'

            if h['bet365']:
                table_string += bet365_button
            if h['betfair']:
                table_string += betfair_button
            table_string += '</div></td></tr>\n'
        table_string += '</tbody>'
        table_string += '</table>\n'

    return table_string + stylesheet

def soccer_tables(df):

    tables_string = ''
    topLeagues = ['England Premier League', 'UEFA Champions League', 'FA Cup', 'England Championship',
                  'England EFL Cup', 'UEFA Europa League', 'Spain Primera Liga', 'Italy Serie A',
                  'Scotland Premiership', 'Scotland Championship', 'Germany Bundesliga I', 'France Ligue 1',
                  'CONCACAF Nations League']

    leagues = df.league.unique()



    for t in topLeagues:
        top_games = df.loc[df['league'] == t]
        table_string=''
        if not top_games.empty:
            table_string = '<table class="table table-hover table-responsive" id="livestream">'
            table_string += '<th colspan="3">' + t + '</th><tbody>\n'

            for _, ge in top_games.iterrows():

                table_string += '<tr>'
                dt = ge['date/time'].split(' ')
                date = dt[0].split('-')
                time = dt[1].split(':')

                if date[2][0] == '0':
                    date[2] = date[2][1:]
                table_string += '<td>' + calendar.month_abbr[int(date[1])] + ' ' + date[2] + ' ' + time[0] + ':' + time[
                    1] + '</td>'
                table_string += '<td id="eventName">' + ge[
                    'match'] + '</td>' + '<td ><div id=buttonContainer>'

                if ge['bet365']:
                    table_string += bet365_button
                if ge['betfair']:
                    table_string += betfair_button

                table_string += '</div></td></tr>\n'

            table_string += '</tbody>'
            table_string += '</table>\n'
        tables_string+=table_string

    for l in leagues:
        if l in topLeagues:
            continue
        league = df.loc[df['league'] == l]
        table_string = '<table class="table table-hover table-responsive" id="livestream">'
        table_string += '<th colspan="3">' + l + '</th><tbody>\n'

        for _, ge in league.iterrows():
            table_string += '<tr>'
            dt = ge['date/time'].split(' ')
            date = dt[0].split('-')
            time = dt[1].split(':')

            if date[2][0] == '0':
                date[2] = date[2][1:]
            table_string += '<td>' + calendar.month_abbr[int(date[1])] + ' ' + date[2] + ' ' + time[0] + ':' + time[
                1] + '</td>'
            table_string += '<td id="eventName">' + ge[
                'match'] + '</td>' + '<td ><div id=buttonContainer>'

            if ge['bet365']:
                table_string += bet365_button
            if ge['betfair']:
                table_string += betfair_button

            table_string += '</div></td></tr>\n'

        table_string += '</tbody>'
        table_string += '</table>\n'
        tables_string+=table_string

    return tables_string+stylesheet