"""
STT ساختگی برای تست (بدون مدل واقعی)
"""
from pathlib import Path

from app.core.logger import logger
from app.engines.stt.base import STTProvider, STTResult


class DummySTT(STTProvider):
    """
    STT ساختگی - ورودی رو به عنوان متن برمی‌گرداند.
    مفید برای تست بدون میکروفون.
    """

    name = "dummy"

    def __init__(self, fixed_text: str | None = None):
        """
        Args:
            fixed_text: اگر مقدار داشته باشد، همیشه این متن برمی‌گردد.
        """
        self.fixed_text = fixed_text

    def transcribe(self, audio_input) -> STTResult:
        if self.fixed_text:
            text = self.fixed_text
        elif isinstance(audio_input, str):
            # اگر متن مستقیم داده شده (برای تست)
            text = audio_input
        elif isinstance(audio_input, bytes):
            # تلاش برای decode
            try:
                text = audio_input.decode("utf-8")
            except UnicodeDecodeError:
                text = "[صدای نامفهوم]"
        else:
            text = "[ورودی ناشناخته]"

        logger.debug(f"DummySTT: {text!r}")
        return STTResult(
            text=text,
            language="fa",
            confidence=1.0,
            duration=0.0,
        )

    def is_available(self) -> bool:
        return True