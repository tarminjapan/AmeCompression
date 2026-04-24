import time

from video_compressor.gui.compression_worker import CompressionWorker
from video_compressor.progress_handler import ProgressParser


class TestParseProgress:
    def test_valid_line(self):
        line = "frame=  100 fps=25.0 q=28.0 size=  12345kB time=00:00:04.00 bitrate=25300.0kbits/s speed=1.0x"
        parser = ProgressParser(total_duration=10.0)
        parser.set_start_time(time.time() - 1.0)
        event = parser.parse_line(line)
        assert event is not None
        assert event.percent == 40.0
        assert event.fps == 25.0
        assert event.speed == 1.0
        assert event.frame == 100

    def test_zero_duration(self):
        line = "time=00:00:04.00"
        parser = ProgressParser(total_duration=0)
        result = parser.parse_line(line)
        assert result is None

    def test_no_time_match(self):
        line = "frame=  100 fps=25.0"
        parser = ProgressParser(total_duration=10.0)
        result = parser.parse_line(line)
        assert result is None

    def test_complete_line(self):
        line = "frame= 500 fps=30.0 q=25.0 size=  50000kB time=00:01:00.00 bitrate=6826.7kbits/s speed=1.5x"
        parser = ProgressParser(total_duration=120.0)
        parser.set_start_time(time.time() - 40.0)
        event = parser.parse_line(line)
        assert event is not None
        assert event.percent == 50.0
        assert event.fps == 30.0
        assert event.speed == 1.5

    def test_percent_capped_at_100(self):
        line = "time=00:02:00.00"
        parser = ProgressParser(total_duration=60.0)
        event = parser.parse_line(line)
        assert event is not None
        assert event.percent == 100.0

    def test_eta_calculation(self):
        line = "time=00:00:30.00 speed=1.0x"
        parser = ProgressParser(total_duration=60.0)
        parser.set_start_time(time.time() - 30.0)
        event = parser.parse_line(line)
        assert event is not None
        assert event.eta > 0

    def test_fractional_seconds(self):
        line = "time=00:00:05.50"
        parser = ProgressParser(total_duration=10.0)
        event = parser.parse_line(line)
        assert event is not None
        assert abs(event.current_time - 5.5) < 0.1

    def test_hours_minutes_seconds(self):
        line = "time=01:30:45.00"
        parser = ProgressParser(total_duration=7200.0)
        event = parser.parse_line(line)
        assert event is not None
        expected = 1 * 3600 + 30 * 60 + 45
        assert event.current_time == expected

    def test_no_fps(self):
        line = "time=00:00:05.00 speed=1.0x"
        parser = ProgressParser(total_duration=10.0)
        event = parser.parse_line(line)
        assert event is not None
        assert event.fps == 0.0

    def test_no_speed(self):
        line = "time=00:00:05.00 fps=25.0"
        parser = ProgressParser(total_duration=10.0)
        event = parser.parse_line(line)
        assert event is not None
        assert event.speed == 0.0


class TestCompressionWorkerInit:
    def test_initial_state(self):
        worker = CompressionWorker()
        assert worker.is_running is False

    def test_cancel_when_not_running(self):
        worker = CompressionWorker()
        worker.cancel()
        assert not worker.is_running
