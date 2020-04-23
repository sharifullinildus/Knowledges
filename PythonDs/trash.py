# coding=utf-8
import random,os, pandas as pd
buk = ('q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m')


def hash1(str):
    has = 0
    p=1
    p2=1
    p3=1
    z=1
    for i in str:
        y=(ord(i))#+100000)%300
        if has >184467440737095516:
            has%=184467440737095516
        has +=(y+p2)*(y+p3)*p+z*(y+p2)*(y+p3+p)+p*(y+p3*p2)*z
        z+=1
        p+=z
        p2+=y%61
        p3+=y%31
    return has

def unics():
    words = []
    for i in product(buk, repeat=4):
        words.append(''.join(i))
    for i in product(buk, repeat=3):
        words.append(''.join(i))
    for i in product(buk, repeat=2):
        words.append(''.join(i))
    for i in product(buk, repeat=1):
        words.append(''.join(i))
    z=0
    asd =set()
    for i in words:
        z+=1
        asd.add(hash1(i)%1000000)
    print(len(asd),len(words))

def perestanovki():
    def RandomPermutation():
        perm = list(range(8))
        random.shuffle(perm)
        return perm

    def StupidPermutation():
        partialSums = [0, 1, 8, 35, 111, 285,
                       628, 1230, 2191, 3606, 5546, 8039, 11056, 14506, 18242,
                       22078, 25814, 29264, 32281, 34774, 36714, 38129, 39090,
                       39692, 40035, 40209, 40285, 40312, 40319, 40320]
        r = random.randint(0, partialSums[-1])
        numInv = 0
        while partialSums[numInv] < r:
            numInv += 1
        perm = list(range(8))
        for step in range(numInv):
            t1 = random.randint(0, 7)
            t2 = random.randint(0, 7)
            perm[t1], perm[t2] = perm[t2], perm[t1]
        return perm

    with open('gen_unics','w') as f:
        pass

class asd:
    def __init__(self):
        self.z=2


class asd2(asd):
    def __init__(self):
        asd.__init__(self)

    class B:
        def __init__(self):
            pass

    class C(B):
        def __init__(self):
            asd2.B.__init__(self)
        pass

def create_1type_predict_for_match(header):
    team1_data = pd.read_csv(os.path.abspath('../../') + '/stavki_data/' + header.country+'/'+header.team1+'type1.csv')
    team2_data = pd.read_csv(os.path.abspath('../../') + '/stavki_data/' + header.country+'/'+header.team2+'type1.csv')
    h2h = team1_data[team1_data.team2 == header.team2].head(5)
    same_teams = set(team1_data.team2) & set(team2_data.team2)
    bag_of_pars = []
    bag_of_id = []
    for game in team1_data[team1_data.team2 in (same_teams)]:
        game2= team2_data[(team2_data.team2 == game.team2) & (team2_data.id not in bag_of_id)]
        if game2:
            game2=game2.iloc[0]
            bag_of_pars.append((game.id,game2.id,abs(game.data-game2.data)))
            bag_of_id.append(game2.id)
    bag_of_pars= sorted(bag_of_pars,key=lambda x:x[-1])[:5]
    


asd =[(1,6,3),(3,4,5)]
print sorted(asd,key=lambda x:x[1])