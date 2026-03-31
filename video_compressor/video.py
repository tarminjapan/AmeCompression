"""
Video compression functionality.
"""

import subprocess
import sys
from pathlib import Path

from .config import (
    AUDIO_CODEC,
    CRF_MAX,
    CRF_MIN,
    DEFAULT_AUDIO_BITRATE,
    DEFAULT_CRF,
    MAX_AUDIO_BITRATE,
    MAX_FPS,
    VIDEO_CODEC,
    VIDEO_PRESET,
)
from .ffmpeg import get_video_info
from .progress import show_final_progress, update_progress
from .utils import calculate_scaled_resolution, format_time, parse_bitrate
from .volume import (
    analyze_volume_level,
    build_audio_filter,
    parse_volume_gain,
    validate_denoise_level,
)


def compress_video(
    input_path,
    output_path=None,
    crf=None,
    preset=None,
    audio_bitrate=None,
    audio_enabled=True,
    max_fps=None,
    resolution=None,
    volume_gain=None,
    denoise=None,
    analyze_only=False,
    ffmpeg_path="ffmpeg",
    ffprobe_path="ffprobe",
):
    """
    Compress video using FFmpeg with AV1 codec.

    Args:
        input_path (str): Input video file path
        output_path (str): Output video file path (optional)
        crf (int): AV1 CRF value (default: DEFAULT_CRF)
        preset (int): Encoding preset (default: VIDEO_PRESET)
        audio_bitrate (str): Audio bitrate (default: DEFAULT_AUDIO_BITRATE)
        audio_enabled (bool): Whether to include audio (default: True)
        max_fps (int): Maximum FPS (default: None = keep original)
        resolution (str): Custom resolution in WxH format (default: None)
        volume_gain (str): Volume gain (e.g., "2.0", "10dB", "auto", None)
        denoise (float): Denoise level 0.0-1.0 (None = disabled)
        analyze_only (bool): Only analyze volume, don't compress
        ffmpeg_path (str): Path to ffmpeg executable
        ffprobe_path (str): Path to ffprobe executable
    """
    from .config import TARGET_VOLUME_LEVEL

    # Set default values
    if crf is None:
        crf = DEFAULT_CRF
    if preset is None:
        preset = VIDEO_PRESET
    if audio_bitrate is None:
        audio_bitrate = DEFAULT_AUDIO_BITRATE
    input_path = Path(input_path)

    # Validate input file
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' does not exist.")
        sys.exit(1)

    # Set default output path
    if output_path is None:
        output_path = (
            input_path.parent / f"{input_path.stem}_compressed{input_path.suffix}"
        )
    else:
        output_path = Path(output_path)

    # Get video information
    print(f"Analyzing video: {input_path}")
    video_info = get_video_info(input_path, ffprobe_path)

    if not video_info:
        print("Error: Could not retrieve video information.")
        sys.exit(1)

    original_width = video_info["width"]
    original_height = video_info["height"]
    original_fps = video_info["fps"]
    total_duration = video_info["duration"] or 0

    print(f"Original resolution: {original_width}x{original_height}")
    if original_fps:
        print(f"Original FPS: {original_fps:.2f}")
    if total_duration:
        print(f"Duration: {format_time(total_duration)}")

    # Handle volume analysis only mode
    if analyze_only:
        print("\nAnalyzing volume level...")
        volume_info = analyze_volume_level(input_path, ffmpeg_path)

        if volume_info["mean_volume"] is not None:
            print("-" * 60)
            print("Volume Analysis Results:")
            print(f"  Mean volume: {volume_info['mean_volume']:.1f} dB")
            print(f"  Max volume:  {volume_info['max_volume']:.1f} dB")
            if volume_info["recommended_gain"] is not None:
                print(f"  Recommended gain: {volume_info['recommended_gain']:+.1f} dB")
                print(f"  Target level: {TARGET_VOLUME_LEVEL} dB")
            print("-" * 60)
        else:
            print("Error: Could not analyze volume level.")
        return

    # Parse volume gain
    volume_gain_db = None
    if volume_gain is not None:
        volume_gain_db, is_auto = parse_volume_gain(volume_gain)
        if is_auto:
            # Analyze and calculate auto gain
            print("\nAnalyzing volume level for auto gain...")
            volume_info = analyze_volume_level(input_path, ffmpeg_path)
            if volume_info["recommended_gain"] is not None:
                volume_gain_db = volume_info["recommended_gain"]
                print(f"Auto volume gain: {volume_gain_db:+.1f} dB")
                print(f"  Current mean volume: {volume_info['mean_volume']:.1f} dB")
                print(f"  Current max volume: {volume_info['max_volume']:.1f} dB")
            else:
                print("Warning: Could not analyze volume, skipping volume adjustment")

    # Validate denoise level
    denoise = validate_denoise_level(denoise)
    if denoise is not None:
        print(f"Denoise level: {denoise}")

    # Parse custom resolution if provided
    custom_max_width = None
    custom_max_height = None
    if resolution:
        try:
            res_parts = resolution.lower().split("x")
            if len(res_parts) == 2:
                custom_max_width = int(res_parts[0])
                custom_max_height = int(res_parts[1])
                print(
                    f"Custom resolution limit: {custom_max_width}x{custom_max_height}"
                )
        except ValueError:
            print(f"Warning: Invalid resolution format '{resolution}', using defaults")

    # Calculate scaled resolution if needed
    scaled_res = calculate_scaled_resolution(
        original_width, original_height, custom_max_width, custom_max_height
    )

    # Build ffmpeg command
    cmd = [ffmpeg_path, "-i", str(input_path), "-y"]  # -y to overwrite output

    # Build video filter chain
    video_filters = []

    # Add scaling filter if needed
    if scaled_res:
        scaled_width, scaled_height = scaled_res
        print(
            f"Scaling to {scaled_width}x{scaled_height} while maintaining aspect ratio"
        )
        video_filters.append(f"scale={scaled_width}:{scaled_height}")
    else:
        print("No scaling needed (resolution within limits)")

    # Add FPS filter if needed
    fps_filter = None
    if max_fps is not None and original_fps and original_fps > max_fps:
        print(f"Limiting FPS from {original_fps:.2f} to {max_fps}")
        fps_filter = f"fps={max_fps}"
        video_filters.append(fps_filter)
    elif max_fps is not None:
        print(
            f"FPS limit: {max_fps} (original: {f'{original_fps:.2f}' if original_fps else 'unknown'})"
        )

    # Apply video filters if any
    if video_filters:
        cmd.extend(["-vf", ",".join(video_filters)])

    # Video codec settings
    cmd.extend(
        [
            "-c:v",
            VIDEO_CODEC,
            "-crf",
            str(crf),
            "-b:v",
            "0",  # Disable bitrate-based encoding (CRF mode)
            "-preset",
            str(preset),
        ]
    )

    # Audio codec settings
    if audio_enabled:
        # Validate and cap audio bitrate
        bitrate_kbps = parse_bitrate(audio_bitrate)
        if bitrate_kbps > MAX_AUDIO_BITRATE:
            print(
                f"Warning: Audio bitrate capped to {MAX_AUDIO_BITRATE}k (requested: {audio_bitrate})"
            )
            audio_bitrate = f"{MAX_AUDIO_BITRATE}k"

        # Build audio filter for volume and denoise
        audio_filter = build_audio_filter(volume_gain_db, denoise)
        if audio_filter:
            cmd.extend(["-af", audio_filter])

        cmd.extend(
            [
                "-c:a",
                AUDIO_CODEC,
                "-b:a",
                audio_bitrate,
            ]
        )
        print(f"Audio: {AUDIO_CODEC} @ {audio_bitrate}")
    else:
        cmd.extend(["-an"])  # No audio
        print("Audio: Disabled")

    # Output file
    cmd.append(str(output_path))

    # Display command for reference
    print(f"\nFFmpeg command: {' '.join(cmd)}\n")
    print("Starting compression...")
    print("-" * 60)

    # Execute ffmpeg command
    process = None
    stats = {"fps_list": [], "speed_list": [], "frame_list": []}

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,  # Close stdin to prevent blocking
            encoding="utf-8",
            errors="replace",
        )

        # Display progress in real-time
        if process.stdout:
            for line in process.stdout:
                # Try to parse and display progress
                if not update_progress(line, total_duration, stats):
                    # Only show non-progress lines that are errors or important info
                    line_stripped = line.strip()
                    if line_stripped and (
                        "error" in line_stripped.lower()
                        or "warning" in line_stripped.lower()
                    ):
                        print(f"\n  {line_stripped}")

        process.wait()

        if process.returncode == 0:
            # Show 100% progress bar
            if total_duration > 0:
                show_final_progress(total_duration)
            print()  # New line after progress bar
            print("-" * 60)
            print("✓ Compression completed successfully!")
            print(f"  Output: {output_path}")

            # Get output file size
            output_size = output_path.stat().st_size / (1024 * 1024)  # MB
            input_size = input_path.stat().st_size / (1024 * 1024)  # MB
            compression_ratio = (1 - output_size / input_size) * 100

            print(f"  Input size: {input_size:.2f} MB")
            print(f"  Output size: {output_size:.2f} MB")
            print(f"  Compression: {compression_ratio:.1f}% reduction")

            # Display average statistics
            if stats["fps_list"]:
                avg_fps = sum(stats["fps_list"]) / len(stats["fps_list"])
                avg_speed = sum(stats["speed_list"]) / len(stats["speed_list"])
                total_frames = stats["frame_list"][-1] if stats["frame_list"] else 0
                print(
                    f"  Avg encoding speed: {avg_fps:.1f} fps, {avg_speed:.2f}x | Total frames: {total_frames}"
                )
        else:
            print(f"\n✗ Compression failed (return code: {process.returncode})")
            sys.exit(1)

    except FileNotFoundError:
        print(
            "Error: FFmpeg not found. Please ensure FFmpeg is installed and added to PATH."
        )
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nCompression interrupted by user.")
        if process is not None:
            process.terminate()
        sys.exit(1)
