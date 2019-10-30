from bs4 import BeautifulSoup
import calendar
import requests
import pandas as pd
from datetime import datetime
from tabulate import tabulate


def get_b365_streams():
    r = requests.get("https://react2wp.com/bet365.xml")
    soup = BeautifulSoup(r.content, 'html.parser')

    events= soup.find_all("event")

    df=pd.DataFrame()

    for e in events:

        dt = datetime.fromisoformat(e['eventstart'])

        league = e['eventgroup']
        match = e['eventname']
        sport= e['classification']



        data = [dt, match, league, sport, True, False, None]

        res = pd.DataFrame([data], index=[1],
                           columns=['date/time', 'match', 'league', 'sport', 'bet365', 'betfair', 'st'])

        df=pd.concat([df, res], ignore_index=True)


    df.to_csv('bet365.csv')
    return df
