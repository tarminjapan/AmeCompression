"""Entry point for running as module: uv run python -m video_compressor

Starts the API server for the GUI application.
"""

import argparse
import sys

from .api import create_app


def main():
    parser = argparse.ArgumentParser(description="AmeCompression API Server")
    parser.add_argument(
        "--port", type=int, default=5000, help="Port for API server (default: 5000)"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="prod",
        choices=["dev", "prod", "test"],
        help="API configuration mode (default: prod)",
    )

    args = parser.parse_args()

    try:
        app = create_app(config_name=args.config)
        print(f"Starting AmeCompression API server on port {args.port} (config: {args.config})...")
        # In production, debug should be False.
        # The GUI usually connects to 127.0.0.1.
        app.run(host="127.0.0.1", port=args.port, debug=(args.config == "dev"))
    except ImportError as e:
        print(f"Error: Required dependencies for API mode not found. {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting API server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
