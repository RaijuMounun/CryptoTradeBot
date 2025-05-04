"""
Module that represents the main window of the application.
"""

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from DataFetcher.symbol_provider import SymbolProvider
from gui.widgets.filtered_dropdown import AutocompleteDropdown
from DataFetcher.data_fetcher import DataFetcher


class MainWindow:
    """
    Represents the main window of the application.

    Attributes:
        root (ctk.CTk): Main ctk window.
    """

    def __init__(self, root: ctk.CTk) -> None:
        """
        ınitializes the main window.

        Args:
            root (ctk.CTk): cTk root window
        """
        self.root = root
        self.root.title("Crypto Bot Arayüzü")
        self.root.geometry("900x600")

        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Creates the main ui components.
        """
        # Başlık
        self.title_label = ctk.CTkLabel(
            self.root, text="Crypto Analyzer", font=("Segoe UI", 28))
        self.title_label.pack(pady=20)

        # Sembol listesini al
        provider = SymbolProvider()
        symbols = provider.get_symbols(quote_asset="USDT")

        # Frame for the inputs
        self.input_frame = ctk.CTkFrame(self.root)
        self.input_frame.pack(padx=10, pady=10)

        # Symbol Selection
        self.symbol_label = ctk.CTkLabel(
            self.input_frame, text="Symbol", font=("Segoe UI", 16))
        self.symbol_label.grid(row=0, column=0, pady=(10, 0))  # Label

        self.symbol_dropdown = AutocompleteDropdown(
            master=self.input_frame,
            values=symbols,
            command=self.on_symbol_selected,
            width=300,
            height=35
        )
        self.symbol_dropdown.grid(row=1, column=0, pady=(0, 10))  # Dropdown

        # Interval Dropdown
        self.interval_label = ctk.CTkLabel(
            self.input_frame, text="Interval", font=("Segoe UI", 16))
        self.interval_label.grid(row=0, column=1, pady=(10, 0))  # Label

        self.interval_dropdown = ctk.CTkOptionMenu(
            self.input_frame, values=["1m", "5m", "15m", "1h", "4h", "1d"])
        self.interval_dropdown.set("15m")  # Varsayılan
        self.interval_dropdown.grid(row=1, column=1, pady=(0, 10))  # Dropdown

        # Lookback Girdisi
        self.lookback_label = ctk.CTkLabel(
            self.input_frame, text="Lookback Time", font=("Segoe UI", 16))
        self.lookback_label.grid(row=0, column=2, pady=(10, 0))  # Label

        self.lookback_entry = ctk.CTkEntry(
            self.input_frame, placeholder_text="Lookback süresi (örn: 14d)")
        self.lookback_entry.insert(0, "14d")  # Varsayılan
        self.lookback_entry.grid(row=1, column=2, pady=(0, 10))  # Entry

        # Candle Count Girdisi
        self.candle_count_label = ctk.CTkLabel(
            self.input_frame, text="Candle Count", font=("Segoe UI", 16))
        self.candle_count_label.grid(row=0, column=3, pady=(10, 0))  # Label

        self.candle_count_entry = ctk.CTkEntry(
            self.input_frame, placeholder_text="Görüntülenecek mum sayısı")
        self.candle_count_entry.insert(0, "200")  # Varsayılan
        self.candle_count_entry.grid(row=1, column=3, pady=(0, 10))  # Entry

        # Bilgi / Uyarı Mesajı
        self.message_label = ctk.CTkLabel(
            self.root, text="", text_color="orange", font=("Segoe UI", 14))
        self.message_label.pack(pady=(0, 10))

        # Analizi Başlat Butonu
        self.start_button = ctk.CTkButton(
            self.root, text="Analyze", command=self.on_start)
        self.start_button.pack(pady=10)

        # Çıkış Butonu
        self.quit_button = ctk.CTkButton(
            self.root, text="Exit", command=self.root.quit, fg_color="red")
        self.quit_button.pack(pady=10)

        # Plot Frame
        self.plot_frame = ctk.CTkFrame(self.root)
        self.plot_frame.pack(padx=10, pady=10, fill="both", expand=True)

    def on_start(self) -> None:
        """
        Method that will be executed when the 'Start Analysis' button is clicked.
        """
        from main import draw_plot

        symbol = self.symbol_dropdown.get().strip()
        interval = self.interval_dropdown.get()
        lookback = self.lookback_entry.get().strip()
        candle_count = self.candle_count_entry.get().strip()

        data_fetcher = DataFetcher(
            symbol=symbol,
            interval=interval,
            lookback=lookback
        )
        df = data_fetcher.fetch_data()
        current_price = df["close"].iloc[-1]

        # Yeni bir plot çizmeden önce eski canvas'ı temizleyin
        for widget in self.plot_frame.winfo_children():
            widget.destroy()  # Frame içindeki eski widget'ları kaldır

        draw_plot(
            df=df,
            current_price=current_price,
            draw_supports=True,
            draw_resistances=True,
            _candle_count=int(candle_count) if candle_count.isdigit() else 200,
            plot_frame=self.plot_frame,
            pair=symbol,
        )

        if not symbol:
            self.message_label.configure(
                text="⚠️ Please enter a symbol.", text_color="orange")
        else:
            self.message_label.configure(
                text=f"✅ 'Analyze started for {symbol}'.", text_color="green")
            print(f"Analyze starting: {symbol}")
            # Burada ilgili analiz fonksiyonu çağrılabilir

    def run(self) -> None:
        """
        Starts the main loop.
        """
        self.root.mainloop()

    def on_symbol_selected(self, selected_symbol):
        """Callback for when the user selects a symbol."""
        print(f"Seçilen sembol: {selected_symbol}")
        # Buradan DataFetcher gibi sınıflara bu sembol gönderilebilir.
