"""
Audio compression view placeholder.
"""

import customtkinter as ctk

from ..i18n import t
from ..theme.fonts import DEFAULT_FONT_FAMILY


class AudioView(ctk.CTkFrame):
    """Placeholder view for audio compression functionality."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._label = ctk.CTkLabel(
            self,
            text=t("nav.audio"),
            font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=18, weight="bold"),
        )
        self._label.grid(row=0, column=0)

    def refresh_texts(self):
        self._label.configure(text=t("nav.audio"))
