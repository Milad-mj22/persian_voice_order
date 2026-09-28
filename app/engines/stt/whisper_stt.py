"""
STT با OpenAI Whisper (آفلاین)
نیازمند: pip install openai-whisper
نیازمند: ffmpeg در PATH
"""
import tempfile
from pathlib import Path

from app.core.logger import logger
from app.engines.stt.base import STTProvider, STTResult


class WhisperSTT(STTProvider):
    """STT با Whisper"""

    name = "whisper"

    def __init__(self, model_size: str = "base"):
        """
        Args:
            model_size: tiny | base | small | medium | large
        """
        self.model_size = model_size
        self._model = None

    # =========================================================
    def _load_model(self):
        """بارگذاری مدل در اولین استفاده"""
        if self._model is not None:
            return

        try:
            import whisper
        except ImportError:
            logger.error("openai-whisper نصب نیست. pip install openai-whisper")
            raise

        logger.info(f"بارگذاری مدل Whisper ({self.model_size})...")
        self._model = whisper.load_model(self.model_size)
        logger.info("مدل Whisper آماده است")

    # =========================================================
    def transcribe(self, audio_input) -> STTResult:
        """
        تبدیل صوت به متن

        پشتیبانی از:
        - Path / str که به فایل صوتی اشاره می‌کند
        - bytes که در فایل موقت ذخیره می‌شود

        ⚠️ اگر رشته ورودی، فایل موجود نباشد، خطای واضح می‌دهد.
        """
        # ---- ۱. تعیین مسیر فایل ----
        path, is_temporary = self._resolve_audio_path(audio_input)

        if path is None:
            # ورودی نامعتبر (مثلاً متن خالی یا str غیر-فایل)
            return STTResult(
                text="",
                language="fa",
                confidence=0.0,
                raw={"error": "invalid_audio_input"},
            )

        try:
            self._load_model()
            logger.debug(f"Whisper در حال پردازش: {path}")

            result = self._model.transcribe(
                str(path),
                language="fa",
                fp16=False,  # روی CPU
            )

            text = result.get("text", "").strip()
            logger.debug(f"Whisper نتیجه: {text!r}")

            return STTResult(
                text=text,
                language=result.get("language", "fa"),
                confidence=1.0,
                duration=0.0,
                raw=result,
            )

        except Exception as e:
            logger.error(f"خطا در WhisperSTT: {e}")
            return STTResult(
                text="",
                language="fa",
                confidence=0.0,
                raw={"error": str(e)},
            )

        finally:
            # پاک کردن فایل موقت
            if is_temporary and path is not None:
                try:
                    Path(path).unlink(missing_ok=True)
                except Exception:
                    pass

    # =========================================================
    def _resolve_audio_path(self, audio_input) -> tuple[str | None, bool]:
        """
        تعیین مسیر فایل صوتی از ورودی

        Returns:
            (path, is_temporary)
            path = None اگر ورودی نامعتبر باشد
        """
        # ---- حالت ۱: bytes ----
        if isinstance(audio_input, bytes):
            if len(audio_input) == 0:
                return None, False
            with tempfile.NamedTemporaryFile(
                suffix=".wav", delete=False
            ) as f:
                f.write(audio_input)
                return f.name, True

        # ---- حالت ۲: Path ----
        if isinstance(audio_input, Path):
            if audio_input.exists():
                return str(audio_input), False
            logger.warning(f"فایل صوتی پیدا نشد: {audio_input}")
            return None, False

        # ---- حالت ۳: str ----
        if isinstance(audio_input, str):
            # چک کن فایل هست یا نه
            p = Path(audio_input)
            if p.exists() and p.is_file():
                return str(p), False

            # اگه متن بود، خطای واضح بده
            logger.warning(
                f"WhisperSTT فقط فایل صوتی قبول می‌کند، ولی متن داده شد: "
                f"{audio_input[:50]!r}..."
            )
            return None, False

        return None, False

    # =========================================================
    def is_available(self) -> bool:
        try:
            import whisper  # noqa
            return True
        except ImportError:
            return False