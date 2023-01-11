from datetime import datetime

class ForecastedDay:

    def __init__(self):
        self.start_date=datetime.now()
        self.hours=[]

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def hours(self):
        return self._hours

    @hours.setter
    def hours(self, value):
        self._hours = value
    
    