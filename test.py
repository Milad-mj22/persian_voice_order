# app/engines/stt/openai_gpt4o_audio.py
from openai import OpenAI

client = OpenAI(api_key="...")

# صدا → base64
import base64
audio_b64 = base64.b64encode(wav_bytes).decode()

response = client.chat.completions.create(
    model="gpt-4o-audio-preview",
    modalities=["text", "audio"],
    audio={"voice": "alloy", "format": "wav"},
    messages=[
        {
            "role": "system",
            "content": "تو اپراتور سفارش‌گیری فست‌فود سکه طلا هستی..."
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "به این پیام صوتی مشتری گوش بده:"},
                {
                    "type": "input_audio",
                    "input_audio": {"data": audio_b64, "format": "wav"}
                }
            ]
        }
    ]
)

# پاسخ متنی
text = response.choices[0].message.content

# پاسخ صوتی
audio_response_b64 = response.choices[0].message.audio.data
audio_bytes = base64.b64decode(audio_response_b64)