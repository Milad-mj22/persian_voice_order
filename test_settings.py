"""تست سرویس تنظیمات"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.models.database import init_database
from app.services.settings_service import get_settings_service


def main():
    print("=" * 60)
    print("🧪 تست Settings Service")
    print("=" * 60)

    # ۱. ساخت دیتابیس
    print("\n📦 ساخت جداول...")
    init_database()

    # ۲. ساخت سرویس
    print("\n🔧 ساخت سرویس...")
    settings = get_settings_service()

    # ۳. خواندن
    print("\n📖 خواندن تنظیمات پیش‌فرض:")
    print(f"   business_name: {settings.get('business_name')!r}")
    print(f"   tone: {settings.get('tone')!r} (type: {type(settings.get('tone')).__name__})")
    print(f"   ask_phone_confirmation: {settings.get('ask_phone_confirmation')!r}")
    print(f"   max_phone_retry: {settings.get('max_phone_retry')!r}")

    # ۴. خواندن JSON
    print("\n📖 Fallback messages (JSON):")
    fallbacks = settings.get("fallback_messages")
    for i, msg in enumerate(fallbacks, 1):
        print(f"   {i}. {msg}")

    # ۵. نوشتن
    print("\n✍️  نوشتن مقدار جدید...")
    settings.set("business_name", "پیتزا فروشی رستمی")
    settings.set("tone", 8)
    settings.set("ask_phone_confirmation", False)

    # ۶. خواندن مجدد
    print("\n✅ خواندن مجدد:")
    print(f"   business_name: {settings.get('business_name')!r}")
    print(f"   tone: {settings.get('tone')!r}")
    print(f"   ask_phone_confirmation: {settings.get('ask_phone_confirmation')!r}")

    # ۷. ذخیره گروهی
    print("\n💾 ذخیره گروهی...")
    settings.save_all({
        "business_name": "فست‌فود سکه طلا",
        "humor": "زیاد",
        "address": "تهران، خیابان ولیعصر، پلاک ۱۲۳",
    })
    print(f"   business_name: {settings.get('business_name')!r}")
    print(f"   humor: {settings.get('humor')!r}")
    print(f"   address: {settings.get('address')!r}")

    # ۸. تعداد کل
    all_settings = settings.get_all()
    print(f"\n📊 تعداد کل تنظیمات: {len(all_settings)}")

    print("\n" + "=" * 60)
    print("🎉 همه تست‌ها موفق!")
    print("=" * 60)


if __name__ == "__main__":
    main()