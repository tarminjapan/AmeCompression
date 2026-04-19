"""
Theme management for AmeCompression GUI.

Provides persistent dark/light/system appearance mode switching via CustomTkinter.
"""

import json
import os
import sys
from pathlib import Path

import customtkinter as ctk

_THEME_OPTIONS = ("dark", "light", "system")
_DEFAULT_THEME = "dark"
_SETTINGS_FILENAME = "settings.json"


def _get_config_dir():
    """Return the platform-specific configuration directory."""
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home()))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "AmeCompression"


def get_theme_options():
    """Return the tuple of supported theme option names."""
    return _THEME_OPTIONS


def load_theme_preference():
    """Load and apply the saved theme preference, or fall back to default."""
    theme = _DEFAULT_THEME
    config_dir = _get_config_dir()
    settings_path = config_dir / _SETTINGS_FILENAME
    if settings_path.is_file():
        try:
            with open(settings_path, encoding="utf-8") as f:
                settings = json.load(f)
            saved = settings.get("theme")
            if saved and saved in _THEME_OPTIONS:
                theme = saved
        except (json.JSONDecodeError, OSError):
            pass
    ctk.set_appearance_mode(theme)
    return theme


def save_theme_preference(theme):
    """Persist the chosen theme and apply it immediately."""
    if theme not in _THEME_OPTIONS:
        return
    ctk.set_appearance_mode(theme)
    config_dir = _get_config_dir()
    settings_path = config_dir / _SETTINGS_FILENAME
    settings = {}
    if settings_path.is_file():
        try:
            with open(settings_path, encoding="utf-8") as f:
                settings = json.load(f)
        except (json.JSONDecodeError, OSError):
            settings = {}
    settings["theme"] = theme
    try:
        config_dir.mkdir(parents=True, exist_ok=True)
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
    except OSError:
        pass
