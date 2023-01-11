from math import sqrt
import datetime
import copy
import pandas as pd
from typing import List
from pathlib import Path
import sys
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
from MODEL import day

class DeviationFilter:

    def deviation_filter(self, dataset, L, Z):
        data=dataset
        if len(dataset)>Z:
            data=dataset[0:int(Z)]
        
        data, deviation=self.calculate_deviation(data)

        if deviation>L:
            del data[0]
            
        return data

    def calculate_deviation(self, data):
     
        current_day= day.Day()
        helper= []
        helper=data
        sumLoad=[0]*25
        sum=0
        coef=0
        deviation_coef_sum=0
        
        for i_day in range(len(data)):

            current_day=copy.copy(data[i_day])                                                  
            helper=[d for d in data if d.start_date != current_day.start_date]

            for j_day in range(len(helper)):

                for i_hour in range(len(current_day.hours)):
                    sumLoad[i_hour]+=helper[j_day].hours[i_hour].load

            for j_hour in range(len(current_day.hours)):

                sum+=pow(copy.copy(current_day.hours[j_hour].load)-(sumLoad[j_hour]/len(helper)), 2)

            coef=sqrt(sum/len(current_day.hours))
            
            data[i_day].deviation_coef=copy.copy(coef)
            deviation_coef_sum+=copy.copy(coef)
            coef=0
            sum=0
            sumLoad.clear()
            sumLoad=[0]*len(current_day.hours)

        data.sort(key=lambda x: x.deviation_coef, reverse=True)
        deviation=(len(data)*data[0].deviation_coef)/deviation_coef_sum
        
        return data, deviation

        
            
            