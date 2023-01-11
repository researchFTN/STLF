from datetime import datetime

class Day:

    def __init__(self):
        self.part=0
        self.start_date=datetime.now()
        self.hours=[]
        self.t_avg=0
        self.load_avg=0
        self.spec_day=False
        self.day_light=0
        self.weather_coef=0
        self.inertial_coef=0
        self.distance_coef=0
        self.deviation_coef=0
        self.day_light_coef=0
        self.coef=0

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        self._start_date = value

    @property
    def part(self):
        return self._part

    @part.setter
    def part(self, value):
        self._part = value

    @property
    def hours(self):
        return self._hours

    @hours.setter
    def hours(self, value):
        self._hours = value
    
    @property
    def t_avg(self):
        return self._t_avg

    @t_avg.setter
    def t_avg(self, value):
        self._t_avg = value

    @property
    def load_avg(self):
        return self._load_avg

    @load_avg.setter
    def load_avg(self, value):
        self._load_avg = value

    @property
    def spec_day(self):
        return self._spec_day

    @spec_day.setter
    def spec_day(self, value):
        self._spec_day = value
    
    @property
    def day_light(self):
        return self._day_light

    @day_light.setter
    def day_light(self, value):
        self._day_light = value

    @property
    def weather_coef(self):
        return self._weather_coef

    @weather_coef.setter
    def weather_coef(self, value):
        self._weather_coef = value

    @property
    def inertial_coef(self):
        return self._inertial_coef

    @inertial_coef.setter
    def inertial_coef(self, value):
        self._inertial_coef = value

    @property
    def distance_coef(self):
        return self._distance_coef

    @distance_coef.setter
    def distance_coef(self, value):
        self._distance_coef = value

    @property
    def deviation_coef(self):
        return self._deviation_coef

    @deviation_coef.setter
    def deviation_coef(self, value):
        self._deviation_coef = value

    @property
    def day_light_coef(self):
        return self._day_light_coef

    @day_light_coef.setter
    def day_light_coef(self, value):
        self._day_light_coef= value

    @property
    def coef(self):
        return self._coef

    @coef.setter
    def coef(self, value):
        self._coef = value