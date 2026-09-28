"""
TTS آفلاین با pyttsx3
نیازمند: pip install pyttsx3
"""
import tempfile
from pathlib import Path

from app.core.logger import logger
from app.engines.tts.base import TTSProvider, TTSResult


class Pyttsx3TTS(TTSProvider):
    """TTS آفلاین (روی ویندوز از SAPI استفاده می‌کند)"""

    name = "pyttsx3"

    def __init__(self, voice_id: str | None = None, rate: int = 150):
        self.voice_id = voice_id
        self.rate = rate
        self._engine = None

    def _get_engine(self):
        if self._engine is None:
            import pyttsx3
            self._engine = pyttsx3.init()
            self._engine.setProperty("rate", self.rate)
            if self.voice_id:
                self._engine.setProperty("voice", self.voice_id)
        return self._engine

    def synthesize(self, text: str, **kwargs) -> TTSResult:
        engine = self._get_engine()

        # ذخیره در فایل موقت
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            tmp_path = f.name

        engine.save_to_file(text, tmp_path)
        engine.runAndWait()

        audio_bytes = Path(tmp_path).read_bytes()
        Path(tmp_path).unlink(missing_ok=True)

        return TTSResult(
            audio_bytes=audio_bytes,
            format="wav",
            sample_rate=22050,
            duration=len(audio_bytes) / 44100.0,  # تخمین
        )

    def is_available(self) -> bool:
        try:
            import pyttsx3  # noqa
            return True
        except ImportError:
            return False

    def get_voices(self) -> list[str]:
        try:
            engine = self._get_engine()
            voices = engine.getProperty("voices")
            return [v.id for v in voices]
        except Exception:
            return []