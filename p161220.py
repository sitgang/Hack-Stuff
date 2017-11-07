import numpy as np
import pandas as pd
import talib

N = 500

closes = np.random.random_integers(1800,2300,N)

index = pd.DatetimeIndex(pd.date_range('20160903',periods = N,freq = '10T'))

sr = pd.Series(closes,index = index)

df = sr.resample('H').ohlc().astype('float')

cciArray = talib.CCI(df.high.values,df.low.values,df.close.values)
