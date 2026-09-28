"""
تعریف OpenAI Tools (Function Calling)
"""
import json
from typing import Any

from app.core.logger import logger
from app.engines.chatbot.base import ChatContext
from app.services.product_service import get_product_service
from app.services.phone_validator import IranianPhoneValidator


# =========================================================
# تعریف Tool ها برای OpenAI
# =========================================================
OPENAI_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_menu",
            "description": "گرفتن لیست کامل محصولات موجود. وقتی مشتری منو می‌خواد یا نمی‌دونه چی داریم، این رو صدا بزن.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "اختیاری - نام دسته‌بندی برای فیلتر (مثلاً پیتزا، نوشیدنی)",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_to_cart",
            "description": "افزودن یک محصول به سبد خرید مشتری. وقتی مشتری صریحاً یه محصول خواست، این رو صدا بزن.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "نام محصول (مثلاً 'پیتزا مخصوص')",
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "تعداد (پیش‌فرض ۱)",
                        "default": 1,
                    },
                },
                "required": ["product_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "remove_from_cart",
            "description": "حذف یک محصول از سبد یا کم کردن تعداد آن.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {"type": "string"},
                    "quantity": {
                        "type": "integer",
                        "description": "تعداد برای کم کردن (اگر خالی، کل حذف می‌شه)",
                    },
                },
                "required": ["product_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "view_cart",
            "description": "مشاهده سبد فعلی مشتری و مجموع قیمت.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "clear_cart",
            "description": "پاک کردن کل سبد خرید.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_address",
            "description": "ثبت آدرس تحویل مشتری. وقتی مشتری آدرس داد، این رو صدا بزن.",
            "parameters": {
                "type": "object",
                "properties": {
                    "address": {
                        "type": "string",
                        "description": "آدرس کامل مشتری",
                    }
                },
                "required": ["address"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_phone",
            "description": "ثبت شماره تماس برای سفارش. وقتی مشتری شماره جدید داد.",
            "parameters": {
                "type": "object",
                "properties": {
                    "phone": {"type": "string", "description": "شماره موبایل ۱۱ رقمی"}
                },
                "required": ["phone"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_customer_name",
            "description": "ثبت نام مشتری (اگر خودش گفت).",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"],
            },
        },
    },
]


# =========================================================
# اجرای Tool ها
# =========================================================
class ToolExecutor:
    """اجرای Tool ها روی ChatContext"""

    def __init__(self):
        self.products = get_product_service()

    def execute(self, tool_name: str, args: dict, context: ChatContext) -> dict:
        """
        اجرای یک tool و برگرداندن نتیجه به صورت dict
        """
        logger.info(f"🔧 اجرای tool: {tool_name}({args})")

        try:
            method = getattr(self, f"_tool_{tool_name}", None)
            if method is None:
                return {"success": False, "error": f"Tool ناشناخته: {tool_name}"}
            return method(args, context)
        except Exception as e:
            logger.exception(f"خطا در اجرای tool {tool_name}: {e}")
            return {"success": False, "error": str(e)}

    # =========================================================
    # Tool Implementations
    # =========================================================
    def _tool_get_menu(self, args: dict, context: ChatContext) -> dict:
        category = args.get("category")
        products = self.products.get_all(only_active=True, category=category)

        menu = [
            {
                "name": p.name,
                "price": p.price,
                "category": p.category,
                "description": p.description or "",
                "stock": p.stock,
            }
            for p in products
        ]

        return {
            "success": True,
            "items": menu,
            "count": len(menu),
            "categories": self.products.get_categories(),
        }

    def _tool_add_to_cart(self, args: dict, context: ChatContext) -> dict:
        product_name = args.get("product_name", "").strip()
        quantity = int(args.get("quantity", 1))

        if quantity < 1:
            quantity = 1

        # پیدا کردن محصول
        product = self._find_product(product_name)
        if product is None:
            return {
                "success": False,
                "error": f"محصول «{product_name}» پیدا نشد",
                "available_products": [
                    p.name for p in self.products.get_all(only_active=True)
                ][:10],
            }

        if product.stock <= 0:
            return {
                "success": False,
                "error": f"«{product.name}» ناموجود است",
            }

        # افزودن به سبد
        context.add_to_cart(
            product_id=product.id,
            name=product.name,
            price=product.price,
            qty=quantity,
        )

        return {
            "success": True,
            "product": product.name,
            "quantity": quantity,
            "price": product.price,
            "cart_total": context.cart_total,
            "cart_items": len(context.cart),
        }

    def _tool_remove_from_cart(self, args: dict, context: ChatContext) -> dict:
        name = args.get("product_name", "").strip().lower()
        qty = args.get("quantity")

        # پیدا کردن آیتم در سبد
        target = None
        for item in context.cart:
            if name in item["name"].lower() or item["name"].lower() in name:
                target = item
                break

        if target is None:
            return {"success": False, "error": f"«{name}» در سبد نیست"}

        if qty is None:
            # کل حذف
            context.cart.remove(target)
        else:
            target["quantity"] -= int(qty)
            if target["quantity"] <= 0:
                context.cart.remove(target)

        return {
            "success": True,
            "removed": target["name"],
            "cart_total": context.cart_total,
        }

    def _tool_view_cart(self, args: dict, context: ChatContext) -> dict:
        return {
            "success": True,
            "items": [
                {
                    "name": it["name"],
                    "quantity": it["quantity"],
                    "price": it["price"],
                    "subtotal": it["price"] * it["quantity"],
                }
                for it in context.cart
            ],
            "total": context.cart_total,
            "count": len(context.cart),
        }

    def _tool_clear_cart(self, args: dict, context: ChatContext) -> dict:
        context.clear_cart()
        return {"success": True, "message": "سبد پاک شد"}

    def _tool_set_address(self, args: dict, context: ChatContext) -> dict:
        address = args.get("address", "").strip()
        if len(address) < 5:
            return {"success": False, "error": "آدرس خیلی کوتاه است"}
        context.address = address
        return {"success": True, "address": address}

    def _tool_set_phone(self, args: dict, context: ChatContext) -> dict:
        phone = args.get("phone", "").strip()
        result = IranianPhoneValidator.validate(phone)
        if not result.valid:
            return {"success": False, "error": "شماره نامعتبر است"}
        context.order_phone = result.normalized
        context.is_same_as_caller = (
            result.normalized == context.caller_phone
        )
        return {
            "success": True,
            "phone": result.normalized,
            "is_same_as_caller": context.is_same_as_caller,
        }

    def _tool_set_customer_name(self, args: dict, context: ChatContext) -> dict:
        name = args.get("name", "").strip()
        if not name:
            return {"success": False, "error": "نام خالی است"}
        context.customer_name = name
        return {"success": True, "name": name}

    # =========================================================
    # Helper
    # =========================================================
    def _find_product(self, name: str):
        """پیدا کردن محصول با نام (تطابق دقیق یا جزئی)"""
        name_l = name.lower().strip()
        products = self.products.get_all(only_active=True)

        # ۱. تطابق دقیق
        for p in products:
            if p.name.lower() == name_l:
                return p

        # ۲. تطابق جزئی (شامل باشد)
        for p in products:
            if name_l in p.name.lower():
                return p
            if p.name.lower() in name_l:
                return p

        # ۳. کلمات مشترک
        words = set(name_l.split())
        best = None
        best_score = 0
        for p in products:
            p_words = set(p.name.lower().split())
            score = len(words & p_words)
            if score > best_score:
                best_score = score
                best = p
        if best_score > 0:
            return best

        return None