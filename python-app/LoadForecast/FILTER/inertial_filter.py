import copy
import datetime
from typing import List
from pathlib import Path
import sys
from MODEL import day
from DATA_MANIPULATION import write_read_file
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)

class InertialFilter:

    def inertial_filter(self, f_day: day.Day, historical_data:List[day.Day], M, pc_load, pc_temp, pc_h, ddwc, wcL, wcT, wcH):
       
        f_day_history=write_read_file.get_history(f_day.start_date, M)
        
        h_days_history=[]
        numerator_temp=0
        numerator_load=0
        denominator=0
        load_coef=0
        thermal_coef=0
        last_h_coef=0
        day_num=min(len(h_days_history), len(f_day_history))

        for i_history in range(len(historical_data)):

            h_days_history=write_read_file.get_history(historical_data[i_history].start_date, M)

            for i_historic_day in range(day_num):

                numerator_temp+=abs(float(f_day_history[i_historic_day].t_avg)-float(h_days_history[i_historic_day].t_avg))* pow(ddwc,i_historic_day-1)
                numerator_load=+abs(float(f_day_history[i_historic_day].load_avg)-float(h_days_history[i_historic_day].load_avg))* pow(ddwc,i_historic_day-1)
                denominator+= pow(ddwc, i_historic_day-1)
                
            if day_num>0:

                load_coef=((copy.deepcopy(numerator_load)/denominator)*pc_load)
                thermal_coef=((copy.deepcopy(numerator_temp)/denominator)*pc_temp)
                last_h_coef=abs(f_day_history[0].hours[0].load-h_days_history[i_historic_day].hours[0].load)*pc_h
            
                historical_data[i_history].inertial_coef=copy.deepcopy(((wcL*load_coef)+(wcT*thermal_coef)+(wcH*last_h_coef))/(wcL+wcT+wcH))
                
                numerator_load=0
                numerator_temp=0
                denominator=0
                load_coef=0
                thermal_coef=0
                last_h_coef=0
        
        return  historical_data
