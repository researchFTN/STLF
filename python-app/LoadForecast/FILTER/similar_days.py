import copy
from typing import List
from pathlib import Path
import sys
from datetime import timedelta
from MODEL import day
from MODEL import forecasted_day, forecasted_hour
from FILTER import weather_filter
from FILTER import inertial_filter
from FILTER import initial_filter
from FILTER import deviation_filter
from FILTER import distance_filter
from FILTER import special_days
from FILTER import day_light_filter
from GA import ga_sd
from DATA_MANIPULATION import write_read_file
from HELPER import DST
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)

initial_filter=initial_filter.InitialFilter()
weather_filter=weather_filter.WeatherFilter()
inertial_filter=inertial_filter.InertialFilter()
deviation_filter=deviation_filter.DeviationFilter()
distance_filter=distance_filter.DistanceFilter()
special_days=special_days.SpecialDays()
day_light_filter=day_light_filter.DayLightFilter()

pc=[1.0,1.14,0.10]
pc_load=0.01286
pc_temp=1
pc_h=0.014286
pc_dl=0.05
wc=0.002738 

def get_forecast(F_day):
   
    data=[]
    day_type:int
    day_type=(F_day.start_date).weekday()
    s_day=special_days.is_specialday(F_day.start_date + timedelta(hours=1))

    if s_day!=None and s_day.value[1]==False:
        
        day_type=6
        F_day.spec_day=True

    # get similar days
    solution=filter_preparer(F_day)
    data=filter(F_day, day_type, solution)
    # forecast based on the arithmetic average
    forecast=arithmetic_average_per_hour(F_day, data)

    # if  F_day.spec_day==True:
    #     # correcting results for special days based on error trend
    #     #data= data + special_days.select_same_type(s_day.value[0])
    #     #return fix_using_error_trend(s_day.value[0], forecast, day_type)
    #     return forecast
    # else:
    return forecast
    #return data + [F_day]

def fix_using_error_trend(spec_day_type:int, forecast, day_type):
    
    forecast_spec=[]
    list_for_LR=[]
    historical_days=special_days.select_same_type(spec_day_type)
    historical_days=deviation_filter.deviation_filter(historical_days, 1.1 , 5)

    for i_history in range(len(historical_days)):

        similar_days=filter(historical_days[i_history], day_type, filter_preparer(historical_days[i_history]))
        forecast_for_similar_spec_day=arithmetic_average_per_hour(historical_days[i_history], similar_days)
        list_for_LR.append(forecast_for_similar_spec_day) 
    #list_for_LR=deviation_filter.deviation_filter(list_for_LR, 1.1 , 3)

    forecast_spec=special_days.calculate_load(historical_days, forecast, list_for_LR) 
    return forecast_spec 

def filter(F_day:day.Day, day_type:int, solution):

    filter_result=[]
    dataSet=[x for x in write_read_file.data_copy if x.start_date<F_day.start_date and x.part==F_day.part]
    filter_result=initial_filter.initial_filter(F_day, day_type, dataSet)
    filter_result =DST.get_all_hours(F_day, copy.deepcopy(filter_result))
    filter_result=weather_filter.weather_filter(F_day, filter_result.copy(), solution[0:3], pc)
    filter_result=inertial_filter.inertial_filter(F_day, filter_result.copy(), solution[3], pc_load, pc_temp, pc_h, solution[4], solution[5], solution[6], solution[7])
    filter_result=distance_filter.distance_filter(F_day, filter_result.copy(), wc)
    filter_result=day_light_filter.day_light_filter(F_day, filter_result.copy(), pc_dl)
    
    for i_coef in range(0, len(filter_result)):

        filter_result[i_coef].coef=copy.copy(((solution[8]*filter_result[i_coef].weather_coef)+(solution[9]*filter_result[i_coef].inertial_coef)+(solution[10]*filter_result[i_coef].distance_coef)+(solution[13]*filter_result[i_coef].day_light_coef))/(solution[8]+solution[9]+solution[10]+solution[13]))
        
    filter_result.sort(key=lambda x: x.coef, reverse=False)
    
    filter_result=deviation_filter.deviation_filter(filter_result.copy(), solution[11], solution[12])
  
    return filter_result

def filter_preparer(F_day:day.Day):

    solution=[]
    solution=write_read_file.read_optimal_param(F_day.start_date, F_day.part)

    if len(solution)==0:

        solution=ga_sd.run_ga(F_day)

    return solution

def arithmetic_average_per_hour(F_day:day.Day, data:List[day.Day]):

    load=[]
    elem=0
    day=forecasted_day.ForecastedDay()
    h=forecasted_hour.ForecastedHour()
    day.date=F_day.start_date
    hours=[]

    for i_hour_in_f_day in range(len(F_day.hours)):

        load.append(F_day.hours[i_hour_in_f_day].load)
        
        for i_similar_days in range(len(data)):

            elem+=data[i_similar_days].hours[i_hour_in_f_day].load
          
        h.dateTime=F_day.hours[i_hour_in_f_day].dateTime
        h.load=copy.deepcopy(elem)/len(data)
        hours.append(copy.deepcopy(h))
        elem=0
    day.hours=copy.deepcopy(hours)
    hours.clear()

    return day