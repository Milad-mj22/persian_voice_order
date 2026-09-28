"""
کنترلر صفحه تنظیمات
"""
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Qt, QTime, Signal, QTimer

from app.core.logger import logger
from app.services.settings_service import get_settings_service
from app.ui.ui_loader import get_ui_class


class SettingsController(QWidget):
    """صفحه تنظیمات"""

    settings_saved = Signal()  # وقتی تنظیمات ذخیره شد

    # =========================================================
    # نگاشت نام‌های UI به کلیدهای Settings
    # =========================================================
    LINE_EDIT_FIELDS = {
        "business_name_edit": "business_name",
        "address_edit": "address",
        "phone_edit": "phone",
        "delivery_area_edit": "delivery_area",
        "payment_methods_edit": "payment_methods",
        "phone_confirm_msg_edit": "phone_confirm_message",
        "ask_phone_again_msg_edit": "ask_phone_again_message",
        "invalid_phone_msg_edit": "invalid_phone_message",
    }

    TEXT_EDIT_FIELDS = {
        "business_goal_edit": "business_goal",
        "welcome_message_edit": "welcome_message",
        "goodbye_message_edit": "goodbye_message",
        "discount_policy_edit": "discount_policy",
        "brand_story_edit": "brand_story",
    }

    COMBO_FIELDS = {
        "humor_combo": "humor",
        "language_combo": "language",
    }

    SPIN_FIELDS = {
        "max_phone_retry_spin": "max_phone_retry",
    }

    CHECK_FIELDS = {
        "ask_phone_confirmation_check": "ask_phone_confirmation",
    }

    TIME_FIELDS = {
        "open_time_edit": "open_time",
        "close_time_edit": "close_time",
    }

    # متن برچسب لحن
    TONE_LABELS = {
        0: "۰ - کاملاً رسمی",
        1: "۱ - رسمی",
        2: "۲ - نسبتاً رسمی",
        3: "۳ - کمی رسمی",
        4: "۴ - نزدیک به متعادل",
        5: "۵ - متعادل",
        6: "۶ - نزدیک به صمیمی",
        7: "۷ - کمی صمیمی",
        8: "۸ - نسبتاً صمیمی",
        9: "۹ - صمیمی",
        10: "۱۰ - کاملاً صمیمی",
    }

    # =========================================================
    # سازنده
    # =========================================================
    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = get_settings_service()
        self._loading = False  # برای جلوگیری از trigger سیگنال‌ها هنگام بارگذاری

        # لود UI
        ui_class = get_ui_class("settings_page")
        self.ui = ui_class()
        self.ui.setupUi(self)

        # اتصال سیگنال‌ها
        self._connect_signals()

        # بارگذاری
        self.load_settings()

        logger.info("صفحه تنظیمات ساخته شد")

    # =========================================================
    # اتصال سیگنال‌ها
    # =========================================================
    def _connect_signals(self):
        # دکمه‌ها
        self.ui.save_btn.clicked.connect(self.save_settings)
        self.ui.reset_btn.clicked.connect(self.reset_settings)

        # Slider لحن
        self.ui.tone_slider.valueChanged.connect(self._on_tone_changed)

        # پیام موفقیت
        self._status_timer = QTimer(self)
        self._status_timer.setSingleShot(True)
        self._status_timer.timeout.connect(self._clear_status)

    # =========================================================
    # بارگذاری
    # =========================================================
    def load_settings(self):
        """بارگذاری تنظیمات از سرویس به UI"""
        self._loading = True

        try:
            s = self.settings.get_all()

            # LineEdits
            for widget_name, key in self.LINE_EDIT_FIELDS.items():
                widget = getattr(self.ui, widget_name, None)
                if widget is not None:
                    widget.setText(str(s.get(key, "")))

            # TextEdits
            for widget_name, key in self.TEXT_EDIT_FIELDS.items():
                widget = getattr(self.ui, widget_name, None)
                if widget is not None:
                    widget.setPlainText(str(s.get(key, "")))

            # Combos
            for widget_name, key in self.COMBO_FIELDS.items():
                widget = getattr(self.ui, widget_name, None)
                if widget is not None:
                    value = str(s.get(key, ""))
                    idx = widget.findText(value)
                    if idx >= 0:
                        widget.setCurrentIndex(idx)

            # SpinBoxes
            for widget_name, key in self.SPIN_FIELDS.items():
                widget = getattr(self.ui, widget_name, None)
                if widget is not None:
                    try:
                        widget.setValue(int(s.get(key, 0)))
                    except (ValueError, TypeError):
                        widget.setValue(0)

            # CheckBoxes
            for widget_name, key in self.CHECK_FIELDS.items():
                widget = getattr(self.ui, widget_name, None)
                if widget is not None:
                    widget.setChecked(bool(s.get(key, False)))

            # TimeEdits
            for widget_name, key in self.TIME_FIELDS.items():
                widget = getattr(self.ui, widget_name, None)
                if widget is not None:
                    time_str = str(s.get(key, "00:00"))
                    try:
                        h, m = time_str.split(":")
                        widget.setTime(QTime(int(h), int(m)))
                    except (ValueError, AttributeError):
                        widget.setTime(QTime(0, 0))

            # Slider لحن
            tone = int(s.get("tone", 5))
            self.ui.tone_slider.setValue(tone)
            self._update_tone_label(tone)

            logger.debug("تنظیمات در UI بارگذاری شد")

        finally:
            self._loading = False

    # =========================================================
    # ذخیره
    # =========================================================
    def save_settings(self):
        """خواندن UI و ذخیره در سرویس"""
        try:
            data: dict = {}

            # LineEdits
            for widget_name, key in self.LINE_EDIT_FIELDS.items():
                widget = getattr(self.ui, widget_name, None)
                if widget is not None:
                    data[key] = widget.text().strip()

            # TextEdits
            for widget_name, key in self.TEXT_EDIT_FIELDS.items():
                widget = getattr(self.ui, widget_name, None)
                if widget is not None:
                    data[key] = widget.toPlainText().strip()

            # Combos
            for widget_name, key in self.COMBO_FIELDS.items():
                widget = getattr(self.ui, widget_name, None)
                if widget is not None:
                    data[key] = widget.currentText()

            # SpinBoxes
            for widget_name, key in self.SPIN_FIELDS.items():
                widget = getattr(self.ui, widget_name, None)
                if widget is not None:
                    data[key] = widget.value()

            # CheckBoxes
            for widget_name, key in self.CHECK_FIELDS.items():
                widget = getattr(self.ui, widget_name, None)
                if widget is not None:
                    data[key] = widget.isChecked()

            # TimeEdits
            for widget_name, key in self.TIME_FIELDS.items():
                widget = getattr(self.ui, widget_name, None)
                if widget is not None:
                    data[key] = widget.time().toString("HH:mm")

            # Slider لحن
            data["tone"] = self.ui.tone_slider.value()

            # ذخیره
            success = self.settings.save_all(data)

            if success:
                self._show_status("✅  تنظیمات با موفقیت ذخیره شد", "success")
                self.settings_saved.emit()
                logger.info("تنظیمات از UI ذخیره شد")
            else:
                self._show_status("❌  خطا در ذخیره تنظیمات", "error")
                QMessageBox.warning(
                    self, "خطا", "ذخیره تنظیمات ناموفق بود."
                )

        except Exception as e:
            logger.error(f"خطا در ذخیره تنظیمات: {e}")
            QMessageBox.critical(
                self, "خطا", f"خطای غیرمنتظره:\n{e}"
            )

    # =========================================================
    # بازنشانی
    # =========================================================
    def reset_settings(self):
        """بازگشت به مقادیر پیش‌فرض"""
        reply = QMessageBox.question(
            self,
            "تایید بازنشانی",
            "آیا مطمئن هستید که می‌خواهید همه تنظیمات را به حالت پیش‌فرض برگردانید؟",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        try:
            if self.settings.reset_to_defaults():
                self.load_settings()
                self._show_status("↺  تنظیمات به پیش‌فرض بازگشت", "success")
                self.settings_saved.emit()
                logger.info("تنظیمات به پیش‌فرض بازگشت")
            else:
                self._show_status("❌  خطا در بازنشانی", "error")

        except Exception as e:
            logger.error(f"خطا در بازنشانی: {e}")
            QMessageBox.critical(self, "خطا", f"خطای غیرمنتظره:\n{e}")

    # =========================================================
    # رویدادهای کوچک
    # =========================================================
    def _on_tone_changed(self, value: int):
        """وقتی کاربر Slider لحن را حرکت داد"""
        self._update_tone_label(value)

    def _update_tone_label(self, value: int):
        """آپدیت متن برچسب لحن"""
        text = self.TONE_LABELS.get(value, str(value))
        self.ui.tone_label.setText(text)

    def _show_status(self, message: str, kind: str = "info"):
        """نمایش پیام وضعیت"""
        colors = {
            "success": "#16a34a",
            "error": "#dc2626",
            "info": "#2563eb",
        }
        color = colors.get(kind, "#2563eb")
        self.ui.status_label.setStyleSheet(
            f"color: {color}; font-weight: bold;"
        )
        self.ui.status_label.setText(message)

        # پاک کردن بعد از ۴ ثانیه
        self._status_timer.start(4000)

    def _clear_status(self):
        """پاک کردن پیام وضعیت"""
        self.ui.status_label.setText("")
        self.ui.status_label.setStyleSheet("")