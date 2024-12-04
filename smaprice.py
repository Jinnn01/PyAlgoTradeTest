# print closing SMA price
from pyalgotrade import strategy
from pyalgotrade.barfeed import csvfeed
from pyalgotrade.bar import Frequency
from pyalgotrade.technical import ma

def safe_round(value,digits):
  if value is not None:
    value = round(value,digits)
  return value

class MyStrategy(strategy.BacktestingStrategy):
  def __init__(self,feed,instrument):
    super(MyStrategy,self).__init__(feed)
    self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(),15)
    self.__instrument = instrument

  def onBars(self,bars):
    bar = bars[self.__instrument]
    self.info("%s %s" % (bar.getClose(), safe_round(self.__sma[-1], 2)))

# Frequency.DAY, HOUR, MINUTE
def runStrategy(name,csvfile,frequency):
  feed = csvfeed.GenericBarFeed(frequency=frequency)
  feed.addBarsFromCSV(name,csvfile)
  myStrategy = MyStrategy(feed,name)
  myStrategy.run()

# runStrategy('AAPL','AAPL1d5m_cleaned.csv',Frequency.MINUTE)
runStrategy('MSFT','MSFT3mo1d_cleaned.csv',Frequency.DAY)