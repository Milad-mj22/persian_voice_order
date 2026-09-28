"""
دیالوگ افزودن/ویرایش محصول
"""
from PySide6.QtWidgets import QDialog, QMessageBox, QComboBox
from PySide6.QtCore import Qt

from app.core.logger import logger
from app.ui.ui_loader import get_ui_class


class ProductEditDialog(QDialog):
    """دیالوگ فرم محصول"""

    def __init__(self, product=None, categories=None, parent=None):
        """
        product: اگر None باشد → افزودن، وگرنه ویرایش
        categories: لیست دسته‌بندی‌های موجود
        """
        super().__init__(parent)

        self.product = product
        self.is_edit = product is not None

        # لود UI
        ui_class = get_ui_class("product_edit_dialog")
        self.ui = ui_class()
        self.ui.setupUi(self)

        # تنظیمات
        self.setModal(True)
        self.setWindowTitle("ویرایش محصول" if self.is_edit else "افزودن محصول جدید")
        self.ui.dialog_title.setText(
            "✏️  ویرایش محصول" if self.is_edit else "➕  افزودن محصول جدید"
        )

        # پر کردن دسته‌بندی‌ها
        self._populate_categories(categories or [])

        # اتصال دکمه‌ها
        self.ui.save_btn.clicked.connect(self._on_save)
        self.ui.cancel_btn.clicked.connect(self.reject)

        # اگر ویرایش است، مقادیر را پر کن
        if self.is_edit:
            self._load_product()

        # پاک کردن پیام خطا
        self.ui.error_label.setText("")

    # =========================================================
    def _populate_categories(self, categories: list):
        """پر کردن ComboBox دسته‌بندی"""
        # پاک کردن
        self.ui.category_combo.clear()

        # پیش‌فرض‌ها
        defaults = ["پیتزا", "برگر", "ساندویچ", "نوشیدنی", "پیش‌غذا", "دسر"]
        all_cats = list(dict.fromkeys(defaults + list(categories)))  # حذف تکراری

        for cat in all_cats:
            self.ui.category_combo.addItem(cat)

    def _load_product(self):
        """بارگذاری اطلاعات محصول در فرم"""
        p = self.product
        self.ui.name_edit.setText(p.name)

        # انتخاب دسته‌بندی
        idx = self.ui.category_combo.findText(p.category)
        if idx >= 0:
            self.ui.category_combo.setCurrentIndex(idx)
        else:
            self.ui.category_combo.setEditText(p.category)

        self.ui.price_spin.setValue(p.price)
        self.ui.stock_spin.setValue(p.stock)
        self.ui.display_order_spin.setValue(p.display_order)
        self.ui.description_edit.setPlainText(p.description or "")
        self.ui.is_active_check.setChecked(p.is_active)
        self.ui.is_featured_check.setChecked(p.is_featured)

    # =========================================================
    def _on_save(self):
        """اعتبارسنجی و ذخیره"""
        # پاک کردن خطا
        self.ui.error_label.setText("")

        # اعتبارسنجی
        name = self.ui.name_edit.text().strip()
        if not name:
            self._show_error("نام محصول الزامی است")
            self.ui.name_edit.setFocus()
            return

        category = self.ui.category_combo.currentText().strip()
        if not category:
            self._show_error("دسته‌بندی الزامی است")
            self.ui.category_combo.setFocus()
            return

        price = self.ui.price_spin.value()
        if price <= 0:
            self._show_error("قیمت باید بزرگتر از صفر باشد")
            self.ui.price_spin.setFocus()
            return

        # همه چیز اوکی → پذیرش دیالوگ
        self.accept()

    def _show_error(self, message: str):
        """نمایش خطا"""
        self.ui.error_label.setText(f"❌  {message}")
        self.ui.error_label.setStyleSheet(
            "color: #dc2626; font-weight: bold; padding: 6px;"
        )

    # =========================================================
    def get_data(self) -> dict:
        """گرفتن داده‌های فرم"""
        return {
            "name": self.ui.name_edit.text().strip(),
            "category": self.ui.category_combo.currentText().strip(),
            "price": self.ui.price_spin.value(),
            "stock": self.ui.stock_spin.value(),
            "display_order": self.ui.display_order_spin.value(),
            "description": self.ui.description_edit.toPlainText().strip(),
            "is_active": self.ui.is_active_check.isChecked(),
            "is_featured": self.ui.is_featured_check.isChecked(),
        }