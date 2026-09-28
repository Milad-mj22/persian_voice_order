"""
TTS با Microsoft Edge (edge-tts) - رایگان و طبیعی
"""
import asyncio
import tempfile
from pathlib import Path

from app.core.logger import logger
from app.engines.tts.base import TTSProvider, TTSResult


class EdgeTTS(TTSProvider):
    """TTS با edge-tts (صداهای Neural مایکروسافت)"""

    name = "edge_tts"

    # صداهای فارسی موجود
    VOICES = {
        "fa-IR-FaridNeural": "مرد فارسی - فرید",
        "fa-IR-DilaraNeural": "زن فارسی - دلارا",
    }

    DEFAULT_VOICE = "fa-IR-FaridNeural"

    def __init__(
        self,
        voice: str = DEFAULT_VOICE,
        rate: str = "+0%",
        volume: str = "+0%",
    ):
        """
        Args:
            voice: نام صدا
            rate: سرعت (+10% یا -10%)
            volume: صدا (+0%)
        """
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self._loop = None

    # =========================================================
    def _run_async(self, coro):
        """اجرای coroutine در event loop"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # توی نخ دیگه‌است
                return asyncio.run_coroutine_threadsafe(coro, loop).result()
            return loop.run_until_complete(coro)
        except RuntimeError:
            return asyncio.run(coro)

    # =========================================================
    def synthesize(self, text: str, **kwargs) -> TTSResult:
        """تبدیل متن به صدا"""
        if not text.strip():
            return TTSResult(audio_bytes=b"", format="mp3")

        try:
            import edge_tts
        except ImportError:
            logger.error("edge-tts نصب نیست: pip install edge-tts")
            return TTSResult(audio_bytes=b"", format="mp3")

        voice = kwargs.get("voice", self.voice)
        rate = kwargs.get("rate", self.rate)
        volume = kwargs.get("volume", self.volume)

        async def _do():
            communicate = edge_tts.Communicate(
                text=text,
                voice=voice,
                rate=rate,
                volume=volume,
            )
            buf = bytearray()
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    buf.extend(chunk["data"])
            return bytes(buf)

        try:
            audio_bytes = self._run_async(_do())
            logger.info(
                f"🔊 EdgeTTS: {len(audio_bytes)} bytes | voice={voice}"
            )
            return TTSResult(
                audio_bytes=audio_bytes,
                format="mp3",
                sample_rate=24000,
                duration=len(text) / 15.0,
            )
        except Exception as e:
            logger.exception(f"خطا در EdgeTTS: {e}")
            return TTSResult(audio_bytes=b"", format="mp3")

    # =========================================================
    def is_available(self) -> bool:
        try:
            import edge_tts  # noqa
            return True
        except ImportError:
            return False

    def get_voices(self) -> list[str]:
        return list(self.VOICES.keys())

    @classmethod
    async def list_all_voices(cls):
        """لیست همه صداهای موجود در edge-tts"""
        import edge_tts
        voices = await edge_tts.list_voices()
        return voices