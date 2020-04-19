# coding=utf-8
#import pandas as pd
import re, os, enum, requests, pandas as pd

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
                footbal_match_stat(text)



def footbal_match_stat(text):
    head = re.findall('>(.*?)<', text)
    teams = re.search(r'content="Результат матча (.*?) - (.*?) \d', text)  # 2 - страна, 3 - лига
    teams = (teams.group(1), teams.group(2))
    simple_stat = re.search('MatchCourseListing(.*?)Развернуть', text).group(1) + 'p5qQ'
    simple_stat = re.findall('9 f_12-16(.*?)p5qQ', simple_stat)
    activs = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for stat in simple_stat:
        minut = stat[:stat.find('<')]
        get_activ(stat, activs, minut)
    if re.search('СТАТИСТИКА МАТЧА', text):
        full_stat = [None] * 20
        full_stat_text = re.search('СТАТИСТИКА МАТЧА(.*?)rse7X f_12-16_semibold', text).group(1)
        vladenie = re.findall('>\d+?%<', full_stat_text)
        if vladenie:
            full_stat[0], full_stat[1] = vladenie[0], vladenie[1]
        chisla = re.findall('>\d+?<', full_stat_text)
        if chisla:
            i = 0
            if 'Удары в створ' in full_stat_text:
                full_stat_text[2], full_stat_text[3] = chisla[i], chisla[1 + i]
                full_stat_text[4], full_stat_text[5] = chisla[i + 2], chisla[3 + i]
                i += 4
            if 'Сейвы' in full_stat_text:
                full_stat_text[6], full_stat_text[7] = chisla[i], chisla[1 + i]
                i += 2
            if 'Угловые' in full_stat_text:
                full_stat_text[8], full_stat_text[9] = chisla[i], chisla[1 + i]
                i += 2
            if 'Оффсайды' in full_stat_text:
                full_stat_text[10], full_stat_text[11] = chisla[i], chisla[1 + i]
                i += 2
            if 'Ауты' in full_stat_text:
                full_stat_text[12], full_stat_text[13] = chisla[i], chisla[1 + i]
                i += 2
            if 'Удары от ворот' in full_stat_text:
                full_stat_text[14], full_stat_text[15] = chisla[i], chisla[1 + i]
                i += 2
            if 'Штрафные' in full_stat_text:
                full_stat_text[16], full_stat_text[17] = chisla[i], chisla[1 + i]
                i += 2
            if 'Фолы' in full_stat_text:
                full_stat_text[18], full_stat_text[19] = chisla[i], chisla[1 + i]


def football_match_coef(text):
    coefs = [None]*20
    text.replace('\\','/')



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
asd = r'{\"type\":\"x\",\"rates\":[{\"change\":\"0.055\",\"value\":\"3.24\",\"bookmaker\":\"1xbet\"},{\"change\":\"0.15\",\"value\":\"3.25\",\"bookmaker\":\"zenitbet\"},{\"change\":\"-0.1\",\"value\":\"3.20\",\"bookmaker\":\"marathonbet\"},{\"change\":\"-0.1\",\"va'
print(re.search("type",asd).group(0))
