# coding=utf-8
import random,os, pandas as pd
buk = ('q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m')
asd=pd.DataFrame(columns=[1,2,3])





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

import datetime, multiprocessing


def run():
    now = datetime.datetime.now()
    qwe=pd.DataFrame(columns=[1,2,3,4,5,6])
    for i in range(6000):
        qwe.loc[i]=[5]*6
    print(datetime.datetime.now()-now)

run()
'''if __name__ == '__main__':
    pr1=multiprocessing.Process(target=run)
    pr2=multiprocessing.Process(target=run)
    pr3 = multiprocessing.Process(target=run)
    now = datetime.datetime.now()
    pr1.start()
    pr2.start()
    pr3.start()
    pr1.join()
    pr2.join()
    pr3.join()
    print(datetime.datetime.now() - now)'''