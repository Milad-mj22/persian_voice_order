"""تست کیفیت ضبط"""
import sys
import time
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).parent))

from app.workers.audio_recorder import AudioRecorder
from app.models.database import init_database
from app.engines.factory import create_stt


def main():
    print("=" * 60)
    print("🎤 تست کیفیت ضبط")
    print("=" * 60)

    init_database()

    recorder = AudioRecorder(
        silence_threshold=0.010,
        silence_duration=1.8,
        max_duration=20.0,
        grace_period=0.6,
        pre_buffer_seconds=0.3,
        device=1,
    )

    stt = create_stt()

    phrases = [
        "سلام سلام یه پیتزا مخصوص میخوام لطفا",
        "یه نوشابه کوکاکولا هم اضافه کن",
        "آدرسم تهران خیابان ولیعصر پلاک صد و بیست و سه",
    ]

    for i, expected in enumerate(phrases, 1):
        print(f"\n{'='*60}")
        print(f"تست {i}: «{expected}»")
        print(f"{'='*60}")
        print("🎤 بگو...")

        audio = recorder.record_until_silence()

        if audio is None:
            print("❌ ضبط نشد")
            continue

        duration = len(audio) / 16000
        rms = np.sqrt(np.mean(audio.astype(float)**2))
        maxv = np.abs(audio).max()

        print(f"⏱️  مدت: {duration:.1f}s")
        print(f"📊 RMS: {rms:.0f}  MAX: {maxv}")

        # ذخیره برای گوش دادن
        out = Path(f"data/test_{i}.wav")
        sf.write(str(out), audio, 16000, subtype="PCM_16")
        print(f"💾 ذخیره شد: {out}")
        print("   🎧 گوش کن — پیوسته‌ست؟")

        # STT
        print("🧠 در حال تبدیل...")
        t0 = time.time()
        result = stt.transcribe(audio)
        elapsed = time.time() - t0

        print(f"⏱️  STT: {elapsed:.2f}s")
        print(f"📝 نتیجه: {result.text!r}")

        if result.text.strip() == expected.strip():
            print("✅ دقیقاً مطابق!")
        else:
            print(f"📋 انتظار: {expected!r}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()