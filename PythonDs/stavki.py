#import pandas as pd
import requests, re

def daily_football(date):
    try:
        req = requests.get('https://scores24.live/ru/soccer/'+date)
        status = req.status_code
    except:
        status = 0
    if status == 200:
        text = req.text
        matches = re.findall(r'href="(/ru/soccer.*?)"',text)
        for match in matches:
            try:
                req = requests.get('https://scores24.live'+match)
                status = req.status_code
            except:
                status = 0
            if status == 200:
                text = req.text






daily_football('2020-04-16')