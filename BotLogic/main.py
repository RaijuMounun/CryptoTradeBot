import pandas as pd
import matplotlib.pyplot as plt
from binance import Client
from talib import RSI, MACD, SMA

api_key = "LvqAwj2cLmN4cMZmNRhkD2uzZ49XIa1ATamAN06sEqSreyLriuV8moKuKqURaWcw"
api_secret = "GfsfYlsWctS2mWNnuraE4gI5L1Trc2zEceaT8AphP60ZEv0efrlYScbeqRoI8knY"

client = Client(api_key, api_secret)

symbol = "BTCUSDT"
time_interval = Client.KLINE_INTERVAL_15MINUTES

candles = client.get_historical_klines(
    symbol=symbol,
    interval=time_interval,
    start_str="30 days ago UTC"
)
print("mumlar: ")
print(candles)