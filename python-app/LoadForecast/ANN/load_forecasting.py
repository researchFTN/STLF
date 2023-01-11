from datetime import date
import time
import pandas
from ann_regression import AnnRegression
from plotting import Ploting
from preparer import Preparer
from scorer import Scorer
import pyodbc
import datetime as dt


NUMBER_OF_COLUMNS = 11
SHARE_FOR_TRAINING = 0.9

#load the dataset
conn = pyodbc.connect() # DEFINE

dataframe = pandas.read_sql_query('SELECT Date, T, Ff, N, Load FROM Data', conn)

# prepare data
preparer = Preparer(dataframe, NUMBER_OF_COLUMNS, SHARE_FOR_TRAINING)
trainX, trainY, testX, testY = preparer.prepare_for_training()

# make predictions
ann_regression = AnnRegression()
time_begin = time.time()
trainPredict, testPredict = ann_regression.compile_fit_predict(trainX, trainY, testX)
time_end = time.time()
print('Training duration: ' + str((time_end - time_begin)) + ' seconds')

# invert predictions
trainPredict, trainY, testPredict, testY = preparer.inverse_transform(trainPredict, testPredict)

# error
scorer = Scorer()
trainScoreSqrt, testScoreSqrt, trainScoreAbs, testScoreAbs = scorer.get_training_and_test_score(trainY, trainPredict, testY, testPredict)
print('Train Score: %.2f MSE' % (trainScoreSqrt))
print('Test Score: %.2f MSE' % (testScoreSqrt))
print('Train Score: %.2f MAPE' % (trainScoreAbs))
print('Test Score: %.2f MAPE' % (testScoreAbs))

# plotting
plotting = Ploting()
plotting.show_plots(testPredict, testY)