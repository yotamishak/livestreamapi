import pandas as pd
from time import sleep
import calendar
import subprocess
from datetime import datetime
import json
from pytz import timezone
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
import re


def get_bf_streams():

    options=Options()
    options.headless= True

    browser = webdriver.Firefox(options=options)

    # browser.get("https://www.hidemyass.com/en-gb/proxy")


    # browser.find_element_by_id("form_url").click().send_keys('https://video.betfair.com/')
    # browser.find_element_by_xpath('/html/body/form/div[2]/div[1]/div/div[5]').click()

    # browser.find_element_by_xpath('/html/body/form/div[3]/a').click()
    browser.get('https://video.betfair.com/')

    events= browser.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[2]")

    streams=events.text

    browser.close()
    return streams.split('\n')

def bf_make_event(e,t,pairs):
    sport = e.split(':')[0].strip()
    sport = sport_fix(sport)
    sport_clasification=e.split(':')[1].strip()

    if len(sport_clasification.split(' - '))>1:
        event=sport_clasification.split(' - ')[0].strip()
        match=sport_clasification.split(' - ')[1].strip()
    else:
        if len(sport_clasification.split('.'))>1:
            event=sport_clasification.split('.')[0].strip()
            match=sport_clasification.strip()
        else:
            if sport=='Horse Racing':
                event=''
                e=sport_clasification.split()
                for c in e:
                    if not re.search(r'\d',c):
                        event+=c+' '
                    else:
                        event=event.strip()
                        break
            else:
                event='Other'
            match=sport_clasification.strip()

    m=t[10:].split(' ')
    month=list(calendar.month_abbr).index(m[1])
    time=t[:5].split(':')

    tz = timezone('Etc/GMT+0')
    hour=int(time[0])
    # if hour<1:
    #     hour=24
    dt=datetime(year=2019,month=int(month),day=int(m[0]),hour=hour,minute=int(time[1]),second=0,microsecond=0,tzinfo=tz)

    if event in pairs:
        event=pairs[event]

    data=[dt,match,event,sport,False, True, None]

    res=pd.DataFrame([data],index=[1],columns=['date/time','match','league','sport','bet365','betfair','st'])

    return res


def bf_streams():
    with open('matches.json', 'r') as f:
        pairs=json.load(f)
    streams = get_bf_streams()

    stream_len=len(streams)

    df=pd.DataFrame()

    for x in range(0, stream_len, 3):
        y= bf_make_event(streams[x], streams[x + 1], pairs)
        df=pd.concat([df, y], ignore_index=True)

    f.close()
    df.to_csv('betfair.csv')
    return df


def sport_fix(s):
    if s == 'Football':
        return 'Soccer'
    if s== 'Horseracing':
        return 'Horse Racing'
    if s== 'Ice hockey':
        return 'Ice Hockey'
    return s


