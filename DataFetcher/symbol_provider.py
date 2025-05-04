"""
SymbolProvider module to fetch available trading pairs from Binance.
"""

import os
from typing import List, Optional
from dotenv import load_dotenv
from binance import Client
from binance.exceptions import BinanceAPIException

# Load environment variables when the module is imported
load_dotenv()


class SymbolProvider:
    """
    Class to fetch available trading pairs from Binance.

    Attributes:
        client (binance.Client): Binance API client used to fetch exchange information.
    """

    def __init__(self, client: Optional[Client] = None):
        """
        Initialize the SymbolProvider.

        Parameters:
            client (Optional[Client]): An optional Binance Client instance.
                                       If not provided, environment variables will be used.
        Raises:
            ValueError: If API credentials are not found in environment variables.
        """
        if client is not None:
            self.client = client
        else:
            api_key = os.getenv("BINANCE_API_KEY")
            api_secret = os.getenv("BINANCE_API_SECRET")
            if not api_key or not api_secret:
                raise ValueError("BINANCE_API_KEY or BINANCE_API_SECRET is missing in environment variables.")
            self.client = Client(api_key, api_secret)

    def get_symbols(self, quote_asset: str = "USDT") -> List[str]:
        """
        Fetches trading pairs that end with the given quote asset (e.g., USDT).

        Parameters:
            quote_asset (str): The asset you want pairs for (default is "USDT").

        Returns:
            List[str]: A list of trading pairs like "BTCUSDT", "ETHUSDT".

        Raises:
            BinanceAPIException: If the API call fails.
        """
        try:
            exchange_info = self.client.get_exchange_info()
            return [
                s["symbol"]
                for s in exchange_info["symbols"]
                if s["status"] == "TRADING" and s.get("quoteAsset") == quote_asset
            ]
        except BinanceAPIException as e:
            print(f"Failed to fetch exchange info: {e}")
            return []
