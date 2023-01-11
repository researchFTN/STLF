import copy
import pandas
from typing import List
from pathlib import Path
import sys
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
from MODEL import hour
from MODEL import day
from MODEL import day

class Converter:
   
    def convert_to_list(dataframe):
        dataframe['date'] = pandas.to_datetime(dataframe['date'])
        retVal=[]
        hours=[]
        dataframe.sort_values(by=['date'], inplace=True, ascending=True)
        dataframe = dataframe.reset_index(drop=True)
        first_part=dataframe['part'][0]
        d=day.Day()
        h=hour.Hour()

        for i_row in range(0, dataframe.shape[0]):
            
            if first_part!=dataframe['part'][i_row]:

                d.hours=copy.deepcopy(hours)
                retVal.append(copy.deepcopy(d))
                hours.clear()
               
                first_part=dataframe['part'][i_row]
                d.start_date=dataframe['date'][i_row]
                d.day_light=dataframe['day_light'][i_row+1]
                d.t_avg=dataframe['Tavg'][i_row]
                d.load_avg=dataframe['Loadavg'][i_row]
                d.part=dataframe['part'][i_row]

            h.dateTime=(dataframe['date'][i_row])
            h.temp=dataframe['temp'][i_row]
            h.windspeed=dataframe['windspeed'][i_row]
            h.cloudcover=dataframe['cloudcover'][i_row]
            h.load=dataframe['load'][i_row]
            hours.append(copy.deepcopy(h))
                
        d.hours=copy.deepcopy(hours)
        retVal.append(copy.deepcopy(d))
        
        return retVal

    def convert_to_dataframe(data: List[day.Day]):
        list=[]
        for i_day in range(len(data)):
            for i_hour in range(len(data[i_day].hours)):
                list.append([data[i_day].hours[i_hour].time, (data[i_day].date).weekday(), data[i_day].hours[i_hour].temp, data[i_day].hours[i_hour].windspeed, data[i_day].hours[i_hour].cloudcover, data[i_day].weather_coef, data[i_day].inertial_coef, data[i_day].distance_coef, data[i_day].hours[i_hour].load])
  
        df=pandas.DataFrame(list, columns=['Hour', 'Day', 'T', 'WindSpeed', 'CloudCover', 'WeatherCoef', 'InertialCoef', 'DistanceCoef','Load'], dtype=float)
        return df