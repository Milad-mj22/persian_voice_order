# app/ui/ui_loader.py
"""
لودر کلاس‌های تولیدشده از .ui
"""
import importlib
from typing import Type

from app.core.logger import logger


UI_REGISTRY = {
    "main_window": ("ui_main_window", "Ui_MainWindow"),
    "dashboard_page": ("ui_dashboard_page", "Ui_DashboardPage"),
    "test_call_page": ("ui_test_call_page", "Ui_TestCallPage"),
    "orders_page": ("ui_orders_page", "Ui_OrdersPage"),
    "products_page": ("ui_products_page", "Ui_ProductsPage"),
    "settings_page": ("ui_settings_page", "Ui_SettingsPage"),
    "conversation_page": ("ui_conversation_page", "Ui_ConversationPage"),
    "knowledge_page": ("ui_knowledge_page", "Ui_KnowledgePage"),
    "reports_page": ("ui_reports_page", "Ui_ReportsPage"),
    "product_edit_dialog": (
        "dialogs.ui_product_edit_dialog",
        "Ui_ProductEditDialog",
    ),
    "order_detail_dialog": (
        "dialogs.ui_order_detail_dialog",
        "Ui_OrderDetailDialog",
    ),
    "about_dialog": ("dialogs.ui_about_dialog", "Ui_AboutDialog"),
}


def get_ui_class(ui_name: str) -> Type:
    if ui_name not in UI_REGISTRY:
        raise KeyError(
            f"UI با نام '{ui_name}' ثبت نشده. "
            f"موجود: {list(UI_REGISTRY.keys())}"
        )
    module_name, class_name = UI_REGISTRY[ui_name]
    full_module = f"app.ui.ui_generated.{module_name}"
    try:
        module = importlib.import_module(full_module)
        return getattr(module, class_name)
    except ImportError as e:
        raise ImportError(
            f"ماژول '{full_module}' لود نشد. "
            f"آیا 'python compile_ui.py' را اجرا کرده‌ای؟\n{e}"
        )
    except AttributeError as e:
        raise AttributeError(
            f"کلاس '{class_name}' در '{full_module}' پیدا نشد.\n{e}"
        )


def load_ui(ui_name: str, widget) -> object:
    ui_class = get_ui_class(ui_name)
    ui = ui_class()
    ui.setupUi(widget)
    return ui