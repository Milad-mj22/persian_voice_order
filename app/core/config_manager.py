"""
مدیریت تنظیمات کلی برنامه (config.json + .env)
"""
import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


class ConfigManager:
    """مدیریت فایل config.json و متغیرهای محیطی .env"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config_path: str | Path = "config.json"):
        if self._initialized:
            return

        self.config_path = Path(config_path).resolve()
        self.project_root = self.config_path.parent
        self._config: dict = {}

        # ⭐ خواندن .env
        env_path = self.project_root / ".env"
        if env_path.exists():
            load_dotenv(env_path)
        else:
            load_dotenv()  # از مسیر پیش‌فرض

        self._load()
        self._initialized = True

    def _load(self):
        """بارگذاری فایل config.json"""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"فایل تنظیمات پیدا نشد: {self.config_path}"
            )

        with open(self.config_path, "r", encoding="utf-8") as f:
            self._config = json.load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """خواندن مقدار با پشتیبانی از نقطه (nested)"""
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def get_env(self, key: str, default: Any = None) -> Any:
        """خواندن از متغیرهای محیطی (.env)"""
        return os.environ.get(key, default)

    def get_path(self, key: str) -> Path:
        """گرفتن مسیر مطلق"""
        rel = self.get(key)
        if rel is None:
            raise KeyError(f"کلید مسیر پیدا نشد: {key}")
        return (self.project_root / rel).resolve()

    def set(self, key: str, value: Any):
        """تنظیم مقدار"""
        keys = key.split(".")
        data = self._config
        for k in keys[:-1]:
            data = data.setdefault(k, {})
        data[keys[-1]] = value

    def save(self):
        """ذخیره تنظیمات"""
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self._config, f, ensure_ascii=False, indent=2)


# نمونه استفاده
if __name__ == "__main__":
    config = ConfigManager()
    print("نام برنامه:", config.get("app.name"))
    print("مسیر دیتابیس:", config.get_path("database.path"))
    print("OPENAI_API_KEY:", (config.get_env("OPENAI_API_KEY") or "تنظیم نشده")[:20], "...")