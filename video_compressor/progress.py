"""
Progress bar display functionality.
"""

import re
import sys

from .config import PROGRESS_BAR_LENGTH
from .utils import format_time


def update_progress(line, total_duration, stats=None):
    """
    Parse progress from FFmpeg log and display progress bar.

    Args:
        line (str): FFmpeg output line
        total_duration (float): Total video duration in seconds
        stats (dict): Dictionary to collect statistics (fps_list, speed_list, frame_list)

    Returns:
        bool: True if progress was displayed, False otherwise
    """
    # Parse time= pattern (e.g., time=00:00:02.33 or time=N/A)
    time_match = re.search(r"time=(\d+):(\d+):(\d+\.?\d*)", line)

    if time_match and total_duration > 0:
        hours = int(time_match.group(1))
        minutes = int(time_match.group(2))
        seconds = float(time_match.group(3))
        current_time = hours * 3600 + minutes * 60 + seconds

        # Calculate progress percentage (maximum 100%)
        progress = min(100, (current_time / total_duration) * 100)

        # Extract fps
        fps_match = re.search(r"fps=\s*([\d.]+)", line)
        fps = float(fps_match.group(1)) if fps_match else 0.0

        # Extract speed
        speed_match = re.search(r"speed=\s*([\d.]+)x", line)
        speed = float(speed_match.group(1)) if speed_match else 0.0

        # Extract frame count
        frame_match = re.search(r"frame=\s*(\d+)", line)
        frame = int(frame_match.group(1)) if frame_match else 0

        # Collect statistics if stats dictionary is provided
        if stats is not None and fps > 0 and speed > 0:
            stats["fps_list"].append(fps)
            stats["speed_list"].append(speed)
            stats["frame_list"].append(frame)

        # Extract elapsed time and calculate estimated remaining time
        elapsed_match = re.search(r"elapsed=(\d+):(\d+):(\d+\.?\d*)", line)
        eta_str = "--:--"
        if elapsed_match and progress > 0:
            elapsed_hours = int(elapsed_match.group(1))
            elapsed_minutes = int(elapsed_match.group(2))
            elapsed_seconds = float(elapsed_match.group(3))
            elapsed_time = elapsed_hours * 3600 + elapsed_minutes * 60 + elapsed_seconds

            # Estimated remaining time = elapsed time * (remaining progress / current progress)
            if progress < 100:
                remaining_progress = 100 - progress
                eta_seconds = elapsed_time * (remaining_progress / progress)
                eta_str = format_time(eta_seconds)
            else:
                eta_str = "00:00.0"

        # Display progress bar
        filled = int(PROGRESS_BAR_LENGTH * progress / 100)
        bar = "█" * filled + "░" * (PROGRESS_BAR_LENGTH - filled)

        # Format current time
        current_min = int(current_time // 60)
        current_sec = current_time % 60
        total_min = int(total_duration // 60)
        total_sec = total_duration % 60

        # Update the same line (return to beginning of line with \r)
        sys.stdout.write(
            f"\r  [{bar}] {progress:5.1f}% | "
            f"{current_min:02d}:{current_sec:04.1f}/{total_min:02d}:{total_sec:04.1f} | "
            f"ETA {eta_str} | {fps:.0f} fps | {speed:.2f}x | Frame: {frame}"
        )
        sys.stdout.flush()
        return True
    return False


def show_final_progress(total_duration):
    """
    Display 100% progress bar after completion.

    Args:
        total_duration (float): Total video duration in seconds
    """
    bar = "█" * PROGRESS_BAR_LENGTH
    total_min = int(total_duration // 60)
    total_sec = total_duration % 60

    sys.stdout.write(
        f"\r  [{bar}] 100.0% | "
        f"{total_min:02d}:{total_sec:04.1f}/{total_min:02d}:{total_sec:04.1f} | "
        f"ETA 00:00.0 | -- fps | --x | Frame: --"
    )
    sys.stdout.flush()
