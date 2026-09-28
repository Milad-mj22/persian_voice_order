"""
Factory برای ساخت موتورها بر اساس تنظیمات
"""
from app.core.config_manager import ConfigManager
from app.core.logger import logger


def create_stt():
    """ساخت موتور STT بر اساس config.json"""
    config = ConfigManager()
    provider = config.get("engines.stt_provider", "dummy")

    if provider == "whisper":
        from app.engines.stt.whisper_stt import WhisperSTT
        return WhisperSTT()

    from app.engines.stt.dummy_stt import DummySTT
    return DummySTT()


def create_tts():
    """ساخت موتور TTS"""
    config = ConfigManager()
    provider = config.get("engines.tts_provider", "dummy")

    if provider == "pyttsx3":
        from app.engines.tts.pyttsx3_tts import Pyttsx3TTS
        engine = Pyttsx3TTS()
        if engine.is_available():
            return engine
        logger.warning("pyttsx3 در دسترس نیست، استفاده از DummyTTS")

    from app.engines.tts.dummy_tts import DummyTTS
    return DummyTTS()


def create_chatbot():
    """ساخت موتور Chatbot"""
    config = ConfigManager()
    provider = config.get("engines.chatbot_provider", "rule_based")

    # فعلاً فقط rule_based
    from app.engines.chatbot.rule_based import RuleBasedChatbot
    return RuleBasedChatbot()