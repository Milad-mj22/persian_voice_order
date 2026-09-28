"""
نقطه ورود برنامه - مرحله ۳
"""
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def ensure_ui_compiled():
    """اطمینان از تبدیل خودکار .ui"""
    ui_dir = PROJECT_ROOT / "app" / "ui" / "ui_files"
    py_dir = PROJECT_ROOT / "app" / "ui" / "ui_generated"
    if not ui_dir.exists():
        return
    need_compile = False
    if not py_dir.exists():
        need_compile = True
    else:
        for ui_file in ui_dir.rglob("*.ui"):
            rel = ui_file.relative_to(ui_dir)
            py_file = py_dir / rel.parent / f"ui_{rel.stem}.py"
            if not py_file.exists() or ui_file.stat().st_mtime > py_file.stat().st_mtime:
                need_compile = True
                break
    if need_compile:
        print("🔄 تبدیل فایل‌های .ui ...")
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "compile_ui.py")],
            cwd=PROJECT_ROOT,
        )
        if result.returncode != 0:
            sys.exit(1)


ensure_ui_compiled()


from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase, QFont

from app.core.config_manager import ConfigManager
from app.core.logger import logger
from app.ui.controllers.main_controller import MainController


def load_stylesheet(app: QApplication):
    """بارگذاری استایل QSS"""
    qss_file = PROJECT_ROOT / "app" / "ui" / "resources" / "styles.qss"
    if qss_file.exists():
        with open(qss_file, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
        logger.info("استایل QSS بارگذاری شد")
    else:
        logger.warning(f"فایل QSS پیدا نشد: {qss_file}")


def load_fonts():
    """بارگذاری فونت‌های سفارشی"""
    fonts_dir = PROJECT_ROOT / "app" / "ui" / "resources" / "fonts"
    if not fonts_dir.exists():
        logger.info("پوشه فونت پیدا نشد (اختیاری)")
        return

    loaded = 0
    for font_file in fonts_dir.glob("*.ttf"):
        font_id = QFontDatabase.addApplicationFont(str(font_file))
        if font_id != -1:
            families = QFontDatabase.applicationFontFamilies(font_id)
            logger.info(f"فونت بارگذاری شد: {families}")
            loaded += 1

    if loaded > 0:
        # فونت پیش‌فرض
        font = QFont("Vazirmatn", 10)
        QApplication.setFont(font)


def main():
    logger.info("=" * 50)
    logger.info("شروع برنامه - مرحله ۳")

    # ✅ راه‌اندازی دیتابیس
    from app.models.database import init_database
    init_database()


    # ⭐ اضافه کردن محصولات نمونه (فقط اگر دیتابیس خالی است)
    from app.services.product_service import get_product_service
    added = get_product_service().seed_default_products()
    if added > 0:
        logger.info(f"{added} محصول نمونه اضافه شد")




    app = QApplication(sys.argv)

    # تنظیمات RTL
    app.setLayoutDirection(Qt.RightToLeft)
    app.setApplicationName("PersianVoiceOrdering")

    # بارگذاری منابع
    load_fonts()
    load_stylesheet(app)

    # پنجره اصلی
    window = MainController()
    window.show()

    logger.info("پنجره اصلی نمایش داده شد")

    exit_code = app.exec()
    logger.info(f"خروج با کد: {exit_code}")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()