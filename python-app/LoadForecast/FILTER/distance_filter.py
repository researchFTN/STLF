from typing import List
import copy
from pathlib import Path
import sys
from MODEL import day
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)

class DistanceFilter:

    def distance_filter(self, f_day: day.Day, historical_data: List[day.Day], wc):
        
        for i_day in range(0, len(historical_data)):

            coef=abs((f_day.start_date- historical_data[i_day].start_date).days)*wc
            historical_data[i_day].distance_coef=copy.deepcopy(coef)
            
        return  historical_data
