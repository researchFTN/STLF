from datetime import datetime

class Hour:

  def __init__(self):
    self.dateTime=datetime.now()
    self.temp=0
    self.windspeed=0
    self.cloudcover=0
    self.load=-1

  @property
  def dateTime(self):
    return self._dateTime

  @dateTime.setter
  def dateTime(self, value):
    self._dateTime = value

  @property
  def temp(self):
    return self._temp

  @temp.setter
  def temp(self, value):
    self._temp = value
  
  @property
  def windspeed(self):
      return self._windspeed

  @windspeed.setter
  def windspeed(self, value):
      self._windspeed = value

  @property
  def cloudcover(self):
      return self._cloudcover

  @cloudcover.setter
  def cloudcover(self, value):
      self._cloudcover = value

  @property
  def load(self):
      return self._load

  @load.setter
  def load(self, value):
      self._load = value