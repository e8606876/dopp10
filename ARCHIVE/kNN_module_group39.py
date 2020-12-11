from math import sqrt

import pandas
import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree

def euclidean_distance(row1, row2):
    d = 0.0
    for j in range(len(row1) - 1):
        d = d + (row1[j] - row2[j]) ** 2
    return sqrt(d)

def manhattan_distance(row1, row2):
    d = 0.0
    for j in range(len(row1) - 1):
        d = d + abs((row1[j] - row2[j]))
    return d

class KNRegressorG39:

    def __init__(self, n, distance, algo):
        self.n = n
        self.Xtrain = []
        self.ytrain = []
        self.Xtest = []
        self.model = pd.DataFrame()  # columns: distance
        self.result = pd.DataFrame()  # columns: estimate
        self.distance = distance # euclidean or manhattan
        self.algo = algo # brute or ball_tree
        self.tree = []

    def param(self):
        print('Parameter list:')
        print('n_neighbours = ' + str(self.n))
        print('distance metric = ' + str(self.distance))
        print('algorithm = ' + str(self.algo))
        print('--------------')

    # prepare data structures
    def fit(self, X_train: pandas.core.frame.DataFrame, y_train):
        self.Xtrain = X_train.reset_index(drop=True)
        self.ytrain = pd.DataFrame(y_train)
        self.ytrain = self.ytrain.reset_index(drop=True)
        self.model = pd.DataFrame(99999, index=np.arange(len(self.Xtrain)), columns=['distance'])

        if self.algo == 'ball_tree':
            self.tree = BallTree(self.Xtrain, leaf_size=2, metric=self.distance)

    # perform prediction based on data provided by fit function
    def predict(self, X_test: pandas.core.frame.DataFrame):
        self.Xtest = X_test.reset_index(drop=True)
        self.result = pd.DataFrame(0, index=np.arange(len(self.Xtest)), columns=['estimate'])

        if self.algo == 'brute':
            # iterate test data set and make prediction based on train data set (the model)
            counter = 0
            for idx1 in self.Xtest.index:
                # iterate train data set (the model)
                row1 = self.Xtest.loc[idx1, :]

                for idx2 in self.Xtrain.index:
                    row2 = self.Xtrain.loc[idx2, :]
                    # calculate distance between row 1 (test data) and row 2 (train data)
                    # store distance in data structure "model"
                    if self.distance == 'euclidean':
                        self.model.loc[idx2, 'distance'] = euclidean_distance(row1, row2)
                    if self.distance == 'manhattan':
                        self.model.loc[idx2, 'distance'] = manhattan_distance(row1, row2)

                sorted_model = self.model.sort_values(by=['distance'], ascending=True)
                estimate = int(0)
                # choose k tuples with smallest distance
                for i in range(self.n):
                    estimate = estimate + self.ytrain.iloc[sorted_model.index[i]]
                # make prediction by simply calculating the average
                #self.result.loc[counter, 'estimate'] = estimate / self.n
                self.result.iat[counter, 0] = estimate / self.n
                counter += 1

        if self.algo == 'ball_tree':
            # iterate test data set and make prediction based on BallTree (= tree)
            counter = 0
            for idx1 in self.Xtest.index:
                row1 = self.Xtest.loc[idx1, :]
                dist, ind = self.tree.query([row1], k=self.n)

                estimate = 0
                for i in range(self.n):
                    estimate = estimate + self.ytrain.iloc[ind[0][i]]

                # make prediction by simply calculating the average
                #self.result.loc[counter, 'estimate'] = estimate / self.n
                self.result.iat[counter, 0] = estimate / self.n
                counter += 1

        return self.result
