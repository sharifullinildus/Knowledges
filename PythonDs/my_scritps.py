from sklearn import metrics as mt, model_selection as ms, preprocessing as pr
from sklearn import tree as tr, neighbors as kn, linear_model as lm, datasets as data
import pandas as pd
import re
ms.
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


def dummies(data, features=()):
    return pd.get_dummies(data.drop(features, axis=1)).copy()


def get_estim_name(estimator):
    return ''.join(re.findall('[A-Z]',estimator.__str__()[:estimator.__str__().index('(')]))


def estimators_compare(x, y, estiamtors, params, scaler=pr.StandardScaler, scorer=mt.make_scorer(mt.f1_score), cv=10):
    sc = scaler()
    results = []
    xsc = pd.DataFrame(sc.fit_transform(x))
    for num, estiamtor in enumerate(estiamtors):
        gr = ms.GridSearchCV(estiamtor, param_grid=params[num], scoring=scorer, n_jobs=-1, cv=cv)
        gr.fit(xsc, y)
        results.append((gr.best_score_, get_estim_name(estiamtor), gr.best_params_))
    results = results.sort()
    return results


class Grid:
    def __init__(self,cv=10, scorer=mt.make_scorer(mt.f1_score)):
        self.fitted = False
        self.cv=cv
        self.scorer=scorer

    def fit(self, x, y):
        self.fitted = True
        self.grid.fit(x, y)
        self.predictor = self.grid.best_estimator_

    def predict(self,x):
        return self.predictor.predict(x)


class KNN(Grid):
    def __init__(self, n_neighbors=(1,2,3,5,7,9,12,15),weights=('uniform','distance'),metric=('euclidean','manhattan')):
        Grid.__init__(self)
        self.params = {'n_neighbors':n_neighbors, 'weights':weights,'metric':metric}
        self.estim = kn.KNeighborsClassifier()
        self.grid = ms.GridSearchCV(self.estim, param_grid=self.params, cv=cv, scoring=scorer, n_jobs=-1)


class LGC(Grid):
    def __init__(self, C=(0.0001,0.001,0.01,0.1,1,10,100,1000), type=1,max_iter=100,tol=1e-4):
        Grid.__init__(self)
        if type==1:
            self.params1={'solver':('liblinear'),'penalty':('l2','l1','elasticnet')}
        if type==2:
            self.params1={'solver':('newton-cg','lbfgs', 'sag'), 'penalty':('l2')}
            self.params2={'solver':('saga'),'penalty':('elsticnet','l1','l2')}
        self.params = {'C':C}
        self.estim = lm.LogisticRegression(max_iter=max_iter,tol=tol)
        self.grid = ms.GridSearchCV(self.estim, param_grid=self.params, cv=cv, scoring=scorer, n_jobs=-1)

gr = ms.GridSearchCV(lm.LogisticRegression(),param_grid={'C':(1,2),'penalty':('l1','l2','elasticent','none'),'solver':('newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga')})
lgr=lm.LogisticRegression(solver='liblinear',penalty='l1')
x=pd.DataFrame(data.load_iris().data)
y=pd.Series(data.load_iris().target)
