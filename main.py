"""Main module for bot."""
import matplotlib.pyplot as plt
from support_analyzer import SupportAnalyzer
from data_fetcher import DataFetcher

def main():
    """Main function to run the bot."""
    # Fetch data
    data_fetcher = DataFetcher(symbol="BTCUSDT", interval="15m", lookback="30d")
    df = data_fetcher.fetch_data()

    # Calculate support and buy zone
    analyzer = SupportAnalyzer(df, window=20)
    buy_zone_lower, buy_zone_upper = analyzer.calculate_mean_based_ideal_buy_zone()

    current_price = df["close"].iloc[-1]

    # Draw plot
    plt.figure(figsize=(14,7))
    plt.plot(df["timestamp"], df["close"], label="Fiyat")
    plt.axhline(y=buy_zone_upper, color="g", linestyle="--", label="Alım Bölgesi (Üst Sınır)")
    plt.axhline(y=buy_zone_lower, color="r", linestyle="--", label="Alım Bölgesi (Alt Sınır)")
    plt.title(f"Alım Bölgesi: {buy_zone_lower:.2f} - {buy_zone_upper:.2f} | Şu Anki Fiyat: {current_price:.2f}")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
