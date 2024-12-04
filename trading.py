from __future__ import print_function
from pyalgotrade import strategy
from pyalgotrade.barfeed import csvfeed
from pyalgotrade.bar import Frequency
from pyalgotrade.technical import ma


# trading: above SMA buy, below SMA sell
class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        super(MyStrategy, self).__init__(feed, 100000)
        self.__position = None
        self.__instrument = instrument
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__sma = ma.SMA(feed[instrument].getPriceDataSeries(), smaPeriod)

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("BUY at $%.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        if self.__sma[-1] is None:
            return

        bar = bars[self.__instrument]
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if bar.getPrice() > self.__sma[-1]:
                # Enter a buy market order for 10 shares. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, 10, True)
        # Check if we have to exit the position.
        elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
            self.__position.exitMarket()



# Frequency.DAY, HOUR, MINUTE
def run_strategy(name,csvfile,frequency,smaPeriod):
  feed = csvfeed.GenericBarFeed(frequency=frequency)
  feed.addBarsFromCSV(name,csvfile)
  myStrategy = MyStrategy(feed,name,smaPeriod)
  myStrategy.run()
  print("Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity())

run_strategy('AAPL','AAPL1d5m_cleaned.csv',Frequency.MINUTE,15)
run_strategy('TSLA','TSLA3mo1d_cleaned.csv',Frequency.DAY,15)
