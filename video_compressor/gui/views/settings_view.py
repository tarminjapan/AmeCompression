"""
Settings view placeholder.
"""

import customtkinter as ctk

from ..i18n import t


class SettingsView(ctk.CTkFrame):
    """Placeholder view for application settings."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(
            self,
            text=t("nav.settings"),
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        label.grid(row=0, column=0)
