"""
مدل سفارش
"""
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    String, Text, Integer, DateTime, Boolean, BigInteger, JSON,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.database import Base


class Order(Base):
    """جدول سفارشات"""
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_code: Mapped[str] = mapped_column(
        String(20), unique=True, index=True, nullable=False
    )
    session_id: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # اطلاعات مشتری
    caller_phone: Mapped[str] = mapped_column(String(15), index=True)
    order_phone: Mapped[str] = mapped_column(String(15))
    is_same_as_caller: Mapped[bool] = mapped_column(Boolean, default=True)
    customer_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    address: Mapped[str] = mapped_column(Text, default="")

    # اقلام (JSON)
    items: Mapped[list] = mapped_column(JSON, default=list)
    items_count: Mapped[int] = mapped_column(Integer, default=0)
    total_price: Mapped[int] = mapped_column(BigInteger, default=0)

    # وضعیت
    status: Mapped[str] = mapped_column(
        String(20), default="pending"
    )  # pending | confirmed | delivered | cancelled

    # فراداده
    duration_seconds: Mapped[int] = mapped_column(Integer, default=0)
    transcript: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    def __repr__(self):
        return f"<Order #{self.id} {self.order_code} - {self.total_price:,}>"

    @property
    def total_formatted(self) -> str:
        return f"{self.total_price:,}"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "order_code": self.order_code,
            "session_id": self.session_id,
            "caller_phone": self.caller_phone,
            "order_phone": self.order_phone,
            "is_same_as_caller": self.is_same_as_caller,
            "customer_name": self.customer_name,
            "address": self.address,
            "items": self.items,
            "items_count": self.items_count,
            "total_price": self.total_price,
            "status": self.status,
            "duration_seconds": self.duration_seconds,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "notes": self.notes,
        }

    STATUS_LABELS = {
        "pending": "در انتظار",
        "confirmed": "تایید شده",
        "delivered": "تحویل شده",
        "cancelled": "لغو شده",
    }

    @property
    def status_label(self) -> str:
        return self.STATUS_LABELS.get(self.status, self.status)