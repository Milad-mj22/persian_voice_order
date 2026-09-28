"""
ضبط صدا از میکروفون با VAD (تشخیص سکوت)
"""
import queue
import threading
import time

import numpy as np
import sounddevice as sd

from app.core.logger import logger


class AudioRecorder:
    SAMPLE_RATE = 16000
    CHANNELS = 1
    DTYPE = "int16"
    BLOCK_SIZE = 1024  # ⭐ کم‌تر → پاسخ سریع‌تر VAD

    def __init__(
        self,
        silence_threshold: float = 0.008,   # ⭐ خیلی پایین‌تر!
        silence_duration: float = 1.8,       # ⭐ صبر بیشتر
        max_duration: float = 20.0,
        min_duration: float = 0.5,
        device: int | str | None = None,
        # ⭐ پارامترهای جدید
        grace_period: float = 0.5,           # بعد از شروع، 0.5s حرف بزنه
        pre_buffer_seconds: float = 0.3,     # ⭐ نگه‌داشتن 0.3s قبل از تشخیص
    ):
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.max_duration = max_duration
        self.min_duration = min_duration
        self.grace_period = grace_period
        self.pre_buffer_seconds = pre_buffer_seconds

        # ⭐ خوندن MIC_DEVICE از .env اگه device پاس داده نشد
        if device is None:
            try:
                from app.core.config_manager import ConfigManager
                cfg = ConfigManager()
                env_device = cfg.get_env("MIC_DEVICE", "").strip()
                if env_device:
                    if env_device.isdigit():
                        device = int(env_device)
                    else:
                        device = env_device
                    logger.info(f"دستگاه میکروفون از .env: {device}")
            except Exception as e:
                logger.warning(f"خطا در خواندن MIC_DEVICE از .env: {e}")

        self.device = device

        self._audio_queue: queue.Queue = queue.Queue()
        self._frames: list[np.ndarray] = []
        self._recording = False
        self._stop_flag = False

        self.on_volume = None
        self.on_status = None

        logger.info(
            f"AudioRecorder آماده | sr={self.SAMPLE_RATE} | "
            f"device={self.device} | silence_th={silence_threshold}"
        )
    # =========================================================
    def _audio_callback(self, indata, frames, time_info, status):
        """Callback صدا"""
        if status:
            logger.warning(f"وضعیت صدا: {status}")
        self._audio_queue.put(indata.copy())

    # =========================================================
    def record_until_silence(self) -> np.ndarray | None:
        """
        ضبط با VAD هوشمند

        ویژگی‌ها:
        - Pre-buffer: صداهای قبل از تشخیص رو نگه می‌داره
        - Grace period: بعد از شروع، تا 0.5s حرف نزنه، صبر می‌کنه
        - Silence duration: بعد از 1.8s سکوت، پایان
        """
        logger.info("🎤 شروع ضبط...")
        if self.on_status:
            self.on_status("recording")

        self._frames = []
        self._recording = True
        self._stop_flag = False

        start_time = time.time()
        last_voice_time = time.time()
        has_voice = False
        voice_started_time = None

        # ⭐ pre-buffer: نگه‌داشتن فریم‌های قبل از تشخیص صدا
        pre_buffer: list[np.ndarray] = []
        pre_buffer_max = int(
            self.pre_buffer_seconds * self.SAMPLE_RATE / self.BLOCK_SIZE
        )

        try:
            with sd.InputStream(
                samplerate=self.SAMPLE_RATE,
                channels=self.CHANNELS,
                dtype=self.DTYPE,
                blocksize=self.BLOCK_SIZE,
                device=self.device,
                latency="high",   # ⭐ جلوگیری از dropout
                callback=self._audio_callback,
            ):
                while self._recording:
                    elapsed = time.time() - start_time
                    if elapsed > self.max_duration:
                        logger.info("⏱️ حداکثر مدت ضبط")
                        break

                    if self._stop_flag:
                        logger.info("⏹️ ضبط متوقف شد")
                        break

                    try:
                        chunk = self._audio_queue.get(timeout=0.1)
                    except queue.Empty:
                        continue

                    # ⭐ محاسبه دامنه
                    audio_float = chunk.astype(np.float32) / 32768.0
                    rms = float(np.sqrt(np.mean(audio_float ** 2)))

                    if self.on_volume:
                        self.on_volume(min(rms * 10, 1.0))

                    # ⭐ VAD اصلاح‌شده
                    if rms > self.silence_threshold:
                        # صدا تشخیص داده شد
                        if not has_voice:
                            has_voice = True
                            voice_started_time = time.time()
                            logger.debug(f"🎤 صدا شروع شد (rms={rms:.4f})")

                            # ⭐ اضافه کردن pre-buffer
                            self._frames.extend(pre_buffer)
                            pre_buffer.clear()
                        elif len(pre_buffer) > 0:
                            # اگه pre_buffer هنوز داره، اضافه کن
                            self._frames.extend(pre_buffer)
                            pre_buffer.clear()

                        self._frames.append(chunk)
                        last_voice_time = time.time()

                    else:
                        # سکوت
                        if has_voice:
                            # ⭐ grace period: اگه تازه شروع شده، صبر کن
                            grace_elapsed = time.time() - voice_started_time
                            if grace_elapsed < self.grace_period:
                                # هنوز توی grace هستیم، ادامه بده
                                self._frames.append(chunk)
                                continue

                            # افزودن فریم سکوت (به عنوان context)
                            self._frames.append(chunk)

                            silence_time = time.time() - last_voice_time
                            if silence_time >= self.silence_duration:
                                logger.info(
                                    f"🔇 سکوت تشخیص داده شد ({silence_time:.1f}s)"
                                )
                                break
                        else:
                            # ⭐ هنوز صدایی نیومده، توی pre_buffer نگه دار
                            pre_buffer.append(chunk)
                            if len(pre_buffer) > pre_buffer_max:
                                pre_buffer.pop(0)

        except Exception as e:
            logger.exception(f"خطا در ضبط: {e}")
            if self.on_status:
                self.on_status("error")
            return None
        finally:
            self._recording = False
            if self.on_status:
                self.on_status("stopped")

        if not self._frames:
            logger.warning("❌ هیچ صدایی ضبط نشد")
            return None

        audio = np.concatenate(self._frames, axis=0)
        duration = len(audio) / self.SAMPLE_RATE

        if duration < self.min_duration:
            logger.warning(f"❌ ضبط خیلی کوتاه ({duration:.1f}s)")
            return None

        logger.info(f"✅ ضبط تمام شد ({duration:.1f}s, {len(self._frames)} frames)")
        return audio
    # =========================================================
    def stop(self):
        """توقف ضبط از نخ دیگر"""
        self._stop_flag = True

    # =========================================================
    @staticmethod
    def audio_to_bytes(audio: np.ndarray) -> bytes:
        """تبدیل numpy array به bytes (PCM 16-bit)"""
        return audio.tobytes()

    @staticmethod
    def list_devices():
        """لیست دستگاه‌های صوتی"""
        return sd.query_devices()

    @staticmethod
    def default_input_device():
        """دستگاه ورودی پیش‌فرض"""
        try:
            return sd.query_devices(kind="input")
        except Exception as e:
            logger.error(f"خطا در دستگاه ورودی: {e}")
            return None