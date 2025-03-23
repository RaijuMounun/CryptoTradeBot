"""Module to plot price data."""
from typing import Tuple
import matplotlib.pyplot as plt
import pandas as pd


class PricePlotter:
    """Class to plot price data. \n
    Candle count can be specified to plot last n candles, or can be left None to plot all.
    """

    def __init__(self, df: pd.DataFrame, candle_count: int = None):
        plt.style.use('dark_background')
        self.df = df if candle_count is None else df.iloc[-candle_count:]
        self.fig, self.ax = plt.subplots(figsize=(14, 7))
        self._setup_base_plot()

    def _setup_base_plot(self):
        """Draws the base plot."""
        self.ax.plot(self.df["timestamp"], self.df["close"],
                     label="Fiyat", color="blue")

    def add_buy_zone_comparison(self, zone1: Tuple[float, float], zone2: Tuple[float, float]):
        """
        Shows the two buy zones comparatively on the plot.
        Parameters:
        zone1: (lower1, upper1) - First buy zone
        zone2: (lower2, upper2) - Second buy zone
        """
        lower1, upper1 = zone1
        lower2, upper2 = zone2

        # Transparent red fill between upper borders
        self.ax.axhspan(
            ymin=min(upper1, upper2),
            ymax=max(upper1, upper2),
            color='red',
            alpha=0.2,
            label='Üst Alım Bölgeleri Arası'
        )

        # Transparent green fill between lower borders
        self.ax.axhspan(
            ymin=min(lower1, lower2),
            ymax=max(lower1, lower2),
            color='green',
            alpha=0.2,
            label='Alt Alım Bölgeleri Arası'
        )

    def add_support_levels(self, support_levels: list):
        """Adds support levels to the plot."""
        valid_levels = [i for i in support_levels if i < len(self.df)]
        self.ax.scatter(
            self.df["timestamp"].iloc[valid_levels],
            self.df["low"].iloc[valid_levels],
            color="orange",
            marker="^",
            label="Destek Seviyeleri"
        )

    def add_current_price(self, current_price: float):
        """Adds current price to the plot."""
        self.ax.scatter(
            self.df["timestamp"].iloc[-1],
            current_price,
            color="purple",
            s=100,
            label="Şu Anki Fiyat"
        )

    def customize_plot(self, title: str):
        """Customizes the plot."""
        self.ax.set_title(title)
        self.ax.set_xlabel("Tarih")
        self.ax.set_ylabel("Fiyat (USDT)")
        self.ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

    def show(self):
        """Shows the plot."""
        plt.show()

    def save(self, filename: str = "price_chart.png"):
        """Saves the plot."""
        self.fig.savefig(filename, dpi=300)
