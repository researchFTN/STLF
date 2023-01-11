from math import sqrt
from typing import List
import copy
from pathlib import Path
import sys
from MODEL import day
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)

class WeatherFilter:
    
    def weather_filter(self, f_day: day.Day, historical_data: List[day.Day], weight_coef, pc):
        
        square_of_the_difference = [0, 0, 0]
        sum_weights=0
        numerator=0
        
        for i_day in range(len(historical_data)):
            
            for i_hour_in_f_day in range(len(f_day.hours)):

                square_of_the_difference[0] += pow((f_day.hours[i_hour_in_f_day].temp-historical_data[i_day].hours[i_hour_in_f_day].temp),2)
                square_of_the_difference[1] += pow((f_day.hours[i_hour_in_f_day].windspeed-historical_data[i_day].hours[i_hour_in_f_day].windspeed),2)
                square_of_the_difference[2] += pow((f_day.hours[i_hour_in_f_day].cloudcover-historical_data[i_day].hours[i_hour_in_f_day].cloudcover),2)
                
            for i_coef in range(len(weight_coef)):

                numerator+=weight_coef[i_coef]*pc[i_coef]*copy.deepcopy(sqrt(square_of_the_difference[i_coef]/24))
            
            sum_weights+=sum(weight_coef)
            weather_coef=numerator/sum_weights
            historical_data[i_day].weather_coef=weather_coef
            square_of_the_difference=[0,0,0]
            numerator=0
            sum_weights=0
            
        return historical_data