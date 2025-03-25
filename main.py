"""Main module for bot."""
from plotter import PricePlotter
from support_analyzer import SupportAnalyzer
from resistance_analyzer import ResistanceAnalyzer
from data_fetcher import DataFetcher


def main():
    """Main function to run the bot."""
    data_fetcher = DataFetcher(symbol="DOGEUSDT", interval="15m", lookback="4d")
    df = data_fetcher.fetch_data()
    current_price = df["close"].iloc[-1]

    draw_plot(df=df, current_price=current_price)

def setup_analyzer(df):
    """Sets up the analyzer."""
    support_analyzer = SupportAnalyzer(df, window=20)
    resistance_analyzer = ResistanceAnalyzer(df, window=20)
    support_indices = support_analyzer.find_support_levels()
    mean_buy_zone = support_analyzer.calculate_mean_based_buy_zone(sensitivity=1)
    median_buy_zone = support_analyzer.calculate_median_based_buy_zone(iqr_multiplier=1.5)
    resistance_indices = resistance_analyzer.find_resistance_levels()
    mean_sell_zone = resistance_analyzer.calculate_mean_based_sell_zone(sensitivity=1)
    median_sell_zone = resistance_analyzer.calculate_median_based_sell_zone(iqr_multiplier=1.5)
    return support_indices, mean_buy_zone, median_buy_zone, resistance_indices, mean_sell_zone, median_sell_zone

def draw_plot(save=False, draw_supports=False, draw_resistances=False, df=None, current_price=None):
    """Draws the plot."""
    support_indices, mean_buy_zone, median_buy_zone, resistance_levels, mean_sell_zone, median_sell_zone = setup_analyzer(df)

    plotter = PricePlotter(df, candle_count=None)
    plotter.add_buy_zone_comparison(mean_buy_zone, median_buy_zone)
    if draw_supports:
        plotter.add_support_levels(support_indices)
    plotter.add_sell_zone_comparison(mean_sell_zone, median_sell_zone)
    if draw_resistances:
        plotter.add_resistance_levels(resistance_levels)
    plotter.add_current_price(current_price)
    plotter.customize_plot(
        title="Buy Zone: " +
        f"~{((mean_buy_zone[0]+median_buy_zone[0])/2):.8f} - {((mean_buy_zone[1]+median_buy_zone[1])/2):.8f}"
        + f" | Current Price: {current_price:.8f}"
    )

    plotter.show()
    if save:
        plotter.save("chart.png")

if __name__ == "__main__":
    main()
