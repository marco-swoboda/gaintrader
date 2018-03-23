import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import requests
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BINANCE_URL = "https://api.binance.com"

def getExchangeInfo():
    url = BINANCE_URL + "/api/v1/exchangeInfo"
    response = requests.get(url)
    return response.json()

def getPriceInfo(symbol, limit = 500):
    url = BINANCE_URL + f"/api/v1/trades?symbol={symbol}&limit={limit}"
    #url = BINANCE_URL + f"/api/v3/ticker/price?symbol={symbol}"
    #url = BINANCE_URL + f"/api/v3/ticker/price"
    response = requests.get(url)
    return response.text

def getHistoricalInfo(symbol, limit = 500, interval='1m', startTime=None, endTime=None):
    start = f"&startTime={startTime}" if startTime else ''
    end = f"&startTime={endTime}" if endTime else ''
    url = BINANCE_URL + f"/api/v1/klines?symbol={symbol}&interval={interval}&limit={limit}{start}{end}"
    #url = BINANCE_URL + f"/api/v3/ticker/price?symbol={symbol}"
    #url = BINANCE_URL + f"/api/v3/ticker/price"
    response = requests.get(url)
    list = response.json()
    return list

def getTickerInfo():
    url = BINANCE_URL + f"/api/v3/ticker/price"
    response = requests.get(url)
    priceInfo = response.json()

    result = {}
    return {info['symbol'] : info['price'] for info in priceInfo}


def addToMarket(markets, symbol, price):
    for market in markets.keys():
        mlen = -(len(market))
        if symbol[mlen:] == market:
            markets[market][symbol[:mlen]] = price

def main():
    # list = getHistoricalInfo('ADABTC')
    # with open("ada_candle.pickle", "wb") as f:
    #     pickle.dump(list, f)
    with open("ada_candle.pickle", "rb") as f:
        list = pickle.load(f)

    labels = [
        'Open time',
        'Open',
        'High',
        'Low',
        'Close',
        'Volume',
        'Close time',
        'Quote asset volume',
        'Number of trades',
        'Taker buy base asset volume',
        'Taker buy quote asset volume',
        'Ignore'
    ]
    print(list)
    df = pd.DataFrame.from_records(list, columns=labels)
    #df['Date'] = pd.to_datetime(df['Open time'], unit='ms')
    df['Date'] = df['Open time']/1000

    df = df.drop(columns=['Open time', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    df = df[:-1]
    #df.set_index('Date', inplace=True)
    df_ohlc = df[['Date', 'Open', 'High', 'Low', 'Close']]
#    df_ohlc['open'] = df_ohlc['Open']
#    df_ohlc['high'] = df_ohlc['High']
#    df_ohlc['low'] = df_ohlc['Low']
#    df_ohlc['close'] = df_ohlc['Close']
#    df_ohlc.drop(columns=['Open', 'High', 'Low', 'Close'])

#    df_ohlc['Open', 'High', 'Low', 'Close'] = df_ohlc['Open', 'High', 'Low', 'Close'].convert_objects(convert_numeric=True)
    df_ohlc['Open'] = df_ohlc['Open'].convert_objects(convert_numeric=True)
    df_ohlc['High'] = df_ohlc['High'].convert_objects(convert_numeric=True)
    df_ohlc['Low'] = df_ohlc['Low'].convert_objects(convert_numeric=True)
    df_ohlc['Close'] = df_ohlc['Close'].convert_objects(convert_numeric=True)
    print(df_ohlc.tail())
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.epoch2num)
    #df_ohlc.reset_index(inplace=True)
    df_volume = df['Volume']
    df_volume.index = df['Date']

    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
    ax1.xaxis_date()

    candlestick_ohlc(ax1, quotes=df_ohlc[-60:].values, width=.7/(24*60), colorup='g')
    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
    plt.show()


def main3():
    # ada = getPriceInfo('ADABTC', 1000)
    # with open("ada.pickle", "wb") as f:
    #     pickle.dump(ada, f)
    with open("ada.pickle", "rb") as f:
        ada = pickle.load(f)

    df = pd.read_json(ada, precise_float=True)
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df.set_index('time', inplace=True)
    # df['price'].plot()
    # plt.show();

    print(df)

    minuteData = pd.DataFrame()
    minuteData['price'] = df['price'].resample('30s').mean()
    minuteData['price'].fillna(method='ffill', inplace=True)
    minuteData['volume'] = df['qty'].resample('30s').sum()

    minuteData['EMAfast'] = minuteData['price'].rolling()


#    minuteData.plot()

    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)

    ax1.plot(minuteData.index, minuteData['price'])
#    ax1.plot(df.index, df['500ma'])
#    ax1.plot(df.index, df['1200ma'])
    ax2.bar(minuteData.index, minuteData['volume'])

    plt.show()

    print(minuteData)
#    df = df.resample('1s')
    # for idx, it in enumerate(ada):
    #     #print(f"{idx}. {it['time']}")
    #     print(it['time'])


def main2():
    #data = getExchangeInfo()

    markets = {'BTC' : {}, 'ETH': {}, 'USDT': {}, 'BNB': {}}

    priceInfo = getTickerInfo()
    #print(priceInfo)
    for symbol, price in priceInfo.items():
        addToMarket(markets, symbol, price)
        #print(f"Price ({symbol[:-3]}): {price} {symbol[-3:]}")

    for market in markets.keys():
        print(market, markets[market])

    print(len(priceInfo))

    #json.load(urllib.urlopen(BINANCE_URL))

if __name__ == '__main__':
    main()