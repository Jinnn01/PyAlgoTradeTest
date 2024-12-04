from pyalgotrade import strategy
from pyalgotrade.barfeed import csvfeed
from pyalgotrade.bar import Frequency

# print closing price
class MyStrategy(strategy.BacktestingStrategy):
  def __init__(self,feed,instrument):
    super(MyStrategy,self).__init__(feed)
    self.__instrument = instrument

  def onBars(self,bars):
    bar = bars[self.__instrument]
    self.info(bar.getClose())


# Frequency.DAY, HOUR, MINUTE
def runStrategy(name,csvfile,frequency):
  feed = csvfeed.GenericBarFeed(frequency=frequency)
  feed.addBarsFromCSV(name,csvfile)
  myStrategy = MyStrategy(feed,name)
  myStrategy.run()

print('-----AAPL-----')
runStrategy('AAPL','AAPL1d5m_cleaned.csv',Frequency.MINUTE)
print('-----MSFT-----')
runStrategy('MSFT','MSFT3mo1d_cleaned.csv',Frequency.DAY)
print('-----ORCL-----')
runStrategy('ORCL','ORCL1mo1h_cleaned.csv',Frequency.HOUR)
