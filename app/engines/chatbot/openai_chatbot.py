"""
چت‌بات متصل به OpenAI API (GPT)
"""
import json
from typing import Optional

from app.core.config_manager import ConfigManager
from app.core.logger import logger
from app.engines.chatbot.base import (
    ChatbotEngine, ChatContext, ChatMessage, MessageRole,
)
from app.services.product_service import get_product_service
from app.services.settings_service import get_settings_service


class OpenAIChatbot(ChatbotEngine):
    """چت‌بات با GPT-4/3.5 از OpenAI"""

    name = "openai"

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.config = ConfigManager()
        self.settings = get_settings_service()
        self.products = get_product_service()

        # API Key
        self.api_key = api_key or self.config.get_env("OPENAI_API_KEY", "")
        self.model = model or self.config.get_env("OPENAI_MODEL", "gpt-4o-mini")
        self.temperature = float(
            self.config.get_env("OPENAI_TEMPERATURE", "0.7")
        )
        self.max_tokens = int(
            self.config.get_env("OPENAI_MAX_TOKENS", "500")
        )
        base_url = self.config.get_env("OPENAI_BASE_URL", "").strip() or None

        self._client = None

        # اطلاعات
        logger.info(
            f"OpenAIChatbot آماده شد | model={self.model} | "
            f"base_url={base_url or 'default'}"
        )

    # =========================================================
    def _get_client(self):
        """ساخت کلاینت در اولین استفاده"""
        if self._client is not None:
            return self._client

        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY در .env تنظیم نشده. "
                "لطفاً کلید API رو در فایل .env قرار بده."
            )

        from openai import OpenAI

        base_url = self.config.get_env("OPENAI_BASE_URL", "").strip() or None

        self._client = OpenAI(
            api_key=self.api_key,
            base_url=base_url,
        )
        return self._client

    # =========================================================
    def is_available(self) -> bool:
        """بررسی موجود بودن"""
        if not self.api_key:
            return False
        try:
            from openai import OpenAI  # noqa
            return True
        except ImportError:
            return False

    # =========================================================
    def get_welcome_message(self, context: ChatContext) -> str:
        """پیام خوش‌آمدگویی از تنظیمات"""
        business_name = self.settings.get("business_name", "کسب‌وکار")
        template = self.settings.get(
            "welcome_message",
            "سلام، به {business_name} خوش آمدید."
        )
        return template.replace("{business_name}", business_name)

    # =========================================================
    def get_response(
        self,
        user_input: str,
        context: ChatContext,
        history: list[ChatMessage] | None = None,
    ) -> str:
        """گرفتن پاسخ از GPT"""
        try:
            client = self._get_client()

            # ساخت messages
            messages = self._build_messages(user_input, context, history)

            # فراخوانی API
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            text = response.choices[0].message.content or ""
            text = text.strip()

            logger.debug(f"OpenAI پاسخ: {text[:80]!r}...")

            # استخراج دیتا از پاسخ (اختیاری - اگر JSON خواسته بودیم)
            return text

        except Exception as e:
            logger.error(f"خطای OpenAI: {e}")
            return self._fallback_response(e)

    # =========================================================
    # ساخت System Prompt
    # =========================================================
    def _build_system_prompt(self, context: ChatContext) -> str:
        """ساخت پرامپت سیستمی پویا بر اساس تنظیمات"""
        s = self.settings.get_all()

        business_name = s.get("business_name", "کسب‌وکار")
        business_goal = s.get("business_goal", "دریافت سفارش")
        tone = int(s.get("tone", 5))
        humor = s.get("humor", "متوسط")

        # تبدیل لحن به توضیح
        tone_desc = self._tone_description(tone)

        # منو
        products = self.products.get_all(only_active=True)
        menu_text = self._format_menu(products)

        # اطلاعات شرکت
        address = s.get("address", "")
        phone = s.get("phone", "")
        delivery_area = s.get("delivery_area", "")
        payment = s.get("payment_methods", "")

        # سبد فعلی
        cart_text = "سبد خالی است."
        if context.cart:
            lines = []
            for item in context.cart:
                lines.append(
                    f"  • {item['name']} × {item['quantity']} "
                    f"= {item['price'] * item['quantity']:,} تومان"
                )
            cart_text = (
                "\n".join(lines) +
                f"\nمجموع: {context.cart_total:,} تومان"
            )

        prompt = f"""شما یک اپراتور تلفنی هوشمند برای «{business_name}» هستید.
وظیفه شما: {business_goal}

## لحن و شخصیت
{tone_desc}
میزان شوخ‌طبعی: {humor}

## قواعد مهم
1. فقط و فقط فارسی صحبت کنید.
2. پاسخ‌ها کوتاه و محاوره‌ای باشند (مثل یک اپراتور واقعی تلفنی).
3. از ایموجی استفاده نکنید (چون متن به صدا تبدیل می‌شود).
4. درخواست‌های خارج از سفارش‌گیری را مؤدبانه رد کنید.
5. اگر محصولی ناموجود بود، جایگزین پیشنهاد بدهید.
6. برای آپ‌سلا (Upsell) پیشنهاد نوشیدنی، پیش‌غذا یا دسر بدهید.
7. اگر مشتری آدرس داد، آن را تایید کنید.
8. اگر مشتری شماره جدید داد، آن را تایید کنید.

## منوی موجود
{menu_text}

## اطلاعات شرکت
- آدرس: {address or "ثبت نشده"}
- تلفن: {phone or "ثبت نشده"}
- محدوده ارسال: {delivery_area or "ثبت نشده"}
- روش پرداخت: {payment or "نقدی"}

## سبد فعلی مشتری
{cart_text}

## اطلاعات جاری مکالمه
- شماره تماس‌گیرنده: {context.caller_phone}
- آدرس مشتری: {context.address or "ثبت نشده"}
- شماره ثبت: {context.order_phone or context.caller_phone}

حالا به مشتری پاسخ بده. فقط متن پاسخ را بنویس، بدون هیچ توضیح اضافه."""

        return prompt

    def _tone_description(self, tone: int) -> str:
        """تبدیل عدد لحن به توضیح"""
        if tone <= 2:
            return "لحن شما رسمی و مؤدبانه است. از کلمات محترمانه استفاده کنید."
        if tone <= 4:
            return "لحن شما نسبتاً رسمی است، ولی کمی صمیمیت هم دارد."
        if tone <= 6:
            return "لحن شما متعادل است. نه خیلی رسمی، نه خیلی خودمانی."
        if tone <= 8:
            return "لحن شما صمیمی و دوستانه است. مثل یک دوست صحبت کنید."
        return "لحن شما کاملاً خودمانی و گرم است. با مشتری مثل یک رفیق قدیمی حرف بزنید."

    def _format_menu(self, products) -> str:
        """تبدیل لیست محصولات به متن"""
        if not products:
            return "منو خالی است."

        by_cat: dict[str, list] = {}
        for p in products:
            by_cat.setdefault(p.category, []).append(p)

        lines = []
        for cat, items in by_cat.items():
            lines.append(f"\n### {cat}")
            for p in items:
                desc = f" - {p.description}" if p.description else ""
                lines.append(f"  • {p.name} ({p.price:,} تومان){desc}")
        return "\n".join(lines)

    # =========================================================
    # ساخت Messages
    # =========================================================
    def _build_messages(
        self,
        user_input: str,
        context: ChatContext,
        history: list[ChatMessage] | None,
    ) -> list[dict]:
        """ساخت آرایه messages برای OpenAI"""
        messages = [
            {
                "role": "system",
                "content": self._build_system_prompt(context),
            }
        ]

        # اضافه کردن تاریخچه (حداکثر 20 پیام آخر)
        if history:
            recent = history[-20:]
            for msg in recent:
                role = "user" if msg.role == MessageRole.USER else "assistant"
                messages.append({
                    "role": role,
                    "content": msg.content,
                })

        # پیام فعلی کاربر
        messages.append({
            "role": "user",
            "content": user_input,
        })

        return messages

    # =========================================================
    def _fallback_response(self, error: Exception) -> str:
        """پاسخ در صورت خطا"""
        err_str = str(error).lower()

        if "api key" in err_str or "authentication" in err_str:
            return "متأسفم، مشکل فنی پیش آمده. لطفاً بعداً تماس بگیرید."
        if "rate limit" in err_str or "quota" in err_str:
            return "متأسفم، خطوط ما شلوغ است. لطفاً چند لحظه دیگر امتحان کنید."
        if "timeout" in err_str or "connection" in err_str:
            return "متأسفم، ارتباط با سرور قطع شد. لطفاً دوباره بفرمایید."
        return "متأسفم، متوجه نشدم. لطفاً دوباره بفرمایید."