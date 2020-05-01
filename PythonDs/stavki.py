# coding=utf-8
import pandas as pd
import sys
sys.path.append(r'C:\Users\qwerty\AppData\Local\Programs\Python\Python37\Lib\site-packages')
import re, requests, os, datetime
from namedlist import namedlist
import multiprocessing

def eazy_add(self,entry,name):
    entry=pd.Series(entry,index=list(self.columns),name=name)
    return self.append(entry)


def add_empty(df,name):
    entry = pd.Series([0]*len(list(df.columns)), index=list(df.columns),name=name)
    return df.append(entry)


def insertdf(series,array,offset):
    series[offset:offset+len(array)]=array
    return offset+len(array)

# 1 тип - только счет
# 2 - счет и  кэфы
# 3 - счет и стата
# 4 - все

match_header_names =['data','id','country','liga','team1','team2','ref','type']

simple_stat = ['gols1t1','gols2t1','gols1t2','gols2t2',
                          'kart1','kart2']
coefs_names = ['p1','p2','tb1','tb2','oz','x1','x2']

stat_names = ['vladenie1','vstvor1','mimo1','vstvor2','mimo2','save1','save2',
                'uglov1','uglov2','offsaid1','offsaid2','aut1','aut2','otvorot1','otvorot2','shtraf1','shtraf2','fol1',
                'fol2']


ability_params_names = ['id','selfcoef','h2h4','h2h3','h2h2','h2h1','smt41','smtpair4','smtpair3','smtpair2','smtpair1','team1s4','team2s4','team1s3','team2s3','team1s2','team2s2','team1s1','team2s1','h2h4id','h2h3id','h2h2id','h2h1id','smtpair4id','smtpair3id','smtpair2id','smtpair1id',
                           'team1s4id','team2s4id','team1s3id','team2s3id','team1s2id','team2s2id','team1s1id','team2s1id','allid']

match_prognoz_data_names = ['selfcoef','h2h4','h2h3','h2h2','h2h1','smt41','smtpair4','smtpair3','smtpair2','smtpair1','team1s4','team2s4','team1s3','team2s3','team1s2','team2s2','team1s1','team2s1']

full_header = match_header_names+simple_stat+stat_names+coefs_names
type4_data = simple_stat+coefs_names+stat_names

type2_data = simple_stat+coefs_names

type3_data= simple_stat+stat_names

type1_data = simple_stat

types=[type1_data,type2_data,type3_data,type4_data]

match_ability = namedlist('prognoz',ability_params_names)
ability_params = namedlist('ability',match_prognoz_data_names)
match_header = namedlist('match',full_header)


def get_data_by_type(data, type):
    return data[types[type]]


def go_stavki_football_forward(dates,iter,fail):
    fail = os.path.abspath('../../') + 'stavki_data/' + fail
    with open(fail,'w') as f:
        with open(fail+'rev', 'w') as f2:
            f.write(','.join(full_header)+'\n')
            f2.write(','.join(full_header)+'\n')
            forward = dates
            for _ in range(iter):
                forward=forward+datetime.timedelta(days=1)
                get_daily_football(forward,f,f2)


def go_stavki_football_back(dates,iter,fail):
    fail=os.path.abspath('../../')+'stavki_data/'+fail
    with open(fail,'w') as f:
        with open(fail+'rev', 'w') as f2:
            f.write(','.join(full_header) + '\n')
            f2.write(','.join(full_header) + '\n')
            forward = dates
            for _ in range(iter):
                forward=forward-datetime.timedelta(days=1)
                get_daily_football(forward,f,f2)


def get_better_type(t1,t2):
    if t1==3 and t2==2:
        return 1
    elif t1==2 and t2==3:
        return 1
    else:
        return min(t1,t2)


def get_worth_type(type):
    if type==4:
        return ['1','2','3','4']
    elif type==3:
        return ['1','3']
    elif type==2:
        return ['1','2']
    else:
        return ['1',]


def get_daily_football(date,fail,fail2):
    if date.day < 10:
        day = '0' + str(date.day)
    else:
        day = date.day
    if date.month < 10:
        month = '0' + str(date.month)
    else:
        month = date.month
    ref ='https://scores24.live/en/soccer/'+'{}-{}-{}'.format(date.year,month,day)
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
        matches = re.findall(r'{/"slug/":/"(\d\d.*?)/"',text)
        for match in matches:
            try:
                req = requests.get('https://scores24.live/en/soccer/m-'+match)
                status = req.status_code
            except:
                with open(os.path.abspath('../../')+'stavki_data/match_faults.txt','a') as f:
                    f.write('https://scores24.live'+match+'\n')
                    return
            if status == 200:
                # Парсим матч
                text =req.text
                if re.search('Cancelled', text):
                    continue
                header = get_full_match(text, date)
                header1=[str(i) for i in header]
                fail.write(','.join(header1)+'\n')
                revert_header(header)
                header1 = [str(i) for i in header]
                fail2.write(','.join(header1) + '\n')
            else:
                with open(os.path.abspath('../../')+'stavki_data/match_faults.txt', 'a') as f:
                    f.write('https://scores24.live' + match + '\n')
    else:
        with open(os.path.abspath('../../')+'stavki_data/fault_days.txt','a') as f:
            f.write(ref + '\n')


def revert_header(header):
    header.team1,header.team2=header.team2,header.team1
    header.kart1,header.kart1=header.kart1,header.kart1
    header.aut1,header.aut2=header.aut2,header.aut1
    header.fol2,header.fol1=header.fol1,header.fol2
    header.gols2t2,header.gols2t1=header.gols2t1,header.gols2t2
    header.gols1t2,header.gols1t1=header.gols1t1,header.gols1t2
    header.x2,header.x1=header.x1,header.x2
    header.mimo2,header.mimo1=header.mimo1,header.mimo2
    header.vstvor2,header.vstvor1=header.vstvor1,header.vstvor2
    if header.vladenie1!=None:
        header.vladenie1 = str(100-int(header.vladenie1))
    header.uglov2,header.uglov2=header.uglov1,header.uglov2
    header.p2,header.p1=header.p2,header.p2
    header.shtraf2,header.shtraf1=header.shtraf1,header.shtraf2
    header.offsaid2,header.offsaid1=header.offsaid1,header.offsaid2
    header.save2,header.save1=header.save1,header.save2
    header.otvorot2,header.otvorot1 = header.otvorot1,header.otvorot2


def get_full_match(text,date):
    text=text.replace('\\','/')
    ref = re.search('content="(http.*?)"/',text).group(1)
    header = match_header(*[0]*len(full_header))
    header.ref = ref
    header.data = date.year-2018*365+date.month*30+date.day
    header.type = 1
    teams = re.search(r'span><a href="/en/soccer/t-(.*?)".*?span><a href="/en/soccer/t-(.*?)"', text)
    header.team1,header.team2 = teams.group(1),teams.group(2)
    countr_leag = re.search(r'</svg></a><a href="/en/soccer/.*?>(.*?)<.*?12-16">(.*?)<',text)
    header.country,header.liga=countr_leag.group(1),countr_leag.group(2).strip()
    get_stat(text,header,re.findall('-(\w*)',ref)[-2])
    if re.search('Match statistic', text):
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
    p2 = re.search(r'"type/":/"w2/(.*?)value/":/"(.*?)/"', text)
    if p2:
        header.p2= p2.group(2)
    t1 = re.search(r'"type/":/"1.5/(.*?)value/":/"(.*?)/"', text) or re.search(r'"type/":/"1/(.*?)value/":/"(.*?)/"', text) or re.search(r'"type/":/"2/(.*?)value/":/"(.*?)/"', text)
    if t1:
        header.tb1 = t1.group(2)
    t2 = re.search(r'"type/":/"2.5/(.*?)value/":/"(.*?)/"', text) or  re.search(r'"type/":/"3/(.*?)value/":/"(.*?)/"', text) or  re.search(r'"type/":/"3.5/(.*?)value/":/"(.*?)/"', text)
    if t2:
        header.tb2 = t2.group(2)
    oz = re.search(r'"type/":/"yes/(.*?)value/":/"(.*?)/"', text)
    if oz:
        header.oz = oz.group(2)
    x1 = re.search(r'"type/":/"x1/(.*?)value/":/"(.*?)/"', text)
    if x1:
        header.x1 = x1.group(2)
    x2 = re.search(r'"type/":/"x2/(.*?)value/":/"(.*?)/"', text)
    if x2:
        header.x2 = x2.group(2)
        header.type += 1


def get_full_stat(text,header):
    full_stat_text = re.search('Match statistic(.*?)rse7X f_12-16_semibold', text).group(1)
    vladenie = re.findall('>(\d+?)%<', full_stat_text)
    i = 0
    if vladenie:
        header.vladenie1 = vladenie[0]
    chisla = re.findall('>(\d+?)<', full_stat_text)
    if len(chisla) ==16:
        if 'Shots on goal' in full_stat_text:
            header.vstvor1, header.mimo1 = chisla[i], chisla[1 + i]
            header.vstvor2, header.mimo2 = chisla[i + 2], chisla[3 + i]
            i += 4
        if 'oalkeeper saves' in full_stat_text:
            header.save1, header.save2 = chisla[i], chisla[1 + i]
            i += 2
        if 'Corners' in full_stat_text:
            header.uglov1, header.uglov2 = chisla[i], chisla[1 + i]
            i += 2
        if 'Offsides' in full_stat_text:
            header.offsaid1, header.offsaid2 = chisla[i], chisla[1 + i]
            i += 2
        if 'Throw in' in full_stat_text:
            header.aut1, header.aut2 = chisla[i], chisla[1 + i]
            i += 2
        if 'oalkeeper kicks' in full_stat_text:
            header.otvorot1, header.otvorot2 = chisla[i], chisla[1 + i]
            i += 2
        if 'Free kicks' in full_stat_text:
            header.shtraf1, header.shtraf2 = chisla[i], chisla[1 + i]
            i += 2
        if 'Fouls' in full_stat_text:
            header.fol1, header.fol2 = chisla[i], chisla[1 + i]
        header.type+=2


def get_stat(text,header,team1):
    if not re.search('MatchCourseListing(.*?)Open</button>', text):
        gol3 = re.search('"result_score/":/"(\d*?):(\d*?)/',text)
        header.gols1t1, header.gols1t2 = str(int(gol3.group(1)) // 2), str(int(gol3.group(2)) // 2)
        header.gols2t1, header.gols2t2 = gol3.group(1), gol3.group(2)
        return
    simple_stat = re.search('MatchCourseListing(.*?)Open</button>', text).group(1)+'p5qQ'
    jelt1,jelt2=0,0
    gol11,gol12,gol21,gol22=0,0,0,0
    for i in re.findall('9 f_12-16">(\d*)(.*?)p5qQ', simple_stat):
        if '.svg#card' in i[1]:
            if team1 in i[1]:
                jelt1+=1
            else:
                jelt2+=1
        if '.svg#soccer' in i[1]:
            if team1 not in i[1]:
                if int(i[0])<46:
                    gol11+=1
                else:
                    gol12+=1
            else:
                if int(i[0])<46:
                    gol12+=1
                else:
                    gol22+=1
    gol3 = re.search('Match ended with score.*?(\d+?):(\d+?)', simple_stat)
    gol2 = re.search('Full time.*?(\d+?):(\d+?)', simple_stat)
    gol1 = re.search('1st half.*?(\d):(\d)', simple_stat[:gol2.start(0)])
    if gol1:
        header.gols1t1, header.gols1t2 = gol1.group(1), gol1.group(2)
        header.gols2t1, header.gols2t2 = gol3.group(1), gol3.group(2)
    elif re.findall('9 f_12-16">(\d*)(.*?)p5qQ', simple_stat)!=[]:
        header.gols1t1, header.gols1t2 = str(gol11),str(gol12)
        header.gols2t1, header.gols2t2 = gol3.group(1), gol3.group(2)
    else:
        header.gols1t1, header.gols1t2 =str(int(gol3.group(1))//2), str(int(gol3.group(2))//2)
        header.gols2t1, header.gols2t2 = gol3.group(1), gol3.group(2)
    header.kart1, header.kart2 = str(jelt1), str(jelt2)


def get_match_prognoz_abilities(header,matches1,matches2,prognoz_data):
    team1_data = matches1[matches1.team1==header.team1].append(matches2[matches2.team1==header.team1])
    team2_data = matches1[matches1.team1==header.team2].append(matches2[matches2.team1==header.team2])
    last = header.id
    prognoz_data = add_empty(prognoz_data,last)
    new =prognoz_data.loc[last]
    bag_of_id = set()
    bag_of_id.add(header.id)
    for i in ability_params_names[ability_params_names.index('h2h4id'):]:
        new[i]=[]
    h2h = team1_data[team1_data.team2 == header.team2]
    for _, row in h2h.iterrows():
        for type in get_worth_type(row.type):
            new['h2h'+type]+=1
            new['h2h'+type+'id'].append(row.id)
            bag_of_id.add(row.id)
    same_teams = set(team1_data.team2) & set(team2_data.team2)
    bag_of_pars = []
    for _, game in team1_data[team1_data.team2.isin(same_teams)].iterrows():
        game2 = team2_data[(team2_data.team2 == game.team2) & ~(team2_data.id.isin(bag_of_id))]
        if game2:
            game2 = game2.iloc[0]
            bag_of_pars.append((game.id, game2.id, abs(game.data - game2.data),get_better_type(game.type,game2.type)))
            bag_of_id.add(game2.id)
            bag_of_id.add(game.id)
    for match in bag_of_pars:
        for type in get_worth_type(match[-1]):
            new['smtpair' + type] += 1
            new['smtpair' + type+'id'].append((match[0],match[1]))
    for _, match in team1_data.iterrows():
        if match.id not in bag_of_id:
            for type in get_worth_type(match['type']):
                new['team1s' + type] += 1
                new['team1s' + type+'id'].append(match.id)
                bag_of_id.add(match.id)
    for _, match in team2_data.iterrows():
        if match.id not in bag_of_id:
            for type in get_worth_type(match['type']):
                new['team2s' + type] += 1
                new['team2s' + type+'id'].append(match.id)
                bag_of_id.add(match.id)
    header.allid = bag_of_id
    return prognoz_data


def create_prognoz_df(params,ability_header,matches,prognoz):
    for i,j in params,ability_header[ability_params_names.index('self.coef'):ability_params_names.index('h2h4id')]:
        if i>j:
            return
    prognoz=add_empty(prognoz,ability_header.id)
    last = prognoz.loc[ability_header.id]
    used_id=set()
    offset=0
    matches=matches[matches.id.isin(ability_header.allid)]
    if params.selfcoef == ability_header.selfcoef == 1:
        offset = insertdf(last,list(matches.loc[ability_header.id][coefs_names]),offset)
    for index,i in enumerate(params[1:]):
        for j in range(i):
            for l in ability_header[match_header_names.index('h2h4id')+index]:
                if l not in used_id:
                    offset = insertdf(last,get_data_by_type(matches.loc[l],4-index%4),offset)
                    used_id.add(l)


def proces_run_back(strt,offset):
    proces=[]
    for i in range(5):
        date = strt-datetime.timedelta(days=i*offset)
        proc = multiprocessing.Process(target=go_stavki_football_back,args=(date,offset,'proc'+str(i)))
        proces.append(proc)
        proc.start()
    for i in proces:
        i.join()
