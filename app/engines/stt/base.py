"""
Interface موتور STT (Speech-to-Text)
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class STTResult:
    """نتیجه تبدیل گفتار به متن"""
    text: str
    language: str = "fa"
    confidence: float = 1.0
    duration: float = 0.0
    raw: dict = field(default_factory=dict)

    @property
    def is_empty(self) -> bool:
        return not self.text.strip()


class STTProvider(ABC):
    """کلاس پایه STT"""

    name: str = "base"

    @abstractmethod
    def transcribe(self, audio_input: bytes | Path | str) -> STTResult:
        """
        تبدیل صوت به متن

        Args:
            audio_input: می‌تواند bytes، Path، یا مسیر فایل باشد

        Returns:
            STTResult
        """
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """آیا موتور آماده است؟"""
        ...

    def warmup(self):
        """آماده‌سازی اولیه (اختیاری - برای مدل‌های سنگین)"""
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name!r}>"