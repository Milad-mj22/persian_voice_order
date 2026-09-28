"""
اعتبارسنجی شماره تلفن ایرانی
"""
import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class PhoneValidationResult:
    """نتیجه اعتبارسنجی شماره"""
    valid: bool
    normalized: Optional[str] = None
    error: Optional[str] = None


class IranianPhoneValidator:
    """اعتبارسنجی شماره‌های موبایل ایرانی"""

    # اعداد فارسی، عربی و انگلیسی
    PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
    ARABIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"
    ENGLISH_DIGITS = "0123456789"

    # الگوهای قابل قبول
    PATTERNS = [
        r"^09\d{9}$",        # 09123456789
        r"^9\d{9}$",         # 9123456789
        r"^\+989\d{9}$",     # +989123456789
        r"^00989\d{9}$",     # 00989123456789
        r"^989\d{9}$",       # 989123456789
    ]

    @classmethod
    def normalize_digits(cls, text: str) -> str:
        """تبدیل اعداد فارسی/عربی به انگلیسی"""
        trans_table = str.maketrans(
            cls.PERSIAN_DIGITS + cls.ARABIC_DIGITS,
            cls.ENGLISH_DIGITS * 2,
        )
        return text.translate(trans_table)

    @classmethod
    def clean(cls, number: str) -> str:
        """پاکسازی کاراکترهای اضافی"""
        if not number:
            return ""
        # حذف فاصله، خط تیره، پرانتز و ...
        number = re.sub(r"[\s\-\(\)\._]", "", number)
        # تبدیل اعداد فارسی/عربی
        number = cls.normalize_digits(number)
        return number

    @classmethod
    def validate(cls, number: str) -> PhoneValidationResult:
        """
        اعتبارسنجی یک شماره موبایل ایرانی

        Returns:
            PhoneValidationResult با valid=True و normalized اگر معتبر بود
        """
        if not number:
            return PhoneValidationResult(
                valid=False,
                error="شماره خالی است",
            )

        # پاکسازی
        cleaned = cls.clean(number)

        if not cleaned:
            return PhoneValidationResult(
                valid=False,
                error="شماره خالی است",
            )

        # بررسی الگوها
        for pattern in cls.PATTERNS:
            if re.match(pattern, cleaned):
                # نرمال‌سازی به فرمت 09xxxxxxxxx
                normalized = cls._normalize(cleaned)
                return PhoneValidationResult(
                    valid=True,
                    normalized=normalized,
                )

        return PhoneValidationResult(
            valid=False,
            error="فرمت شماره صحیح نیست",
        )

    @classmethod
    def _normalize(cls, number: str) -> str:
        """تبدیل به فرمت استاندارد 09xxxxxxxxx"""
        if number.startswith("+98"):
            number = "0" + number[3:]
        elif number.startswith("0098"):
            number = "0" + number[4:]
        elif number.startswith("98"):
            number = "0" + number[2:]
        elif number.startswith("9") and not number.startswith("09"):
            number = "0" + number
        return number

    @classmethod
    def is_valid(cls, number: str) -> bool:
        """بررسی سریع معتبر بودن"""
        return cls.validate(number).valid

    @classmethod
    def format_pretty(cls, number: str) -> str:
        """نمایش خوانا: 0912 345 6789"""
        result = cls.validate(number)
        if not result.valid:
            return number
        n = result.normalized
        return f"{n[:4]} {n[4:7]} {n[7:]}"