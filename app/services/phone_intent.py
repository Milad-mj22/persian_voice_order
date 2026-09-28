"""
تشخیص قصد مشتری در مورد شماره تماس
"""
from enum import Enum


class PhoneIntent(str, Enum):
    CONFIRM_SAME_NUMBER = "confirm_same"
    PROVIDE_NEW_NUMBER = "provide_new"
    ASK_TO_PROVIDE = "ask_to_provide"
    UNCLEAR = "unclear"


class PhoneIntentDetector:
    """تشخیص قصد مشتری در پاسخ به سوال تایید شماره"""

    CONFIRM_KEYWORDS = [
        "بله", "آره", "بلی", "درسته", "درست", "همین",
        "همینه", "همون", "اوکی", "yes", "ok",
    ]
    DENY_KEYWORDS = [
        "نه", "خیر", "نخیر", "دیگه", "شماره دیگه",
        "شماره دیگری", "شماره جدید", "no",
    ]

    @classmethod
    def detect(cls, text: str, validator_cls) -> tuple[PhoneIntent, str | None]:
        """
        Returns:
            (intent, normalized_phone or None)
        """
        text = (text or "").strip()

        # ۱. بررسی شماره
        result = validator_cls.validate(text)
        if result.valid:
            return PhoneIntent.PROVIDE_NEW_NUMBER, result.normalized

        # ۲. کلمات تایید
        text_l = text.lower()
        for kw in cls.CONFIRM_KEYWORDS:
            if kw in text_l:
                return PhoneIntent.CONFIRM_SAME_NUMBER, None

        # ۳. کلمات رد
        for kw in cls.DENY_KEYWORDS:
            if kw in text_l:
                return PhoneIntent.ASK_TO_PROVIDE, None

        return PhoneIntent.UNCLEAR, None