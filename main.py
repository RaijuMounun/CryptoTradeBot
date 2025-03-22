"""Main module for bot."""
from plotter import PricePlotter
from support_analyzer import SupportAnalyzer
from data_fetcher import DataFetcher


def main():
    """Main function to run the bot."""
    # Fetch data
    data_fetcher = DataFetcher(
        symbol="BTCUSDT", interval="15m", lookback="7d")
    df = data_fetcher.fetch_data()

    # Calculate support and buy zone
    analyzer = SupportAnalyzer(df, window=20)
    support_indices = analyzer.find_support_levels()
    mean_zone = analyzer.calculate_mean_based_buy_zone(sensitivity=1)
    median_zone = analyzer.calculate_median_based_buy_zone(iqr_multiplier=1.5)
    buy_zone = analyzer.calculate_mean_based_buy_zone()

    current_price = df["close"].iloc[-1]

    # Draw plot
    plotter = PricePlotter(df)
    plotter.add_buy_zone_comparison(mean_zone, median_zone)
    plotter.add_support_levels(support_indices)
    plotter.add_current_price(current_price)
    plotter.customize_plot(
        title=f"Buy Zone: {buy_zone[0]:.2f} - {buy_zone[1]:.2f} | Current Price: {current_price:.2f}"
    )

    plotter.show()  # Grafiği göster
    # plotter.save("btc_chart2.png")  # Kaydetmek için


if __name__ == "__main__":
    main()
