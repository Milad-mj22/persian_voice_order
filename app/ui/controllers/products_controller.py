"""
کنترلر صفحه مدیریت محصولات
"""
from PySide6.QtWidgets import (
    QWidget, QMessageBox, QTableWidgetItem, QHeaderView, QDialog
)
from PySide6.QtCore import Qt, Signal

from app.core.logger import logger
from app.services.product_service import get_product_service
from app.ui.ui_loader import get_ui_class
from app.ui.controllers.product_edit_dialog import ProductEditDialog


class ProductsController(QWidget):
    """صفحه مدیریت محصولات"""

    products_changed = Signal()

    # ستون‌های جدول
    COL_ID = 0
    COL_NAME = 1
    COL_CATEGORY = 2
    COL_PRICE = 3
    COL_STOCK = 4
    COL_ACTIVE = 5
    COL_FEATURED = 6

    def __init__(self, parent=None):
        super().__init__(parent)

        self.product_service = get_product_service()

        # لود UI
        ui_class = get_ui_class("products_page")
        self.ui = ui_class()
        self.ui.setupUi(self)

        # اتصال‌ها
        self._connect_signals()

        # تنظیم جدول
        self._setup_table()

        # بارگذاری داده
        self.load_products()

        logger.info("صفحه محصولات ساخته شد")

    # =========================================================
    def _connect_signals(self):
        self.ui.add_btn.clicked.connect(self.add_product)
        self.ui.edit_btn.clicked.connect(self.edit_product)
        self.ui.delete_btn.clicked.connect(self.delete_product)
        self.ui.refresh_btn.clicked.connect(self.load_products)

        # دابل‌کلیک روی ردیف → ویرایش
        self.ui.products_table.doubleClicked.connect(self.edit_product)

        # جستجو (با debounce طبیعی)
        self.ui.search_edit.textChanged.connect(self.load_products)

        # فیلتر دسته
        self.ui.category_combo.currentTextChanged.connect(self.load_products)

    def _setup_table(self):
        """تنظیمات ظاهری جدول"""
        table = self.ui.products_table

        # ارتفاع ردیف‌ها
        table.verticalHeader().setDefaultSectionSize(40)
        table.verticalHeader().setVisible(False)

        # عرض ستون‌ها
        header = table.horizontalHeader()
        header.setSectionResizeMode(self.COL_ID, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(self.COL_NAME, QHeaderView.Stretch)
        header.setSectionResizeMode(self.COL_CATEGORY, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(self.COL_PRICE, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(self.COL_STOCK, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(self.COL_ACTIVE, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(self.COL_FEATURED, QHeaderView.ResizeToContents)

    # =========================================================
    def load_products(self):
        """بارگذاری محصولات با فیلترهای فعلی"""
        try:
            search = self.ui.search_edit.text().strip()
            category = self.ui.category_combo.currentText().strip()
            if category == "همه دسته‌ها":
                category = ""

            products = self.product_service.get_all(
                search=search or None,
                category=category or None,
            )

            self._fill_table(products)
            self._update_categories_combo()
            self._update_stats(len(products))

        except Exception as e:
            logger.error(f"خطا در بارگذاری محصولات: {e}")
            QMessageBox.critical(self, "خطا", f"بارگذاری محصولات ناموفق بود:\n{e}")

    def _fill_table(self, products):
        """پر کردن جدول با محصولات"""
        table = self.ui.products_table
        table.setSortingEnabled(False)
        table.setRowCount(0)

        for p in products:
            row = table.rowCount()
            table.insertRow(row)

            # شناسه
            item_id = QTableWidgetItem()
            item_id.setData(Qt.DisplayRole, p.id)
            table.setItem(row, self.COL_ID, item_id)

            # نام
            table.setItem(row, self.COL_NAME, QTableWidgetItem(p.name))

            # دسته
            table.setItem(row, self.COL_CATEGORY, QTableWidgetItem(p.category))

            # قیمت (با sortable data)
            item_price = QTableWidgetItem()
            item_price.setData(Qt.DisplayRole, p.price)
            item_price.setText(p.price_formatted + " تومان")
            table.setItem(row, self.COL_PRICE, item_price)

            # موجودی
            item_stock = QTableWidgetItem()
            item_stock.setData(Qt.DisplayRole, p.stock)
            if p.stock == 0:
                item_stock.setText("❌ ناموجود")
                item_stock.setForeground(Qt.red)
            elif p.stock < 5:
                item_stock.setText(f"⚠️  {p.stock}")
                item_stock.setForeground(Qt.darkYellow)
            else:
                item_stock.setText(f"✅  {p.stock}")
                item_stock.setForeground(Qt.darkGreen)
            table.setItem(row, self.COL_STOCK, item_stock)

            # فعال
            active_text = "✅ فعال" if p.is_active else "⛔ غیرفعال"
            table.setItem(row, self.COL_ACTIVE, QTableWidgetItem(active_text))

            # ویژه
            featured_text = "⭐" if p.is_featured else ""
            table.setItem(row, self.COL_FEATURED, QTableWidgetItem(featured_text))

            # ذخیره ID در UserRole
            table.item(row, self.COL_NAME).setData(Qt.UserRole, p.id)

        table.setSortingEnabled(True)

    def _update_categories_combo(self):
        """آپدیت کمبوباکس دسته‌بندی"""
        combo = self.ui.category_combo
        current = combo.currentText()

        categories = self.product_service.get_categories()
        combo.blockSignals(True)
        combo.clear()
        combo.addItem("همه دسته‌ها")
        for c in categories:
            combo.addItem(c)

        # بازگرداندن انتخاب قبلی
        idx = combo.findText(current)
        if idx >= 0:
            combo.setCurrentIndex(idx)
        combo.blockSignals(False)

    def _update_stats(self, count: int):
        """آپدیت نوار وضعیت"""
        total = self.product_service.count()
        active = self.product_service.count(only_active=True)
        self.ui.stats_label.setText(
            f"📊  نمایش: {count}  |  کل: {total}  |  فعال: {active}"
        )

    # =========================================================
    def _get_selected_product_id(self) -> int | None:
        """گرفتن ID محصول انتخاب‌شده"""
        row = self.ui.products_table.currentRow()
        if row < 0:
            return None
        item = self.ui.products_table.item(row, self.COL_NAME)
        if item is None:
            return None
        return item.data(Qt.UserRole)

    # =========================================================
    def add_product(self):
        """افزودن محصول جدید"""
        categories = self.product_service.get_categories()
        dialog = ProductEditDialog(
            product=None, categories=categories, parent=self
        )

        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            product = self.product_service.create(data)
            if product:
                logger.info(f"محصول جدید: {product.name}")
                self.load_products()
                self.products_changed.emit()
            else:
                QMessageBox.warning(
                    self, "خطا", "ساخت محصول ناموفق بود."
                )

    def edit_product(self):
        """ویرایش محصول انتخاب‌شده"""
        product_id = self._get_selected_product_id()
        if product_id is None:
            QMessageBox.information(
                self, "توجه", "لطفاً یک محصول را انتخاب کنید."
            )
            return

        product = self.product_service.get_by_id(product_id)
        if product is None:
            QMessageBox.warning(self, "خطا", "محصول پیدا نشد.")
            self.load_products()
            return

        categories = self.product_service.get_categories()
        dialog = ProductEditDialog(
            product=product, categories=categories, parent=self
        )

        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            updated = self.product_service.update(product_id, data)
            if updated:
                logger.info(f"محصول آپدیت شد: {updated.name}")
                self.load_products()
                self.products_changed.emit()
            else:
                QMessageBox.warning(
                    self, "خطا", "آپدیت محصول ناموفق بود."
                )

    def delete_product(self):
        """حذف محصول انتخاب‌شده"""
        product_id = self._get_selected_product_id()
        if product_id is None:
            QMessageBox.information(
                self, "توجه", "لطفاً یک محصول را انتخاب کنید."
            )
            return

        product = self.product_service.get_by_id(product_id)
        if product is None:
            return

        reply = QMessageBox.question(
            self,
            "تایید حذف",
            f"آیا از حذف «{product.name}» مطمئن هستید؟",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        if self.product_service.delete(product_id):
            logger.info(f"محصول حذف شد: {product.name}")
            self.load_products()
            self.products_changed.emit()
        else:
            QMessageBox.warning(self, "خطا", "حذف محصول ناموفق بود.")

    # =========================================================
    def refresh(self):
        """درخواست بروزرسانی از بیرون"""
        self.load_products()