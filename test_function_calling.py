"""تست Function Calling"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.models.database import init_database
from app.engines.chatbot.base import ChatContext, ChatMessage, MessageRole
from app.engines.chatbot.openai_chatbot import OpenAIChatbot


def main():
    print("=" * 60)
    print("🧪 تست Function Calling")
    print("=" * 60)

    init_database()
    bot = OpenAIChatbot()

    context = ChatContext(
        session_id="test-fc",
        caller_phone="09123456789",
    )

    history = []

    test_inputs = [
        "سلام، یه پیتزا میخوام",
        "مخصوص",
        "دو تا",
        "سبدم چیه؟",
        "بله یه نوشابه هم میخوام",
        "کوکاکولا",
        "نه ممنون",
        "تهران، خیابان ولیعصر، پلاک ۱۲۳",
    ]

    for user_msg in test_inputs:
        print(f"\n{'=' * 60}")
        print(f"👤 {user_msg}")

        response = bot.get_response(user_msg, context, history)
        print(f"🤖 {response}")

        # خلاصه سبد
        print(f"   [سبد: {len(context.cart)} آیتم | "
              f"مجموع: {context.cart_total:,} | "
              f"آدرس: {context.address or '-'}]")

        history.append(ChatMessage(role=MessageRole.USER, content=user_msg))
        history.append(ChatMessage(role=MessageRole.ASSISTANT, content=response))

    print("\n" + "=" * 60)
    print("📦 سبد نهایی:")
    for item in context.cart:
        print(f"   • {item['name']} × {item['quantity']} = "
              f"{item['price'] * item['quantity']:,}")
    print(f"   💰 مجموع: {context.cart_total:,} تومان")
    print(f"   📍 آدرس: {context.address}")
    print("=" * 60)


if __name__ == "__main__":
    main()