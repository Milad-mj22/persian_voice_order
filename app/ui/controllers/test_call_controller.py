"""
کنترلر صفحه تست تماس
"""
import json
import uuid
from datetime import datetime
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget, QMessageBox, QListWidgetItem, QFileDialog
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


class TestCallController(QWidget):
    """صفحه تست تماس"""

    order_completed = Signal(dict)  # وقتی سفارش نهایی می‌شه

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

        # لود UI
        ui_class = get_ui_class("test_call_page")
        self.ui = ui_class()
        self.ui.setupUi(self)

        # جایگزینی QWidget چت با ChatContainer
        self._setup_chat_container()

        # تایمر
        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # هر ثانیه
        self.timer.timeout.connect(self._update_timer)

        # اتصالات
        self._connect_signals()

        # وضعیت اولیه
        self._set_state_idle()

        logger.info("صفحه تست تماس ساخته شد")

    # =========================================================
    def _setup_chat_container(self):
        """جایگزینی layout چت با ChatContainer"""
        # ChatContainer رو به عنوان ویجت به chat_scroll اضافه می‌کنیم
        self.chat_container = ChatContainer()
        self.ui.chat_scroll.setWidget(self.chat_container)

    # =========================================================
    def _connect_signals(self):
        self.ui.start_call_btn.clicked.connect(self.start_call)
        self.ui.end_call_btn.clicked.connect(self.end_call)
        self.ui.send_btn.clicked.connect(self.send_user_message)
        self.ui.user_input_edit.returnPressed.connect(self.send_user_message)
        self.ui.save_order_btn.clicked.connect(self.save_final_order)
        self.ui.download_transcript_btn.clicked.connect(self.download_transcript)

    # =========================================================
    # مدیریت وضعیت
    # =========================================================
    def _set_state_idle(self):
        """وضعیت آماده"""
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
        """وضعیت در حال مکالمه"""
        self.ui.start_call_btn.setEnabled(False)
        self.ui.end_call_btn.setEnabled(True)
        self.ui.send_btn.setEnabled(True)
        self.ui.user_input_edit.setEnabled(True)
        self.ui.save_order_btn.setEnabled(True)
        self.ui.download_transcript_btn.setEnabled(True)
        self.ui.caller_phone_edit.setEnabled(False)
        self.ui.status_indicator.setText("🟢  در حال مکالمه")
        self.ui.status_indicator.setStyleSheet("color: #16a34a; font-weight: bold;")
        self.ui.user_input_edit.setFocus()

    def _set_state_ended(self):
        """وضعیت پایان‌یافته"""
        self.ui.start_call_btn.setEnabled(True)
        self.ui.end_call_btn.setEnabled(False)
        self.ui.send_btn.setEnabled(False)
        self.ui.user_input_edit.setEnabled(False)
        self.ui.save_order_btn.setEnabled(False)
        self.ui.download_transcript_btn.setEnabled(True)
        self.ui.caller_phone_edit.setEnabled(True)
        self.ui.status_indicator.setText("🔴  تماس پایان یافت")
        self.ui.status_indicator.setStyleSheet("color: #dc2626; font-weight: bold;")

    # =========================================================
    # شروع تماس
    # =========================================================
    def start_call(self):
        """شروع تماس جدید"""
        # ۱. اعتبارسنجی شماره
        phone_input = self.ui.caller_phone_edit.text().strip()
        result = IranianPhoneValidator.validate(phone_input)

        if not result.valid:
            QMessageBox.warning(
                self, "شماره نامعتبر",
                "لطفاً یک شماره موبایل معتبر وارد کنید.\n"
                "مثال: 09123456789"
            )
            self.ui.caller_phone_edit.setFocus()
            return

        caller_phone = result.normalized

        # ۲. پاک کردن وضعیت قبلی
        self.chat_container.clear()
        self.history.clear()
        self.call_ended = False

        # ۳. ساخت Session و Context
        self.session_id = str(uuid.uuid4())
        self.context = ChatContext(
            session_id=self.session_id,
            caller_phone=caller_phone,
        )
        self.context.extras["stage"] = "welcome"
        self.call_start_time = datetime.now()

        # ۴. شروع تایمر
        self.timer.start()

        # ۵. آپدیت UI
        self._set_state_active()
        self._update_cart_display()
        self._update_customer_display()

        # ۶. پیام خوش‌آمدگویی
        welcome = self.chatbot.get_welcome_message(self.context)
        self._add_bot_message(welcome)

        logger.info(f"تماس شروع شد: {self.session_id[:8]} | {caller_phone}")

    # =========================================================
    # پایان تماس
    # =========================================================
    def end_call(self):
        """پایان دادن به تماس"""
        if not self.session_id:
            return

        # پیام خداحافظی
        goodbye = self.settings.get(
            "goodbye_message",
            "نوش جان، منتظر تماس شما هستیم."
        )
        self._add_system_message("— تماس پایان یافت —")

        self.timer.stop()
        self.call_ended = True
        self._set_state_ended()

        logger.info(f"تماس پایان یافت: {self.session_id[:8]}")

    # =========================================================
    # ارسال پیام کاربر
    # =========================================================
    def send_user_message(self):
        """گرفتن ورودی کاربر و ارسال به چت‌بات"""
        if not self.context or self.call_ended:
            return

        text = self.ui.user_input_edit.text().strip()
        if not text:
            return

        # پاک کردن ورودی
        self.ui.user_input_edit.clear()

        # افزودن پیام کاربر به چت
        self._add_user_message(text)

        # افزودن به history
        self.history.append(ChatMessage(
            role=MessageRole.USER,
            content=text,
        ))

        # گرفتن پاسخ
        try:
            response = self.chatbot.get_response(
                text, self.context, self.history
            )
        except Exception as e:
            logger.exception(f"خطا در Chatbot: {e}")
            response = "متأسفم، خطایی رخ داد. لطفاً دوباره امتحان کنید."

        # افزودن پاسخ بات
        self._add_bot_message(response)

        self.history.append(ChatMessage(
            role=MessageRole.ASSISTANT,
            content=response,
        ))

        # آپدیت سبد و اطلاعات مشتری
        self._update_cart_display()
        self._update_customer_display()

        # اگه مرحله DONE شد، پیشنهاد پایان
        stage = self.context.extras.get("stage", "")
        if stage == "done" and not self.call_ended:
            # اتوماتیک پایان نده، ولی می‌تونیم یک راهنمایی نشون بدیم
            pass

    # =========================================================
    # نمایش پیام‌ها
    # =========================================================
    def _add_user_message(self, text: str):
        """نمایش پیام کاربر"""
        ts = datetime.now().strftime("%H:%M")
        self.chat_container.add_message(text, role="user", timestamp=ts)
        self._scroll_chat_to_bottom()

    def _add_bot_message(self, text: str):
        """نمایش پیام بات"""
        ts = datetime.now().strftime("%H:%M")
        self.chat_container.add_message(text, role="bot", timestamp=ts)
        self._scroll_chat_to_bottom()

    def _add_system_message(self, text: str):
        """نمایش پیام سیستم"""
        ts = datetime.now().strftime("%H:%M")
        self.chat_container.add_message(text, role="system", timestamp=ts)
        self._scroll_chat_to_bottom()

    def _scroll_chat_to_bottom(self):
        """اسکرول به پایین"""
        # تاخیر کوچک تا layout آپدیت بشه
        QTimer.singleShot(
            50,
            lambda: self.ui.chat_scroll.verticalScrollBar().setValue(
                self.ui.chat_scroll.verticalScrollBar().maximum()
            )
        )

    # =========================================================
    # نمایش سبد
    # =========================================================
    def _update_cart_display(self):
        """آپدیت لیست سبد خرید"""
        self.ui.cart_list.clear()

        if not self.context or not self.context.cart:
            self.ui.cart_total_label.setText("💰  مجموع: 0 تومان")
            return

        for item in self.context.cart:
            qty = item["quantity"]
            price = item["price"]
            subtotal = price * qty
            text = f"• {item['name']}\n   {qty} × {price:,} = {subtotal:,}"
            li = QListWidgetItem(text)
            self.ui.cart_list.addItem(li)

        total = self.context.cart_total
        self.ui.cart_total_label.setText(f"💰  مجموع: {total:,} تومان")

    # =========================================================
    # نمایش اطلاعات مشتری
    # =========================================================
    def _update_customer_display(self):
        """آپدیت شماره و آدرس"""
        if not self.context:
            self.ui.customer_phone_label.setText("📞  شماره ثبت: -")
            self.ui.customer_address_label.setText("📍  آدرس: -")
            return

        phone = self.context.order_phone or self.context.caller_phone or "-"
        address = self.context.address or "-"

        self.ui.customer_phone_label.setText(f"📞  شماره ثبت: {phone}")
        self.ui.customer_address_label.setText(f"📍  آدرس: {address}")

    # =========================================================
    # تایمر
    # =========================================================
    def _update_timer(self):
        """آپدیت تایمر هر ثانیه"""
        if not self.call_start_time:
            return

        elapsed = (datetime.now() - self.call_start_time).total_seconds()
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        self.ui.timer_label.setText(f"⏱️  {minutes:02d}:{seconds:02d}")

    # =========================================================
    # ذخیره سفارش نهایی
    # =========================================================
    def save_final_order(self):
        """ذخیره سفارش در فایل"""
        if not self.context:
            return

        if not self.context.cart:
            QMessageBox.information(
                self, "سبد خالی", "سبد خرید خالی است."
            )
            return

        if not self.context.address:
            QMessageBox.warning(
                self, "آدرس ناقص",
                "آدرس مشتری ثبت نشده است."
            )
            return

        try:
            # ساخت داده سفارش
            order_data = {
                "order_id": str(uuid.uuid4())[:8].upper(),
                "session_id": self.session_id,
                "created_at": datetime.now().isoformat(),
                "caller_phone": self.context.caller_phone,
                "order_phone": self.context.order_phone or self.context.caller_phone,
                "is_same_as_caller": self.context.is_same_as_caller,
                "address": self.context.address,
                "items": self.context.cart,
                "total": self.context.cart_total,
                "duration_seconds": int(
                    (datetime.now() - self.call_start_time).total_seconds()
                ) if self.call_start_time else 0,
                "transcript": self._build_transcript(),
            }

            # ذخیره در فایل
            confirmations_dir = self.config.get_path("paths.confirmations_dir")
            confirmations_dir.mkdir(parents=True, exist_ok=True)

            filename = f"order_{order_data['order_id']}.json"
            filepath = confirmations_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(order_data, f, ensure_ascii=False, indent=2)

            logger.info(f"سفارش ذخیره شد: {filepath}")

            # نمایش به کاربر
            QMessageBox.information(
                self, "✅ سفارش ثبت شد",
                f"سفارش با کد {order_data['order_id']} ثبت شد.\n\n"
                f"مجموع: {order_data['total']:,} تومان\n"
                f"تعداد اقلام: {len(order_data['items'])}\n\n"
                f"📁 فایل: {filepath}"
            )

            self.order_completed.emit(order_data)

            # پاک کردن وضعیت
            self._reset_after_save()

        except Exception as e:
            logger.exception(f"خطا در ذخیره سفارش: {e}")
            QMessageBox.critical(
                self, "خطا",
                f"ذخیره سفارش ناموفق بود:\n{e}"
            )

    def _reset_after_save(self):
        """بازنشانی بعد از ذخیره موفق"""
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
    # دانلود transcript
    # =========================================================
    def download_transcript(self):
        """ذخیره متن مکالمه در فایل متنی"""
        if not self.history:
            QMessageBox.information(
                self, "خالی", "مکالمه‌ای برای ذخیره وجود ندارد."
            )
            return

        default_name = f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "ذخیره متن مکالمه",
            str(Path.home() / default_name),
            "Text Files (*.txt);;All Files (*)",
        )

        if not filepath:
            return

        try:
            text = self._build_transcript()
            Path(filepath).write_text(text, encoding="utf-8")
            QMessageBox.information(
                self, "✅ ذخیره شد", f"فایل ذخیره شد:\n{filepath}"
            )
            logger.info(f"متن مکالمه ذخیره شد: {filepath}")

        except Exception as e:
            QMessageBox.critical(self, "خطا", f"ذخیره ناموفق بود:\n{e}")

    def _build_transcript(self) -> str:
        """ساخت متن کامل مکالمه"""
        lines = []
        lines.append("=" * 60)
        lines.append("📞 متن مکالمه")
        lines.append("=" * 60)

        if self.call_start_time:
            lines.append(f"شروع: {self.call_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        if self.context:
            lines.append(f"شماره تماس‌گیرنده: {self.context.caller_phone}")
        lines.append("-" * 60)

        for msg in self.history:
            role_fa = {
                MessageRole.USER: "👤 مشتری",
                MessageRole.ASSISTANT: "🤖 بات",
                MessageRole.SYSTEM: "⚙️ سیستم",
            }.get(msg.role, "?")

            time_str = msg.timestamp.strftime("%H:%M:%S")
            lines.append(f"[{time_str}] {role_fa}:")
            lines.append(f"  {msg.content}")
            lines.append("")

        # خلاصه سفارش
        if self.context and self.context.cart:
            lines.append("=" * 60)
            lines.append("🛒 خلاصه سفارش")
            lines.append("=" * 60)
            for item in self.context.cart:
                lines.append(
                    f"  • {item['name']} × {item['quantity']} "
                    f"= {item['price'] * item['quantity']:,} تومان"
                )
            lines.append(f"\n💰 مجموع: {self.context.cart_total:,} تومان")
            if self.context.address:
                lines.append(f"📍 آدرس: {self.context.address}")

        return "\n".join(lines)

    # =========================================================
    def refresh(self):
        """بروزرسانی (در صورت نیاز)"""
        pass