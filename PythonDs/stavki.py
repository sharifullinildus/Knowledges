# coding=utf-8
#import pandas as pd
import re, requests, os, datetime, calendar, json
from namedlist import namedlist

match_header = namedlist('match',['data','country','liga','team1','team2','gols1t1','gols2t1','gols3t1','gols1t2','gols2t2',
                          'gols3t2','kart1','kart2','vladenie1','vstvor1','mimo1','vstvor2','mimo2','save1','save2',
                'uglov1','uglov2','offsaid1','offsaid2','aut1','aut2','otvorot1','otvorot2','shtraf1','shtraf2','fol1',
                'fol2','p1','X','p2','tb1','tb2','tb3','tb4','tb5','tb6','oz','x1','x12','x2','ref'])


def go_stavki_football_forward(iter):
    with open(os.path.abspath('../../')+'stavki_data/stavki_days.txt','r') as f:
        data = json.load(f)
        dates = data[0]
        forward = datetime.date(dates[0],dates[1],dates[2])
    for i in range(iter):
        forward=forward+datetime.timedelta(days=1)
        get_daily_football(forward)
    data[0]=[forward.year,forward.month,forward.day]
    with open(os.path.abspath('../../') + 'stavki_data/stavki_days.txt', 'w') as f:
        json.dump(data,f)


def go_stavki_football_back(iter):
    with open(os.path.abspath('../../')+'stavki_data/stavki_days.txt','r') as f:
        data = json.load(f)
        dates = data[1]
        forward = datetime.date(dates[0],dates[1],dates[2])
    for i in range(iter):
        forward=forward-datetime.timedelta(days=1)
        get_daily_football(forward)
    data[1]=[forward.year,forward.month,forward.day]
    with open(os.path.abspath('../../') + 'stavki_data/stavki_days.txt', 'w') as f:
        json.dump(data,f)


def get_daily_football(date):
    if date.day < 10:
        day = '0' + str(date.day)
    else:
        day = date.day
    ref ='https://scores24.live/ru/soccer/'+'{}-{}-{}'.format(date.year,date.month,day)
    try:
        req = requests.get(ref)
        status = req.status_code
    except:
        with open(os.path.abspath('../../')+'stavki_data/fault_days.txt','a') as f:
            f.write(ref+'\n')
            return
    if status == 200:
        # Парсим день
        text =req.text.replace('\\','/')
        matches = re.findall(r'{/"slug/":/"(.*?)/"',text)
        for match in matches:
            try:
                req = requests.get('https://scores24.live/ru/soccer/m-'+match)
                status = req.status_code
            except:
                with open(os.path.abspath('../../')+'stavki_data/match_faults.txt','a') as f:
                    f.write('https://scores24.live'+match+'\n')
                    return
            if status == 200:
                # Парсим матч
                header = get_full_match(req.text)
                put_match_in_fail(header)
                revert_header(header)
                put_match_in_fail(header)
            else:
                with open(os.path.abspath('../../')+'stavki_data/match_faults.txt', 'a') as f:
                    f.write('https://scores24.live' + match + '\n')
    else:
        with open(os.path.abspath('../../')+'stavki_data/fault_days.txt','a') as f:
            f.write('https://scores24.live/ru/soccer/' + '{}-{}-{}'.format(date.year, date.month, date.day) + '\n')


def put_match_in_fail(header):
    if os.path.exists(os.path.abspath('../../')+'/stavki_data/'+header.country):
        if os.path.exists(os.path.abspath('../../') + '/stavki_data/' + header.country+'/'+header.team1+'.csv'):
            with open(os.path.abspath('../../') + '/stavki_data/' + header.country+'/'+header.team1+'.csv','a')as f:
                f.write(','.join([str(i) for i in header])+'\n')
        else:
            with open(os.path.abspath('../../') + '/stavki_data/' + header.country+'/'+header.team1+'.csv','w')as f:
                f.write(','.join([str(i) for i in header])+'\n')
    else:
        os.mkdir(os.path.abspath('../../')+'/stavki_data/'+header.country)
        with open(os.path.abspath('../../') + '/stavki_data/' + header.country + '/' + header.team1 + '.csv', 'w')as f:
            f.write(','.join([str(i) for i in header])+ '\n')


def revert_header(header):
    header.team1,header.team2=header.team2,header.team1
    header.kart1,header.kart1=header.kart1,header.kart1
    header.aut1,header.aut2=header.aut2,header.aut1
    header.fol2,header.fol1=header.fol1,header.fol2
    header.gols2t2,header.gols2t1=header.gols2t1,header.gols2t2
    header.gols1t2,header.gols1t1=header.gols1t1,header.gols1t2
    header.gols3t2,header.gols3t1=header.gols3t1,header.gols3t2
    header.x2,header.x1=header.x1,header.x2
    header.mimo2,header.mimo1=header.mimo1,header.mimo2
    header.vstvor2,header.vstvor1=header.vstvor1,header.vstvor2
    header.vladenie1 = str(100-int(header.vladenie1))
    header.uglov2,header.uglov2=header.uglov1,header.uglov2
    header.p2,header.p1=header.p2,header.p2
    header.shtraf2,header.shtraf1=header.shtraf1,header.shtraf2
    header.offsaid2,header.offsaid1=header.offsaid1,header.offsaid2
    header.save2,header.save1=header.save1,header.save2
    header.otvorot2,header.otvorot1 = header.otvorot1,header.otvorot2


def get_full_match(text):
    ref = re.search('content="(http.*?)"/',text).group(1)
    header = match_header(*[None]*46)
    header.ref = ref
    header.data = re.search('m-(.*?)-\D',text).group(1)
    teams = re.search(r'Результат матча (.*?) - (.*?) \d', text)
    header.team1,header.team2 = teams.group(1),teams.group(2)
    countr_leag = re.search(r'</svg></a><a href="/ru/soccer/.*?([А-Я].*?)<.*?([А-Я].*?)<',text)
    header.country,header.liga=countr_leag.group(1),countr_leag.group(2).strip()
    get_stat(text,header,header.team1)
    if re.search('Статистика матча', text):
       get_full_stat(text,header)
    if re.search('has_odds...(.*?),',text).group(1)=='true':
        text = requests.get(ref+'/odds').text
        get_match_coef(text,header)
    return header


def get_match_coef(text,header):
    text = text.replace('\\','/')
    text = re.search('/"odds/":{/"odds/":{/"slug(.*?)"standings/":null',text).group(0)
    p1 = re.search('type/":/"w1/(.*?)value/":/"(.*?)/"',text)
    if p1:
        header.p1 = p1.group(2)
    X = re.search(r'"type/":/"x/(.*?)value/":/"(.*?)/"',text)
    if X:
        header.X = X.group(2)
    p2 = re.search(r'"type/":/"w2/(.*?)value/":/"(.*?)/"', text)
    if p2:
        header.p2= p2.group(2)
    t1 = re.search(r'"type/":/"1/(.*?)value/":/"(.*?)/"', text)
    if t1:
        header.tb1 = t1.group(2)
    t2 = re.search(r'"type/":/"2/(.*?)value/":/"(.*?)/"', text)
    if t2:
        header.tb2 = t2.group(2)
    t3 = re.search(r'"type/":/"3/(.*?)value/":/"(.*?)/"', text)
    if t3:
        header.tb3 = t3.group(2)
    t4 = re.search(r'"type/":/"4/(.*?)value/":/"(.*?)/"', text)
    if t4:
        header.tb4 = t4.group(2)
    t5 = re.search(r'"type/":/"5/(.*?)value/":/"(.*?)/"', text)
    if t5:
        header.tb5 = t5.group(2)
    t6 = re.search(r'"type/":/"6/(.*?)value/":/"(.*?)/"', text)
    if t6:
        header.tb6 = t6.group(2)
    oz = re.search(r'"type/":/"yes/(.*?)value/":/"(.*?)/"', text)
    if oz:
        header.oz = oz.group(2)
    x1 = re.search(r'"type/":/"x1/(.*?)value/":/"(.*?)/"', text)
    if x1:
        header.x1 = x1.group(2)
    w12 = re.search(r'"type/":/"w12/(.*?)value/":/"(.*?)/"', text)
    if w12:
        header.x12 = w12.group(2)
    x2 = re.search(r'"type/":/"x2/(.*?)value/":/"(.*?)/"', text)
    if x2:
        header.x2 = x2.group(2)



def get_full_stat(text,header):
    full_stat_text = re.search('Статистика матча(.*?)rse7X f_12-16_semibold', text).group(1)
    vladenie = re.findall('>(\d+?)%<', full_stat_text)
    i = 0
    if vladenie:
        header.vladenie1 = vladenie[0]
    chisla = re.findall('>(\d+?)<', full_stat_text)
    if chisla:
        if 'Удары в створ' in full_stat_text:
            header.vstvor1, header.mimo1 = chisla[i], chisla[1 + i]
            header.vstvor2, header.mimo2 = chisla[i + 2], chisla[3 + i]
            i += 4
        if 'Сейвы' in full_stat_text:
            header.save1, header.save2 = chisla[i], chisla[1 + i]
            i += 2
        if 'Угловые' in full_stat_text:
            header.uglov1, header.uglov2 = chisla[i], chisla[1 + i]
            i += 2
        if 'Оффсайды' in full_stat_text:
            header.offsaid1, header.offsaid2 = chisla[i], chisla[1 + i]
            i += 2
        if 'Ауты' in full_stat_text:
            header.aut1, header.aut2 = chisla[i], chisla[1 + i]
            i += 2
        if 'Удары от ворот' in full_stat_text:
            header.otvorot1, header.otvorot2 = chisla[i], chisla[1 + i]
            i += 2
        if 'Штрафные' in full_stat_text:
            header.shtraf1, header.shtraf2 = chisla[i], chisla[1 + i]
            i += 2
        if 'Фолы' in full_stat_text:
            header.fol1, header.fol2 = chisla[i], chisla[1 + i]


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
    header.gols1t1, header.gols1t2 = gol1.group(1), gol1.group(2)
    header.gols2t1, header.gols2t2 = gol2.group(1), gol2.group(2)
    header.gols3t1, header.gols3t2 = gol3.group(1), gol3.group(2)
    header.kart1, header.kart2 = str(jelt1), str(jelt2)

with open(os.path.abspath('../../')+'stavki_data/stavki_days.txt','w') as f:
    json.dump([[2019,10,3],[1,2,3]],f)
go_stavki_football_forward(1)
