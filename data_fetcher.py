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
        """Binance'tan ham veriyi çeker."""
        klines = self.client.get_historical_klines(
            self.symbol,
            self.interval,
            self.lookback
        )
        df = pd.DataFrame(klines)[[0, 1, 2, 3, 4]].rename(columns={
            0: "timestamp",
            1: "open",
            2: "high",
            3: "low",
            4: "close"
        })
        df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].astype(float)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df
