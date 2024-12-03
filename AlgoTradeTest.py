from pyalgotrade import strategy
from pyalgotrade.barfeed import csvfeed
from pyalgotrade.bar import Frequency

class MyStrategy(strategy.BacktestingStrategy):
  def __init__(self,feed,instrument):
    super(MyStrategy,self).__init__(feed)
    self.__instrument = instrument

  def onBars(self,bars):
    bar = bars[self.__instrument]
    self.info(bar.getClose())


# using basic feed
feed2 = csvfeed.GenericBarFeed(frequency=Frequency.DAY)
feed2.addBarsFromCSV('MSFT','MSFT_cleaned.csv')

myStrategy = MyStrategy(feed2,'MSFT')
myStrategy.run()