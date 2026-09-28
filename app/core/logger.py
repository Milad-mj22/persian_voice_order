"""
سیستم لاگ‌گیری مرکزی
"""
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.core.config_manager import ConfigManager


def setup_logger(name: str = "app") -> logging.Logger:
    """ساخت و پیکربندی Logger"""
    config = ConfigManager()

    logger = logging.getLogger(name)

    # اگه قبلاً تنظیم شده، دوباره تنظیم نکن
    if logger.handlers:
        return logger

    level_name = config.get("logging.level", "INFO")
    logger.setLevel(getattr(logging, level_name, logging.INFO))

    # فرمت
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handler 1: فایل (با چرخش)
    log_file = config.get_path("logging.file")
    log_file.parent.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=config.get("logging.max_bytes", 5 * 1024 * 1024),
        backupCount=config.get("logging.backup_count", 3),
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Handler 2: کنسول
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


# Logger آماده برای استفاده در کل پروژه
logger = setup_logger("pvorder")


if __name__ == "__main__":
    logger.info("تست لاگ‌گیری - پیام اطلاعات")
    logger.warning("تست لاگ‌گیری - هشدار")
    logger.error("تست لاگ‌گیری - خطا")