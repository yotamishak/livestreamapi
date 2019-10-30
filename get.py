from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
import calendar
import json



def get_league(l,r):

    soup = BeautifulSoup(r.content,'html.parser')

    table_string = ''

    games_in_league = soup.find_all("event", {"eventgroup": l})

    if games_in_league:
        table_string += '<table class="table table-hover table-responsive" id="livestream">'
        table_string += '<th colspan="3">' + l + '</th><tbody>\n'

        for ge in games_in_league:


            table_string += '<tr>'
            time = ge["eventstart"].split('+')[0]
            t = time.split('T')[1].split(':')
            date = ge['eventstart'].split('T')[0].split('-')
            if date[2][0] == '0':
                date[2] = date[2][1:]

            table_string += '<td>' + calendar.month_abbr[int(date[1])] + ' ' + date[2] + ' ' + t[0] + ':' + t[1] + '</td>'
            table_string += '<td id="eventName">' + ge[
                'eventname'] + '</td>' + '<td><a class="btn claim" href="/links/bet365-live-stream" style="text-decoration:none;padding:7px;width:100px;font-size:13px;margin:auto;">WATCH NOW</a></td>'

            table_string += '</tr>\n' +createST(ge)
        table_string += '</tbody>'
        table_string += '</table>\n'

    return table_string


def footy_table(r):

    soup = BeautifulSoup(r.content,'html.parser')

    football = soup.find_all("event", {"classification": 'Soccer'})

    tables_string = ''
    topLeagues = ['England Premier League', 'UEFA Champions League', 'FA Cup', 'England Championship',
                  'England EFL Cup', 'UEFA Europa League', 'Spain Primera Liga', 'Italy Serie A',
                  'Scotland Premiership', 'Scotland Championship', 'Germany Bundesliga I', 'France Ligue 1','CONCACAF Nations League']

    for t in topLeagues:
        games_in_league = soup.find_all("event", {"eventgroup": t})
        if games_in_league:
            table_string = '<table class="table table-hover table-responsive" id="livestream">'
            table_string += '<th colspan="3">' + t + '</th><tbody>\n'

            for ge in games_in_league:
                football.remove(ge)
                table_string += '<tr>'
                time = ge["eventstart"].split('+')[0]
                t = time.split('T')[1].split(':')
                date = ge['eventstart'].split('T')[0].split('-')
                if date[2][0] == '0':
                    date[2] = date[2][1:]
                table_string += '<td>' + calendar.month_abbr[int(date[1])] + ' ' + date[2] + ' ' + t[0] + ':' + t[
                    1] + '</td>'
                table_string += '<td id="eventName">' + ge[
                    'eventname'] + '</td>' + '<td><a class="btn claim" href="/links/bet365-live-stream" style="text-decoration:none;padding:7px;width:100px;font-size:13px;margin:auto;">WATCH NOW</a></td>'
                table_string += '</tr>\n' +createST(ge)
            table_string += '</tbody>'
            table_string += '</table>\n'
            tables_string += table_string

    for game in football:

        table_string = '<table class="table table-hover table-responsive" id="livestream">'
        event = game['eventgroup']
        table_string += '<th colspan="3">' + event + '</th><tbody>\n'
        games_in_event = soup.find_all("event", {"eventgroup": event})
        for ge in games_in_event:
            football.remove(ge)
            table_string += '<tr>'
            time = ge["eventstart"].split('+')[0]
            t = time.split('T')[1].split(':')
            date = ge['eventstart'].split('T')[0].split('-')
            if date[2][0] == '0':
                date[2] = date[2][1:]
            table_string += '<td>' + calendar.month_abbr[int(date[1])] + ' ' + date[2] + ' ' + t[0] + ':' + t[
                1] + '</td>'
            table_string += '<td id="eventName">' + ge[
                'eventname'] + '</td>' + '<td><a class="btn claim" href="/links/bet365-live-stream" style="text-decoration:none;padding:7px;width:100px;font-size:13px;margin:auto;">WATCH NOW</a></td>'
            table_string += '</tr>\n' +createST(ge)
        table_string += '</tbody>'
        table_string += '</table>\n'
        tables_string += table_string

    return tables_string


def get_sports(sport_name, r):

    soup = BeautifulSoup(r.content, 'html.parser')

    tables_string = ''

    events = soup.find_all("event", {"classification": sport_name})


    if events:

        eventscpy=events.copy()

        for game in eventscpy:

            if game in events:
                table_string = '<table class="table table-hover table-responsive" id="livestream">'

                event = game['eventgroup']
                table_string += '<th   colspan="3">' + event + '</th><tbody>\n'
                games_in_event = soup.find_all("event", {"eventgroup": event})


                for ge in games_in_event:

                     if ge in events:

                        events.remove(ge)

                        table_string += '<tr>'
                        time = ge["eventstart"].split('+')[0]
                        t = time.split('T')[1].split(':')
                        date = ge['eventstart'].split('T')[0].split('-')
                        if date[2][0] == '0':
                            date[2] = date[2][1:]
                        table_string += '<td>' + calendar.month_abbr[int(date[1])] + ' ' + date[2] + ' ' + t[0] + ':' + t[
                            1] + '</td>'
                        table_string += '<td id="eventName">' + ge[
                            'eventname'] + '</td>' + '<td><a class="btn claim" href="/links/bet365-live-stream" style="text-decoration:none;padding:7px;width:100px;font-size:13px;margin:auto;">WATCH NOW</a></td>'

                        table_string += '</tr>\n' + createST(ge)

                table_string += '</tbody>'
                table_string += '</table>\n'
                tables_string += table_string

    return tables_string


def get_now(r):

    soup = BeautifulSoup(r.content,'html.parser')

    tz = timezone('Europe/London')
    now = datetime.now(tz)
    table_string = ''

    events = soup.find_all("event")
    happening = []

    for e in events:

        starttime = e['eventstart'].split('T')[1].split('+')[0].split(':')
        endtime = e['eventend'].split('T')[1].split('+')[0].split(':')

        startdate = e['eventstart'].split('T')[0].split('-')
        enddate = e['eventend'].split('T')[0].split('-')

        estart = datetime(hour=int(starttime[0]), minute=int(starttime[1]), second=int(starttime[2]),
                          year=int(startdate[0]), month=int(startdate[1]), day=int(startdate[2]), tzinfo=tz)
        eend = datetime(hour=int(endtime[0]), minute=int(endtime[1]), second=int(endtime[0]), year=int(enddate[0]),
                        month=int(enddate[1]), day=int(enddate[2]), tzinfo=tz)

        if estart < now < eend:
            happening.append(e)

        if happening:
            table_string = '<table class="table table-hover table-responsive" id="livestream"><thead><th>Date/ Time</th><th>Match</th><th>League/ Sport</th><th>Watch</th></thead>\n<tbody><tr>'
            for h in happening:
                event = h['eventgroup']
                sport = h['classification']
                time = h["eventstart"].split('+')[0].split('T')[1].split(':')

                date = h['eventstart'].split('T')[0].split('-')
                if date[2][0] == '0':
                    date[2] = date[2][1:]
                table_string += '<tr><td>' + calendar.month_abbr[int(date[1])] + ' ' + date[2] + ' ' + time[0] + ':' + \
                                time[1] + '</td><td>' + h[
                                    'eventname'] + '</td><td><strong>' + event + '</strong><br/> ' + sport + '<td><a class="btn claim" href="/links/bet365-live-stream" style="text-decoration:none;padding:7px;width:80px;font-size:15px;margin:auto;"> WATCH</a></td>'
                table_string +=  '</tr>\n' +createST(h)
            table_string += '</tbody>'
            table_string += '</table>\n'

    return table_string


def createST(e):
    eventdata = {"@context": "http://schema.org", "@type": "BroadcastEvent", "name": e['eventname'],
                 "description": e['eventgroup'], "startdate": e['eventstart'], "endDate": e['eventend']}

    broadcast = {
        "@type": "SportsEvent", "name": e['eventname']
    }

    competitor = []
    match=''
    teams = []

    if len(e['eventname'].split(' v ')) == 2:
        teams = e['eventname'].split(' v ')

    elif len(e['eventname'].split(' vs ')) == 2:
        teams = e['eventname'].split(' vs ')

    elif len(e['eventname'].split(' @ ')) == 2:
        teams = e['eventname'].split(' @ ')
    else:
        match = e['eventname']

    for t in teams:
        competitor.append({"@type": "SportsTeam", "name": t})

    broadcast.update({"competitor": competitor})
    broadcast.update({"location": {
        "@type": "Place",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": e['eventgroup']
        }

    }})
    broadcast.update({"startdate": e['eventstart']})
    broadcast.update({"endDate": e['eventend']})
    eventdata.update({"broadcastofEvent": broadcast})

    if match:
        competitor.append({"@type": "SportsTeam", "name": match})

        broadcast.update({"competitor": competitor})
        broadcast.update({"location": {
            "@type": "Place",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": e['eventgroup']
            }

        }})
        broadcast.update({"startdate": e['eventstart']})
        broadcast.update({"endDate": e['eventend']})
        eventdata.update({"broadcastofEvent": broadcast})

    return '<script type="application/ld+json">' + json.dumps(eventdata) + '</script>\n'

