"""
کنترلر صفحه گزارشات
"""
import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from app.core.logger import logger
from app.services.order_service import get_order_service
from app.ui.ui_loader import get_ui_class


class ReportsController(QWidget):
    """صفحه گزارشات"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.order_service = get_order_service()

        ui_class = get_ui_class("reports_page")
        self.ui = ui_class()
        self.ui.setupUi(self)

        # ساخت نمودار
        self._setup_chart()

        # لود داده
        self.load_stats()

        logger.info("صفحه گزارشات ساخته شد")

    def _setup_chart(self):
        """ساخت نمودار با pyqtgraph"""
        # پاک کردن layout قبلی
        layout = self.ui.chart_container.layout()
        if layout is None:
            layout = QVBoxLayout(self.ui.chart_container)
            layout.setContentsMargins(0, 0, 0, 0)
        else:
            while layout.count():
                item = layout.takeAt(0)
                w = item.widget()
                if w:
                    w.deleteLater()

        # تنظیمات ظاهری
        pg.setConfigOptions(antialias=True, background="#ffffff", foreground="#1e293b")

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel("right", "فروش (تومان)")
        self.plot_widget.setLabel("bottom", "تاریخ")
        self.plot_widget.showGrid(x=False, y=True, alpha=0.2)
        self.plot_widget.setMouseEnabled(x=False, y=False)

        layout.addWidget(self.plot_widget)

    def load_stats(self):
        """بارگذاری آمار"""
        try:
            # کارت‌ها
            today_count = self.order_service.count_today()
            today_sum = self.order_service.sum_today()
            total_count = self.order_service.count()
            total_sum = self.order_service.sum_total()

            self.ui.value_today_count.setText(f"{today_count:,}")
            self.ui.value_today_sum.setText(f"{today_sum:,}")
            self.ui.value_total_count.setText(f"{total_count:,}")
            self.ui.value_total_sum.setText(f"{total_sum:,}")

            # نمودار
            self._update_chart()

            # پر فروش‌ها
            self._update_top_products()

        except Exception as e:
            logger.exception(f"خطا در بارگذاری آمار: {e}")

    def _update_chart(self):
        """آپدیت نمودار فروش ۷ روز اخیر"""
        stats = self.order_service.stats_by_day(days=7)

        x = list(range(len(stats)))
        totals = [s["total"] for s in stats]
        labels = [s["label"] for s in stats]

        self.plot_widget.clear()

        if not totals or sum(totals) == 0:
            text = pg.TextItem("هنوز فروشی ثبت نشده", color="#94a3b8", anchor=(0.5, 0.5))
            self.plot_widget.addItem(text)
            text.setPos(3, 0)
            return

        # Bar graph
        bg = pg.BarGraphItem(
            x=x, height=totals, width=0.6,
            brush="#3b82f6", pen="#2563eb",
        )
        self.plot_widget.addItem(bg)

        # تنظیم محورها
        ax = self.plot_widget.getAxis("bottom")
        ax.setTicks([list(zip(x, labels))])

    def _update_top_products(self):
        """آپدیت لیست پر فروش‌ها"""
        self.ui.top_products_list.clear()
        top = self.order_service.top_products(limit=10)

        if not top:
            self.ui.top_products_list.addItem("هنوز داده‌ای موجود نیست")
            return

        medals = ["🥇", "🥈", "🥉"]
        for i, p in enumerate(top):
            medal = medals[i] if i < 3 else f"  {i + 1}."
            text = (
                f"{medal} {p['name']}\n"
                f"      {p['qty']} عدد  |  {p['revenue']:,} تومان"
            )
            item = QListWidgetItem(text)
            self.ui.top_products_list.addItem(item)

    def refresh(self):
        self.load_stats()