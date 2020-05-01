from sklearn import metrics as mt, model_selection as ms, preprocessing as pr, svm
from sklearn import tree as tr, neighbors as kn, linear_model as lm, datasets as data
from sklearn import naive_bayes as nb, discriminant_analysis as da
import pandas as pd
import re, xgboost

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


def get_estim_name(estimator):
    return ''.join(re.findall('[A-Z]',estimator.__str__()[:estimator.__str__().index('(')]))


class BinaryClassification:

    class BinaryClassGrid:
        def __init__(self,cv=10, scorer=mt.make_scorer(mt.f1_score)):
            self.fitted = False
            self.cv=cv
            self.scorer=scorer

        def fit(self, x, y):
            self.grid = ms.GridSearchCV(self.estim, param_grid=self.params, cv= self.cv, scoring=self.scorer,n_jobs=-1)
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
        def __init__(self, C=(0.0001,0.001,0.01,0.1,1,10,100,1000), max_iter=100,tol=1e-4,cv=10, scorer=mt.make_scorer(mt.f1_score), solver=('liblinear'),penalty=('l2','l1','elasticnet')):
            BinaryClassification.BinaryClassGrid.__init__(self, cv=cv, scorer=scorer)
            self.params={'C':C,'solver':solver,'penalty':penalty}
            self.estim = lm.LogisticRegression(max_iter=max_iter,tol=tol,multi_class='ovr')

    class LRC_B2(BinaryClassGrid):
        name = 'LRC_B2'
        def __init__(self, C=(0.0001,0.001,0.01,0.1,1,10,100,1000), max_iter=100,tol=1e-4,cv=10, scorer=mt.make_scorer(mt.f1_score), solver=('newton-cg','lbfgs','sag','saga'),penalty=('l2')):
            BinaryClassification.BinaryClassGrid.__init__(self, cv=cv, scorer=scorer)
            self.params = {'C': C, 'solver': solver, 'penalty': penalty}
            self.estim = lm.LogisticRegression(max_iter=max_iter, tol=tol, multi_class='auto')

    class RC_B(BinaryClassGrid):
        name = 'RC_B'
        def __init__(self, alpha=(i/10 for i in range(11)), solver=('auto','svd','cholesky','lsqr','sparse_cg','sag','saga'),
                     cv=10, scorer=mt.make_scorer(mt.f1_score)):
            BinaryClassification.BinaryClassGrid.__init__(self, cv=cv, scorer=scorer)
            self.params = {'alpha':alpha,'solver':solver}
            self.estim = lm.RidgeClassifier()

    class SVC_B(BinaryClassGrid):
        name = 'SVC_B'
        def __init__(self, C=(0.0001,0.001,0.01,0.1,1,10,100,10000), kernel=('rbf','sigmoid'),gamma=(0,2,5,9,14,20),
                     cv=10, scorer=mt.make_scorer(mt.f1_score)):
            BinaryClassification.BinaryClassGrid.__init__(self, cv=cv, scorer=scorer)
            self.params = {'C':C,'kernel':kernel,'gamma':gamma}
            self.estim = svm.SVC()

    class LDAC_B(BinaryClassGrid):
        name = 'LDAC_B'
        def __init__(self, solver=('svd'),
                     cv=10, scorer=mt.make_scorer(mt.f1_score)):
            BinaryClassification.BinaryClassGrid.__init__(self, cv=cv, scorer=scorer)
            self.params = {'solver':solver}
            self.estim = da.LinearDiscriminantAnalysis()

    class LDAC_B2(BinaryClassGrid):
        name = 'LDAC_B2'
        def __init__(self, solver=('lsqr','eigen'),shrinkage=('auto'),
                     cv=10, scorer=mt.make_scorer(mt.f1_score)):
            BinaryClassification.BinaryClassGrid.__init__(self, cv=cv, scorer=scorer)
            self.params = {'solver':solver,'shrinkage':shrinkage}
            self.estim = da.LinearDiscriminantAnalysis()

    class NBC_B(BinaryClassGrid):
        ame = 'NBC_B'
        def __init__(self,
                     cv=10, scorer=mt.make_scorer(mt.f1_score)):
            BinaryClassification.BinaryClassGrid.__init__(self, cv=cv, scorer=scorer)
            self.params = {}
            self.estim = nb.GaussianNB()




class BinarEstimators:
    @classmethod
    def fit(x, y):
        for estimator in BinarEstimators.estimators:
            estimator.fit(x, y)
            print(estimator.name, ' - ', estimator.score)

    estimators = {i[0]:i[1]() for i in BinaryClassification.__dict__.items() if 'C_B' in i[0]}