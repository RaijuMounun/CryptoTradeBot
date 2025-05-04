"""
AutocompleteDropdown: CustomTkinter-based widget that filters dropdown options as user types.
"""

import customtkinter as ctk


class AutocompleteDropdown(ctk.CTkFrame):
    """
    A custom autocomplete dropdown widget using CustomTkinter.
    Filters options as user types and displays them in a dropdown menu.

    Attributes:
        entry (ctk.CTkEntry): Input field for user to type.
        dropdown (ctk.CTkOptionMenu): Option menu showing filtered results.
        all_values (list[str]): Full list of options.
    """

    def __init__(self, master, values, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.all_values = values
        self.filtered_values = values
        self.command = command

        self.entry = ctk.CTkEntry(self)
        self.entry.pack(fill="x", padx=5, pady=(5, 0))
        self.entry.bind("<KeyRelease>", self._on_key_release)

        self.dropdown = ctk.CTkOptionMenu(
            self, values=self.filtered_values, command=self._on_select)
        self.dropdown.pack(fill="x", padx=5, pady=5)

    def _on_key_release(self, event):
        _event=event or None  # To avoid errors when called directly
        query = self.entry.get().upper()
        self.filtered_values = [
            v for v in self.all_values if query in v.upper()]

        # Update dropdown menu with new filtered values
        if self.filtered_values:
            self.dropdown.configure(values=self.filtered_values)
            self.dropdown.set(self.filtered_values[0])
        else:
            self.dropdown.configure(values=["No match"])
            self.dropdown.set("No match")

    def _on_select(self, value):
        if self.command:
            self.command(value)

    def get(self):
        """Returns the currently selected value."""
        return self.dropdown.get()

    def set_values(self, new_values):
        """
        Updates the list of all values and refreshes the filtered dropdown.

        Parameters:
            new_values (list[str]): New full list of options.
        """
        self.all_values = new_values
        self._on_key_release(None)  # Refresh based on current entry
