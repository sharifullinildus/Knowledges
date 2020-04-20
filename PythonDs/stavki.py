# coding=utf-8
import pandas as pd
import re, os, enum, requests, pandas as pd

def daily_football(date):
    try:
        req = requests.get('https://scores24.live/ru/soccer/'+date)
        status = req.status_code
    except:
        status = 0
        with open('fault_days.txt','a') as f:
            f.write('https://scores24.live/ru/soccer/'+date+'\n')
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
                with open('match_faults','a') as f:
                    f.write('https://scores24.live'+match+'\n')
            if status == 200:
                text = req.text
                # Парсим матч
                footbal_match_stat(text)


def footbal_match_stat(text):
    header = [None]*50
    head = re.findall('>(.*?)<', text)
    teams = re.search(r'content="Результат матча (.*?) - (.*?) \d', text)  # 2 - страна, 3 - лига
    teams = (teams.group(1), teams.group(2))
    simple_stat = re.search('MatchCourseListing(.*?)Развернуть', text).group(1) + 'p5qQ'
    simple_stat = re.findall('9 f_12-16(.*?)p5qQ', simple_stat)
    header = []
    for stat in simple_stat:
        minut = stat[:stat.find('<')]
        get_activ(stat, header, minut)
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


def football_match_coef(text,header):
    text = re.search('\"odds\":{\"odds\":{\"slug(.*?)"standings\":null',text).group(0)
    text.replace('\\','/')
    p1 = re.search('type/":/"w1/(.*?)value/":/"(.*?)/"',text)
    if p1:
        header[37] = int(p1.group(2))
    X = re.search(r'"type/":/"x/(.*?)value/":/"(.*?)/"',text)
    if X:
        header[38] = int(X.group(2))
    p2 = re.search(r'"type/":/"w2/(.*?)value/":/"(.*?)/"', text)
    if p2:
        header[39] = int(p2.group(2))
    t1 = re.search(r'"type/":/"1/(.*?)value/":/"(.*?)/"', text)
    if t1:
        header[40] = int(t1.group(2))
    t2 = re.search(r'"type/":/"2/(.*?)value/":/"(.*?)/"', text)
    if t2:
        header[41] = int(t2.group(2))
    t3 = re.search(r'"type/":/"3/(.*?)value/":/"(.*?)/"', text)
    if t3:
        header[42] = int(t3.group(2))
    t4 = re.search(r'"type/":/"4/(.*?)value/":/"(.*?)/"', text)
    if t4:
        header[43] = int(t4.group(2))
    t5 = re.search(r'"type/":/"5/(.*?)value/":/"(.*?)/"', text)
    if t5:
        header[44] = int(t5.group(2))
    t6 = re.search(r'"type/":/"6/(.*?)value/":/"(.*?)/"', text)
    if t6:
        header[45] = int(t6.group(2))
    oz = re.search(r'"type/":/"yes/(.*?)value/":/"(.*?)/"', text)
    if oz:
        header[46] = int(oz.group(2))
    x1 = re.search(r'"type/":/"x1/(.*?)value/":/"(.*?)/"', text)
    if X:
        header[47] = int(x1.group(2))
    w12 = re.search(r'"type/":/"w12/(.*?)value/":/"(.*?)/"', text)
    if w12:
        header[48] = int(w12.group(2))
    x2 = re.search(r'"type/":/"x2/(.*?)value/":/"(.*?)/"', text)
    if x2:
        header[49] = int(x2.group(2))



def full_stat(text,header):
    full_stat = [None] * 20
    full_stat_text = re.search('СТАТИСТИКА МАТЧА(.*?)rse7X f_12-16_semibold', text).group(1)
    vladenie = re.findall('>\d+?%<', full_stat_text)
    if vladenie:
        header[17],header[18] = vladenie[0], vladenie[1]
    chisla = re.findall('>\d+?<', full_stat_text)
    if chisla:
        i = 0
        if 'Удары в створ' in full_stat_text:
            header[19],header[20] = chisla[i], chisla[1 + i]
            header[21],header[22] = chisla[i + 2], chisla[3 + i]
            i += 4
        if 'Сейвы' in full_stat_text:
            header[23],header[24] = chisla[i], chisla[1 + i]
            i += 2
        if 'Угловые' in full_stat_text:
            header[25],header[26] = chisla[i], chisla[1 + i]
            i += 2
        if 'Оффсайды' in full_stat_text:
            header[27],header[28] = chisla[i], chisla[1 + i]
            i += 2
        if 'Ауты' in full_stat_text:
            header[29],header[30] = chisla[i], chisla[1 + i]
            i += 2
        if 'Удары от ворот' in full_stat_text:
            header[31],header[32] = chisla[i], chisla[1 + i]
            i += 2
        if 'Штрафные' in full_stat_text:
            header[33],header[34] = chisla[i], chisla[1 + i]
            i += 2
        if 'Фолы' in full_stat_text:
            header[35],header[36] = chisla[i], chisla[1 + i]


def get_activ(text, header, minut):
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
        header[8+i]+=1
    elif jeltcard in text:
        header[i + 11] += 1
    elif zamena in text:
        header[i + 14] += 1


match_header = ('data','country','liga','team1','team2','winner','nichya','nichya_os','gols1','gols2','gols3','kart1',
                'kart2','kart3','jelt1','jelt2','jelt3','vladenie1','vladenie2','vstvor1','mimo1','vstvor2','mimo2','save1','save2',
                'uglov1','uglov2','offsaid1','offsaid2','aut1','aut2','otvorot1','otvorot2','shtraf1','shtraf2','fol1',
                'fol2','p1','X','p2','t>1','t>2','t>3','t>4','t>5','t>6','oz','x1','12','x2')

print match_header[37]