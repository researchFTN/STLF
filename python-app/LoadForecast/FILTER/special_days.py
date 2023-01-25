import numpy as np
from sklearn.linear_model import LinearRegression
from DATA_MANIPULATION import write_read_file
import calendar
import holidays
from datetime import date, datetime, timedelta
from dateutil.easter import *
import copy
from enum import Enum
from typing import List
from pathlib import Path
import sys
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
from MODEL import day
from MODEL import forecasted_day

class HolidayType(Enum):
    NewYearsDay = 0, False
    MartinLutherKingJrDay = 1, False
    ValentinesDay = 2, True
    WashingtonsBirthday = 3, True
    GoodFriday = 4, True
    EasterSunday = 5, False
    MothersDay = 6, True
    MemorialDay = 7, False
    FathersDay = 8, True
    IndependenceDay = 9, False
    LaborDay = 10, False
    ColumbusDay = 11, False
    Halloween = 12, True
    VeteransDay = 13, False
    Thanksgiving = 14, False
    ChristmasDay = 15, False
    JuneteenthNationalIndependenceDay = 16, False
    ChristmasDayObserved=17, False
    IndependenceDayObserved=18, True
    JuneteenthNationalIndependenceDayObserved=19, True
    NewYearsDayObserved=20, True
    ThanksgivingObserved=21, False


class SpecialDays:

    def __init__(self):
        self.working_day = False

    def is_specialday(self, date: datetime):
        us_holidays = holidays.US()
        if date.strftime('%m/%d/%Y') in us_holidays:
            holiday_type = us_holidays.get(date)
            a = "'. ()"
            for char in a:
                holiday_type = holiday_type.replace(char, "")

            return HolidayType[holiday_type]

        if date.date()-timedelta(days=1):
            return HolidayType.ThanksgivingObserved
        elif date.date() == easter(date.year):
            return HolidayType.EasterSunday
        elif date.date() - timedelta(days=2) == easter(date.year):
            return HolidayType.GoodFriday
        elif date.month == 2 and date.day == 14:
            return HolidayType.ValentinesDay
        elif date.month == 10 and date.day == 31:
            return HolidayType.Halloween
        else:
            c = calendar.Calendar(firstweekday=calendar.MONDAY)

            monthcalM = c.monthdatescalendar(date.year, 5)
            mothersDay = [day for week in monthcalM for day in week if day.weekday() == calendar.SUNDAY and day.month == 5][1]

            monthcalF = c.monthdatescalendar(date.year, 6)
            fathersDay = [day for week in monthcalF for day in week if day.weekday() == calendar.SUNDAY and day.month == 6][2]

            if date.date() == mothersDay:
                return HolidayType.MothersDay
            if date.date() == fathersDay:
                return HolidayType.FathersDay

        return None

    def select_same_type(self, type: int):
        retvalDate = []
        retvalData = []
        mindateValue: date
        maxdateValue: date
        dataSet = write_read_file.data
        # mindateValue=min(dataSet.date)
        # maxdateValue=max(dataSet.date)

        for item in holidays.US(years=range(2018, 2021)).items():
            a = " '."
            i = copy.copy(item[1])
            for char in a:
                i = i.replace(char, "")

            if i.find("Observed") == -1:
                if HolidayType[i].value[0] == type:
                    retvalDate.append(item)

        for x in write_read_file.data:
            for i in range(len(retvalDate)):
                if x.date == retvalDate[i][0]:
                    retvalData.append(x)
        return retvalData

    def calculate_load(self, historical_days: List[day.Day], forecast: forecasted_day.ForecastedDay, forecast_spec: List[forecasted_day.ForecastedDay]):
        result=0
        X = []
        Y = []
        for i_hours in range(len(forecast.hours)):
            for i_history in range(len(historical_days)):
                X.append(forecast_spec[i_history].hours[i_hours].load)
                Y.append(historical_days[i_history].hours[i_hours].load)
         
            X = np.array(X)
            #forecast = np.array(forecast)
            mlr_model = LinearRegression()
            X = np.reshape(X, newshape=(X.shape[0], 1))
            mlr_model.fit(X, Y)
            result = mlr_model.predict([[forecast.hours[i_hours].load]])
            forecast.hours[i_hours].load=copy.deepcopy(result[0])
            X = []
            Y = []
        return forecast
