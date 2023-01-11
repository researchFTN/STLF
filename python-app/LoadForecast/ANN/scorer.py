import math
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

class Scorer:
    def get_training_and_test_score(self, trainY, trainPredict, testY, testPredict):
        trainScoreSqrt = math.sqrt(mean_squared_error(trainY, trainPredict))
        testScoreSqrt = math.sqrt(mean_squared_error(testY, testPredict))
        trainScoreAbs = mean_absolute_percentage_error(trainY, trainPredict)*100
        testScoreAbs = mean_absolute_percentage_error(testY, testPredict)*100
        return trainScoreSqrt, testScoreSqrt, trainScoreAbs, testScoreAbs

    def get_mape(self, load, forecast):
        mape = mean_absolute_percentage_error(load, forecast)*100
        return mape
