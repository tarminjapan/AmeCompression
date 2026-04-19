"""
Theme management for AmeCompression GUI.

Provides persistent dark/light/system appearance mode switching via CustomTkinter.
"""

import customtkinter as ctk

from ..utils import SettingsManager

_THEME_OPTIONS = ("dark", "light", "system")
_DEFAULT_THEME = "dark"


def get_theme_options():
    """Return the tuple of supported theme option names."""
    return _THEME_OPTIONS


def load_theme_preference():
    """Load and apply the saved theme preference, or fall back to default."""
    theme = _DEFAULT_THEME
    saved = SettingsManager.get_instance().get("theme")
    if saved and saved in _THEME_OPTIONS:
        theme = saved
    ctk.set_appearance_mode(theme)
    return theme


def save_theme_preference(theme):
    """Persist the chosen theme and apply it immediately."""
    if theme not in _THEME_OPTIONS:
        return
    ctk.set_appearance_mode(theme)
    SettingsManager.get_instance().set("theme", theme)
