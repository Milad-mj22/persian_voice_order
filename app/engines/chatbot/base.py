"""
Interface موتور Chatbot
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class MessageRole(str, Enum):
    """نقش پیام‌دهنده"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"   # bot


@dataclass
class ChatMessage:
    """یک پیام در مکالمه"""
    role: MessageRole
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "role": self.role.value,
            "content": self.content,
        }


@dataclass
class ChatContext:
    """زمینه مکالمه"""
    session_id: str
    caller_phone: str = ""
    customer_name: str = ""
    address: str = ""
    order_phone: str = ""
    is_same_as_caller: bool = True
    cart: list[dict] = field(default_factory=list)
    extras: dict[str, Any] = field(default_factory=dict)

    @property
    def cart_total(self) -> int:
        total = 0
        for item in self.cart:
            total += item.get("price", 0) * item.get("quantity", 1)
        return total

    def add_to_cart(self, product_id: int, name: str, price: int, qty: int = 1):
        """افزودن به سبد"""
        # اگه قبلاً هست، تعداد رو زیاد کن
        for item in self.cart:
            if item["product_id"] == product_id:
                item["quantity"] += qty
                return
        self.cart.append({
            "product_id": product_id,
            "name": name,
            "price": price,
            "quantity": qty,
        })

    def clear_cart(self):
        self.cart.clear()


class ChatbotEngine(ABC):
    """کلاس پایه Chatbot"""

    name: str = "base"

    @abstractmethod
    def get_response(
        self,
        user_input: str,
        context: ChatContext,
        history: list[ChatMessage] | None = None,
    ) -> str:
        """
        تولید پاسخ بر اساس ورودی کاربر

        Args:
            user_input: پیام کاربر
            context: زمینه مکالمه (سبد، آدرس، ...)
            history: تاریخچه پیام‌ها

        Returns:
            پاسخ به صورت متن
        """
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """آیا موتور آماده است؟"""
        ...

    def get_welcome_message(self, context: ChatContext) -> str:
        """پیام خوش‌آمدگویی (قابل Override)"""
        return "سلام، چطور می‌تونم کمکتون کنم؟"

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name!r}>"