import pandas as pd
from datetime import datetime, timedelta
import json
from betfair import bf_streams
from bet365 import get_b365_streams
from difflib import SequenceMatcher
from apscheduler.schedulers.blocking import BlockingScheduler
import re


def second_check(event1, event2):
  
    try:
        t1 = datetime.fromisoformat(event1['date/time'])
        t2 = datetime.fromisoformat(event2['date/time'])
    except:
        t1 = event1['date/time']
        t2 = event2['date/time']

    t1 = t1.replace(tzinfo=None)
    t2 = t2.replace(tzinfo=None)

    if abs(t1 - t2) < timedelta(seconds=600):
        name1 = ''.join(sorted(event1['match'])).replace(' v ', ' ').replace(
            ' vs ',
            ' ').replace('/', ' ').replace('/', ' ').replace('@', ' ').replace(
                '-', ' ').replace("'", ' ').lower()
        name2 = ''.join(sorted(event2['match'])).replace(' v ', ' ').replace(
            ' vs ',
            ' ').replace('/', ' ').replace('/', ' ').replace('@', ' ').replace(
                '-', ' ').replace("'", ' ').lower()

        name1 = re.sub(r'\b\w{1,2}\b', '', name1)
        name2 = re.sub(r'\b\w{1,2}\b', '', name2)

        if SequenceMatcher(None, name1, name2).ratio() > .8:
            return True

    return False


def find_close_events(t, df, diff):
    res = []
    for i, row in df.iterrows():
        
        try:
            t2 = datetime.fromisoformat(row['date/time'])
        except:
            t2 = row['date/time']
      
        t = t.replace(tzinfo=None)
        t2 = t2.replace(tzinfo=None)

        if abs(t - t2) < timedelta(seconds=diff):
            res.append(row)
    return pd.DataFrame(res)


def match_check(t1, t2):

    t1 = t1.replace(' v ', ' ').replace(' vs ', ' ').replace('/', ' ').replace(
        '@', ' ').replace('-', ' ').replace("'", ' ').lower().split()

    t2 = t2.replace(' v ', ' ').replace(' vs ', ' ').replace('/', ' ').replace(
        '@', ' ').replace('-', ' ').replace("'", ' ').lower().split()

    t3 = set(t1 + t2)
    count = 0

    for x in t3:
        if x in (t2 and t1):
            count += 1

    if count == len(t1) or count == len(t2):
        return True

    return False


def join_streams():
    # b365=pd.read_csv('bet365.csv')
    # bf= pd.read_csv('betfair.csv')
    b365 = get_b365_streams()
    bf = bf_streams()
    with open('matches.json', 'r') as f:
        pairs = json.load(f)
        f.close()
    b365_sports = b365.sport.unique()
    bf_sports = bf.sport.unique()
    inner_leagues = list(set(b365_sports) & set(bf_sports))

    for s in inner_leagues:

        b365_events = b365.loc[b365['sport'] == s].sort_values(by='date/time')
        bf_events = bf.loc[bf['sport'] == s].sort_values(by='date/time')

        for i, row in b365_events.iterrows():

            try:
                t1 = datetime.fromisoformat(row['date/time'])
            except:
                t1 = row['date/time']
            if s == 'Horse Racing':
                diff = 600
            else:
                diff = 3600

            close_events = find_close_events(t1, bf_events, diff)

            for j, c in close_events.iterrows():
                if s == 'Horse Racing':
                    if row['league'] == c['league']:
                       
                        b365.at[i, 'betfair'] = True
                        bf.at[j, 'betfair'] = False
                        if c['league'] not in pairs:
                            pairs.update({c['league']: row['league']})
                    continue
                else:
                    if match_check(row['match'], c['match']):
                        b365.at[i, 'betfair'] = True
                        bf.at[j, 'betfair'] = False
                        if c['league'] not in pairs:
                            pairs.update({c['league']: row['league']})

                    elif second_check(row, c):
                        b365.at[i, 'betfair'] = True
                        bf.at[j, 'betfair'] = False
                        if c['league'] not in pairs:
                            pairs.update({c['league']: row['league']})

    with open('matches.json', 'w') as f:
        json.dump(pairs, f)
        f.close()

    final_df = b365.loc[b365['bet365'] == True]
    bf_final = bf.loc[bf['betfair'] == True]
    final_df = pd.concat([final_df, bf_final], ignore_index=True)

    final_df.to_csv('streams.csv')

    return final_df


join_streams()
s = BlockingScheduler()
s.add_job(join_streams,
          'interval',
          hours=4,
          start_date=datetime.now().replace(hour=0, minute=0))
s.start()