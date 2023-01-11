from pathlib import Path
import sys
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
from FILTER import similar_days
from DATA_MANIPULATION import write_read_file
from datetime import datetime, timedelta
from DATA_MANIPULATION import write_read_file

if __name__=="__main__":   
    
    date= input("Enter date in format YYYY-MM-DD H:M:")
    date=datetime.strptime(date, '%Y-%m-%d %H:%M')

    while True: 
        print(date)
        F_day=write_read_file.get_f_day(date)
        result=similar_days.get_forecast(F_day)
        write_read_file.save_forecast(result)
        date =date+timedelta(hours=len(F_day.hours))