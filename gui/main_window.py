"""
Module that represents the main window of the application.
"""

import customtkinter as ctk
from DataFetcher.symbol_provider import SymbolProvider
from gui.widgets.filtered_dropdown import AutocompleteDropdown


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
            self.root, text="Crypto Bot", font=("Segoe UI", 28))
        self.title_label.pack(pady=20)

        # Sembol listesini al
        provider = SymbolProvider()
        symbols = provider.get_symbols(quote_asset="USDT")

        # Sembol Seçimi
        self.symbol_dropdown = AutocompleteDropdown(
            master=self.root,
            values=symbols,
            command=self.on_symbol_selected,
            width=300,
            height=35
        )
        self.symbol_dropdown.pack(padx=10, pady=10)

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

    def on_start(self) -> None:
        """
        Method that will be executed when the 'Start Analysis' button is clicked.
        """
        symbol = self.symbol_dropdown.get().strip()

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
