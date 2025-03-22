"""Module to plot price data."""
from typing import Tuple
import matplotlib.pyplot as plt
import pandas as pd

class PricePlotter:
    """Class to plot price data."""
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.fig, self.ax = plt.subplots(figsize=(14, 7))
        self._setup_base_plot()

    def _setup_base_plot(self):
        """Draws the base plot."""
        self.ax.plot(self.df["timestamp"], self.df["close"], label="Fiyat", color="blue")

    def add_buy_zone(self, buy_zone: Tuple[float, float]):
        """Adds buy zone to the plot."""
        lower, upper = buy_zone
        self.ax.axhline(y=upper, color="green", linestyle="--", label="Alım Üst Sınırı")
        self.ax.axhline(y=lower, color="red", linestyle="--", label="Alım Alt Sınırı")

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
