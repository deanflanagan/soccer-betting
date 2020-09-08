# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 10:16:59 2020

@author: Dean
"""


import pandas as pd
import datetime

address = 'https://www.football-data.co.uk/new/USA.csv'
df = pd.read_csv(address)
new_dates = []
new_datetimes = []

for x in df[['Date', 'Time']].values:
    day, month, year, hour, minute = list(
        map(int, x[0].split('/'))) + list(map(int, x[1].split(':')))
    new_datetimes.append(datetime.datetime(year, month, day, hour, minute))
    new_dates.append(datetime.date(year, month, day))

df.drop(['Date', 'Time'], axis=1, inplace=True)

df['date'] = new_dates
df['kick_off'] = new_datetimes

df.to_csv('check.csv')
