"""
Factory برای ساخت موتورها بر اساس تنظیمات
"""
from app.core.config_manager import ConfigManager
from app.core.logger import logger


def create_stt():
    config = ConfigManager()
    provider = config.get("engines.stt_provider", "dummy")
    logger.info(f"[FACTORY] stt_provider = {provider!r}")

    if provider == "openai_whisper":
        try:
            from app.engines.stt.openai_whisper_stt import OpenAIWhisperSTT
            stt = OpenAIWhisperSTT()
            if stt.is_available():
                logger.info("✅ OpenAIWhisperSTT")
                return stt
        except Exception as e:
            logger.exception(f"خطا: {e}")

    if provider == "faster_whisper":
        try:
            from app.engines.stt.faster_whisper_stt import FasterWhisperSTT
            return FasterWhisperSTT(
                model_size=config.get_env("WHISPER_MODEL", "small"),
                device=config.get_env("WHISPER_DEVICE", "cpu"),
                compute_type=config.get_env("WHISPER_COMPUTE", "int8"),
            )
        except Exception as e:
            logger.exception(f"خطا: {e}")

    from app.engines.stt.dummy_stt import DummySTT
    return DummySTT()


def create_tts():
    """ساخت موتور TTS"""
    config = ConfigManager()
    provider = config.get("engines.tts_provider", "dummy")

    logger.info(f"[FACTORY] tts_provider = {provider!r}")

    if provider == "edge_tts":
        try:
            from app.engines.tts.edge_tts_provider import EdgeTTS
            voice = config.get_env("TTS_VOICE", "fa-IR-FaridNeural")
            bot = EdgeTTS(voice=voice)
            if bot.is_available():
                return bot
        except Exception as e:
            logger.exception(f"خطا در EdgeTTS: {e}")

    if provider == "pyttsx3":
        try:
            from app.engines.tts.pyttsx3_tts import Pyttsx3TTS
            engine = Pyttsx3TTS()
            if engine.is_available():
                return engine
        except Exception as e:
            logger.exception(f"خطا در Pyttsx3TTS: {e}")

    from app.engines.tts.dummy_tts import DummyTTS
    return DummyTTS()

def create_chatbot():
    config = ConfigManager()
    provider = config.get("engines.chatbot_provider", "rule_based")

    print(f"🔥 [FACTORY] create_chatbot called, provider = {provider!r}")

    if provider == "openai":
        print("🔥 [FACTORY] → openai branch")
        try:
            from app.engines.chatbot.openai_chatbot import OpenAIChatbot
            print("🔥 [FACTORY] imported OpenAIChatbot")

            bot = OpenAIChatbot()
            print(f"🔥 [FACTORY] created bot: {type(bot).__name__}")

            if bot.is_available():
                print("🔥 [FACTORY] ✅ returning OpenAIChatbot")
                return bot

            print("🔥 [FACTORY] ⚠️ openai not available")

        except Exception as e:
            print(f"🔥 [FACTORY] ❌ EXCEPTION: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()

        print("🔥 [FACTORY] 🔄 Fallback to RuleBased")

    # fallback یا default
    from app.engines.chatbot.rule_based import RuleBasedChatbot
    bot = RuleBasedChatbot()
    print(f"🔥 [FACTORY] returning {type(bot).__name__}")
    return bot