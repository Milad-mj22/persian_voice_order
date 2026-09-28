#!/usr/bin/env python3
"""
اسکریپت تبدیل خودکار فایل‌های .ui به .py
اجرا: python compile_ui.py
      python compile_ui.py --force     # تبدیل اجباری همه
      python compile_ui.py --watch     # نظارت بر تغییرات
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path


# ============================================================
# تنظیمات مسیرها
# ============================================================
PROJECT_ROOT = Path(__file__).parent.resolve()
UI_FILES_DIR = PROJECT_ROOT / "app" / "ui" / "ui_files"
UI_GENERATED_DIR = PROJECT_ROOT / "app" / "ui" / "ui_generated"


# ============================================================
# پیدا کردن pyside6-uic
# ============================================================
def find_uic_command() -> str:
    """پیدا کردن دستور pyside6-uic"""
    import shutil

    # ۱. جستجو در PATH
    uic = shutil.which("pyside6-uic")
    if uic:
        return uic

    # ۲. جستجو در venv
    venv_scripts = PROJECT_ROOT / "venv" / "Scripts"
    candidates = [
        venv_scripts / "pyside6-uic.exe",
        venv_scripts / "pyside6-uic",
        venv_scripts / "pyside6-uic.bat",
    ]
    for c in candidates:
        if c.exists():
            return str(c)

    # ۳. تلاش به عنوان ماژول
    return f"{sys.executable} -m PySide6.scripts.pyside_tool uic"


# ============================================================
# تبدیل یک فایل .ui
# ============================================================
def convert_ui_to_py(ui_path: Path, out_path: Path, uic_cmd: str) -> bool:
    """تبدیل یک فایل .ui به .py"""
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # دستور تبدیل
    if " " in uic_cmd:  # اگر به صورت ماژول باشه
        parts = uic_cmd.split()
        cmd = parts + [str(ui_path), "-o", str(out_path)]
    else:
        cmd = [uic_cmd, str(ui_path), "-o", str(out_path)]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        if result.returncode != 0:
            print(f"   ❌ خطا در {ui_path.name}")
            print(f"      {result.stderr.strip()}")
            return False

        # اضافه کردن هدر به فایل تولیدشده
        if out_path.exists():
            add_header(out_path, ui_path)

        return True

    except Exception as e:
        print(f"   ❌ استثنا در {ui_path.name}: {e}")
        return False


def add_header(py_path: Path, ui_path: Path):
    """اضافه کردن هدر توضیحی به فایل تولیدشده"""
    header = (
        "# -*- coding: utf-8 -*-\n"
        "# ⚠️ این فایل به صورت خودکار تولید شده است.\n"
        f"# 📄 فایل منبع: {ui_path.relative_to(PROJECT_ROOT)}\n"
        "# 🚫 تغییرات دستی در این فایل از بین خواهند رفت.\n"
        "# 🔧 برای ویرایش، فایل .ui را در Qt Designer باز کنید.\n"
        "#\n"
        "# تولید شده توسط: compile_ui.py\n"
        "# =====================================================\n\n"
    )
    content = py_path.read_text(encoding="utf-8")
    py_path.write_text(header + content, encoding="utf-8")


# ============================================================
# بررسی نیاز به تبدیل
# ============================================================
def needs_conversion(ui_path: Path) -> bool:
    """بررسی اینکه آیا فایل .ui نیاز به تبدیل مجدد دارد"""
    rel = ui_path.relative_to(UI_FILES_DIR)
    out_path = UI_GENERATED_DIR / rel.parent / f"ui_{rel.stem}.py"

    # اگه فایل خروجی وجود نداشت
    if not out_path.exists():
        return True

    # اگه فایل .ui جدیدتر بود
    if ui_path.stat().st_mtime > out_path.stat().st_mtime:
        return True

    return False


# ============================================================
# ساخت فایل‌های __init__.py
# ============================================================
def ensure_init_files():
    """ساخت __init__.py در پوشه‌های لازم"""
    folders = [UI_GENERATED_DIR, UI_GENERATED_DIR / "dialogs"]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
        init_file = folder / "__init__.py"
        if not init_file.exists():
            init_file.write_text(
                "# فایل‌های تولیدشده از .ui\n", encoding="utf-8"
            )


# ============================================================
# فرآیند اصلی تبدیل
# ============================================================
def compile_all(force: bool = False) -> tuple[int, int]:
    """تبدیل همه فایل‌های .ui"""
    if not UI_FILES_DIR.exists():
        print(f"❌ پوشه پیدا نشد: {UI_FILES_DIR}")
        return 0, 0

    uic_cmd = find_uic_command()
    print(f"🔧 pyside6-uic: {uic_cmd}\n")

    ensure_init_files()

    ui_files = list(UI_FILES_DIR.rglob("*.ui"))

    if not ui_files:
        print("⚠️  هیچ فایل .ui پیدا نشد.")
        print(f"   مسیر جستجو: {UI_FILES_DIR}")
        return 0, 0

    print(f"📄 {len(ui_files)} فایل .ui پیدا شد.\n")

    success, failed, skipped = 0, 0, 0

    for ui_file in ui_files:
        rel = ui_file.relative_to(UI_FILES_DIR)
        out_name = f"ui_{rel.stem}.py"
        out_path = UI_GENERATED_DIR / rel.parent / out_name

        # بررسی نیاز به تبدیل
        if not force and not needs_conversion(ui_file):
            print(f"   ⏭️  {rel} (بدون تغییر)")
            skipped += 1
            continue

        print(f"   🔄 {rel} → {out_name}")
        if convert_ui_to_py(ui_file, out_path, uic_cmd):
            success += 1
        else:
            failed += 1

    return success, failed, skipped


# ============================================================
# حالت Watch
# ============================================================
def watch_mode():
    """نظارت بر تغییرات فایل‌های .ui"""
    print("👁️  حالت نظارت فعال. برای خروج Ctrl+C بزنید.\n")

    try:
        while True:
            success, failed, skipped = compile_all(force=False)
            if success > 0:
                print(f"\n✅ {success} فایل تبدیل شد.\n")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n👋 خروج از حالت نظارت.")


# ============================================================
# CLI
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="تبدیل فایل‌های .ui به .py"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="تبدیل اجباری همه فایل‌ها (نادیده گرفتن timestamp)",
    )
    parser.add_argument(
        "--watch", "-w",
        action="store_true",
        help="نظارت مداوم بر تغییرات",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("🔄 تبدیل فایل‌های .ui به .py")
    print("=" * 60)

    if args.watch:
        watch_mode()
        return

    success, failed, skipped = compile_all(force=args.force)

    print("\n" + "=" * 60)
    print(f"✅ موفق: {success}    ❌ ناموفق: {failed}    ⏭️ رد شده: {skipped}")
    print("=" * 60)

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()