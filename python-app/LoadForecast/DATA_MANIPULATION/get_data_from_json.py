import json
import glob
from datetime import datetime
import pandas as pd
import copy


def read_data():

    json_weather_data = json.loads(open('DATA/weather.json').read())
    weather_data = []

    for day in range(len(json_weather_data)):

        for hour in range(len(json_weather_data[day]["hours"])):

            date=datetime.strptime(json_weather_data[day]["datetime"]+ " " +json_weather_data[day]["hours"][hour]["datetime"], '%Y-%m-%d %H:%M:%S')
            tempmax=json_weather_data[day]["tempmax"]
            tempmin=json_weather_data[day]["tempmin"]
            temp=json_weather_data[day]["hours"][hour]["temp"]
            feelslike=json_weather_data[day]["hours"][hour]["feelslike"]
            humidity=json_weather_data[day]["hours"][hour]["humidity"]
            snow=json_weather_data[day]["hours"][hour]["snow"]
            snowdepth=json_weather_data[day]["hours"][hour]["snowdepth"]
            windspeed=json_weather_data[day]["hours"][hour]["windspeed"]
            pressure=json_weather_data[day]["hours"][hour]["pressure"]
            cloudcover=json_weather_data[day]["hours"][hour]["cloudcover"]
            sunrise=json_weather_data[day]["sunrise"]
            sunset=json_weather_data[day]["sunset"]
            day_light=(datetime.strptime(sunset, '%H:%M:%S') - datetime.strptime(sunrise, '%H:%M:%S'))/60
            weather_data.append([date, tempmax, tempmin, temp, feelslike, humidity, snow, snowdepth, windspeed, pressure, cloudcover, sunrise, sunset, day_light.seconds, -1, -1, -1, -1])

    files = glob.glob('Data/Load/*', recursive=True)
    data=[]

    for single_file in files:

        with open(single_file, 'r') as f:

            try:

                json_data = json.load(f)

                for day in range(len(json_data['days'])):

                    for hour in range(len(json_data['days'][day]['load_per_hour'])):

                        load =json_data['days'][day]['load_per_hour'][hour]['load']
                        timestamp=datetime.strptime(json_data['days'][day]['load_per_hour'][hour]['timestamp'], '%m/%d/%Y %H:%M:%S')
                    
                        data.append([timestamp, load])

            except KeyError:
                print(f'Skipping {single_file}')

    retVal=[]

    for i_hour_load in range(len(data)):

        for i_weather_load in range(len(weather_data)):

            if data[i_hour_load][0]==weather_data[i_weather_load][0]:

                weather_data[i_weather_load][14]=copy.deepcopy(data[i_hour_load][1])
                retVal.append(copy.deepcopy(weather_data[i_weather_load]))  
                break       

    df = pd.DataFrame(retVal)
    df.to_excel('Data1.xlsx', header=['date', 'tempmax', 'tempmin', 'temp', 'feelslike', 'humidity', 'snow', 'snowdepth', 'windspeed', 'pressure', 'cloudcover', 'sunrise', 'sunset', 'day_light', 'load', 'Tavg', 'Loadavg', 'part'], index=False)
    ExcelApp = None

def add_avg_temp_and_load(data, start):
    avgTempandLoad=[]
    Tavg=0
    Loadavg=0
    hour_num=0
    part=0
    for hour_iterator in range(len(data)):
        
        Tavg+=data['temp'][hour_iterator]
        Loadavg+=data['load'][hour_iterator]
        hour_num+=1

        if data['date'][hour_iterator].hour in start:
            
            Tavg=Tavg/hour_num
            Loadavg=Loadavg/hour_num

            if data['date'][hour_iterator].hour==start[0]:
                part=0
            elif data['date'][hour_iterator].hour==start[1]:
                part=1
            elif data['date'][hour_iterator].hour==start[2]:
                part=2
            elif data['date'][hour_iterator].hour==start[3]:
                part=3
            else:
                pass
            
            avgTempandLoad.append([data['date'][hour_iterator], copy.deepcopy(Tavg), copy.deepcopy(Loadavg), copy.deepcopy(part)])
            hour_num=0
            Tavg=0
            Loadavg=0

    current_hour=0
    for i_day in range(len(avgTempandLoad)):
        for i_hour in range(current_hour,len(data)):

            data['Tavg'][i_hour]=copy.deepcopy(avgTempandLoad[i_day][1])
            data['Loadavg'][i_hour]=copy.deepcopy(avgTempandLoad[i_day][2])
            data['part'][i_hour]=copy.deepcopy(avgTempandLoad[i_day][3])

            if data['date'][i_hour].hour in start:
            
                current_hour=i_hour+1
                break

    df = pd.DataFrame(data)
    return df
    #df.to_excel('Data.xlsx', header=['date', 'tempmax', 'tempmin', 'temp', 'feelslike', 'humidity', 'snow', 'snowdepth', 'windspeed', 'pressure', 'cloudcover', 'sunrise', 'sunset', 'day_light', 'load', 'Tavg', 'Loadavg', 'part'], index=False)
    #ExcelApp = None