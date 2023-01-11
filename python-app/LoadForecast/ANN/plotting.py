import numpy
import matplotlib.pyplot as plt
from pathlib import Path
import sys
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)

class Ploting:
    
    def make_plot(self, collection):
        trainPredictPlot = numpy.empty_like(collection)
        trainPredictPlot[:] = numpy.nan
        trainPredictPlot[0:len(collection)] = collection
        return trainPredictPlot

    def show_plots(self, testPredict, testY, pod3):
        plot1 = self.make_plot(testPredict)    
        plot2 = self.make_plot(testY)
        plot3=self.make_plot(pod3)
        plt.plot(plot1)
        plt.plot(plot2)
        plt.plot(plot3)
        plt.show()