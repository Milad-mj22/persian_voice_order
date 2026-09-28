"""
کنترلر صفحه تست تماس - با پشتیبانی کامل صوتی
"""
import json
import threading
import uuid
from datetime import datetime
from pathlib import Path

import numpy as np

from PySide6.QtWidgets import (
    QWidget, QMessageBox, QListWidgetItem, QFileDialog,
)
from PySide6.QtCore import Qt, QTimer, Signal

from app.core.config_manager import ConfigManager
from app.core.logger import logger
from app.engines.factory import create_stt, create_tts, create_chatbot
from app.engines.chatbot.base import ChatContext, ChatMessage, MessageRole
from app.services.settings_service import get_settings_service
from app.services.phone_validator import IranianPhoneValidator
from app.ui.ui_loader import get_ui_class
from app.ui.widgets.chat_bubble import ChatContainer
from app.workers.audio_recorder import AudioRecorder
from app.workers.audio_player import AudioPlayer


class TestCallController(QWidget):
    """صفحه تست تماس"""

    order_completed = Signal(dict)

    # ⭐ Signal ها برای ارتباط بین thread و UI
    audio_recorded = Signal(object)   # numpy array یا None
    transcription_done = Signal(str)  # متن Whisper

    def __init__(self, parent=None):
        super().__init__(parent)

        self.config = ConfigManager()
        self.settings = get_settings_service()

        # موتورها
        self.stt = create_stt()
        self.tts = create_tts()
        self.chatbot = create_chatbot()

        # Session
        self.session_id: str | None = None
        self.context: ChatContext | None = None
        self.history: list[ChatMessage] = []
        self.call_start_time: datetime | None = None
        self.call_ended: bool = False

        # ⭐ صدا
        mic_device_str = self.config.get_env("MIC_DEVICE", "").strip()
        mic_device = int(mic_device_str) if mic_device_str.isdigit() else None


        self.audio_recorder = AudioRecorder(
            silence_threshold=0.020,   # ⭐ پایین — حساس به صداهای نرم
            silence_duration=1.5,       # ⭐ صبر زیاد — وسط جمله قطع نشه
            max_duration=20.0,
            min_duration=0.5,
            grace_period=0.6,           # ⭐ 0.6 ثانیه اول، حتی اگه ساکت بود، ادامه بده
            pre_buffer_seconds=0.3,     # ⭐ 0.3 ثانیه قبل از شروع صدا رو هم ذخیره کن
            device=mic_device)

        self.audio_player = AudioPlayer(self)

        self.voice_mode = True
        self.is_recording = False
        self.is_playing = False
        self._recording_thread: threading.Thread | None = None

        # لود UI
        ui_class = get_ui_class("test_call_page")
        self.ui = ui_class()
        self.ui.setupUi(self)

        self._setup_chat_container()
        self._setup_timer()
        self._connect_signals()
        self._set_state_idle()

        logger.info("صفحه تست تماس ساخته شد")

    # =========================================================
    # تنظیمات اولیه
    # =========================================================
    def _setup_chat_container(self):
        self.chat_container = ChatContainer()
        self.ui.chat_scroll.setWidget(self.chat_container)

    def _setup_timer(self):
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._update_timer)

    def _connect_signals(self):
        # UI
        self.ui.start_call_btn.clicked.connect(self.start_call)
        self.ui.end_call_btn.clicked.connect(self.end_call)
        self.ui.send_btn.clicked.connect(self.send_user_message)
        self.ui.user_input_edit.returnPressed.connect(self.send_user_message)
        self.ui.save_order_btn.clicked.connect(self.save_final_order)
        self.ui.download_transcript_btn.clicked.connect(self.download_transcript)

        # ⭐ AudioPlayer
        self.audio_player.finished.connect(self._on_audio_finished)
        self.audio_player.error.connect(self._on_audio_error)

        # ⭐ Signal های thread-safe
        self.audio_recorded.connect(self._on_audio_recorded)
        self.transcription_done.connect(self._on_transcription_done)

    # =========================================================
    # وضعیت‌ها
    # =========================================================
    def _set_state_idle(self):
        self.ui.start_call_btn.setEnabled(True)
        self.ui.end_call_btn.setEnabled(False)
        self.ui.send_btn.setEnabled(False)
        self.ui.user_input_edit.setEnabled(False)
        self.ui.save_order_btn.setEnabled(False)
        self.ui.download_transcript_btn.setEnabled(False)
        self.ui.caller_phone_edit.setEnabled(True)
        self.ui.status_indicator.setText("⚪  آماده")
        self.ui.status_indicator.setStyleSheet("color: #64748b; font-weight: bold;")
        self.ui.timer_label.setText("⏱️  00:00")

    def _set_state_active(self):
        self.ui.start_call_btn.setEnabled(False)
        self.ui.end_call_btn.setEnabled(True)
        self.ui.send_btn.setEnabled(True)
        self.ui.user_input_edit.setEnabled(True)
        self.ui.save_order_btn.setEnabled(True)
        self.ui.download_transcript_btn.setEnabled(True)
        self.ui.caller_phone_edit.setEnabled(False)
        self.ui.status_indicator.setText("🎤  در حال شنیدن...")
        self.ui.status_indicator.setStyleSheet("color: #16a34a; font-weight: bold;")

    def _set_state_ended(self):
        self.ui.start_call_btn.setEnabled(True)
        self.ui.end_call_btn.setEnabled(False)
        self.ui.send_btn.setEnabled(False)
        self.ui.user_input_edit.setEnabled(False)
        self.ui.save_order_btn.setEnabled(False)
        self.ui.download_transcript_btn.setEnabled(True)
        self.ui.caller_phone_edit.setEnabled(True)
        self.ui.status_indicator.setText("🔴  تماس پایان یافت")
        self.ui.status_indicator.setStyleSheet("color: #dc2626; font-weight: bold;")

    def _update_voice_status(self, text: str):
        self.ui.status_indicator.setText(text)

    # =========================================================
    # شروع / پایان تماس
    # =========================================================
    def start_call(self):
        phone_input = self.ui.caller_phone_edit.text().strip()
        result = IranianPhoneValidator.validate(phone_input)

        if not result.valid:
            QMessageBox.warning(
                self, "شماره نامعتبر",
                "لطفاً یک شماره موبایل معتبر وارد کنید.\nمثال: 09123456789"
            )
            return

        caller_phone = result.normalized

        self.chat_container.clear()
        self.history.clear()
        self.call_ended = False

        self.session_id = str(uuid.uuid4())
        self.context = ChatContext(
            session_id=self.session_id,
            caller_phone=caller_phone,
        )
        self.context.extras["stage"] = "welcome"
        self.call_start_time = datetime.now()

        self.timer.start()
        self._set_state_active()
        self._update_cart_display()
        self._update_customer_display()

        # ⭐ پیام خوش‌آمد + پخش صوتی
        welcome = self.chatbot.get_welcome_message(self.context)
        self._add_bot_message(welcome)
        self._speak_and_listen(welcome)

        logger.info(f"تماس شروع شد: {self.session_id[:8]} | {caller_phone}")

    def end_call(self):
        if not self.session_id:
            return

        # توقف همه فعالیت‌ها
        self.voice_mode = False
        self.audio_recorder.stop()
        self.audio_player.stop()

        self._add_system_message("— تماس پایان یافت —")

        self.timer.stop()
        self.call_ended = True
        self._set_state_ended()
        logger.info(f"تماس پایان یافت: {self.session_id[:8]}")

    # =========================================================
    # ⭐ مکالمه صوتی
    # =========================================================
    def _speak_and_listen(self, text: str):
        """پخش پاسخ + شروع ضبط خودکار"""
        if not self.tts.is_available():
            logger.warning("TTS در دسترس نیست")
            self._start_recording()
            return

        try:
            tts_result = self.tts.synthesize(text)
            if tts_result.audio_bytes:
                self.is_playing = True
                self._update_voice_status("🔊 در حال پخش...")
                self.audio_player.play_bytes(tts_result.audio_bytes, tts_result.format)
                return  # _on_audio_finished ضبط رو شروع می‌کنه
        except Exception as e:
            logger.exception(f"خطا در TTS: {e}")

        # اگه پخش نشد
        self._start_recording()

    def _on_audio_finished(self):
        """بعد از پایان پخش"""
        self.is_playing = False
        logger.info("پخش صدا تمام شد")

        if not self.call_ended and self.voice_mode:
            QTimer.singleShot(300, self._start_recording)

    def _on_audio_error(self, msg: str):
        self.is_playing = False
        logger.error(f"خطای پخش: {msg}")
        if not self.call_ended and self.voice_mode:
            QTimer.singleShot(300, self._start_recording)

    # =========================================================
    # ⭐ ضبط (در thread جداگانه)
    # =========================================================
    def _start_recording(self):
        """شروع ضبط"""
        if self.is_recording or self.call_ended:
            return

        self.is_recording = True
        self._update_voice_status("🎤 در حال شنیدن...")

        self._recording_thread = threading.Thread(
            target=self._record_worker,
            daemon=True,
        )
        self._recording_thread.start()

    def _record_worker(self):
        """Worker ضبط - در thread جداگانه"""
        try:
            logger.info("🎤 شروع ضبط...")
            audio = self.audio_recorder.record_until_silence()
            # ⭐ Signal برای برگشت به نخ اصلی
            self.audio_recorded.emit(audio)
        except Exception as e:
            logger.exception(f"خطا در ضبط: {e}")
            self.audio_recorded.emit(None)

    def _on_audio_recorded(self, audio):
        """بعد از ضبط - در نخ اصلی"""
        self.is_recording = False

        if audio is None:
            self._update_voice_status("❓ صدایی شنیده نشد")
            if not self.call_ended and self.voice_mode:
                QTimer.singleShot(500, self._start_recording)
            return

        # محاسبه مدت
        try:
            duration = len(audio) / 16000
        except Exception:
            duration = 0.0

        self._update_voice_status(f"🧠 در حال پردازش ({duration:.1f}s)...")
        logger.info(f"🎧 صوت دریافت شد: {duration:.1f}s — شروع STT")

        # ⭐ STT در thread جداگانه
        threading.Thread(
            target=self._stt_worker,
            args=(audio,),
            daemon=True,
        ).start()

    def _stt_worker(self, audio):
        """Worker STT - در thread جداگانه"""
        try:
            logger.info("🧠 در حال تبدیل با Whisper...")
            result = self.stt.transcribe(audio)
            text = result.text.strip()
            logger.info(f"📝 Whisper: {text!r}")
            self.transcription_done.emit(text)
        except Exception as e:
            logger.exception(f"خطا در STT: {e}")
            self.transcription_done.emit("")

    def _on_transcription_done(self, text: str):
        """بعد از STT - در نخ اصلی"""
        if not text:
            self._update_voice_status("❓ متوجه نشدم")
            self._add_system_message("(صدای نامفهوم)")
            if not self.call_ended and self.voice_mode:
                QTimer.singleShot(500, self._start_recording)
            return

        self._update_voice_status("✅ دریافت شد")
        self.ui.user_input_edit.setText(text)
        # ارسال خودکار
        self.send_user_message()

    # =========================================================
    # ارسال پیام
    # =========================================================
    def send_user_message(self):
        if not self.context or self.call_ended:
            return

        text = self.ui.user_input_edit.text().strip()
        if not text:
            return

        self.ui.user_input_edit.clear()
        self._add_user_message(text)

        self.history.append(ChatMessage(role=MessageRole.USER, content=text))

        # ⭐ پاسخ در thread جداگانه (چون OpenAI کند است)
        self._update_voice_status("🤔 در حال فکر...")
        threading.Thread(
            target=self._llm_worker,
            args=(text,),
            daemon=True,
        ).start()

    def _llm_worker(self, text: str):
        """Worker Chatbot - در thread جداگانه"""
        try:
            response = self.chatbot.get_response(text, self.context, self.history)
            # برگشت به نخ اصلی
            self.transcription_done.emit(f"__BOT__{response}")  # علامت‌گذاری
        except Exception as e:
            logger.exception(f"خطا در Chatbot: {e}")
            self.transcription_done.emit("__BOT__متأسفم، خطایی رخ داد.")

    # (این متد رو جایگزین _on_transcription_done می‌کنیم)
    def _on_transcription_done(self, text: str):
        """بعد از STT یا LLM - در نخ اصلی"""
        # اگه از سمت LLM میاد
        if text.startswith("__BOT__"):
            response = text[len("__BOT__"):]
            self._add_bot_message(response)
            self.history.append(ChatMessage(role=MessageRole.ASSISTANT, content=response))
            self._update_cart_display()
            self._update_customer_display()

            # ⭐ پخش پاسخ + ضبط مجدد
            if not self.call_ended:
                self._speak_and_listen(response)
            return

        # از سمت STT میاد
        if not text:
            self._update_voice_status("❓ متوجه نشدم")
            self._add_system_message("(صدای نامفهوم)")
            if not self.call_ended and self.voice_mode:
                QTimer.singleShot(500, self._start_recording)
            return

        self._update_voice_status("✅ دریافت شد")
        self.ui.user_input_edit.setText(text)
        self.send_user_message()

    # =========================================================
    # نمایش پیام‌ها
    # =========================================================
    def _add_user_message(self, text: str):
        ts = datetime.now().strftime("%H:%M")
        self.chat_container.add_message(text, role="user", timestamp=ts)
        self._scroll_chat_to_bottom()

    def _add_bot_message(self, text: str):
        ts = datetime.now().strftime("%H:%M")
        self.chat_container.add_message(text, role="bot", timestamp=ts)
        self._scroll_chat_to_bottom()

    def _add_system_message(self, text: str):
        ts = datetime.now().strftime("%H:%M")
        self.chat_container.add_message(text, role="system", timestamp=ts)
        self._scroll_chat_to_bottom()

    def _scroll_chat_to_bottom(self):
        QTimer.singleShot(
            50,
            lambda: self.ui.chat_scroll.verticalScrollBar().setValue(
                self.ui.chat_scroll.verticalScrollBar().maximum()
            )
        )

    # =========================================================
    # سبد و مشتری
    # =========================================================
    def _update_cart_display(self):
        self.ui.cart_list.clear()
        if not self.context or not self.context.cart:
            self.ui.cart_total_label.setText("💰  مجموع: 0 تومان")
            return
        for item in self.context.cart:
            qty = item["quantity"]
            price = item["price"]
            text = f"• {item['name']}\n   {qty} × {price:,} = {qty * price:,}"
            self.ui.cart_list.addItem(QListWidgetItem(text))
        self.ui.cart_total_label.setText(f"💰  مجموع: {self.context.cart_total:,} تومان")

    def _update_customer_display(self):
        if not self.context:
            return
        phone = self.context.order_phone or self.context.caller_phone or "-"
        address = self.context.address or "-"
        self.ui.customer_phone_label.setText(f"📞  شماره ثبت: {phone}")
        self.ui.customer_address_label.setText(f"📍  آدرس: {address}")

    # =========================================================
    # تایمر
    # =========================================================
    def _update_timer(self):
        if not self.call_start_time:
            return
        elapsed = (datetime.now() - self.call_start_time).total_seconds()
        m = int(elapsed // 60)
        s = int(elapsed % 60)
        self.ui.timer_label.setText(f"⏱️  {m:02d}:{s:02d}")

    # =========================================================
    # ذخیره سفارش
    # =========================================================
    def save_final_order(self):
        if not self.context:
            return
        if not self.context.cart:
            QMessageBox.information(self, "سبد خالی", "سبد خرید خالی است.")
            return
        if not self.context.address:
            QMessageBox.warning(self, "آدرس ناقص", "آدرس مشتری ثبت نشده است.")
            return

        try:
            from app.services.order_service import get_order_service
            order_service = get_order_service()

            duration = 0
            if self.call_start_time:
                duration = int((datetime.now() - self.call_start_time).total_seconds())

            order_data = {
                "session_id": self.session_id,
                "caller_phone": self.context.caller_phone,
                "order_phone": self.context.order_phone or self.context.caller_phone,
                "is_same_as_caller": self.context.is_same_as_caller,
                "address": self.context.address,
                "items": self.context.cart,
                "total_price": self.context.cart_total,
                "duration_seconds": duration,
                "transcript": self._build_transcript(),
                "status": "pending",
            }

            order = order_service.create(order_data)
            if order is None:
                QMessageBox.warning(self, "خطا", "ذخیره سفارش ناموفق بود.")
                return

            QMessageBox.information(
                self, "✅ سفارش ثبت شد",
                f"کد سفارش: {order.order_code}\n\n"
                f"مجموع: {order.total_price:,} تومان\n"
                f"تعداد اقلام: {order.items_count}\n\n"
                f"در صفحه «📋 سفارشات» قابل مشاهده است."
            )
            self.order_completed.emit(order.to_dict())
            self._reset_after_save()
        except Exception as e:
            logger.exception(f"خطا در ذخیره سفارش: {e}")
            QMessageBox.critical(self, "خطا", str(e))

    def _reset_after_save(self):
        self.session_id = None
        self.context = None
        self.history.clear()
        self.call_start_time = None
        self.chat_container.clear()
        self.ui.cart_list.clear()
        self.ui.cart_total_label.setText("💰  مجموع: 0 تومان")
        self.ui.customer_phone_label.setText("📞  شماره ثبت: -")
        self.ui.customer_address_label.setText("📍  آدرس: -")
        self._set_state_idle()

    # =========================================================
    # Transcript
    # =========================================================
    def download_transcript(self):
        if not self.history:
            QMessageBox.information(self, "خالی", "مکالمه‌ای برای ذخیره وجود ندارد.")
            return
        default_name = f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath, _ = QFileDialog.getSaveFileName(
            self, "ذخیره متن مکالمه",
            str(Path.home() / default_name),
            "Text Files (*.txt);;All Files (*)",
        )
        if not filepath:
            return
        try:
            Path(filepath).write_text(self._build_transcript(), encoding="utf-8")
            QMessageBox.information(self, "✅", f"ذخیره شد:\n{filepath}")
        except Exception as e:
            QMessageBox.critical(self, "خطا", str(e))

    def _build_transcript(self) -> str:
        lines = ["=" * 60, "📞 متن مکالمه", "=" * 60]
        if self.call_start_time:
            lines.append(f"شروع: {self.call_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        if self.context:
            lines.append(f"شماره: {self.context.caller_phone}")
        lines.append("-" * 60)
        for msg in self.history:
            role_fa = {
                MessageRole.USER: "👤 مشتری",
                MessageRole.ASSISTANT: "🤖 بات",
                MessageRole.SYSTEM: "⚙️ سیستم",
            }.get(msg.role, "?")
            lines.append(f"[{msg.timestamp.strftime('%H:%M:%S')}] {role_fa}:")
            lines.append(f"  {msg.content}")
            lines.append("")
        if self.context and self.context.cart:
            lines.append("=" * 60)
            lines.append("🛒 خلاصه سفارش")
            lines.append("=" * 60)
            for it in self.context.cart:
                lines.append(f"  • {it['name']} × {it['quantity']} = "
                             f"{it['price'] * it['quantity']:,}")
            lines.append(f"\n💰 مجموع: {self.context.cart_total:,} تومان")
            if self.context.address:
                lines.append(f"📍 آدرس: {self.context.address}")
        return "\n".join(lines)

    def refresh(self):
        pass