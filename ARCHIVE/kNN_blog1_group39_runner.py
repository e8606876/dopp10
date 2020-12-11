#
# Code source: Josef Glas 08606876
# Date: 29.11.2020
# used for pre-processing and regression for data set BlogFeedback
#
# Pre-processing
# - no missing values need to be treated
# - scaling to be considered
# - maybe feature selection to simplify model
#
# attributes only real and integer
# feature 281 is the target: the number of comments in the next 24h (relative to base time)
#

import timeit

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer
from sklearn.feature_selection import VarianceThreshold
from sklearn.metrics import explained_variance_score, max_error, mean_absolute_error, \
    mean_squared_error, mean_squared_log_error, median_absolute_error, r2_score
from TSErrors import FindErrors

import kNN_module_group39 as knn

# parameters for steering experiments
normalization = True
n_neighbors = 39  # default = 5
distance = 'euclidean'  # euclidean or manhattan
algo = 'brute'  # brute or ball_tree

# Load data: blog feedback
blog_train = pd.read_csv("../data/BlogFeedback/blogData_train.csv", header=None)

# TODO: limit data set to reduce runtime
blog_train = blog_train.iloc[0:2000, :]

blog_train_X = blog_train.drop(blog_train.columns[280], axis=1)
blog_train_y = blog_train[blog_train.columns[280]]

print(blog_train_X.shape)

# feature selection: variance lower than threshold will be removed
sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
df = sel.fit_transform(blog_train_X)
blog_train_X = pd.DataFrame(df)
print('Shape after feature selection = ' + str(blog_train_X.shape))

# used for splitting training data into train and test data sets
X_train, X_test, y_train, y_test = \
    train_test_split(blog_train_X,
                     blog_train_y,
                     test_size=0.2,
                     random_state=13)

# transform features by scaling each feature to a given range
if normalization:
    scaler = Normalizer()
    scaler.fit(X_train)
    X_normalized = scaler.transform(X_train)
    X_train = pd.DataFrame(X_normalized)
    X_test = pd.DataFrame(X_test)
    print('Training shape = ' + str(X_train.shape))
    print('Test shape = ' + str(X_test.shape))


# def for execute one classifier
def run_regressor(X_train, y_train, X_test, y_test):
    neigh = knn.KNRegressorG39(n=n_neighbors, distance=distance, algo=algo)
    neigh.param()
    neigh.fit(X_train, y_train)
    prediction = neigh.predict(X_test)

    # print('PREDICTION:')
    # print(prediction)

    # print regression metrics
    print('REGRESSION METRICS:')

    # root mean_squared_error
    rmse = mean_squared_error(y_test, prediction, squared=False)
    print('root mean_squared_error =      ' + str('{:.2f}'.format(rmse)))

    # mean_absolute_error
    mae = mean_absolute_error(y_test, prediction)
    print('mean_absolute_error =          ' + str('{:.2f}'.format(mae)))

    er = FindErrors(y_test, prediction)
    # Root relative squared error
    print('Root relative squared error =  ' + str('{:.2f}'.format(er.rrse())))

    # Relative absolute error
    print('Relative absolute error =      ' + str('{:.2f}'.format(er.rae())))

    # r2_score
    r2 = r2_score(y_test, prediction)
    print('Correlation coeff (r2_score) = ' + str('{:.2f}'.format(r2)))


# MAIN: run classifier
execution_time = timeit.timeit('run_regressor(X_train, y_train, X_test, y_test)',
                               number=1, globals=globals())

print('-----------------------')
print('Execution time= ' + str('{:.2f}'.format(execution_time)) + ' sec')

exit(0)
