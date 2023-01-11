import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_percentage_error
import csv
from typing import List
from datetime import timedelta
from pathlib import Path
import sys
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
from DATA_MANIPULATION import converter
from MODEL import day


data_copy=converter.Converter.convert_to_list(pd.read_excel('Data.xlsx'))

def get_history(date, M):
    date1=date - timedelta(days=M)
    retVal=[]
    for x in data_copy:
        if date1<=x.start_date and x.start_date<date:
            retVal.append(x)
    return retVal

def get_f_day(date):
    index=[x.start_date for x in data_copy].index(date)
    F_day=data_copy[index]
    return F_day

def save_forecast(result):
    i=0
    (result.hours).sort(key=lambda x: x.dateTime, reverse=True)
    forecast_results = pd.read_csv('RESULTS/Results.csv')
    forecast_results['Date'] = pd.to_datetime(forecast_results['Date'])
    for i_date in range(0, forecast_results.shape[0]):  
        if forecast_results['Date'][i_date]==result.hours[i].dateTime:
            forecast_results['MyForecast'][i_date]=result.hours[i].load
            forecast_results['MyMAPE'][i_date]=mean_absolute_percentage_error([forecast_results['MeasuredLoad'][i_date]], [result.hours[i].load])*100
            forecast_results['TheirMAPE'][i_date]=mean_absolute_percentage_error([forecast_results['MeasuredLoad'][i_date]], [forecast_results['TheirForecast'][i_date]])*100
            i+=1
            if i==len(result.hours):
                break
       
    forecast_results.drop(forecast_results.filter(regex="Unnamed"),axis=1, inplace=True)
    forecast_results.to_csv('RESULTS/Results.csv', index=False, date_format='%Y-%m-%d %H:%M')  

def save_optimal_param( array, date, part):
    
    file = open('RESULTS/optimal_param_sd.csv', 'a', newline ='')
 
    with file:
        header = ['Date', 'part', 'temp_coef', 'wind_coef', 'cloud_coef','M', 'ddwc', 'wcL', 'wcT', 'wcH', 'Weather','Inertia', 'Distance', 'L', 'z', 'wcdd']
        writer = csv.DictWriter(file, fieldnames = header)
        #writer.writeheader()
        writer.writerow({
                         'Date':date,
                         'part':part,
                         'temp_coef':array[0], 
                         'wind_coef':array[1], 
                         'cloud_coef':array[2],
                         'M':array[3], 
                         'ddwc':array[4], 
                         'wcL':array[5], 
                         'wcT':array[6], 
                         'wcH':array[7], 
                         'Weather':array[8],
                         'Inertia':array[9], 
                         'Distance':array[10], 
                         'L':array[11], 
                         'z':array[12],
                         'wcdd':array[13]
                        })

def save_the_optimal_start_of_the_sequence( array, month):
    
    file = open('RESULTS/optimal_param_array.csv', 'a', newline ='')
 
    with file:
        header = ['Month', 'part_0', 'part_1', 'part_2', 'part_3']
        writer = csv.DictWriter(file, fieldnames = header)
        #writer.writeheader()
        writer.writerow({
                         'Month':month,
                         'part_0':array[0],
                         'part_1':array[1], 
                         'part_2':array[2], 
                         'part_3':array[3]
                        })

def read_optimal_param(date, part):
    solution=[]
    with open("RESULTS/optimal_param_sd.csv", 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        #next(file)
        for row in csvreader:
            if pd.to_datetime(row[0]).date()==date.date() and int(row[1])==part:
                solution= np.array(row[2:], dtype=float)
        return solution