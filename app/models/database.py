"""
اتصال به دیتابیس و Base model
"""
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

from app.core.config_manager import ConfigManager
from app.core.logger import logger


class Base(DeclarativeBase):
    """Base class برای همه مدل‌ها"""
    pass


class DatabaseManager:
    """مدیریت اتصال به دیتابیس"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        config = ConfigManager()
        db_type = config.get("database.type", "sqlite")

        if db_type == "sqlite":
            db_path = config.get_path("database.path")
            db_path.parent.mkdir(parents=True, exist_ok=True)
            db_url = f"sqlite:///{db_path}"
            logger.info(f"اتصال به SQLite: {db_path}")
        else:
            # برای آینده: PostgreSQL/MySQL
            db_url = config.get("database.url")
            logger.info(f"اتصال به دیتابیس: {db_type}")

        echo = config.get("database.echo", False)

        self.engine = create_engine(
            db_url,
            echo=echo,
            future=True,
        )

        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=Session,
        )

        self._initialized = True

    def create_all(self):
        """ساخت همه جداول"""
        # اطمینان از import مدل‌ها
        from app.models import settings, product, order, call_session  # noqa
        Base.metadata.create_all(self.engine)
        logger.info("جداول دیتابیس ساخته/بررسی شدند")

    def get_session(self) -> Session:
        """گرفتن یک Session جدید"""
        return self.SessionLocal()

    def drop_all(self):
        """حذف همه جداول (برای تست)"""
        Base.metadata.drop_all(self.engine)
        logger.warning("همه جداول حذف شدند!")


# نمونه Singleton
db = DatabaseManager()


def init_database():
    """راه‌اندازی دیتابیس - در main فراخوانی می‌شه"""
    db.create_all()