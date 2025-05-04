"""ResistanceAnalyzer class, which analyzes resistance levels in a time series data."""
import numpy as np
from scipy.signal import argrelextrema

class ResistanceAnalyzer:
    """A class for analyzing resistance levels in a time series data."""
    def __init__(self, df, window=30):
        if df.empty or 'high' not in df.columns:
            raise ValueError("Invalid or empty DataFrame")
        self.df = df
        self.window = window
        self.resistance_levels = None

    def find_resistance_levels(self):
        """Finds local maxima."""
        maxima_indices = argrelextrema(
            self.df["high"].values,
            np.greater,
            order=self.window
        )[0]

        if len(maxima_indices) == 0:
            raise ValueError(f"Resistance level not found with period {self.window}")

        self.resistance_levels = self.df.iloc[maxima_indices]["high"].values
        return self.resistance_levels

    def calculate_mean_based_sell_zone(self, sensitivity=1):
        """Calculates sell zone with mean and standard deviation."""
        if self.resistance_levels is None:
            self.find_resistance_levels()

        if len(self.resistance_levels) < 2:
            raise ValueError("En az 2 direnç seviyesi gereklidir")

        mean_resistance = np.mean(self.resistance_levels)
        std_resistance = np.std(self.resistance_levels)

        sell_zone_lower = mean_resistance
        sell_zone_upper = mean_resistance + (sensitivity * std_resistance)

        return (sell_zone_lower, sell_zone_upper)

    def calculate_median_based_sell_zone(self, iqr_multiplier=1.5):
        """Calculates sell zone with median and IQR."""
        if self.resistance_levels is None:
            self.find_resistance_levels()

        if len(self.resistance_levels) < 4:
            raise ValueError("IQR için en az 4 direnç seviyesi gereklidir")

        # Calculate median and IQR
        median = np.median(self.resistance_levels)
        q1 = np.percentile(self.resistance_levels, 25)
        q3 = np.percentile(self.resistance_levels, 75)
        iqr = q3 - q1

        # Sell zone
        sell_zone_lower = median
        sell_zone_upper = median + (iqr_multiplier * iqr)
        return (sell_zone_lower, sell_zone_upper)
