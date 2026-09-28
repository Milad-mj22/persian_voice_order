"""
مدل تنظیمات - Key/Value Store
"""
from datetime import datetime

from sqlalchemy import String, Text, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.database import Base


class Setting(Base):
    """جدول تنظیمات به صورت Key/Value"""
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=True)
    value_type: Mapped[str] = mapped_column(String(20), default="str")
    # value_type: str | int | float | bool | json
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    def __repr__(self):
        return f"<Setting {self.key}={self.value!r} ({self.value_type})>"