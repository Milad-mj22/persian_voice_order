"""
Factory برای ساخت موتورها بر اساس تنظیمات
"""
from app.core.config_manager import ConfigManager
from app.core.logger import logger


def create_stt():
    """ساخت موتور STT"""
    config = ConfigManager()
    provider = config.get("engines.stt_provider", "dummy")

    logger.info(f"[FACTORY] stt_provider = {provider!r}")

    if provider == "whisper":
        try:
            from app.engines.stt.whisper_stt import WhisperSTT
            return WhisperSTT()
        except Exception as e:
            logger.error(f"[FACTORY] خطا در ساخت WhisperSTT: {e}")

    from app.engines.stt.dummy_stt import DummySTT
    return DummySTT()


def create_tts():
    """ساخت موتور TTS"""
    config = ConfigManager()
    provider = config.get("engines.tts_provider", "dummy")

    logger.info(f"[FACTORY] tts_provider = {provider!r}")

    if provider == "pyttsx3":
        try:
            from app.engines.tts.pyttsx3_tts import Pyttsx3TTS
            engine = Pyttsx3TTS()
            if engine.is_available():
                return engine
            logger.warning("[FACTORY] pyttsx3 نیست، DummyTTS")
        except Exception as e:
            logger.error(f"[FACTORY] خطا در Pyttsx3TTS: {e}")

    from app.engines.tts.dummy_tts import DummyTTS
    return DummyTTS()


def create_chatbot():
    """ساخت موتور Chatbot"""
    config = ConfigManager()
    provider = config.get("engines.chatbot_provider", "rule_based")

    logger.info(f"[FACTORY] ================================")
    logger.info(f"[FACTORY] chatbot_provider = {provider!r}")
    logger.info(f"[FACTORY] ================================")

    if provider == "openai":
        logger.info("[FACTORY] → شاخه openai")
        try:
            from app.engines.chatbot.openai_chatbot import OpenAIChatbot

            logger.info("[FACTORY] ساخت OpenAIChatbot...")
            bot = OpenAIChatbot()

            available = bot.is_available()
            logger.info(f"[FACTORY] is_available() = {available}")

            if available:
                logger.info("[FACTORY] ✅ برمی‌گرداند OpenAIChatbot")
                return bot
            else:
                logger.warning("[FACTORY] ⚠️ OpenAI در دسترس نیست")

        except Exception as e:
            logger.exception(f"[FACTORY] ❌ خطا: {e}")

        logger.warning("[FACTORY] 🔄 Fallback به RuleBased")
        from app.engines.chatbot.rule_based import RuleBasedChatbot
        return RuleBasedChatbot()

    # پیش‌فرض: rule_based
    logger.info(f"[FACTORY] → شاخه پیش‌فرض (provider != openai)")
    from app.engines.chatbot.rule_based import RuleBasedChatbot
    return RuleBasedChatbot()