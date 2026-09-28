"""
سرویس تنظیمات - با کش، نوع‌داده و مقادیر پیش‌فرض
"""
import json
from typing import Any

from sqlalchemy import select

from app.core.logger import logger
from app.models.database import db
from app.models.settings import Setting


# ============================================================
# مقادیر پیش‌فرض
# ============================================================
DEFAULT_SETTINGS: dict[str, dict] = {
    # اطلاعات کسب‌وکار
    "business_name": {
        "value": "فست‌فود سکه طلا",
        "type": "str",
        "description": "نام کسب‌وکار",
    },
    "business_goal": {
        "value": "دریافت سفارش، ترغیب مشتری، آپ‌سلا",
        "type": "str",
        "description": "اهداف کلی چت‌بات",
    },
    "welcome_message": {
        "value": "سلام، به {business_name} خوش آمدید. چطور می‌توانم کمکتان کنم؟",
        "type": "str",
        "description": "پیام خوش‌آمدگویی",
    },
    "goodbye_message": {
        "value": "نوش جان، منتظر تماس شما هستیم.",
        "type": "str",
        "description": "پیام خداحافظی",
    },

    # شخصیت چت‌بات
    "tone": {
        "value": 5,
        "type": "int",
        "description": "لحن (0=رسمی، 10=صمیمی)",
    },
    "humor": {
        "value": "متوسط",
        "type": "str",
        "description": "میزان شوخ‌طبعی",
    },
    "language": {
        "value": "فارسی",
        "type": "str",
        "description": "زبان چت‌بات",
    },

    # ساعات کاری
    "open_time": {
        "value": "11:00",
        "type": "str",
        "description": "ساعت شروع کار",
    },
    "close_time": {
        "value": "23:59",
        "type": "str",
        "description": "ساعت پایان کار",
    },

    # تایید شماره تماس
    "ask_phone_confirmation": {
        "value": True,
        "type": "bool",
        "description": "پرسیدن تایید شماره",
    },
    "phone_confirm_message": {
        "value": "آیا با همین شماره‌ای که تماس گرفته‌اید ثبت شود؟",
        "type": "str",
        "description": "پیام تایید شماره",
    },
    "ask_phone_again_message": {
        "value": "لطفاً شماره تماس را بفرمایید.",
        "type": "str",
        "description": "پیام درخواست شماره جدید",
    },
    "invalid_phone_message": {
        "value": "متأسفم، شماره صحیح نیست. لطفاً دوباره شماره ۱۱ رقمی را بفرمایید.",
        "type": "str",
        "description": "پیام شماره نامعتبر",
    },
    "max_phone_retry": {
        "value": 3,
        "type": "int",
        "description": "حداکثر تلاش برای گرفتن شماره",
    },

    # اطلاعات عمومی شرکت (Knowledge Base)
    "address": {
        "value": "",
        "type": "str",
        "description": "آدرس فیزیکی",
    },
    "phone": {
        "value": "",
        "type": "str",
        "description": "شماره تماس شرکت",
    },
    "delivery_area": {
        "value": "",
        "type": "str",
        "description": "محدوده ارسال",
    },
    "working_hours": {
        "value": "",
        "type": "str",
        "description": "ساعات کاری",
    },
    "payment_methods": {
        "value": "نقدی، کارت",
        "type": "str",
        "description": "روش‌های پرداخت",
    },
    "discount_policy": {
        "value": "",
        "type": "str",
        "description": "سیاست تخفیف",
    },
    "brand_story": {
        "value": "",
        "type": "str",
        "description": "معرفی برند",
    },

    # Fallback ها (JSON)
    "fallback_messages": {
        "value": [
            "متأسفم، متوجه نشدم. لطفاً دوباره بفرمایید.",
            "می‌توانید واضح‌تر بگویید؟",
            "برای سفارش، لطفاً از منو انتخاب کنید.",
        ],
        "type": "json",
        "description": "پیام‌های Fallback",
    },
}


# ============================================================
# تبدیل نوع
# ============================================================
def _parse_value(raw: str, value_type: str) -> Any:
    """تبدیل مقدار رشته‌ای از DB به نوع اصلی"""
    if raw is None:
        return None
    try:
        if value_type == "int":
            return int(raw)
        if value_type == "float":
            return float(raw)
        if value_type == "bool":
            return raw.lower() in ("true", "1", "yes")
        if value_type == "json":
            return json.loads(raw)
        return raw
    except (ValueError, json.JSONDecodeError) as e:
        logger.error(f"خطا در تبدیل مقدار '{raw}' به {value_type}: {e}")
        return raw


def _serialize_value(value: Any, value_type: str) -> str:
    """تبدیل مقدار به رشته برای ذخیره در DB"""
    if value is None:
        return ""
    if value_type == "json":
        return json.dumps(value, ensure_ascii=False)
    if value_type == "bool":
        return "true" if value else "false"
    return str(value)


# ============================================================
# Settings Service
# ============================================================
class SettingsService:
    """سرویس تنظیمات با کش داخلی"""

    def __init__(self):
        self._cache: dict[str, Any] = {}
        self._types: dict[str, str] = {}
        self._ensure_defaults()
        self._reload_cache()
        logger.info("SettingsService آماده شد")

    # -------------------------
    # مقداردهی اولیه
    # -------------------------
    def _ensure_defaults(self):
        """اطمینان از وجود همه تنظیمات پیش‌فرض در DB"""
        with db.get_session() as session:
            existing_keys = set(
                session.scalars(select(Setting.key)).all()
            )

            added = 0
            for key, meta in DEFAULT_SETTINGS.items():
                if key not in existing_keys:
                    setting = Setting(
                        key=key,
                        value=_serialize_value(meta["value"], meta["type"]),
                        value_type=meta["type"],
                        description=meta.get("description"),
                    )
                    session.add(setting)
                    added += 1

            if added:
                session.commit()
                logger.info(f"{added} تنظیم پیش‌فرض اضافه شد")

    def _reload_cache(self):
        """بارگذاری مجدد کش از DB"""
        self._cache.clear()
        self._types.clear()

        with db.get_session() as session:
            settings = session.scalars(select(Setting)).all()
            for s in settings:
                self._cache[s.key] = _parse_value(s.value, s.value_type)
                self._types[s.key] = s.value_type

    # -------------------------
    # خواندن
    # -------------------------
    def get(self, key: str, default: Any = None) -> Any:
        """خواندن یک تنظیم"""
        if key in self._cache:
            return self._cache[key]
        # اگه در DB نبود، از پیش‌فرض‌ها
        if key in DEFAULT_SETTINGS:
            return DEFAULT_SETTINGS[key]["value"]
        return default

    def get_all(self) -> dict[str, Any]:
        """خواندن همه تنظیمات"""
        return dict(self._cache)

    def get_by_prefix(self, prefix: str) -> dict[str, Any]:
        """خواندن تنظیمات با پیشوند مشخص"""
        return {
            k: v for k, v in self._cache.items()
            if k.startswith(prefix)
        }

    # -------------------------
    # نوشتن
    # -------------------------
    def set(self, key: str, value: Any) -> bool:
        """نوشتن یک تنظیم"""
        value_type = self._types.get(
            key,
            DEFAULT_SETTINGS.get(key, {}).get("type", "str")
        )

        with db.get_session() as session:
            setting = session.scalar(
                select(Setting).where(Setting.key == key)
            )

            if setting is None:
                setting = Setting(
                    key=key,
                    value=_serialize_value(value, value_type),
                    value_type=value_type,
                )
                session.add(setting)
            else:
                setting.value = _serialize_value(value, value_type)

            session.commit()

        # آپدیت کش
        self._cache[key] = value
        self._types[key] = value_type

        logger.debug(f"تنظیم ذخیره شد: {key} = {value!r}")
        return True

    def save_all(self, data: dict[str, Any]) -> bool:
        """ذخیره گروهی تنظیمات"""
        try:
            with db.get_session() as session:
                for key, value in data.items():
                    value_type = self._types.get(
                        key,
                        DEFAULT_SETTINGS.get(key, {}).get("type", "str")
                    )

                    setting = session.scalar(
                        select(Setting).where(Setting.key == key)
                    )
                    if setting is None:
                        setting = Setting(
                            key=key,
                            value=_serialize_value(value, value_type),
                            value_type=value_type,
                        )
                        session.add(setting)
                    else:
                        setting.value = _serialize_value(value, value_type)
                        setting.value_type = value_type

                    self._cache[key] = value
                    self._types[key] = value_type

                session.commit()

            logger.info(f"{len(data)} تنظیم ذخیره شد")
            return True

        except Exception as e:
            logger.error(f"خطا در ذخیره تنظیمات: {e}")
            return False

    # -------------------------
    # بازنشانی
    # -------------------------
    def reset_to_defaults(self) -> bool:
        """بازگرداندن همه تنظیمات به پیش‌فرض"""
        try:
            with db.get_session() as session:
                # حذف همه
                session.query(Setting).delete()

                # درج مجدد پیش‌فرض‌ها
                for key, meta in DEFAULT_SETTINGS.items():
                    session.add(Setting(
                        key=key,
                        value=_serialize_value(meta["value"], meta["type"]),
                        value_type=meta["type"],
                        description=meta.get("description"),
                    ))

                session.commit()

            self._reload_cache()
            logger.info("تنظیمات به پیش‌فرض بازگشت")
            return True

        except Exception as e:
            logger.error(f"خطا در بازنشانی: {e}")
            return False

    def reload(self):
        """بارگذاری مجدد از DB"""
        self._ensure_defaults()
        self._reload_cache()


# ============================================================
# Singleton
# ============================================================
_settings_service: SettingsService | None = None


def get_settings_service() -> SettingsService:
    """گرفتن نمونه Singleton"""
    global _settings_service
    if _settings_service is None:
        _settings_service = SettingsService()
    return _settings_service