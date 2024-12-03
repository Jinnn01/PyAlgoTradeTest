import yfinance as yf
import pandas as pd

def downloadCSV(name,period,interval):
  stock_df = yf.download(name,period=period,interval=interval)
  print(stock_df.columns)

  stock_df.reset_index(inplace=True)
  if 'Datetime' in stock_df.columns:
    stock_df.rename(columns={"Datetime": "Date Time"}, inplace=True)
  else:
    stock_df.rename(columns={"Date": "Date Time"}, inplace=True)

  stock_df['Date Time'] = pd.to_datetime(stock_df["Date Time"]).dt.strftime("%Y-%m-%d %H:%M:%S")
  stock_df.to_csv(name+'.csv',index=False)
  
  df = pd.read_csv(name+'.csv')
  # drop empty value
  df_dropped= df.dropna()
  df_dropped.to_csv(name+'_cleaned.csv',index=False)


downloadCSV('MSFT','3mo','1d')

downloadCSV('ORCL','1mo','1h')



