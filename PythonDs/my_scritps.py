from sklearn import metrics as mt, model_selection as ms, preprocessing as pr
from sklearn import tree as tr, neighbors as kn, linear_model as lm, datasets as data
import pandas as pd
import re

import sys

class DataTuninig:
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

    def dummies(data, features=()):
        return pd.get_dummies(data.drop(features, axis=1)).copy()


def estimators_results(x,y, estimators, params, scaler, scorer=mt.make_scorer(mt.f1_score)):
    for estim in estimators:
        scaler.fit_transform(x,y)


def get_estim_name(estimator):
    return ''.join(re.findall('[A-Z]',estimator.__str__()[:estimator.__str__().index('(')]))

class Classification:
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
        self.grid = ms.GridSearchCV(self.estim, param_grid=self.params, cv= self.cv, scoring=self.scorer)
        self.grid.fit(x, y)
        self.predictor = self.grid.best_estimator_
        self.score = self.grid.best_score_
        self.best_params = self.grid.best_params_
        self.fitted = True

    def predict(self, x):
        return self.predictor.predict(x)

    def proba(self, x):
        return self.predictor.proba(x)


class KNN(Grid):
    def __init__(self, n_neighbors=(1,2,3,5,7,9,12,15),weights=('uniform','distance'),metric=('euclidean','manhattan'),cv=10, scorer=mt.make_scorer(mt.f1_score)):
        Grid.__init__(self, cv=cv, scorer=scorer)
        self.params = {'n_neighbors':n_neighbors, 'weights':weights,'metric':metric}
        self.estim = kn.KNeighborsClassifier()


class LGC(Grid):
    def __init__(self, C=(0.0001,0.001,0.01,0.1,1,10,100,1000), type=1,max_iter=100,tol=1e-4,cv=10, scorer=mt.make_scorer(mt.f1_score)):
        Grid.__init__(self, cv=cv, scorer=scorer)
        if type==1:  #  2 class
            self.params1={'solver':('liblinear'),'penalty':('l2','l1','elasticnet')}
            self.multi = 'ovr'
        if type==2:  #  Multiclass
            self.params1={'solver':('newton-cg','lbfgs', 'sag'), 'penalty':('l2')}
            self.params2={'solver':('saga'),'penalty':('elsticnet','l1','l2')}
            self.multi = 'multinomial'
        self.params = {'C':C,}
        self.type = type
        self.estim = lm.LogisticRegression(max_iter=max_iter,tol=tol,multi_class=self.multi)

    def fit(self, x, y):
        if self.type ==1:
            self.grid = ms.GridSearchCV(self.estim, param_grid=self.params.update(self.params1), cv=cv, scoring=scorer, n_jobs=-1)
            self.grid.fit(x, y)
            self.predictor = self.grid.best_estimator_
            self.score = self.grid.best_score_
            self.params = self.grid.best_params_
            self.fitted = True
        else:
            grid=[1,1]
            grid[0] = ms.GridSearchCV(self.estim, param_grid=self.params.update(self.params1), cv=cv, scoring=scorer, n_jobs=-1)
            grid1.fit(x,y)
            grid[1] = ms.GridSearchCV(self.estim, param_grid=self.params.update(self.params2), cv=cv, scoring=scorer,
                                    n_jobs=-1)
            grid2.fit(x, y)
            i=0
            if grid[0].best_score_ < grid[1].best_score_:
                i=1
            self.predictor = grid[i].best_estimator_
            self.score = grid[i].best_score_
            self.best_params = grid[i].best_params_


class RC(Grid):
    def __init__(self, alpha=(i/10 for i in range(11)), solver=('auto','svd','cholesky','lsqr','sparse_cg','sag','saga'),
                 cv=10, scorer=mt.make_scorer(mt.f1_score)):
        Grid.__init__(self, cv=cv, scorer=scorer)
        self.params = {'alpha':alpha,'solver':solver}
        self.estim = lm.RidgeClassifier()


class SVM(Grid):
    pass


