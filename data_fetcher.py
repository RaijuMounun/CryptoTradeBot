"""Module to fetch data from Binance API."""
import os
from binance import Client
import pandas as pd
from dotenv import load_dotenv

class DataFetcher:
    """Class to fetch data from Binance API."""
    def __init__(self, symbol="BTCUSDT", interval="1d", lookback="200d"):
        load_dotenv()
        self.client = Client(os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_API_SECRET"))
        self.symbol = symbol
        self.interval = interval
        self.lookback = lookback

    def fetch_data(self):
        """Fetches data from Binance API and returns as DataFrame."""
        klines = self.get_klines()
        df = self.get_dataframe(klines)
        df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].astype(float)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df

    def get_klines(self):
        """Functions to get klines from Binance API."""
        return self.client.get_historical_klines(
            self.symbol,
            self.interval,
            self.lookback
        )

    def get_dataframe(self, klines_):
        """Returns DataFrame from klines."""
        return pd.DataFrame(klines_)[[0, 1, 2, 3, 4]].rename(columns={
            0: "timestamp",
            1: "open",
            2: "high",
            3: "low",
            4: "close"
        })
