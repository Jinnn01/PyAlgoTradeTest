import itertools
from pyalgotrade.optimizer import server
from pyalgotrade.barfeed import csvfeed
from pyalgotrade.bar import Frequency


def parameters_generator():
    instrument = ["TSLA"]
    entrySMA = range(150, 251)
    exitSMA = range(5, 16)
    rsiPeriod = range(2, 11)
    overBoughtThreshold = range(75, 96)
    overSoldThreshold = range(5, 26)
    return itertools.product(instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)


# The if __name__ == '__main__' part is necessary if running on Windows.
if __name__ == '__main__':
    # Load the bar feed from the CSV files.
    feed = csvfeed.GenericBarFeed(frequency=Frequency.DAY)
    feed.addBarsFromCSV("TSLA", "TSLA3mo1d_cleaned.csv")
    # Run the server.
    server.serve(feed, parameters_generator(), "localhost", 5000)