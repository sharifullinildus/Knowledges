# coding=utf-8
#import pandas as pd
import re,requests
from collections import namedtuple
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
                get_full_match(text)


def get_full_match(text):
    header = [0]*50
    teams = re.search(r'content="Результат матча (.*?) - (.*?) \d', text)
    header[3],header[4]=teams.group(1),teams.group(2)
    countr_leag = re.search(r'</svg></a><a href="/ru/soccer/.*?([А-Я].*?)<.*?([А-Я].*?)<',text)
    header[1],header[2]=countr_leag.group(1),countr_leag.group(2)
    get_activ(text,header,header[3])
    if re.search('Статистика матча', text):
        get_full_stat(text,header)
    if re.search('has_odds..(.*?),',text).group(1)=='true':
        get_match_coef(text,header)
    return header


def get_match_coef(text,header):
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



def get_full_stat(text,header):
    full_stat_text = re.search('Статистика матча(.*?)rse7X f_12-16_semibold', text).group(1)
    vladenie = re.findall('>(\d+?)%<', full_stat_text)
    if vladenie:
        header[17],header[18] = vladenie[0], vladenie[1]
    chisla = re.findall('>(\d+?)<', full_stat_text)
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


def get_activ(text,header,team1):
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
    header[5],header[8]=gol1.group(1),gol1.group(2)
    header[6], header[9] = gol2.group(1), gol2.group(2)
    header[7], header[10] = gol3.group(1), gol3.group(2)
    header[11],header[12] = jelt1,jelt2



match_header = namedtuple('match',['data','country','liga','team1','team2','gols1t1','gols2t1','gols3t1','gols1t2','gols2t2',
                          'gols3t2','kart1','kart2','vladenie1','vstvor1','mimo1','vstvor2','mimo2','save1','save2',
                'uglov1','uglov2','offsaid1','offsaid2','aut1','aut2','otvorot1','otvorot2','shtraf1','shtraf2','fol1',
                'fol2','p1','X','p2','tb1','tb2','tb3','tb4','tb5','tb6','oz','x1','x12','x2'])

#text =requests.get('https://scores24.live/ru/soccer/m-05-11-2019-fc-barcelona-sk-slavia-prague').text
asd = match_header(*([0]*45))
print(asd.match)
