from typing import List
import copy
from pathlib import Path
import sys
from MODEL import day
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)

class DayLightFilter:

    def day_light_filter(self, f_day: day.Day, historical_data: List[day.Day], pc):
        
        for i_day in range(0, len(historical_data)):

            coef=abs(f_day.day_light-historical_data[i_day].day_light)*pc
            historical_data[i_day].day_light_coef=copy.deepcopy(coef)
            
        return  historical_data
