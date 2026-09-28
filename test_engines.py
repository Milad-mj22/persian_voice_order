"""تست موتورهای AI"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.models.database import init_database
from app.engines.factory import create_stt, create_tts, create_chatbot
from app.engines.chatbot.base import ChatContext


def main():
    print("=" * 60)
    print("🧪 تست موتورهای AI")
    print("=" * 60)

    init_database()

    # ---- ساخت موتورها ----
    stt = create_stt()
    tts = create_tts()
    bot = create_chatbot()

    print(f"\n📥 STT: {stt}")
    print(f"   available: {stt.is_available()}")

    print(f"\n📤 TTS: {tts}")
    print(f"   available: {tts.is_available()}")

    print(f"\n🤖 Chatbot: {bot}")
    print(f"   available: {bot.is_available()}")

    # ---- تست STT ----
    # ⚠️ نکته: STT واقعی فقط فایل صوتی می‌گیرد
    # برای تست، بگذارید پیام خالی برگرداند
    print("\n" + "=" * 60)
    print("🎤 تست STT (بدون فایل صوتی - تست امن)")
    print("=" * 60)

    # با ورودی نامعتبر → باید gracefully برگرده
    result = stt.transcribe("")  # ورودی نامعتبر
    print(f"   ورودی نامعتبر → text: {result.text!r}, "
          f"confidence: {result.confidence}")

    # اگه یک فایل صوتی تست داری، این‌طوری:
    # test_audio = Path("data/test.wav")
    # if test_audio.exists():
    #     result = stt.transcribe(test_audio)
    #     print(f"   متن: {result.text!r}")

    # ---- تست TTS ----
    print("\n" + "=" * 60)
    print("🔊 تست TTS")
    print("=" * 60)
    tts_result = tts.synthesize("سلام، به سکه طلا خوش آمدید")
    print(f"   format: {tts_result.format}")
    print(f"   bytes: {len(tts_result.audio_bytes)}")
    print(f"   duration: {tts_result.duration:.2f}s")

    # ---- تست Chatbot ----
    print("\n" + "=" * 60)
    print("🤖 تست Chatbot - شبیه‌سازی مکالمه کامل")
    print("=" * 60)

    context = ChatContext(
        session_id="test-001",
        caller_phone="09123456789",
    )
    context.extras["stage"] = "welcome"

    welcome = bot.get_welcome_message(context)
    print(f"\n🤖 بات: {welcome}")

    test_inputs = [
        "سلام",
        "پیتزا",
        "پیتزا مخصوص",
        "دو",
        "بله یک نوشیدنی هم میخوام",
        "کوکاکولا",
        "یک",
        "نه ممنون",
        "تهران، خیابان ولیعصر پلاک ۱۲۳",
        "بله",
        "بله",
    ]

    for user_msg in test_inputs:
        print(f"\n👤 کاربر: {user_msg}")
        response = bot.get_response(user_msg, context)
        print(f"🤖 بات: {response}")
        print(f"   [stage={context.extras.get('stage')}, "
              f"cart={len(context.cart)}]")

    # ---- خلاصه ----
    print("\n" + "=" * 60)
    print("📦 خلاصه سفارش")
    print("=" * 60)
    for item in context.cart:
        print(f"   • {item['name']} × {item['quantity']} = "
              f"{item['price'] * item['quantity']:,} تومان")
    print(f"   💰 مجموع: {context.cart_total:,} تومان")
    print(f"   📍 آدرس: {context.address}")
    print(f"   📞 موبایل: {context.order_phone}")

    print("\n" + "=" * 60)
    print("🎉 همه تست‌ها موفق!")
    print("=" * 60)


if __name__ == "__main__":
    main()