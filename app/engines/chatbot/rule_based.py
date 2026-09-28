"""
چت‌بات ساده مبتنی بر قوانین (Rule-Based)
این نسخه برای MVP است و بعداً می‌توان OpenAI یا Ollama را جایگزین کرد.
"""
import re
from enum import Enum

from app.core.logger import logger
from app.engines.chatbot.base import (
    ChatbotEngine, ChatContext, ChatMessage, MessageRole,
)
from app.services.settings_service import get_settings_service
from app.services.product_service import get_product_service


class OrderStage(str, Enum):
    """مراحل ثبت سفارش"""
    WELCOME = "welcome"
    ASK_CATEGORY = "ask_category"
    ASK_PRODUCT = "ask_product"
    ASK_QUANTITY = "ask_quantity"
    ASK_MORE = "ask_more"
    ASK_DRINK = "ask_drink"
    ASK_ADDRESS = "ask_address"
    CONFIRM_PHONE = "confirm_phone"
    CONFIRM_ORDER = "confirm_order"
    DONE = "done"


# =========================================================
# الگوهای تشخیص قصد مشتری
# =========================================================
INTENT_PATTERNS = {
    "greeting": [
        r"\bسلام\b", r"\bدرود\b", r"\bخوبی\b", r"\bخوبید\b",
    ],
    "yes": [
        r"^بله$", r"^آره$", r"^بلی$", r"^درسته$", r"^درست$",
        r"^همین$", r"^اوکی$", r"^ok$", r"^okay$", r"\bبله\b",
    ],
    "no": [
        r"^نه$", r"^خیر$", r"^نخیر$", r"\bنه\b", r"\bنمیخوام\b",
    ],
    "thanks": [
        r"\bممنون\b", r"\bمرسی\b", r"\bسپاس\b", r"\bمتشکر\b",
    ],
    "bye": [
        r"\bخداحافظ\b", r"\bخدافظ\b", r"\bبدرود\b", r"\bخداحافظی\b",
    ],
    "cart_view": [
        r"\bسبد\b", r"\bچی دارم\b", r"\bسفارشم\b", r"\bچی سفارش\b",
    ],
    "total": [
        r"\bجمع\b", r"\bمجموع\b", r"\bچقد شد\b", r"\bچقدر شد\b",
        r"\bحساب\b",
    ],
    "help": [
        r"\bکمک\b", r"\bراهنما\b", r"\bچه کار میتون\b",
    ],
    "menu": [
        r"\bمنو\b", r"\bلیست غذا\b", r"\bچیا دارید\b", r"\bچی دارید\b",
    ],
}


def detect_intent(text: str) -> str | None:
    """تشخیص قصد مشتری"""
    text = text.strip().lower()
    for intent, patterns in INTENT_PATTERNS.items():
        for p in patterns:
            if re.search(p, text):
                return intent
    return None


def extract_number(text: str) -> int | None:
    """استخراج عدد از متن فارسی/انگلیسی"""
    # تبدیل اعداد فارسی/عربی به انگلیسی
    trans = str.maketrans(
        "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
        "01234567890123456789",
    )
    text = text.translate(trans)
    m = re.search(r"\d+", text)
    if m:
        return int(m.group())
    # اعداد کلمه‌ای
    word_numbers = {
        "یک": 1, "دو": 2, "سه": 3, "چهار": 4, "پنج": 5,
        "شش": 6, "هفت": 7, "هشت": 8, "نه": 9, "ده": 10,
    }
    for word, num in word_numbers.items():
        if word in text:
            return num
    return None


# =========================================================
# Chatbot Rule-Based
# =========================================================
class RuleBasedChatbot(ChatbotEngine):
    """چت‌بات مبتنی بر قوانین"""

    name = "rule_based"

    def __init__(self):
        self.settings = get_settings_service()
        self.products = get_product_service()
        logger.info("RuleBasedChatbot آماده شد")

    # =========================================================
    def is_available(self) -> bool:
        return True

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
        """تولید پاسخ بر اساس ورودی و مرحله مکالمه"""
        text = (user_input or "").strip()
        stage = context.extras.get("stage", OrderStage.WELCOME.value)
        logger.debug(f"[{stage}] user: {text!r}")

        # ---- ۱. قصدهای عمومی که همیشه پاسخ داده می‌شن ----
        intent = detect_intent(text)

        if intent == "greeting":
            return self._greeting_response(context)

        if intent == "cart_view":
            return self._cart_response(context)

        if intent == "total":
            return self._total_response(context)

        if intent == "thanks":
            return "خواهش می‌کنم، در خدمتم."

        if intent == "help":
            return self._help_response(context)

        if intent == "menu":
            return self._menu_response(context)

        if intent == "bye":
            context.extras["stage"] = OrderStage.DONE.value
            return self.settings.get(
                "goodbye_message",
                "نوش جان، منتظر تماس شما هستیم."
            )

        # ---- ۲. پاسخ بر اساس مرحله ----
        if stage == OrderStage.WELCOME.value:
            return self._stage_welcome(context, text)
        if stage == OrderStage.ASK_CATEGORY.value:
            return self._stage_ask_category(context, text)
        if stage == OrderStage.ASK_PRODUCT.value:
            return self._stage_ask_product(context, text)
        if stage == OrderStage.ASK_QUANTITY.value:
            return self._stage_ask_quantity(context, text)
        if stage == OrderStage.ASK_MORE.value:
            return self._stage_ask_more(context, text)
        if stage == OrderStage.ASK_DRINK.value:
            return self._stage_ask_drink(context, text)
        if stage == OrderStage.ASK_ADDRESS.value:
            return self._stage_ask_address(context, text)
        if stage == OrderStage.CONFIRM_PHONE.value:
            return self._stage_confirm_phone(context, text)
        if stage == OrderStage.CONFIRM_ORDER.value:
            return self._stage_confirm_order(context, text)

        # ---- ۳. Fallback ----
        return self._fallback()

    # =========================================================
    # پاسخ‌های عمومی
    # =========================================================
    def _greeting_response(self, context: ChatContext) -> str:
        business_name = self.settings.get("business_name", "کسب‌وکار")
        return f"سلام و درود! به {business_name} خوش آمدید. چه غذایی میل دارید؟"

    def _cart_response(self, context: ChatContext) -> str:
        if not context.cart:
            return "هنوز چیزی سفارش نداده‌اید."
        lines = ["🛒 سبد سفارش شما:"]
        for item in context.cart:
            lines.append(
                f"  • {item['name']} × {item['quantity']} "
                f"= {item['price'] * item['quantity']:,} تومان"
            )
        lines.append(f"\n💰 مجموع: {context.cart_total:,} تومان")
        return "\n".join(lines)

    def _total_response(self, context: ChatContext) -> str:
        if not context.cart:
            return "سبد خرید شما خالی است."
        return f"مجموع سفارش شما {context.cart_total:,} تومان است."

    def _help_response(self, context: ChatContext) -> str:
        return (
            "من می‌تونم سفارش شما رو ثبت کنم. کافیه بگید چی میل دارید. "
            "مثلاً: «یه پیتزا مخصوص میخوام»."
        )

    def _menu_response(self, context: ChatContext) -> str:
        products = self.products.get_all(only_active=True)
        if not products:
            return "متأسفانه منویی موجود نیست."
        # گروه‌بندی بر اساس دسته
        by_cat: dict[str, list] = {}
        for p in products:
            by_cat.setdefault(p.category, []).append(p)

        lines = ["📋 منوی ما:"]
        for cat, items in by_cat.items():
            lines.append(f"\n🍽 {cat}:")
            for p in items[:5]:  # حداکثر ۵ آیتم در هر دسته
                lines.append(f"   • {p.name} - {p.price:,} تومان")
        return "\n".join(lines)

    def _fallback(self) -> str:
        fallbacks = self.settings.get(
            "fallback_messages",
            ["متأسفم، متوجه نشدم. لطفاً دوباره بفرمایید."]
        )
        # انتخاب اولی برای سادگی
        return fallbacks[0] if fallbacks else "متوجه نشدم، لطفاً تکرار کنید."

    # =========================================================
    # پاسخ‌های مرحله‌ای
    # =========================================================
    def _stage_welcome(self, context: ChatContext, text: str) -> str:
        """شروع مکالمه - اولین پاسخ کاربر"""
        context.extras["stage"] = OrderStage.ASK_CATEGORY.value
        categories = self.products.get_categories()
        if categories:
            cats = "، ".join(categories[:5])
            return f"خیلی خوب! چه دسته‌ای میل دارید؟ ما {cats} داریم."
        return "چه غذایی میل دارید؟"

    def _stage_ask_category(self, context: ChatContext, text: str) -> str:
        """کاربر یک دسته گفته"""
        category = self._match_category(text)
        if category:
            context.extras["selected_category"] = category
            context.extras["stage"] = OrderStage.ASK_PRODUCT.value
            products = self.products.get_all(
                only_active=True, category=category
            )
            if not products:
                return f"متأسفانه از {category} چیزی موجود نیست. چیز دیگه‌ای میل دارید؟"
            lines = [f"از {category} ما این‌ها رو داریم:"]
            for p in products[:5]:
                lines.append(f"  • {p.name} ({p.price:,} تومان)")
            lines.append("کدوم رو میل دارید؟")
            return "\n".join(lines)

        # شاید مستقیم اسم غذا رو گفته
        product = self._match_product(text)
        if product:
            return self._add_to_cart_and_ask_quantity(context, product)

        return "متوجه نشدم کدوم دسته رو می‌خواید. لطفاً واضح‌تر بگید."

    def _stage_ask_product(self, context: ChatContext, text: str) -> str:
        """کاربر محصول رو انتخاب کرده"""
        product = self._match_product(text)
        if product:
            return self._add_to_cart_and_ask_quantity(context, product)
        return "این محصول رو پیدا نکردم. لطفاً از لیست بالا انتخاب کنید."

    def _stage_ask_quantity(self, context: ChatContext, text: str) -> str:
        """کاربر تعداد رو گفته یا گفته فقط یکی"""
        qty = extract_number(text) or 1
        last_item = context.cart[-1] if context.cart else None
        if last_item is None:
            return "سبد خالی است. لطفاً اول محصول انتخاب کنید."

        # آپدیت تعداد
        last_item["quantity"] = qty

        context.extras["stage"] = OrderStage.ASK_MORE.value
        return f"ثبت شد: {qty} عدد {last_item['name']}. چیز دیگه‌ای هم میل دارید؟"

    def _stage_ask_more(self, context: ChatContext, text: str) -> str:
        """آیا چیز دیگه‌ای می‌خواد؟"""
        intent = detect_intent(text)

        if intent == "no" or text.strip() == "":
            # نمی‌خواد → بریم سراغ آدرس
            context.extras["stage"] = OrderStage.ASK_ADDRESS.value
            return "خیلی خوب. لطفاً آدرس تحویل رو بفرمایید."

        if intent == "yes":
            context.extras["stage"] = OrderStage.ASK_CATEGORY.value
            return "چه چیزی میل دارید؟"

        # شاید مستقیم یک محصول گفته
        product = self._match_product(text)
        if product:
            return self._add_to_cart_and_ask_quantity(context, product)

        return "ببخشید، منظورتان را متوجه نشدم. چیز دیگری میل دارید؟"

    def _stage_ask_drink(self, context: ChatContext, text: str) -> str:
        """پیشنهاد نوشیدنی (Upsell)"""
        intent = detect_intent(text)
        if intent == "yes":
            # پیدا کردن نوشیدنی‌ها
            drinks = self.products.get_all(
                only_active=True, category="نوشیدنی"
            )
            if drinks:
                context.extras["stage"] = OrderStage.ASK_PRODUCT.value
                context.extras["selected_category"] = "نوشیدنی"
                names = "، ".join(d.name for d in drinks[:4])
                return f"عالیه! ما {names} داریم. کدوم رو میل دارید؟"
        # بریم سراغ آدرس
        context.extras["stage"] = OrderStage.ASK_ADDRESS.value
        return "خیلی خوب. لطفاً آدرس تحویل رو بفرمایید."

    def _stage_ask_address(self, context: ChatContext, text: str) -> str:
        """کاربر آدرس رو گفته"""
        if len(text.strip()) < 5:
            return "لطفاً آدرس کامل‌تری بفرمایید."

        context.address = text.strip()

        # مرحله بعد: تایید شماره
        if self.settings.get("ask_phone_confirmation", True):
            context.extras["stage"] = OrderStage.CONFIRM_PHONE.value
            msg = self.settings.get(
                "phone_confirm_message",
                "آیا با همین شماره‌ای که تماس گرفته‌اید ثبت شود؟"
            )
            return f"آدرس ثبت شد. {msg}"
        else:
            # بریم سراغ تایید نهایی
            context.extras["stage"] = OrderStage.CONFIRM_ORDER.value
            return self._final_confirmation(context)

    def _stage_confirm_phone(self, context: ChatContext, text: str) -> str:
        """تایید یا رد شماره تماس"""
        from app.services.phone_intent import (
            PhoneIntentDetector, PhoneIntent
        )
        from app.services.phone_validator import IranianPhoneValidator

        intent, new_phone = PhoneIntentDetector.detect(
            text, IranianPhoneValidator
        )

        if intent == PhoneIntent.CONFIRM_SAME_NUMBER:
            context.order_phone = context.caller_phone
            context.is_same_as_caller = True
            context.extras["stage"] = OrderStage.CONFIRM_ORDER.value
            return self._final_confirmation(context)

        if intent == PhoneIntent.PROVIDE_NEW_NUMBER:
            context.order_phone = new_phone
            context.is_same_as_caller = False
            context.extras["stage"] = OrderStage.CONFIRM_ORDER.value
            return self._final_confirmation(context)

        if intent == PhoneIntent.ASK_TO_PROVIDE:
            return self.settings.get(
                "ask_phone_again_message",
                "لطفاً شماره تماس را بفرمایید."
            )

        return "متوجه نشدم. لطفاً بگید «بله» برای همین شماره، یا شماره جدید بدید."

    def _stage_confirm_order(self, context: ChatContext, text: str) -> str:
        """تایید نهایی سفارش"""
        intent = detect_intent(text)
        if intent == "yes" or intent is None:
            context.extras["stage"] = OrderStage.DONE.value
            return (
                f"✅ سفارش شما ثبت شد.\n"
                f"مجموع: {context.cart_total:,} تومان\n"
                f"آدرس: {context.address}\n"
                f"موبایل: {context.order_phone or context.caller_phone}\n"
                f"ممنون از سفارش شما. خدانگهدار!"
            )
        if intent == "no":
            return "چی رو می‌خواید تغییر بدید؟"

        return "متوجه نشدم، سفارش رو تایید می‌کنید؟"

    # =========================================================
    # Helper ها
    # =========================================================
    def _add_to_cart_and_ask_quantity(
        self, context: ChatContext, product
    ) -> str:
        """افزودن محصول به سبد و پرسیدن تعداد"""
        context.add_to_cart(
            product_id=product.id,
            name=product.name,
            price=product.price,
            qty=1,
        )
        context.extras["stage"] = OrderStage.ASK_QUANTITY.value
        return (
            f"{product.name} با قیمت {product.price:,} تومان ثبت شد. "
            f"چند عدد میل دارید؟"
        )

    def _match_category(self, text: str) -> str | None:
        """پیدا کردن دسته از متن"""
        text_l = text.lower()
        for cat in self.products.get_categories():
            if cat.lower() in text_l:
                return cat
        return None

    def _match_product(self, text: str):
        """پیدا کردن محصول از متن"""
        text_l = text.lower()
        products = self.products.get_all(only_active=True)

        # ۱. تطابق دقیق
        for p in products:
            if p.name.lower() == text_l:
                return p

        # ۲. تطابق جزئی (شامل باشد)
        for p in products:
            if p.name.lower() in text_l:
                return p

        # ۳. جستجوی کلمات کلیدی
        words = set(text_l.split())
        for p in products:
            name_words = set(p.name.lower().split())
            if words & name_words:  # حداقل یک کلمه مشترک
                return p

        return None