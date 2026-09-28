"""تست اتصال به سرور API"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

# خواندن .env
load_dotenv()


def main():
    api_key = os.environ.get("OPENAI_API_KEY", "")
    base_url = os.environ.get("OPENAI_BASE_URL", "").strip() or "https://api.openai.com/v1"
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    print("=" * 60)
    print("🔍 تشخیص اتصال به API")
    print("=" * 60)
    print(f"API Key: {api_key[:15] + '...' if api_key else '❌ تنظیم نشده'}")
    print(f"Base URL: {base_url}")
    print(f"Model: {model}")
    print("-" * 60)

    if not api_key:
        print("\n❌ OPENAI_API_KEY در .env تنظیم نشده!")
        print("   فایل .env رو باز کن و کلید رو قرار بده.")
        return

    # تست ۱: دسترسی به اینترنت عمومی
    print("\n🌐 تست ۱: دسترسی به اینترنت عمومی...")
    try:
        import urllib.request
        urllib.request.urlopen("https://www.google.com", timeout=5)
        print("   ✅ اینترنت کار می‌کنه")
    except Exception as e:
        print(f"   ❌ اینترنت کار نمی‌کنه: {e}")
        return

    # تست ۲: دسترسی به سرور API
    print(f"\n🔌 تست ۲: دسترسی به {base_url} ...")
    try:
        import urllib.request
        req = urllib.request.Request(
            base_url,
            headers={"Authorization": f"Bearer {api_key}"},
        )
        urllib.request.urlopen(req, timeout=10)
        print("   ✅ سرور پاسخ داد")
    except urllib.error.HTTPError as e:
        print(f"   ⚠️  سرور پاسخ داد با کد HTTP: {e.code}")
        if e.code == 401:
            print("   ❌ API Key اشتباهه!")
        elif e.code == 403:
            print("   ❌ دسترسی رد شد (شاید IP شما مسدوده)")
        elif e.code == 404:
            print("   ❌ Base URL اشتباهه!")
        else:
            print(f"   توضیح: {e.reason}")
    except Exception as e:
        print(f"   ❌ اتصال برقرار نشد: {e}")
        print("\n💡 راه‌حل‌های پیشنهادی:")
        print("   ۱. VPN روشن کن (اگه OpenAI مستقیم استفاده می‌کنی)")
        print("   ۲. از سرویس واسط ایرانی استفاده کن (AvalAI، Metis)")
        print("   ۳. Base URL رو چک کن")

    # تست ۳: فراخوانی واقعی
    print("\n🤖 تست ۳: فراخوانی Chat Completions...")
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=base_url)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "فقط بگو: سلام"},
            ],
            max_tokens=20,
        )
        print(f"   ✅ پاسخ: {response.choices[0].message.content}")
        print("\n🎉 همه چیز آماده است!")

    except Exception as e:
        print(f"   ❌ خطا: {type(e).__name__}: {e}")
        print("\n💡 نکات:")
        print("   - اگه Connection error گرفتی، یعنی IP شما مسدوده")
        print("   - اگه 401 گرفتی، API Key اشتباهه")
        print("   - اگه 404 گرفتی، Base URL اشتباهه")
        print("   - اگه 429 گرفتی، Rate limit یا اعتبار تموم شده")


if __name__ == "__main__":
    main()