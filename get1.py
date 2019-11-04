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
             "#bet365button{width:50px;height:50px;margin:5px;background:url('data:image/jpeg;base64,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c29LYpO0NLsq7t3bNvncefdVOcody012kzEUNblwszINemfSLdi0+HQYg/8AdySphmU2hUdIeZK9dn682br3V+rM9C6h+qbRW8aQquUegp8cHwAp7aMkOeusqODGcahnMyd10QbCpbZA7H0wqQQfJGGhk7cO3XYl033uVZavTn6b92tm6pAlxXalPqpvBhBnomR3YtTl1av9Malop7KCVuLltd84T2VulCFZCt+86Bati3crfPfTbTdSBOYfRBjU5q1n1mJ2nguCzTKQlT9UXNWW8NNxHhHIOXG2EKLXnNkVivesbVZGr3LG1zvW5rPUvpar08PVG9kVyeHKndPC8/QNFS+iLHTKcQ7JSw0mS62AEOvhCQ84gJASELc6lpAAASQAAOBpXkllUh9UdCm46nnFMNrOVtsqWotIUTyVIQUpUTkkgkknnWHlfVHTjTz51HZPwnH+jkfYk5yPg55yOc86f8/j407J+E/5xk8c5xyM84PyM+Me3x7akEg5BOfnJzzgnnzyQCfkgadk8+E8/P7/AM8kknySeCOSTwcZ8/OBn5wM+BqDz55/POnZE7eE8J2T9k5B54PI54PIwfIx4A5PA451PUo+VE+PJPOMYz84wPPxqeNRpxppxppxppxppxppxppxppxpr//Z')}"\
             "#betfairbutton{width:50px;height:50px;background:url('data:image/jpeg;base64,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')}</style> "
nowsheet = "<style>#livestream{text-align:center;}#eventName{width:70%}#buttonContainer{display: " \
             "flex;flex-wrap: wrap;flex: 1;justify-content: space-around;align-items: " \
             "center;}" \
              "#bet365button{width:50px;height:50px;margin:5px;background:url('data:image/jpeg;base64,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c29LYpO0NLsq7t3bNvncefdVOcody012kzEUNblwszINemfSLdi0+HQYg/8AdySphmU2hUdIeZK9dn682br3V+rM9C6h+qbRW8aQquUegp8cHwAp7aMkOeusqODGcahnMyd10QbCpbZA7H0wqQQfJGGhk7cO3XYl033uVZavTn6b92tm6pAlxXalPqpvBhBnomR3YtTl1av9Malop7KCVuLltd84T2VulCFZCt+86Bati3crfPfTbTdSBOYfRBjU5q1n1mJ2nguCzTKQlT9UXNWW8NNxHhHIOXG2EKLXnNkVivesbVZGr3LG1zvW5rPUvpar08PVG9kVyeHKndPC8/QNFS+iLHTKcQ7JSw0mS62AEOvhCQ84gJASELc6lpAAASQAAOBpXkllUh9UdCm46nnFMNrOVtsqWotIUTyVIQUpUTkkgkknnWHlfVHTjTz51HZPwnH+jkfYk5yPg55yOc86f8/j407J+E/5xk8c5xyM84PyM+Me3x7akEg5BOfnJzzgnnzyQCfkgadk8+E8/P7/AM8kknySeCOSTwcZ8/OBn5wM+BqDz55/POnZE7eE8J2T9k5B54PI54PIwfIx4A5PA451PUo+VE+PJPOMYz84wPPxqeNRpxppxppxppxppxppxppxppxpr//Z')}"\
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
        if abs(now - t2) < timedelta(seconds=60*60*2):
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
    topLeagues = ['England Premier League', 'UEFA Champions League', 'England FA Cup', 'England Championship',
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