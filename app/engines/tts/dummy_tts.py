"""
TTS ساختگی برای تست (بدون صدای واقعی)
"""
from app.core.logger import logger
from app.engines.tts.base import TTSProvider, TTSResult


class DummyTTS(TTSProvider):
    """
    TTS ساختگی - متن رو به bytes ساده تبدیل می‌کنه.
    برای تست بدون نیاز به کتابخانه صوتی.
    """

    name = "dummy"

    def synthesize(self, text: str, **kwargs) -> TTSResult:
        logger.debug(f"DummyTTS: {text!r}")
        # بایت ساده از متن (فقط برای تست)
        data = text.encode("utf-8")
        return TTSResult(
            audio_bytes=data,
            format="txt",
            sample_rate=0,
            duration=len(text) / 15.0,  # تخمین ساده
        )

    def is_available(self) -> bool:
        return True