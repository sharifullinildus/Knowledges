'''from sklearn import metrics as mt, model_selection as ms, preprocessing as pr, svm
from sklearn import tree as tr, neighbors as kn, linear_model as lm, datasets as data
import pandas as pd
import re

import sys

class DataTuninig:
    @staticmethod
    def kvad_kor(datas, colums, add=0):
        data=datas.copy()
        for i in colums:
            if add==0:
                data[i+'_kvad']=data['kvad'].apply(lambda x:x**2)
                data[i + '_kvad'] = data['kvad'].apply(lambda x: x ** 0.5)
            elif add==1:
                data[i + '_kvad'] = data['kvad'].apply(lambda x: x ** 2)
            else:
                data[i + '_kvad'] = data['kvad'].apply(lambda x: x ** 0.5)
        return data

    @staticmethod
    def dummies(data, features=()):
        return pd.get_dummies(data.drop(features, axis=1)).copy()





class Classification:
    @staticmethod
    def estimators_compare(x, y, estiamtors, params, scorer=mt.make_scorer(mt.f1_score), cv=10):
        results = []
        xsc = pd.DataFrame(sc.fit_transform(x))
        for num, estiamtor in enumerate(estiamtors):
            gr = ms.GridSearchCV(estiamtor, param_grid=params[num], scoring=scorer, n_jobs=-1, cv=cv)
            gr.fit(xsc, y)
            results.append((gr.best_score_, get_estim_name(estiamtor), gr.best_params_))
        results = results.sort()
        return results

def get_estim_name(estimator):
    return ''.join(re.findall('[A-Z]',estimator.__str__()[:estimator.__str__().index('(')]))

class BinaryClassification(Classification):

    class BinaryClassGrid():
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


    class KNC_B(BinaryClassGrid):
        name = 'KNC_B'
        def __init__(self, n_neighbors=(1,2,3,5,7,9,12,15),weights=('uniform','distance'),metric=('euclidean','manhattan'),cv=10, scorer=mt.make_scorer(mt.f1_score)):
            BinaryClassification.BinaryClassGrid.__init__(self, cv=cv, scorer=scorer)
            self.params = {'n_neighbors':n_neighbors, 'weights':weights,'metric':metric}
            self.estim = kn.KNeighborsClassifier()


    class LRC_B(BinaryClassGrid):
        name = 'LRC_B'
        def __init__(self, C=(0.0001,0.001,0.01,0.1,1,10,100,1000), max_iter=100,tol=1e-4,cv=10, scorer=mt.make_scorer(mt.f1_score)):
            BinaryClassification.BinaryClassGrid.__init__(self, cv=cv, scorer=scorer)
            self.params={'C':C,'solver':('liblinear'),'penalty':('l2','l1','elasticnet')}
            self.estim = lm.LogisticRegression(max_iter=max_iter,tol=tol,multi_class='ovr')

    class RC_B(BinaryClassGrid):
        name = 'RC_B'
        def __init__(self, alpha=(i/10 for i in range(11)), solver=('auto','svd','cholesky','lsqr','sparse_cg','sag','saga'),
                     cv=10, scorer=mt.make_scorer(mt.f1_score)):
            BinaryClassification.BinaryClassGrid.__init__(self, cv=cv, scorer=scorer)
            self.params = {'alpha':alpha,'solver':solver}
            self.estim = lm.RidgeClassifier()

    class SVC_B(BinaryClassGrid):
        name = 'SVC_B'
        def __init__(self, C=(0.0001,0.001,0.01,0.1,1,10,100,10000), kernel=('linear','poly','rbf','sigmoid'),
                     cv=10, scorer=mt.make_scorer(mt.f1_score)):
            BinaryClassification.BinaryClassGrid.__init__(self, cv=cv, scorer=scorer)
            self.params = {'C':C,'kernel':kernel}
            self.estim = svm.SVC()

'''
print ('фыв')