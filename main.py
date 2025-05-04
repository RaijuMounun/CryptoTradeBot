"""Main module for bot."""
import customtkinter as ctk
from Plotting.plotter import PricePlotter
from Analyze.support_analyzer import SupportAnalyzer
from Analyze.resistance_analyzer import ResistanceAnalyzer
from gui.main_window import MainWindow


def main():
    """Main function to run the bot."""
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    app = MainWindow(root)
    app.run()


def setup_analyzer(df):
    """Sets up the analyzer."""
    support_analyzer = SupportAnalyzer(df, window=20)
    resistance_analyzer = ResistanceAnalyzer(df, window=20)
    support_indices = support_analyzer.find_support_levels()
    # mean_buy_zone = support_analyzer.calculate_mean_based_buy_zone(sensitivity=1)
    # median_buy_zone = support_analyzer.calculate_median_based_buy_zone(iqr_multiplier=1.5)
    unified_buy_zone = support_analyzer.calculate_unified_buy_zone(
        sensitivity=1, iqr_multiplier=1.5)
    resistance_indices = resistance_analyzer.find_resistance_levels()
    mean_sell_zone = resistance_analyzer.calculate_mean_based_sell_zone(
        sensitivity=1)
    median_sell_zone = resistance_analyzer.calculate_median_based_sell_zone(
        iqr_multiplier=1.5)
    return support_indices, unified_buy_zone, resistance_indices, mean_sell_zone, median_sell_zone


def draw_plot(save=False, draw_supports=False, draw_resistances=False, df=None, current_price=None, _candle_count=None, plot_frame=None, pair=None):
    """Draws the plot."""
    support_indices, unified_buy_zone, resistance_levels, mean_sell_zone, median_sell_zone = setup_analyzer(
        df)

    plotter = PricePlotter(df, candle_count=_candle_count, plot_frame=plot_frame)
    # plotter.add_buy_zone_comparison(mean_buy_zone, median_buy_zone)  # Comment out or remove to only show unified zone
    plotter.add_unified_buy_zone(unified_buy_zone)
    if draw_supports:
        plotter.add_support_levels(support_indices)
    plotter.add_sell_zone_comparison(mean_sell_zone, median_sell_zone)
    if draw_resistances:
        plotter.add_resistance_levels(resistance_levels)
    plotter.add_current_price(current_price)
    plotter.customize_plot(pair)

    plotter.show()
    if save:
        plotter.save("chart.png")


if __name__ == "__main__":
    main()
