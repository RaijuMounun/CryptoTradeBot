"""Main module for bot."""
from plotter import PricePlotter
from support_analyzer import SupportAnalyzer
from data_fetcher import DataFetcher


def main():
    """Main function to run the bot."""
    # Fetch data
    data_fetcher = DataFetcher(
        symbol="BTCUSDT", interval="15m", lookback="30d")
    df = data_fetcher.fetch_data()

    current_price = df["close"].iloc[-1]

    draw_plot(df=df, current_price=current_price)


def setup_analyzer(df):
    """Sets up the analyzer."""
    analyzer = SupportAnalyzer(df, window=20)
    support_indices = analyzer.find_support_levels()
    mean_zone = analyzer.calculate_mean_based_buy_zone(sensitivity=1)
    median_zone = analyzer.calculate_median_based_buy_zone(iqr_multiplier=1.5)
    return support_indices, mean_zone, median_zone


def draw_plot(save=False, df=None, current_price=None):
    """Draws the plot."""
    support_indices, mean_zone, median_zone = setup_analyzer(df)

    plotter = PricePlotter(df, candle_count=None)
    plotter.add_buy_zone_comparison(mean_zone, median_zone)
    plotter.add_support_levels(support_indices)
    plotter.add_current_price(current_price)
    plotter.customize_plot(
        title=f"Buy Zone: ~{((mean_zone[0]+median_zone[0])/2):.2f} - {((mean_zone[1]+median_zone[1])/2):.2f}" +
        " | " +
        f"Current Price: {current_price:.2f}"
    )

    plotter.show()
    if save:
        plotter.save("chart.png")


if __name__ == "__main__":
    main()
