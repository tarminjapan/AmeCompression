# Video Compression Script

A Python script for video compression using FFmpeg with SVT-AV1 codec.

## Features

- **Maximum Resolution**: 4K (3840x2160)
- **Codec**: SVT-AV1 (fast AV1 codec)
- **CRF (Quality)**: Default 25 (0-63, lower = higher quality, higher = smaller file size)
- **Audio Codec**: AAC
- **Audio Bitrate**: Maximum 320kbps
- **Maximum FPS**: 120fps
- **Progress Display**: Real-time progress bar with ETA, FPS, and speed indicators

## Prerequisites

To use this script, you need the following:

### FFmpeg Installation

**Option 1: System-wide Installation**

**Windows:**

1. Download FFmpeg from the [official website](https://ffmpeg.org/download.html)
2. Extract and place it in a directory (e.g., `C:\ffmpeg`)
3. Add the FFmpeg bin directory to your system PATH (e.g., `C:\ffmpeg\bin`)
4. Verify installation: `ffmpeg -version` and `ffprobe -version`

**Or using Chocolatey:**

```powershell
choco install ffmpeg
```

**Or using winget:**

```powershell
winget install ffmpeg
```

**macOS:**

```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install ffmpeg
```

**Option 2: Local FFmpeg (Recommended for Portability)**

You can place FFmpeg executables in the same directory as the script:

- Windows: `ffmpeg.exe` and `ffprobe.exe`
- macOS/Linux: `ffmpeg` and `ffprobe`

The script will automatically detect and use local executables if they exist.

## Usage

### Basic Usage

```bash
python compress_video.py input_video.mp4
```

The output file will be automatically created as `input_video_compressed.mp4`.

### Interactive Mode (No Input File Specified)

If you run the script without specifying an input file, you will be prompted to enter the path:

```bash
python compress_video.py
```

```text
Enter the path to the video file to compress: input_video.mp4
```

> **Note**: The script automatically removes surrounding double quotes from file paths, so paths like `"C:\Videos\my video.mp4"` will work correctly.

### Specify Output File Name

```bash
python compress_video.py input_video.mp4 -o output_video.mp4
```

### Change CRF Value (Quality Adjustment)

```bash
python compress_video.py input_video.mp4 --crf 23
```

- CRF 0-23: High quality (larger file size)
- CRF 25: Default (balance between quality and size)
- CRF 26-40: Medium quality
- CRF 40-63: Low quality (smaller file size)

### Change Audio Bitrate

```bash
python compress_video.py input_video.mp4 --audio-bitrate 256k
```

### Disable Audio

```bash
python compress_video.py input_video.mp4 --no-audio
```

### Limit Resolution

```bash
python compress_video.py input_video.mp4 --resolution 1920x1080
```

### Limit FPS

```bash
python compress_video.py input_video.mp4 --fps 30
```

### All Options Combined

```bash
python compress_video.py input_video.mp4 -o output_video.mp4 --crf 23 --audio-bitrate 256k --resolution 1920x1080 --fps 60
```

## Options

| Option | Description | Default |
| - | - | - |
| `input` | Input video file path (optional, will prompt if not provided) | - |
| `-o`, `--output` | Output video file path | `{input_filename}_compressed.{extension}` |
| `--crf` | AV1 CRF value (0-63) | 25 |
| `--audio-bitrate` | Audio bitrate (max: 320k) | 192k |
| `--no-audio` | Disable audio track | Audio enabled |
| `--fps` | Maximum FPS (max: 120) | Original FPS |
| `--resolution` | Maximum resolution in WxH format (e.g., 1920x1080) | 3840x2160 |

## Help

```bash
python compress_video.py --help
```

## Feature Details

### Resolution Limit

- If the original video exceeds 4K (3840x2160), it will be scaled down while maintaining aspect ratio
- If the resolution is within limits, the original resolution is preserved
- Custom resolution limits can be set with `--resolution`

### FPS Limit

- If the original video FPS exceeds the specified maximum, it will be reduced
- Default maximum is 120fps
- If the FPS is within limits, the original FPS is preserved

### SVT-AV1 Codec

- Fast AV1 encoder developed by Intel
- 10-100x faster encoding compared to libaom-av1
- Latest video compression standard with high compression efficiency
- CRF mode encoding (quality-based variable bitrate)
- Automatic multi-threading support

### Audio Processing

- Converted to AAC format
- Maximum 320kbps bitrate
- Can be disabled with `--no-audio`

### Progress Display

During compression, a real-time progress bar is displayed showing:

- Progress percentage with visual bar
- Current time / Total time
- ETA (Estimated Time Remaining)
- Encoding FPS
- Speed multiplier
- Frame count

## Examples

### Compress 8K Video to 4K

```bash
python compress_video.py 8k_video.mp4 -o compressed_4k.mp4
```

Output: Resolution will be scaled down to 3840x2160 or below

### Compress for Web (1080p, 30fps)

```bash
python compress_video.py video.mp4 --resolution 1920x1080 --fps 30
```

### High Quality Compression

```bash
python compress_video.py video.mp4 --crf 20 --audio-bitrate 320k
```

### Small File Size Priority

```bash
python compress_video.py video.mp4 --crf 35 --audio-bitrate 128k
```

### Video Only (No Audio)

```bash
python compress_video.py video.mp4 --no-audio
```

## Notes

- AV1 encoding is CPU-intensive; high-resolution videos may take longer to process
- Press Ctrl+C during encoding to interrupt the process
- If the output file already exists, it will be overwritten (`-y` option)

## Troubleshooting

### `FFmpeg not found` Error

- Ensure FFmpeg is correctly installed
- Check that FFmpeg is included in your system PATH
- Alternatively, place `ffmpeg` and `ffprobe` executables in the script directory
- Verify by running `ffmpeg -version` in the command line

### Video Info Retrieval Error

- Verify that the input file exists
- Check if the file is corrupted
- Ensure the file is a valid video format

### Progress Bar Not Displaying

- The progress bar requires video duration information
- Some video formats may not provide duration metadata
- The compression will still complete successfully

## License

This script is free to use, modify, and distribute.
