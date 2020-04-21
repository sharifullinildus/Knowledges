# coding=utf-8
import pandas as pd
import re, requests, os, datetime, calendar, json
from collections import namedtuple

match_header = namedtuple('match',['data','country','liga','team1','team2','gols1t1','gols2t1','gols3t1','gols1t2','gols2t2',
                          'gols3t2','kart1','kart2','vladenie1','vstvor1','mimo1','vstvor2','mimo2','save1','save2',
                'uglov1','uglov2','offsaid1','offsaid2','aut1','aut2','otvorot1','otvorot2','shtraf1','shtraf2','fol1',
                'fol2','p1','X','p2','tb1','tb2','tb3','tb4','tb5','tb6','oz','x1','x12','x2'])


def go_stavki_football_forward(iter):
    with open(os.path.abspath('../../')+'stavki_times.txt') as f:
        dates = json.load(f)[0]
        forward = datetime.date(dates[0],dates[1],dates[2])
    for i in range(iter):
        forward=forward+datetime.timedelta(days=1)
        get_daily_football(forward)



def get_daily_football(date):
    try:
        req = requests.get('https://scores24.live/ru/soccer/'+'{}-{}-{}'.format(date.year,date.month,date.day))
        status = req.status_code
    except:
        status = 0
        with open(os.path.abspath('../../')+'fault_days.txt','a') as f:
            f.write('https://scores24.live/ru/soccer/'+date+'\n')
    if status == 200:
        text = req.text
        text.replace('\\','/')
        # Парсим день
        matches = re.findall(r'href="(/ru/soccer/m.*?)"',text)
        for match in matches:
            try:
                req = requests.get('https://scores24.live'+match)
                status = req.status_code
            except:
                status = 0
                with open(os.path.abspath('../../')+'match_faults.txt','a') as f:
                    f.write('https://scores24.live'+match+'\n')
            if status == 200:
                text = req.text
                # Парсим матч
                header = get_full_match(text)
            else:
                with open(os.path.abspath('../../')+'match_faults.txt', 'a') as f:
                    f.write('https://scores24.live' + match + '\n')
    else:
        with open(os.path.abspath('../../')+'fault_days.txt','a') as f:
            f.write('https://scores24.live/ru/soccer/'+date+'\n')


def get_full_match(text):
    header = match_header(*[0]*45)
    teams = re.search(r'Результат матча (.*?) - (.*?) \d', text)
    header.team1,header.team2 = teams.group(1),teams.group(2)
    countr_leag = re.search(r'</svg></a><a href="/ru/soccer/.*?([А-Я].*?)<.*?([А-Я].*?)<',text)
    header.country,header.liga=countr_leag.group(1),countr_leag.group(2)
    get_stat(text,header,header.team1)
    if re.search('Статистика матча', text):
       get_full_stat(text,header)
    if re.search('has_odds..(.*?),',text).group(1)=='true':
        get_match_coef(text,header)
    return header


def get_match_coef(text,header):
    text = re.search('/"odds/":{/"odds/":{/"slug(.*?)"standings/":null',text).group(0)
    p1 = re.search('type/":/"w1/(.*?)value/":/"(.*?)/"',text)
    if p1:
        header.p1 = int(p1.group(2))
    X = re.search(r'"type/":/"x/(.*?)value/":/"(.*?)/"',text)
    if X:
        header.X = int(X.group(2))
    p2 = re.search(r'"type/":/"w2/(.*?)value/":/"(.*?)/"', text)
    if p2:
        header.p2= int(p2.group(2))
    t1 = re.search(r'"type/":/"1/(.*?)value/":/"(.*?)/"', text)
    if t1:
        header.tb1 = int(t1.group(2))
    t2 = re.search(r'"type/":/"2/(.*?)value/":/"(.*?)/"', text)
    if t2:
        header.tb2 = int(t2.group(2))
    t3 = re.search(r'"type/":/"3/(.*?)value/":/"(.*?)/"', text)
    if t3:
        header.tb3 = int(t3.group(2))
    t4 = re.search(r'"type/":/"4/(.*?)value/":/"(.*?)/"', text)
    if t4:
        header.tb4 = int(t4.group(2))
    t5 = re.search(r'"type/":/"5/(.*?)value/":/"(.*?)/"', text)
    if t5:
        header.tb5 = int(t5.group(2))
    t6 = re.search(r'"type/":/"6/(.*?)value/":/"(.*?)/"', text)
    if t6:
        header.tb6 = int(t6.group(2))
    oz = re.search(r'"type/":/"yes/(.*?)value/":/"(.*?)/"', text)
    if oz:
        header.oz = int(oz.group(2))
    x1 = re.search(r'"type/":/"x1/(.*?)value/":/"(.*?)/"', text)
    if x1:
        header.x1 = int(x1.group(2))
    w12 = re.search(r'"type/":/"w12/(.*?)value/":/"(.*?)/"', text)
    if w12:
        header.x12 = int(w12.group(2))
    x2 = re.search(r'"type/":/"x2/(.*?)value/":/"(.*?)/"', text)
    if x2:
        header.x2 = int(x2.group(2))



def get_full_stat(text,header):
    full_stat_text = re.search('Статистика матча(.*?)rse7X f_12-16_semibold', text).group(1)
    vladenie = re.findall('>(\d+?)%<', full_stat_text)
    if vladenie:
        header.vladenie1,header[18] = vladenie[0]
    chisla = re.findall('>(\d+?)<', full_stat_text)
    if chisla:
        i = 0
        if 'Удары в створ' in full_stat_text:
            header.vstvor1,header.mimo1 = chisla[i], chisla[1 + i]
            header.vstvor2,header.mimo2 = chisla[i + 2], chisla[3 + i]
            i += 4
        if 'Сейвы' in full_stat_text:
            header.save1,header.save2 = chisla[i], chisla[1 + i]
            i += 2
        if 'Угловые' in full_stat_text:
            header.uglov1,header.uglov2 = chisla[i], chisla[1 + i]
            i += 2
        if 'Оффсайды' in full_stat_text:
            header.offsaid1,header.offsaid2 = chisla[i], chisla[1 + i]
            i += 2
        if 'Ауты' in full_stat_text:
            header.aut1,header.aut2 = chisla[i], chisla[1 + i]
            i += 2
        if 'Удары от ворот' in full_stat_text:
            header.otvorot1,header.otvorot2 = chisla[i], chisla[1 + i]
            i += 2
        if 'Штрафные' in full_stat_text:
            header.shtraf1,header.shtraf2 = chisla[i], chisla[1 + i]
            i += 2
        if 'Фолы' in full_stat_text:
            header.fol1,header.fol2 = chisla[i], chisla[1 + i]


def get_stat(text,header,team1):
    simple_stat = re.search('MatchCourseListing(.*?)Развернуть', text).group(1)+'p5qQ'
    gol1 = re.search('1-й тайм.*?(\d):(\d)',simple_stat)
    gol2 = re.search('Основное время.*?(\d+?):(\d+?)',simple_stat)
    gol3 = re.search('Матч завершён со с.*?(\d+?):(\d+?)',simple_stat)
    jelt1,jelt2=0,0
    for i in re.findall('9 f_12-16">(.*?)p5qQ', simple_stat):
        if '.svg#card' in i:
            if team1 in i:
                jelt1+=1
            else:
                jelt2+=1
    header.gols1t1,header.gols1t2=gol1.group(1),gol1.group(2)
    header.gols2t1, header.gols2t2 = gol2.group(1), gol2.group(2)
    header.gols3t1, header.gols3t2 = gol3.group(1), gol3.group(2)
    header.kart1,header.kart2 = jelt1,jelt2


#text =requests.get('https://scores24.live/ru/soccer/m-23-10-2019-sk-slavia-prague-fc-barcelona/odds').text

import datetime,calendar

asd = datetime.datetime.date(2017,3,3)

print(asd)
