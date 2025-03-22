"""SupportAnalyzer class, which analyzes support levels in a time series data."""
import numpy as np
from scipy.signal import argrelextrema

class SupportAnalyzer:
    """A class for analyzing support levels in a time series data."""
    def __init__(self, df, window=30):
        if df.empty or 'low' not in df.columns:
            raise ValueError("Geçersiz veya boş DataFrame")

        self.df = df
        self.window = window
        self.support_levels = None

    def find_support_levels(self):
        """Yerel minimumları (dip noktalarını) bulur."""
        minima_indices = argrelextrema(
            self.df["low"].values,
            np.less,
            order=self.window
        )[0]

        if len(minima_indices) == 0:
            raise ValueError(f"{self.window} periyot ile destek seviyesi bulunamadı")

        self.support_levels = self.df.iloc[minima_indices]["low"].values
        return self.support_levels

    def calculate_mean_based_buy_zone(self, sensitivity=1):
        """Method to calculate buy zone based on mean and standard deviation.
        Returns lower and upper buy zone in tuple."""
        if self.support_levels is None:
            self.find_support_levels()

        if len(self.support_levels) < 2:
            raise ValueError("En az 2 destek seviyesi gereklidir")

        mean_support = np.mean(self.support_levels)
        std_support = np.std(self.support_levels)

        buy_zone_lower = mean_support - (sensitivity * std_support)
        buy_zone_upper = mean_support

        return (buy_zone_lower, buy_zone_upper)

    def calculate_median_based_buy_zone(self, iqr_multiplier=1.5):
        """Method to calculate buy zone based on median and IQR. \n
        iqr_multiplier=> 1.5: Standard outlier defined,
        1: No outlier, more aggressive. 2: More conservative. \n
        Returns lower and upper buy zone in tuple."""
        if self.support_levels is None:
            self.find_support_levels()
        if len(self.support_levels) < 4:
            raise ValueError("IQR için en az 4 destek seviyesi gereklidir")

        # Calculate IQR and median
        median = np.median(self.support_levels)
        q1 = np.percentile(self.support_levels, 25)
        q3 = np.percentile(self.support_levels, 75)
        iqr = q3 - q1

        # Buy zone
        buy_zone_lower = median - (iqr_multiplier * iqr)
        buy_zone_upper = median  # or + (iqr_multiplier * iqr)
        return (buy_zone_lower, buy_zone_upper)
