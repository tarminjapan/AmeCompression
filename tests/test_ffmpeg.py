from backend.ffmpeg import get_ffmpeg_executables


class TestGetFfmpegExecutables:
    def test_returns_tuple(self) -> None:
        result = get_ffmpeg_executables()
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_returns_strings(self) -> None:
        ffmpeg, ffprobe = get_ffmpeg_executables()
        assert isinstance(ffmpeg, str)
        assert isinstance(ffprobe, str)

    def test_fallback_to_system(self) -> None:
        ffmpeg, ffprobe = get_ffmpeg_executables()
        assert "ffmpeg" in ffmpeg
        assert "ffprobe" in ffprobe
