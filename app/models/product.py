"""مدل محصول - مرحله بعدی تکمیل می‌شود"""
from app.models.database import Base

# فعلاً خالی - مرحله ۷ پر می‌شود


"""
مدل محصول
"""
from datetime import datetime

from sqlalchemy import String, Text, Integer, DateTime, Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.models.database import Base


class Product(Base):
    """جدول محصولات"""
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    price: Mapped[int] = mapped_column(BigInteger, default=0)  # به تومان
    stock: Mapped[int] = mapped_column(Integer, default=0)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)  # پیشنهاد ویژه
    display_order: Mapped[int] = mapped_column(Integer, default=0)  # ترتیب نمایش
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    def __repr__(self):
        return f"<Product #{self.id} {self.name!r} - {self.price:,}>"

    @property
    def price_formatted(self) -> str:
        """قیمت با جداکننده هزارگان"""
        return f"{self.price:,}"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "stock": self.stock,
            "description": self.description or "",
            "is_active": self.is_active,
            "is_featured": self.is_featured,
            "display_order": self.display_order,
        }