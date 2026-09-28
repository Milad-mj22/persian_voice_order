"""
پخش فایل صوتی
"""
import tempfile
from pathlib import Path

from PySide6.QtCore import QUrl, QObject, Signal
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

from app.core.logger import logger


class AudioPlayer(QObject):
    """پخش فایل صوتی با QMediaPlayer"""

    started = Signal()
    finished = Signal()
    error = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(1.0)

        self._temp_file: Path | None = None

        # اتصالات
        self.player.mediaStatusChanged.connect(self._on_status_changed)
        self.player.errorOccurred.connect(self._on_error)

        logger.info("AudioPlayer آماده شد")

    # =========================================================
    def play_bytes(self, audio_bytes: bytes, fmt: str = "mp3"):
        """پخش بایت‌های صوتی"""
        # ذخیره در فایل موقت
        self.stop()
        if self._temp_file and self._temp_file.exists():
            try:
                self._temp_file.unlink()
            except Exception:
                pass

        suffix = f".{fmt}"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
            f.write(audio_bytes)
            self._temp_file = Path(f.name)

        self.player.setSource(QUrl.fromLocalFile(str(self._temp_file)))
        self.player.play()
        logger.debug(f"پخش صدا: {len(audio_bytes)} bytes")

    def play_file(self, filepath: str | Path):
        """پخش از فایل"""
        self.stop()
        self.player.setSource(QUrl.fromLocalFile(str(filepath)))
        self.player.play()

    def stop(self):
        """توقف"""
        if self.player.playbackState() != QMediaPlayer.StoppedState:
            self.player.stop()

    def is_playing(self) -> bool:
        return self.player.playbackState() == QMediaPlayer.PlayingState

    # =========================================================
    def _on_status_changed(self, status):
        if status == QMediaPlayer.LoadingMedia:
            pass
        elif status == QMediaPlayer.LoadedMedia:
            self.started.emit()
        elif status == QMediaPlayer.EndOfMedia:
            self.finished.emit()
            self._cleanup()
        elif status == QMediaPlayer.InvalidMedia:
            self.error.emit("فایل صوتی نامعتبر")

    def _on_error(self, error, error_string):
        logger.error(f"خطای پخش: {error_string}")
        self.error.emit(error_string)

    def _cleanup(self):
        if self._temp_file and self._temp_file.exists():
            try:
                self._temp_file.unlink()
            except Exception:
                pass
            self._temp_file = None