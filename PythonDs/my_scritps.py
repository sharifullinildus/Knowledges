from sklearn import metrics as mt, model_selection as ms, preprocessing as pr
from sklearn import tree
import jupyter
import sys


def kvad_kor(data, colums, add=0):
    data=data.copy()
    for i in colums:
        if add==0:
            data[i+'_kvad']=data['kvad'].apply(lambda x:x**2)
            data[i + '_kvad'] = data['kvad'].apply(lambda x: x ** 0.5)
        elif add==1:
            data[i + '_kvad'] = data['kvad'].apply(lambda x: x ** 2)
        else:
            data[i + '_kvad'] = data['kvad'].apply(lambda x: x ** 0.5)
    return data

def choose_scaler(x,y,estimator):
    asd = 123

def estimators_results(x,y,estimators, params, scaler, scorer=mt.make_scorer(mt.f1_score)):
    for estim in estimators:
        scaler.fit_transform(x,y)
