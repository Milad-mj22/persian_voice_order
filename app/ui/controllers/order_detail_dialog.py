"""
دیالوگ جزئیات سفارش
"""
from PySide6.QtWidgets import QDialog, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt

from app.core.logger import logger
from app.models.order import Order
from app.services.order_service import get_order_service
from app.ui.ui_loader import get_ui_class


class OrderDetailDialog(QDialog):
    """دیالوگ جزئیات سفارش"""

    def __init__(self, order: Order, parent=None):
        super().__init__(parent)

        self.order = order
        self.order_service = get_order_service()

        ui_class = get_ui_class("order_detail_dialog")
        self.ui = ui_class()
        self.ui.setupUi(self)

        self.setModal(True)
        self.setWindowTitle(f"جزئیات سفارش {order.order_code}")
        self.ui.title_label.setText(f"📋  سفارش {order.order_code}")

        self._setup_status_combo()
        self._fill_info()
        self._fill_items()
        self._connect_signals()

    def _setup_status_combo(self):
        """پر کردن کمبوباکس وضعیت"""
        for code, label in Order.STATUS_LABELS.items():
            self.ui.status_combo.addItem(label, code)
        # انتخاب وضعیت فعلی
        idx = self.ui.status_combo.findData(self.order.status)
        if idx >= 0:
            self.ui.status_combo.setCurrentIndex(idx)

    def _fill_info(self):
        """پر کردن اطلاعات"""
        o = self.order
        self.ui.code_value.setText(o.order_code)
        self.ui.phone_value.setText(o.caller_phone or "-")
        self.ui.order_phone_value.setText(o.order_phone or "-")
        self.ui.address_value.setText(o.address or "-")
        self.ui.date_value.setText(
            o.created_at.strftime("%Y/%m/%d - %H:%M") if o.created_at else "-"
        )

        # متن مکالمه
        if o.transcript:
            self.ui.transcript_edit.setPlainText(o.transcript)
        else:
            self.ui.transcript_edit.setPlainText("متن مکالمه ثبت نشده است.")

    def _fill_items(self):
        """پر کردن جدول اقلام"""
        table = self.ui.items_table
        items = self.order.items or []

        table.setRowCount(0)
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(36)
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        for i in range(1, 4):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        total = 0
        for item in items:
            name = item.get("name", "?")
            qty = int(item.get("quantity", 1))
            price = int(item.get("price", 0))
            sub = qty * price
            total += sub

            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(name))
            table.setItem(row, 1, QTableWidgetItem(str(qty)))
            table.setItem(row, 2, QTableWidgetItem(f"{price:,}"))
            table.setItem(row, 3, QTableWidgetItem(f"{sub:,}"))

        self.ui.total_label.setText(f"💰  مجموع: {total:,} تومان")

    def _connect_signals(self):
        self.ui.close_btn.clicked.connect(self.reject)
        self.ui.save_btn.clicked.connect(self._save)
        self.ui.toggle_transcript_btn.toggled.connect(
            self._toggle_transcript
        )

    def _toggle_transcript(self, checked: bool):
        """نمایش/مخفی متن مکالمه"""
        if checked:
            self.ui.transcript_edit.setVisible(True)
            self.ui.transcript_edit.setMaximumHeight(200)
            self.ui.toggle_transcript_btn.setText("🔽  مخفی کردن متن مکالمه")
        else:
            self.ui.transcript_edit.setVisible(False)
            self.ui.transcript_edit.setMaximumHeight(0)
            self.ui.toggle_transcript_btn.setText("📝  نمایش متن مکالمه")

    def _save(self):
        """ذخیره تغییرات (فقط وضعیت)"""
        new_status = self.ui.status_combo.currentData()
        if new_status != self.order.status:
            if self.order_service.update_status(self.order.id, new_status):
                logger.info(f"وضعیت {self.order.order_code} → {new_status}")
        self.accept()