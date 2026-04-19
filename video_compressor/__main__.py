"""
Entry point for running as module: python -m video_compressor

Supports both CLI and GUI modes:
  python -m video_compressor input.mp4          # CLI mode
  python -m video_compressor --gui               # GUI mode
"""

import sys


def main():
    if "--gui" in sys.argv:
        sys.argv.remove("--gui")
        try:
            from gui.app import run_gui

            run_gui()
        except ImportError:
            print(
                "Error: customtkinter is required for GUI mode. "
                "Install it with: pip install customtkinter"
            )
            sys.exit(1)
    else:
        from .cli import main as cli_main

        cli_main()


if __name__ == "__main__":
    main()
