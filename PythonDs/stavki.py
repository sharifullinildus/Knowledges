# coding=utf-8
#import pandas as pd
import re, os, enum

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
                head = re.findall('>(.*?)<',text)
                teams = re.search(r'content="Результат матча (.*?) - (.*?) \d', text)  # 2 - страна, 3 - лига
                teams = (teams.group(1),teams.group(2))
                simple_stat = re.search('MatchCourseListing(.*?)Развернуть', text).group(1) + 'p5qQ'
                simple_stat = re.findall('9 f_12-16(.*?)p5qQ', simple_stat)
                activs=[0,0,0,0,0,0,0,0,0]
                for stat in simple_stat:
                    minut = stat[:stat.find('<')]
                    get_activ(stat,activs, minut)
                if re.search('СТАТИСТИКА МАТЧА',text):
                    full_stat = re.search('СТАТИСТИКА МАТЧА(.*?)rse7X f_12-16_semibold',text).group(1)
                    vladenie = re.findall()




def get_activ(text, counter, minut):
    gol = '_2dgzX f_11-12_bold'
    jeltcard = '_1SxFz ZQq'
    zamena = 'xMKF- ZQq1q'
    if int(minut[:minut.find('+')]<46):
        i = 0
    elif '90+' in minut:
        i=2
    else:
        i=1
    if gol in text:
        counter[i]+=1
    elif jeltcard in text:
        counter[i + 3] += 1
    elif zamena in text:
        counter[i + 6] += 1


match_header = ('data','country','liga','team1','team2','winner','nichya','overtime','gols1','gols2','kart1',\
                'jelt1','jelt2', )
asd = 'sadawqdq'
print asd[:asd.find('3')]
