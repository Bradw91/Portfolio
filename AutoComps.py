import pandas as pd
import numpy as np
import datetime as datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY, date2num
from mpl_finance import *
from yahoo_fin import stock_info as si
from pandas.plotting import scatter_matrix

api_key = '' #quandl api key

symbol = 'TSLA.US' #symbol if using quandl
start = datetime.datetime(2014,1,1)
end = datetime.datetime(2019,1,1)

tsla = web.DataReader('TSLA', 'iex', start, end)
tsla.head()

tsla.to_csv('Tesla_Stock.csv')

ford = web.DataReader('F', 'iex', start, end)
ford

ford.to_csv('Ford_Stock.csv')

gm = web.DataReader('GM', 'iex', start, end)
gm.head()

gm.to_csv('GM_Stock.csv')

#open price
tsla['open'].plot(label='Tesla',figsize=(16,8),title='Open Price')
ford['open'].plot(label='GM')
gm['open'].plot(label='Ford')
plt.legend()

#tables = [tsla,ford,gm]

#for stock in tables:
    #stock['open'].plot(figsize=(16,8),title='Open Price')

#volume
tsla['volume'].plot(label='Tesla',figsize=(16,8),title='Volume')
ford['volume'].plot(label='GM')
gm['volume'].plot(label='Ford')
plt.legend()

#Total amount traded per Day

tsla['Total Traded'] = tsla['open'] * tsla['volume']
ford['Total Traded'] = ford['open'] * ford['volume']
gm['Total Traded'] = gm['open'] * gm['volume']



tsla['Total Traded'].plot(label='Tesla',figsize=(16,8))
gm['Total Traded'].plot(label='GM')
ford['Total Traded'].plot(label='Ford')
plt.legend()
plt.ylabel('Total Traded')


gm['50 Day Moving Average'] = gm['close'].rolling(window=50).mean()
gm['200 Day Moving Average'] = gm['close'].rolling(window=200).mean()


gm[['close','50 Day Moving Average','200 Day Moving Average']].plot(figsize=(16,6))
plt.legend()

car_comp = pd.concat([tsla['open'],gm['open'],ford['open']],axis=1)
car_comp.columns = ['Tesla Open','GM Open','Ford Open']
scatter_matrix(car_comp,figsize=(8,8),alpha=0.2,hist_kwds={'bins':50})


ford_reset = ford.loc['2012-01':'2012-01'].reset_index()

# Create a new column of numerical "date" values for matplotlib to use
ford_reset['date_ax'] = ford_reset['date'].apply(lambda date: date2num(date))
ford_values = [tuple(vals) for vals in ford_reset[['date_ax', 'open', 'high', 'low', 'close']].values]

mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
alldays = DayLocator()              # minor ticks on the days
weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
dayFormatter = DateFormatter('%d')      # e.g., 12

#Plot it
fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)
ax.xaxis.set_major_locator(mondays)
ax.xaxis.set_minor_locator(alldays)
ax.xaxis.set_major_formatter(weekFormatter)

candlestick_ohlc(ax, ford_values, width=0.6, colorup='g',colordown='r')


#daily cumulative returns
tsla['returns'] = tsla['close'].pct_change(1)
tsla.head()
ford['returns'] = ford['close'].pct_change(1)
gm['returns'] = gm['close'].pct_change(1)

tsla['returns'].hist(bins=100,label='Tesla',figsize=(10,8),alpha=0.5)
ford['returns'].hist(bins=100,label='Ford',alpha=0.5)
gm['returns'].hist(bins=100,label='GM',alpha=0.5)
plt.legend()

box_df = pd.concat([tsla['returns'],gm['returns'],ford['returns']],axis=1)
box_df.columns = ['Tesla Returns','GM Returns','Ford Returns']
box_df.plot(kind='box',figsize=(8,11),colormap='jet')

scatter_matrix(box_df,figsize=(8,8),alpha=0.2,hist_kwds={'bins':50})
box_df.plot(kind='scatter',x='GM Returns',y='Ford Returns',alpha=0.4,figsize=(10,8))
