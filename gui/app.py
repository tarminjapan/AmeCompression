"""
Main GUI application for AmeCompression using CustomTkinter.
"""

import customtkinter as ctk

from video_compressor import __version__

from .i18n import t


class App(ctk.CTk):
    """Main application window for AmeCompression GUI."""

    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 640
    MIN_WIDTH = 720
    MIN_HEIGHT = 480

    def __init__(self):
        super().__init__()

        self.title(t("app.title"))
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)

        self._configure_appearance()
        self._create_widgets()

    def _configure_appearance(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    def _create_widgets(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._create_header()
        self._create_main_area()
        self._create_status_bar()

    def _create_header(self):
        header = ctk.CTkFrame(self, corner_radius=0, height=50)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)
        header.grid_propagate(False)

        title_label = ctk.CTkLabel(
            header,
            text=t("app.title"),
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title_label.grid(row=0, column=0, padx=(16, 8), pady=10, sticky="w")

        version_label = ctk.CTkLabel(
            header,
            text=t("app.version", version=__version__),
            font=ctk.CTkFont(size=12),
            text_color="gray",
        )
        version_label.grid(row=0, column=1, padx=(0, 16), pady=10, sticky="w")

        desc_label = ctk.CTkLabel(
            header,
            text=t("app.description"),
            font=ctk.CTkFont(size=12),
        )
        desc_label.grid(row=0, column=2, padx=(0, 16), pady=10, sticky="e")

    def _create_main_area(self):
        main_frame = ctk.CTkFrame(self, corner_radius=0)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=(4, 0))
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        welcome_label = ctk.CTkLabel(
            main_frame,
            text=t("status.ready"),
            font=ctk.CTkFont(size=16),
        )
        welcome_label.grid(row=0, column=0, padx=20, pady=20)

    def _create_status_bar(self):
        status_frame = ctk.CTkFrame(self, corner_radius=0, height=28)
        status_frame.grid(row=2, column=0, sticky="ew")
        status_frame.grid_propagate(False)

        status_label = ctk.CTkLabel(
            status_frame,
            text=t("status.ready"),
            font=ctk.CTkFont(size=11),
            text_color="gray",
        )
        status_label.grid(row=0, column=0, padx=10, pady=4, sticky="w")


def run_gui():
    """Launch the AmeCompression GUI application."""
    app = App()
    app.mainloop()
