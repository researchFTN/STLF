from pathlib import Path
import sys
from datetime import timedelta
from MODEL import day
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)

class InitialFilter:

    def initial_filter(self, f_day:day.Day, type:int, data):

        retVal= []
        for i_day in range(len(data)):

            if(data[i_day].start_date + timedelta(hours=1)).weekday() == type and data[i_day].t_avg < f_day.t_avg+5 and data[i_day].t_avg > f_day.t_avg-5:

                retVal.append(data[i_day])
                
        return retVal