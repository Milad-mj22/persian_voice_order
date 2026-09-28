"""
اسکریپت ساخت خودکار ساختار پروژه
اجرا: python setup_structure.py
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()

# لیست پوشه‌ها
FOLDERS = [
    "app",
    "app/core",
    "app/models",
    "app/services",
    "app/engines",
    "app/engines/stt",
    "app/engines/tts",
    "app/engines/chatbot",
    "app/workers",
    "app/ui",
    "app/ui/ui_files",
    "app/ui/ui_files/dialogs",
    "app/ui/ui_generated",
    "app/ui/ui_generated/dialogs",
    "app/ui/controllers",
    "app/ui/resources",
    "app/ui/resources/fonts",
    "app/ui/resources/icons",
    "data",
    "data/recordings",
    "data/confirmations",
    "tests",
    "logs",
]

# فایل‌های __init__.py (خالی)
INIT_FILES = [
    "app",
    "app/core",
    "app/models",
    "app/services",
    "app/engines",
    "app/engines/stt",
    "app/engines/tts",
    "app/engines/chatbot",
    "app/workers",
    "app/ui",
    "app/ui/ui_generated",
    "app/ui/ui_generated/dialogs",
    "app/ui/controllers",
    "tests",
]


def create_folders():
    print("📁 ساخت پوشه‌ها...")
    for folder in FOLDERS:
        path = PROJECT_ROOT / folder
        path.mkdir(parents=True, exist_ok=True)
        print(f"   ✓ {folder}")


def create_init_files():
    print("\n📄 ساخت فایل‌های __init__.py...")
    for folder in INIT_FILES:
        init_file = PROJECT_ROOT / folder / "__init__.py"
        if not init_file.exists():
            init_file.write_text("", encoding="utf-8")
            print(f"   ✓ {folder}/__init__.py")


def main():
    print("=" * 60)
    print("🚀 ساخت ساختار پروژه")
    print(f"📂 مسیر: {PROJECT_ROOT}")
    print("=" * 60)

    create_folders()
    create_init_files()

    print("\n" + "=" * 60)
    print("✅ ساختار پروژه با موفقیت ساخته شد!")
    print("=" * 60)


if __name__ == "__main__":
    main()