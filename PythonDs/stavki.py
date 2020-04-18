#import pandas as pd
import requests, re, os

def daily_football(date):
    try:
        req = requests.get('https://scores24.live/ru/soccer/'+date)
        status = req.status_code
    except:
        status = 0
    if status == 200:
        text = req.text
        # Парсим день
        matches = re.findall(r'href="(/ru/soccer.*?)"',text)
        for match in matches:
            try:
                req = requests.get('https://scores24.live'+match)
                status = req.status_code
            except:
                status = 0
            if status == 200:
                text = req.text
                # Парсим матч
                head = re.findall('_25ClD f_12-16">(.*?)<',text)


match_header = ('data','country','liga','team1','team2','winner','nichya','overtime','gols1','gols2','kart1',\
                'jelt1','jelt2', )
