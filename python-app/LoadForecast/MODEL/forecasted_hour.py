class ForecastedHour:

  def __init__(self):
    self.dateTime=0
    self.load=-1

  @property
  def time(self):
    return self._time

  @time.setter
  def time(self, value):
    self._time = value

  @property
  def load(self):
      return self._load

  @load.setter
  def load(self, value):
      self._load = value