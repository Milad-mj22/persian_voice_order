"""
کنترلر صفحه سفارشات
"""
import csv
from datetime import datetime
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget, QMessageBox, QTableWidgetItem, QHeaderView,
    QFileDialog, QDialog,
)
from PySide6.QtCore import Qt, Signal

from app.core.logger import logger
from app.models.order import Order
from app.services.order_service import get_order_service
from app.ui.ui_loader import get_ui_class
from app.ui.controllers.order_detail_dialog import OrderDetailDialog


class OrdersController(QWidget):
    """صفحه سفارشات"""

    orders_changed = Signal()

    COL_CODE = 0
    COL_DATE = 1
    COL_PHONE = 2
    COL_ADDRESS = 3
    COL_ITEMS = 4
    COL_TOTAL = 5
    COL_STATUS = 6

    def __init__(self, parent=None):
        super().__init__(parent)

        self.order_service = get_order_service()

        ui_class = get_ui_class("orders_page")
        self.ui = ui_class()
        self.ui.setupUi(self)

        self._setup_table()
        self._setup_filters()
        self._connect_signals()
        self.load_orders()

        logger.info("صفحه سفارشات ساخته شد")

    # =========================================================
    def _setup_table(self):
        table = self.ui.orders_table
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(38)

        header = table.horizontalHeader()
        header.setSectionResizeMode(self.COL_CODE, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(self.COL_DATE, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(self.COL_PHONE, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(self.COL_ADDRESS, QHeaderView.Stretch)
        header.setSectionResizeMode(self.COL_ITEMS, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(self.COL_TOTAL, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(self.COL_STATUS, QHeaderView.ResizeToContents)

    def _setup_filters(self):
        combo = self.ui.status_combo
        combo.addItem("همه", "همه")
        for code, label in Order.STATUS_LABELS.items():
            combo.addItem(label, code)

    def _connect_signals(self):
        self.ui.refresh_btn.clicked.connect(self.load_orders)
        self.ui.search_edit.textChanged.connect(self.load_orders)
        self.ui.status_combo.currentIndexChanged.connect(self.load_orders)
        self.ui.view_btn.clicked.connect(self.view_order)
        self.ui.delete_btn.clicked.connect(self.delete_order)
        self.ui.export_btn.clicked.connect(self.export_csv)
        self.ui.orders_table.doubleClicked.connect(self.view_order)

    # =========================================================
    def load_orders(self):
        """بارگذاری سفارشات"""
        try:
            search = self.ui.search_edit.text().strip()
            status = self.ui.status_combo.currentData()

            orders = self.order_service.get_all(
                status=status,
                search=search or None,
            )
            self._fill_table(orders)
            self._update_stats(len(orders))

        except Exception as e:
            logger.exception(f"خطا در بارگذاری سفارشات: {e}")

    def _fill_table(self, orders):
        table = self.ui.orders_table
        table.setSortingEnabled(False)
        table.setRowCount(0)

        status_colors = {
            "pending": "#f59e0b",
            "confirmed": "#3b82f6",
            "delivered": "#16a34a",
            "cancelled": "#dc2626",
        }

        for o in orders:
            row = table.rowCount()
            table.insertRow(row)

            # کد
            item_code = QTableWidgetItem(o.order_code)
            item_code.setData(Qt.UserRole, o.id)
            table.setItem(row, self.COL_CODE, item_code)

            # تاریخ
            date_str = o.created_at.strftime("%m/%d %H:%M") if o.created_at else "-"
            table.setItem(row, self.COL_DATE, QTableWidgetItem(date_str))

            # شماره
            table.setItem(row, self.COL_PHONE, QTableWidgetItem(o.order_phone or "-"))

            # آدرس
            addr = o.address or "-"
            table.setItem(row, self.COL_ADDRESS, QTableWidgetItem(addr[:60]))

            # اقلام
            items_count = o.items_count
            table.setItem(row, self.COL_ITEMS, QTableWidgetItem(str(items_count)))

            # مبلغ
            item_total = QTableWidgetItem()
            item_total.setData(Qt.DisplayRole, o.total_price)
            item_total.setText(f"{o.total_price:,}")
            table.setItem(row, self.COL_TOTAL, item_total)

            # وضعیت
            status_label = Order.STATUS_LABELS.get(o.status, o.status)
            item_status = QTableWidgetItem(status_label)
            item_status.setForeground(Qt.GlobalColor.black)
            if o.status in status_colors:
                from PySide6.QtGui import QColor
                item_status.setForeground(QColor(status_colors[o.status]))
            table.setItem(row, self.COL_STATUS, item_status)

        table.setSortingEnabled(True)

    def _update_stats(self, shown: int):
        total = self.order_service.count()
        total_sum = self.order_service.sum_total()
        today_count = self.order_service.count_today()
        self.ui.stats_label.setText(
            f"📊  نمایش: {shown}  |  کل: {total}  |  امروز: {today_count}  |  "
            f"فروش کل: {total_sum:,} تومان"
        )

    # =========================================================
    def _get_selected_id(self) -> int | None:
        row = self.ui.orders_table.currentRow()
        if row < 0:
            return None
        item = self.ui.orders_table.item(row, self.COL_CODE)
        if item is None:
            return None
        return item.data(Qt.UserRole)

    # =========================================================
    def view_order(self):
        """مشاهده جزئیات"""
        oid = self._get_selected_id()
        if oid is None:
            QMessageBox.information(self, "توجه", "لطفاً یک سفارش را انتخاب کنید.")
            return

        order = self.order_service.get_by_id(oid)
        if order is None:
            QMessageBox.warning(self, "خطا", "سفارش پیدا نشد.")
            return

        dialog = OrderDetailDialog(order, parent=self)
        if dialog.exec() == QDialog.Accepted:
            self.load_orders()
            self.orders_changed.emit()

    def delete_order(self):
        """حذف سفارش"""
        oid = self._get_selected_id()
        if oid is None:
            QMessageBox.information(self, "توجه", "لطفاً یک سفارش را انتخاب کنید.")
            return

        order = self.order_service.get_by_id(oid)
        if order is None:
            return

        reply = QMessageBox.question(
            self, "تایید حذف",
            f"آیا از حذف سفارش {order.order_code} مطمئن هستید؟",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        if self.order_service.delete(oid):
            self.load_orders()
            self.orders_changed.emit()
            QMessageBox.information(self, "✅", "سفارش حذف شد.")

    # =========================================================
    def export_csv(self):
        """خروجی CSV از سفارشات فعلی"""
        orders = self.order_service.get_all()
        if not orders:
            QMessageBox.information(self, "خالی", "سفارشی برای خروجی نیست.")
            return

        default_name = f"orders_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        filepath, _ = QFileDialog.getSaveFileName(
            self, "ذخیره خروجی",
            str(Path.home() / default_name),
            "CSV Files (*.csv)",
        )
        if not filepath:
            return

        try:
            with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "کد سفارش", "تاریخ", "شماره تماس", "آدرس",
                    "اقلام", "مبلغ", "وضعیت",
                ])
                for o in orders:
                    writer.writerow([
                        o.order_code,
                        o.created_at.strftime("%Y-%m-%d %H:%M") if o.created_at else "",
                        o.order_phone,
                        o.address,
                        o.items_count,
                        o.total_price,
                        Order.STATUS_LABELS.get(o.status, o.status),
                    ])
            QMessageBox.information(self, "✅", f"خروجی ذخیره شد:\n{filepath}")
        except Exception as e:
            QMessageBox.critical(self, "خطا", str(e))

    def refresh(self):
        self.load_orders()
        