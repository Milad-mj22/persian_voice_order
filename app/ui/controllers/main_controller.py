"""
کنترلر پنجره اصلی
"""
from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget
from PySide6.QtCore import Signal
from app.ui.controllers.test_call_controller import TestCallController
from app.core.config_manager import ConfigManager
from app.core.logger import logger
from app.ui.ui_loader import get_ui_class
from app.ui.controllers.settings_controller import SettingsController
from app.ui.controllers.products_controller import ProductsController

class MainController(QMainWindow):
    """پنجره اصلی برنامه"""

    page_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.config = ConfigManager()

        ui_class = get_ui_class("main_window")
        self.ui = ui_class()
        self.ui.setupUi(self)

        self._pages: dict[str, QWidget] = {}

        self._connect_navigation()
        self._setup_ui()

        # ⭐ ثبت صفحات واقعی
        self._register_real_pages()

        self.switch_page("dashboard")

        logger.info("پنجره اصلی ساخته شد")

    # =========================================================
    def _setup_ui(self):
        app_name = self.config.get("app.name", "سامانه سفارش‌گیری")
        self.setWindowTitle(app_name)

        version = self.config.get("app.version", "0.1.0")
        self.ui.version_label.setText(f"نسخه {version}")

        self.ui.statusBar.showMessage("آماده")

    def _connect_navigation(self):
        self.ui.btn_dashboard.clicked.connect(lambda: self.switch_page("dashboard"))
        self.ui.btn_products.clicked.connect(lambda: self.switch_page("products"))
        self.ui.btn_orders.clicked.connect(lambda: self.switch_page("orders"))
        self.ui.btn_test_call.clicked.connect(lambda: self.switch_page("test_call"))
        self.ui.btn_reports.clicked.connect(lambda: self.switch_page("reports"))
        self.ui.btn_settings.clicked.connect(lambda: self.switch_page("settings"))

    # =========================================================
    def _register_real_pages(self):
        """ثبت صفحات واقعی"""
        try:
            self.register_page("settings", SettingsController(parent=self))
            logger.info("صفحه تنظیمات ثبت شد")
        except Exception as e:
            logger.error(f"خطا در ثبت صفحه تنظیمات: {e}")

        try:
            self.register_page("test_call", TestCallController(parent=self))
            logger.info("صفحه تست تماس ثبت شد")
        except Exception as e:
            logger.error(f"خطا در ثبت صفحه تست تماس: {e}")
            
        try:
            # صفحه محصولات
            self.register_page("products", ProductsController(parent=self))
            logger.info("صفحه محصولات ثبت شد")
        except Exception as e:
            logger.error(f"خطا در ثبت صفحه محصولات: {e}")


    # =========================================================
    PAGE_INDEX = {
        "dashboard": 0,
        "products": 1,
        "orders": 2,
        "test_call": 3,
        "reports": 4,
        "settings": 5,
    }

    PAGE_BUTTONS = {
        "dashboard": "btn_dashboard",
        "products": "btn_products",
        "orders": "btn_orders",
        "test_call": "btn_test_call",
        "reports": "btn_reports",
        "settings": "btn_settings",
    }

    PAGE_TITLES = {
        "dashboard": "📊 داشبورد",
        "products": "🍕 مدیریت محصولات",
        "orders": "📋 سفارشات",
        "test_call": "📞 تست تماس",
        "reports": "📈 گزارشات",
        "settings": "⚙️ تنظیمات",
    }

    def switch_page(self, page_name: str):
        if page_name not in self.PAGE_INDEX:
            logger.warning(f"صفحه ناشناخته: {page_name}")
            return

        index = self.PAGE_INDEX[page_name]
        self.ui.stacked_widget.setCurrentIndex(index)
        self._update_sidebar_buttons(page_name)

        title = self.PAGE_TITLES.get(page_name, page_name)
        self.ui.statusBar.showMessage(f"صفحه: {title}")

        self.page_changed.emit(page_name)
        logger.debug(f"تغییر صفحه به: {page_name}")

    def _update_sidebar_buttons(self, active_page: str):
        for page, btn_name in self.PAGE_BUTTONS.items():
            btn: QPushButton = getattr(self.ui, btn_name)
            btn.setChecked(page == active_page)

    # =========================================================
    def register_page(self, name: str, widget: QWidget):
        if name not in self.PAGE_INDEX:
            logger.warning(f"ثبت صفحه ناشناخته: {name}")
            return

        index = self.PAGE_INDEX[name]
        old_widget = self.ui.stacked_widget.widget(index)

        if old_widget is not None:
            self.ui.stacked_widget.removeWidget(old_widget)
            old_widget.deleteLater()

        self.ui.stacked_widget.insertWidget(index, widget)
        self._pages[name] = widget

        logger.debug(f"صفحه ثبت شد: {name} در ایندکس {index}")

    def get_page(self, name: str) -> QWidget | None:
        return self._pages.get(name)