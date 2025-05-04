"""Module to plot price data."""
from typing import Tuple
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PricePlotter:
    """Class to plot price data. \n
    Candle count can be specified to plot last n candles, or can be left None to plot all.
    """

    def __init__(self, df: pd.DataFrame, candle_count: int = None, plot_frame=None):
        plt.style.use('dark_background')
        self.df = df if candle_count is None else df.iloc[-candle_count:]
        self.fig, self.ax = plt.subplots(figsize=(14, 7))
        self._setup_base_plot()
        self.plot_frame = plot_frame  # Tkinter frame where the plot will be shown

    def _setup_base_plot(self):
        """Draws the base plot."""
        self.ax.plot(self.df["timestamp"], self.df["close"],
                     label="Price", color="blue", alpha=0.7)

    def add_sell_zone_comparison(self, zone1: Tuple[float, float], zone2: Tuple[float, float]):
        """
        Compare two sell zones.
        Parameters:
        zone1: (lower1, upper1) - First sell zone
        zone2: (lower2, upper2) - Second sell zone
        """
        lower1, upper1 = zone1
        lower2, upper2 = zone2

        # Upper zone (more aggressive selling)
        self.ax.axhspan(
            ymin=min(upper1, upper2),
            ymax=max(upper1, upper2),
            color='purple',
            alpha=0.3,
            label='Sell Zone (Aggressive)'
        )

        # Lower zone (conservative selling)
        self.ax.axhspan(
            ymin=min(lower1, lower2),
            ymax=max(lower1, lower2),
            color='orange',
            alpha=0.3,
            label='Sell Zone (Conservative)'
        )

    def add_resistance_levels(self, resistance_levels: list):
        """
        Add resistance levels to the plot.
        Parameters:
        resistance_levels (list): List of resistance prices.
        """
        if len(resistance_levels) == 0:
            raise ValueError("Couldn't found any resistance level.")

        # Mark resistance levels
        for level in resistance_levels:
            timestamps = self.df[self.df["high"] == level]["timestamp"]
            if timestamps.empty:
                continue
            self.ax.scatter(
                timestamps,
                [level] * len(timestamps),
                color="red",
                marker="v",
                s=100,
                label="Direnç Seviyeleri" if level == resistance_levels[0] else None
            )

    def add_sell_zone(self, sell_zone: Tuple[float, float], color: str = "cyan"):
        """Adds a single sales territory."""
        lower, upper = sell_zone
        self.ax.axhspan(
            lower,
            upper,
            color=color,
            alpha=0.2,
            label=f"Sell Zone ({lower:.2f}-{upper:.2f})"
        )

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
            label='Buy Zone Top'
        )

        # Transparent green fill between lower borders
        self.ax.axhspan(
            ymin=min(lower1, lower2),
            ymax=max(lower1, lower2),
            color='green',
            alpha=0.2,
            label='Buy Zone Bottom'
        )

    def add_unified_buy_zone(self, zone: Tuple[float, float]):
        """
        Shows a single unified buy zone on the plot.
        Parameters:
        zone: (lower, upper) - Unified buy zone
        """
        lower, upper = zone

        # Transparent blue fill for the unified zone
        self.ax.axhspan(
            ymin=lower,
            ymax=upper,
            color='blue',
            alpha=0.3,
            label='Unified Buy Zone'
        )

    def add_support_levels(self, support_levels: list):
        """
        Adds support levels to the plot as scatter points.
        Parameters:
        support_levels (list): A list of price values representing support levels.
        """
        if len(support_levels) == 0:
            raise ValueError("No support levels found.")

        # Add support levels as scatters
        for level in support_levels:
            # Find timestamp corresponding to support level
            timestamps = self.df[self.df["low"] == level]["timestamp"]
            if timestamps.empty:
                continue
            self.ax.scatter(
                timestamps,
                [level] * len(timestamps),  # Support level price
                color="orange",
                marker="^",
                s=100,
                # Just add labels to the first level
                label="Support levels" if level == support_levels[0] else None
            )

    def add_current_price(self, current_price: float):
        """Adds current price to the plot."""
        self.ax.scatter(
            self.df["timestamp"].iloc[-1],
            current_price,
            color="purple",
            s=100,
            label="Current Price"
        )

    def customize_plot(self, pair):
        """Customizes the plot."""
        _title = f"Pair: {pair} | Current Price: {self.df['close'].iloc[-1]:.8f}"
        self.ax.set_title(_title)
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Price (USDT)")
        self.ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

    def show_on_tkinter(self):
        """Shows the plot inside the Tkinter window."""
        if self.plot_frame:  # Check if a plot_frame is provided
            canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()  # Add the plot canvas to the Tkinter window
        else:
            print("No Tkinter frame provided to show the plot.")

    def show(self):
        """Shows the plot."""
        self.show_on_tkinter()

    def save(self, filename: str = "price_chart.png"):
        """Saves the plot."""
        self.fig.savefig(filename, dpi=300)
