"""تست اتصال به OpenAI"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.models.database import init_database
from app.engines.chatbot.openai_chatbot import OpenAIChatbot
from app.engines.chatbot.base import ChatContext, ChatMessage, MessageRole


def main():
    print("=" * 60)
    print("🧪 تست OpenAIChatbot")
    print("=" * 60)

    init_database()

    bot = OpenAIChatbot()
    print(f"موتور: {bot}")
    print(f"موجود: {bot.is_available()}")
    print(f"مدل: {bot.model}")

    if not bot.is_available():
        print("\n❌ API Key تنظیم نشده یا کتابخانه نصب نیست.")
        return

    # ساخت Context
    context = ChatContext(
        session_id="test-001",
        caller_phone="09123456789",
    )

    # پیام خوش‌آمد
    print("\n" + "-" * 60)
    welcome = bot.get_welcome_message(context)
    print(f"🤖 {welcome}")
    print("-" * 60)

    # دیالوگ تست
    history = []

    test_inputs = [
        "سلام، یه پیتزا میخوام",
        "پیتزا مخصوص",
        "دو تا",
        "بله یه نوشابه هم میخوام",
        "کوکاکولا",
        "نه ممنون",
        "تهران، خیابون ولیعصر، پلاک ۱۲۳",
        "بله همین شماره خوبه",
    ]

    for user_msg in test_inputs:
        print(f"\n👤 {user_msg}")

        response = bot.get_response(user_msg, context, history)
        print(f"🤖 {response}")

        # افزودن به history
        history.append(ChatMessage(
            role=MessageRole.USER, content=user_msg
        ))
        history.append(ChatMessage(
            role=MessageRole.ASSISTANT, content=response
        ))

    print("\n" + "=" * 60)
    print("🎉 تست کامل شد")
    print("=" * 60)


if __name__ == "__main__":
    main()