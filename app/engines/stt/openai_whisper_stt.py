"""
STT با OpenAI Whisper API
"""
import io
import tempfile
from pathlib import Path

import numpy as np

from app.core.config_manager import ConfigManager
from app.core.logger import logger
from app.engines.stt.base import STTProvider, STTResult


class OpenAIWhisperSTT(STTProvider):
    """STT با OpenAI Whisper API — دقت بالا، بدون GPU"""

    name = "openai_whisper"

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "whisper-1",
        language: str = "fa",
    ):
        self.config = ConfigManager()
        self.api_key = api_key or self.config.get_env("OPENAI_API_KEY", "")
        self.model = model
        self.language = language
        self._client = None

        logger.info(f"OpenAIWhisperSTT آماده | model={self.model}")

    def _get_client(self):
        if self._client is not None:
            return self._client
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY تنظیم نشده")

        from openai import OpenAI
        base_url = self.config.get_env("OPENAI_BASE_URL", "").strip() or None
        self._client = OpenAI(api_key=self.api_key, base_url=base_url)
        return self._client

    def transcribe(self, audio_input) -> STTResult:
        try:
            client = self._get_client()

            # ساخت فایل WAV موقت
            wav_bytes = self._to_wav_bytes(audio_input)
            if not wav_bytes:
                return STTResult(text="", language="fa", confidence=0.0,
                                 raw={"error": "invalid_audio"})

            # فایل موقت (چون API فایل می‌خواد)
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                f.write(wav_bytes)
                temp_path = f.name

            try:
                with open(temp_path, "rb") as f:
                    response = client.audio.transcriptions.create(
                        model=self.model,
                        file=f,
                        language=self.language,
                        prompt=(
                            "مکالمه تلفنی سفارش غذا به فارسی محاوره‌ای. "
                            "کلمات: پیتزا، برگر، نوشابه، آدرس، سفارش، بله، نه، ممنون."
                        ),
                        response_format="text",
                    )

                # response می‌تونه str یا obj باشه
                if isinstance(response, str):
                    text = response.strip()
                else:
                    text = (getattr(response, "text", "") or "").strip()

                logger.info(f"🎯 OpenAI Whisper: {text!r}")

                return STTResult(
                    text=text,
                    language=self.language,
                    confidence=1.0,
                    raw={"text": text},
                )

            finally:
                Path(temp_path).unlink(missing_ok=True)

        except Exception as e:
            logger.exception(f"خطا در OpenAIWhisperSTT: {e}")
            return STTResult(text="", language="fa", confidence=0.0,
                             raw={"error": str(e)})

    def _to_wav_bytes(self, audio_input) -> bytes:
        """تبدیل هر ورودی به WAV bytes"""
        try:
            import soundfile as sf

            # به numpy float32 1D تبدیل کن
            if isinstance(audio_input, bytes):
                audio = np.frombuffer(audio_input, dtype=np.int16).astype(np.float32) / 32768.0
            elif isinstance(audio_input, np.ndarray):
                if audio_input.dtype == np.int16:
                    audio = audio_input.astype(np.float32) / 32768.0
                else:
                    audio = audio_input.astype(np.float32)
            elif isinstance(audio_input, (str, Path)):
                p = Path(audio_input)
                if not p.exists():
                    return b""
                audio, sr = sf.read(str(p), dtype="float32")
                # اگه sr مختلفه، برنگردون (faster-whisper می‌تونه handle کنه)
                buf = io.BytesIO()
                sf.write(buf, audio, sr, format="WAV", subtype="PCM_16")
                return buf.getvalue()
            else:
                return b""

            # flatten
            if audio.ndim == 2:
                audio = audio.mean(axis=1) if audio.shape[1] > 1 else audio[:, 0]

            # ذخیره در bytes
            buf = io.BytesIO()
            sf.write(buf, audio, 16000, format="WAV", subtype="PCM_16")
            return buf.getvalue()

        except Exception as e:
            logger.error(f"خطا در تبدیل به WAV: {e}")
            return b""

    def is_available(self) -> bool:
        if not self.api_key:
            return False
        try:
            from openai import OpenAI  # noqa
            return True
        except ImportError:
            return False