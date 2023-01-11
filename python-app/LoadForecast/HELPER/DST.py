from MODEL import day
from MODEL import hour
import copy
from typing import List
from datetime import timedelta
from pathlib import Path
import sys
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)


def get_all_hours(F_day: day.Day, data: List[day.Day]):
    
    retVal=data
    for day in data:

        if len(F_day.hours)!=len(day.hours):

            retVal=fix(F_day, data)
            break

    return retVal          

def fix(F_day: day.Day, data: List[day.Day]):

    i_hour_in_similar_day=0

    for i_hour in range(len(F_day.hours)):
        
        for i_day in range(len(data)):

            if F_day.hours[i_hour].dateTime.hour>data[i_day].hours[i_hour].dateTime.hour:

                i_hour_in_similar_day=i_hour

                while F_day.hours[i_hour].dateTime.hour!=data[i_day].hours[i_hour_in_similar_day].dateTime.hour:

                    data[i_day].hours.remove(data[i_day].hours[i_hour_in_similar_day])
                    

            elif F_day.hours[i_hour].dateTime.hour<data[i_day].hours[i_hour].dateTime.hour:

                i_hour_in_similar_day=i_hour
                elem_num=abs(len(data[i_day].hours)-len(F_day.hours))+1
                step_load =(abs(data[i_day].hours[i_hour_in_similar_day-1].load)-abs(data[i_day].hours[i_hour_in_similar_day].load)) / elem_num
                step_temp=(abs(data[i_day].hours[i_hour_in_similar_day-1].temp)-abs(data[i_day].hours[i_hour_in_similar_day].temp)) / elem_num
                step_wind=(abs(data[i_day].hours[i_hour_in_similar_day-1].windspeed)-abs(data[i_day].hours[i_hour_in_similar_day].windspeed)) / elem_num
                step_cloud=(abs(data[i_day].hours[i_hour_in_similar_day-1].cloudcover)-abs(data[i_day].hours[i_hour_in_similar_day].cloudcover)) / elem_num
                current_hour=F_day.hours[i_hour].dateTime.hour
                
                for num in (range(elem_num-1)):

                    h=hour.Hour()
                    h.dateTime=F_day.hours[i_hour].dateTime+timedelta(hours=num)
                    
                    if data[i_day].hours[i_hour_in_similar_day-1].temp<data[i_day].hours[i_hour_in_similar_day].temp:
                        h.temp=data[i_day].hours[i_hour_in_similar_day-1].temp+abs(step_temp)
                    else:
                        h.temp=data[i_day].hours[i_hour_in_similar_day-1].temp-abs(step_temp)

                    if data[i_day].hours[i_hour_in_similar_day-1].windspeed<data[i_day].hours[i_hour_in_similar_day].windspeed:
                        h.windspeed=data[i_day].hours[i_hour_in_similar_day-1].windspeed+abs(step_wind)
                    else:
                        h.windspeed=data[i_day].hours[i_hour_in_similar_day-1].windspeed-abs(step_wind)

                    if data[i_day].hours[i_hour_in_similar_day-1].cloudcover<data[i_day].hours[i_hour_in_similar_day].cloudcover:
                        h.cloudcover=data[i_day].hours[i_hour_in_similar_day-1].cloudcover+abs(step_cloud)
                    else:
                        h.cloudcover=data[i_day].hours[i_hour_in_similar_day-1].cloudcover-abs(step_cloud)

                    if data[i_day].hours[i_hour_in_similar_day-1].load<data[i_day].hours[i_hour_in_similar_day].load:
                        h.load=data[i_day].hours[i_hour_in_similar_day-1].load+abs(step_load)
                    else:
                        h.load=data[i_day].hours[i_hour_in_similar_day-1].load-abs(step_load)

                    (data[i_day].hours).insert(current_hour+1, copy.deepcopy(h))
                    i_hour_in_similar_day+=1
                
    return data
