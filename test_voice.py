"""تست کامل STT + TTS"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.models.database import init_database
from app.engines.factory import create_stt, create_tts
from app.workers.audio_recorder import AudioRecorder


def main():
    print("=" * 60)
    print("🎤 تست سیستم صوتی")
    print("=" * 60)

    init_database()

    # ساخت موتورها
    stt = create_stt()
    tts = create_tts()

    print(f"\n📥 STT: {type(stt).__name__}")
    print(f"   available: {stt.is_available()}")
    print(f"\n📤 TTS: {type(tts).__name__}")
    print(f"   available: {tts.is_available()}")

    # ---- تست TTS ----
    print("\n" + "=" * 60)
    print("🔊 تست TTS")
    print("=" * 60)
    t0 = time.time()
    result = tts.synthesize("سلام، این یک تست صوتی است")
    print(f"   زمان: {time.time()-t0:.2f}s")
    print(f"   bytes: {len(result.audio_bytes)}")
    print(f"   format: {result.format}")

    if result.audio_bytes:
        out = Path("data/test_tts.mp3")
        out.parent.mkdir(exist_ok=True)
        out.write_bytes(result.audio_bytes)
        print(f"   ✅ فایل ذخیره شد: {out}")
        print(f"   (با پلیر ویندوز پخش کن)")

    # ---- تست STT ----
    print("\n" + "=" * 60)
    print("🎤 تست ضبط و تبدیل")
    print("=" * 60)

    recorder = AudioRecorder(
        silence_threshold=0.008,
        silence_duration=1.5,
        max_duration=15.0,
    )
    print(f"دستگاه: {recorder.device}")
    print("حالا یه چیزی بگو (مثلاً: سلام یه پیتزا میخوام)")
    print("بعد از سکوت، خودکار ضبط تموم می‌شه...\n")

    audio = recorder.record_until_silence()

    if audio is None:
        print("❌ صدایی ضبط نشد")
        return

    duration = len(audio) / 16000
    print(f"✅ {duration:.1f} ثانیه ضبط شد")

    print("\n🧠 در حال تبدیل با Whisper...")
    t0 = time.time()
    result = stt.transcribe(audio)
    elapsed = time.time() - t0

    print(f"⏱️ زمان: {elapsed:.2f}s")
    print(f"📝 متن: {result.text!r}")
    print(f"🌍 زبان: {result.language}")
    print(f"🎯 دقت: {result.confidence:.2f}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()