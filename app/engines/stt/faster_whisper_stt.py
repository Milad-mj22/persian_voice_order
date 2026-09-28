"""
STT با faster-whisper (بهبودیافته برای فارسی)
"""
import tempfile
from pathlib import Path

import numpy as np

from app.core.logger import logger
from app.engines.stt.base import STTProvider, STTResult
from app.services.text_corrector import PersianTextCorrector


class FasterWhisperSTT(STTProvider):
    """STT با faster-whisper — بهینه‌شده برای فارسی محاوره‌ای"""

    name = "faster_whisper"

    # Prompt اولیه برای راهنمایی Whisper
    PERSIAN_PROMPT = (
        "این یک مکالمه تلفنی سفارش غذا به زبان فارسی محاوره‌ای است. "
        "کلمات رایج: سلام، میخوام، بله، آره، نه، ممنون، ببخشید، "
        "پیتزا، برگر، ساندویچ، نوشابه، دوغ، سیب‌زمینی، سالاد، "
        "منو، سفارش، قیمت، تومان، یک، دو، سه، چهار، پنج، ده، "
        "آدرس، خیابان، کوچه، پلاک، تحویل، ارسال، تلفن، موبایل، "
        "مخصوص، پپرونی، سبزیجات، پنیر، ژامبون، قارچ، فلفل."
    )

    def __init__(
        self,
        model_size: str = "medium",
        device: str = "cpu",
        compute_type: str = "int8",
    ):
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self._model = None

    # =========================================================
    def _load_model(self):
        if self._model is not None:
            return

        try:
            from faster_whisper import WhisperModel
        except ImportError:
            logger.error("faster-whisper نصب نیست: pip install faster-whisper")
            raise

        logger.info(
            f"بارگذاری faster-whisper ({self.model_size}) "
            f"device={self.device} compute={self.compute_type}..."
        )
        self._model = WhisperModel(
            self.model_size,
            device=self.device,
            compute_type=self.compute_type,
            # ⭐ دانلود مدل در پوشه پروژه (اگه خواستی)
            # download_root="./models",
        )
        logger.info("✅ faster-whisper آماده است")

    # =========================================================



    def transcribe(self, audio_input) -> STTResult:
        try:
            self._load_model()
            audio = self._prepare_audio(audio_input)

            if audio is None:
                return STTResult(text="", language="fa", confidence=0.0,
                                raw={"error": "invalid_input"})

            # ⭐ پارامترهای بهینه — بدون initial_prompt
            segments, info = self._model.transcribe(
                audio,
                language="fa",
                beam_size=1,                  # ⭐ 1 سریع‌تر (به جای 5)
                best_of=1,                    # ⭐ بدون نمونه‌برداری اضافه
                temperature=0.0,              # ⭐ قطعی
                condition_on_previous_text=False,  # ⭐ حیاتی — جلوگیری از تکرار
                compression_ratio_threshold=2.4,
                log_prob_threshold=-1.0,
                no_speech_threshold=0.6,
                # ⭐ بدون initial_prompt (باعث توهم می‌شد)
                # initial_prompt=None,
                vad_filter=False,             # ⭐ VAD خودمون داریم، لازم نیست
                word_timestamps=False,
                without_timestamps=True,      # ⭐ سریع‌تر
            )

            # ⭐ ادغام segments با فیلتر تکرار
            raw_text = " ".join(
                seg.text.strip()
                for seg in segments
                if seg.no_speech_prob < 0.6      # ⭐ حذف segment های بی‌صدا
                and seg.compression_ratio < 2.4  # ⭐ حذف تکرار
            ).strip()

            # ⭐ حذف تکرار کلمات پشت سر هم
            raw_text = self._remove_repetitions(raw_text)

            # اصلاح متن
            text = PersianTextCorrector.correct(raw_text)

            logger.info(
                f"🎯 Whisper: {text!r} "
                f"(lang={info.language}, prob={info.language_probability:.2f}, "
                f"dur={info.duration:.1f}s)"
            )

            return STTResult(
                text=text,
                language=info.language,
                confidence=info.language_probability,
                duration=info.duration,
                raw={"raw_text": raw_text},
            )

        except Exception as e:
            logger.exception(f"خطا در FasterWhisperSTT: {e}")
            return STTResult(text="", language="fa", confidence=0.0,
                            raw={"error": str(e)})


    @staticmethod
    def _remove_repetitions(text: str) -> str:
        """
        حذف تکرار پشت سر هم کلمات
        مثال: 'سلام سلام سلام پیتزا' → 'سلام پیتزا'
        """
        if not text:
            return text

        words = text.split()
        if len(words) < 3:
            return text

        result = []
        repeat_count = 1

        for i, word in enumerate(words):
            if i == 0:
                result.append(word)
                continue

            if word == words[i - 1]:
                repeat_count += 1
                if repeat_count <= 2:  # حداکثر 2 بار پشت سر هم
                    result.append(word)
            else:
                repeat_count = 1
                result.append(word)

        return " ".join(result)
    # =========================================================
    def _prepare_audio(self, audio_input) -> np.ndarray | None:
        """تبدیل ورودی به numpy float32 1D"""
        audio = None

        if isinstance(audio_input, bytes):
            if not audio_input:
                return None
            audio = np.frombuffer(audio_input, dtype=np.int16).astype(np.float32) / 32768.0

        elif isinstance(audio_input, np.ndarray):
            if audio_input.dtype == np.int16:
                audio = audio_input.astype(np.float32) / 32768.0
            elif audio_input.dtype == np.float32:
                audio = audio_input
            else:
                audio = audio_input.astype(np.float32)

        elif isinstance(audio_input, (str, Path)):
            p = Path(audio_input)
            if p.exists() and p.is_file():
                try:
                    import soundfile as sf
                    audio, sr = sf.read(str(p), dtype="float32")
                except Exception as e:
                    logger.error(f"خطا در خواندن فایل صوتی: {e}")
                    return None
            else:
                return None

        if audio is None:
            return None

        # تبدیل به 1D
        if audio.ndim == 2:
            if audio.shape[1] > 1:
                audio = audio.mean(axis=1)
            else:
                audio = audio[:, 0]
        elif audio.ndim > 2:
            audio = audio.flatten()

        audio = np.ascontiguousarray(audio, dtype=np.float32)

        # ⭐ نرمال‌سازی دامنه (بهبود دقت)
        max_val = np.abs(audio).max()
        if max_val > 0:
            # اگه خیلی ضعیفه، تقویت کن
            if max_val < 0.1:
                audio = audio * (0.5 / max_val)
                logger.debug(f"صدا تقویت شد (max={max_val:.3f})")
            # اگه کلیپینگ داره، کم کن
            elif max_val > 0.99:
                audio = audio * (0.95 / max_val)
                logger.debug("صدا کاهش یافت (کلیپینگ)")

        if len(audio) == 0:
            return None

        logger.debug(
            f"audio shape={audio.shape}, dtype={audio.dtype}, "
            f"max={audio.max():.3f}, min={audio.min():.3f}"
        )
        return audio

    # =========================================================
    def is_available(self) -> bool:
        try:
            from faster_whisper import WhisperModel  # noqa
            return True
        except ImportError:
            return False