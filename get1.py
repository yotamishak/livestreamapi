from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pytz import timezone
import calendar

import pandas as pd

bet365_button = '<a id="bet365button" href="/links/bet365-live-stream" />'
betfair_button = '<a id="betfairbutton" href="/links/betfair-live-stream" />'

stylesheet = "<style>#livestream{text-align:center;}#eventName{width:70%}#buttonContainer{display: " \
             "flex;min-width:110px;flex-wrap: wrap;flex: 1;justify-content: space-around;align-items: " \
             "center;}" \
             "#watchCell{padding:10px;}"\
             "#bet365button{width:50px;height:50px;margin:5px;background:url('data:image/jpeg;base64,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')}"\
             "#betfairbutton{width:50px;height:50px;background:url('data:image/jpeg;base64,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')}</style> "
nowsheet = "<style>#livestream{text-align:center;}#eventName{width:70%}#buttonContainer{display: " \
             "flex;flex-wrap: wrap;flex: 1;justify-content: space-around;align-items: " \
             "center;}" \
              "#bet365button{width:50px;height:50px;margin:5px;background:url('data:image/jpeg;base64,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')}"\
             "#betfairbutton{width:50px;height:50px;background:url('data:image/jpeg;base64,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')}</style> "



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
                    'match'] + '</td>' + '<td "watchCell"><div id="buttonContainer">'

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
            'match'] + '</td>' + '<td id="watchCell"><div id=buttonContainer>'


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
                                'match'] + '</td><td><strong>' + event + '</strong><br/> ' + sport + '</td><td id="watchCell"><div id="buttonContainer">'

            if h['bet365']:
                table_string += bet365_button
            if h['betfair']:
                table_string += betfair_button
            table_string += '</div></td></tr>\n'
        table_string += '</tbody>'
        table_string += '</table>\n'

    return table_string + nowsheet

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
                    'match'] + '</td>' + '<td id="watchCell"><div id=buttonContainer>'

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
                'match'] + '</td>' + '<td id="watchCell"><div id=buttonContainer>'

            if ge['bet365']:
                table_string += bet365_button
            if ge['betfair']:
                table_string += betfair_button

            table_string += '</div></td></tr>\n'

        table_string += '</tbody>'
        table_string += '</table>\n'
        tables_string+=table_string

    return tables_string+stylesheet