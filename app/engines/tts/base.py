"""
Interface موتور TTS (Text-to-Speech)
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TTSResult:
    """نتیجه تبدیل متن به گفتار"""
    audio_bytes: bytes
    format: str = "wav"      # wav | mp3 | ogg
    sample_rate: int = 22050
    duration: float = 0.0

    def save(self, path: str | Path) -> Path:
        """ذخیره در فایل"""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(self.audio_bytes)
        return p


class TTSProvider(ABC):
    """کلاس پایه TTS"""

    name: str = "base"

    @abstractmethod
    def synthesize(self, text: str, **kwargs) -> TTSResult:
        """
        تبدیل متن به گفتار

        Args:
            text: متن ورودی (فارسی)
            **kwargs: تنظیمات اضافی (voice، rate، ...)

        Returns:
            TTSResult
        """
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """آیا موتور آماده است؟"""
        ...

    def get_voices(self) -> list[str]:
        """لیست صداهای موجود"""
        return []

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name!r}>"