# -*- coding: utf-8 -*-
# ⚠️ این فایل به صورت خودکار تولید شده است.
# 📄 فایل منبع: app\ui\ui_files\main_window.ui
# 🚫 تغییرات دستی در این فایل از بین خواهند رفت.
# 🔧 برای ویرایش، فایل .ui را در Qt Designer باز کنید.
#
# تولید شده توسط: compile_ui.py
# =====================================================

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 750)
        MainWindow.setLayoutDirection(Qt.RightToLeft)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.main_layout = QHBoxLayout(self.centralWidget)
        self.main_layout.setSpacing(0)
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar = QWidget(self.centralWidget)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setMinimumSize(QSize(220, 0))
        self.sidebar.setMaximumSize(QSize(220, 16777215))
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setSpacing(6)
        self.sidebar_layout.setObjectName(u"sidebar_layout")
        self.sidebar_layout.setContentsMargins(12, 16, 12, 16)
        self.logo_label = QLabel(self.sidebar)
        self.logo_label.setObjectName(u"logo_label")
        self.logo_label.setAlignment(Qt.AlignCenter)

        self.sidebar_layout.addWidget(self.logo_label)

        self.separator = QFrame(self.sidebar)
        self.separator.setObjectName(u"separator")
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)

        self.sidebar_layout.addWidget(self.separator)

        self.btn_dashboard = QPushButton(self.sidebar)
        self.btn_dashboard.setObjectName(u"btn_dashboard")
        self.btn_dashboard.setCheckable(True)
        self.btn_dashboard.setChecked(True)
        self.btn_dashboard.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebar_layout.addWidget(self.btn_dashboard)

        self.btn_products = QPushButton(self.sidebar)
        self.btn_products.setObjectName(u"btn_products")
        self.btn_products.setCheckable(True)
        self.btn_products.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebar_layout.addWidget(self.btn_products)

        self.btn_orders = QPushButton(self.sidebar)
        self.btn_orders.setObjectName(u"btn_orders")
        self.btn_orders.setCheckable(True)
        self.btn_orders.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebar_layout.addWidget(self.btn_orders)

        self.btn_test_call = QPushButton(self.sidebar)
        self.btn_test_call.setObjectName(u"btn_test_call")
        self.btn_test_call.setCheckable(True)
        self.btn_test_call.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebar_layout.addWidget(self.btn_test_call)

        self.btn_reports = QPushButton(self.sidebar)
        self.btn_reports.setObjectName(u"btn_reports")
        self.btn_reports.setCheckable(True)
        self.btn_reports.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebar_layout.addWidget(self.btn_reports)

        self.vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sidebar_layout.addItem(self.vertical_spacer)

        self.separator_2 = QFrame(self.sidebar)
        self.separator_2.setObjectName(u"separator_2")
        self.separator_2.setFrameShape(QFrame.HLine)
        self.separator_2.setFrameShadow(QFrame.Sunken)

        self.sidebar_layout.addWidget(self.separator_2)

        self.btn_settings = QPushButton(self.sidebar)
        self.btn_settings.setObjectName(u"btn_settings")
        self.btn_settings.setCheckable(True)
        self.btn_settings.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebar_layout.addWidget(self.btn_settings)

        self.version_label = QLabel(self.sidebar)
        self.version_label.setObjectName(u"version_label")
        self.version_label.setAlignment(Qt.AlignCenter)

        self.sidebar_layout.addWidget(self.version_label)


        self.main_layout.addWidget(self.sidebar)

        self.stacked_widget = QStackedWidget(self.centralWidget)
        self.stacked_widget.setObjectName(u"stacked_widget")
        self.dashboard_page = QWidget()
        self.dashboard_page.setObjectName(u"dashboard_page")
        self.dashboard_layout = QVBoxLayout(self.dashboard_page)
        self.dashboard_layout.setObjectName(u"dashboard_layout")
        self.dashboard_title = QLabel(self.dashboard_page)
        self.dashboard_title.setObjectName(u"dashboard_title")
        self.dashboard_title.setAlignment(Qt.AlignCenter)

        self.dashboard_layout.addWidget(self.dashboard_title)

        self.stacked_widget.addWidget(self.dashboard_page)
        self.products_page = QWidget()
        self.products_page.setObjectName(u"products_page")
        self.products_layout = QVBoxLayout(self.products_page)
        self.products_layout.setObjectName(u"products_layout")
        self.products_title = QLabel(self.products_page)
        self.products_title.setObjectName(u"products_title")
        self.products_title.setAlignment(Qt.AlignCenter)

        self.products_layout.addWidget(self.products_title)

        self.stacked_widget.addWidget(self.products_page)
        self.orders_page = QWidget()
        self.orders_page.setObjectName(u"orders_page")
        self.orders_layout = QVBoxLayout(self.orders_page)
        self.orders_layout.setObjectName(u"orders_layout")
        self.orders_title = QLabel(self.orders_page)
        self.orders_title.setObjectName(u"orders_title")
        self.orders_title.setAlignment(Qt.AlignCenter)

        self.orders_layout.addWidget(self.orders_title)

        self.stacked_widget.addWidget(self.orders_page)
        self.test_call_page = QWidget()
        self.test_call_page.setObjectName(u"test_call_page")
        self.test_call_layout = QVBoxLayout(self.test_call_page)
        self.test_call_layout.setObjectName(u"test_call_layout")
        self.test_call_title = QLabel(self.test_call_page)
        self.test_call_title.setObjectName(u"test_call_title")
        self.test_call_title.setAlignment(Qt.AlignCenter)

        self.test_call_layout.addWidget(self.test_call_title)

        self.stacked_widget.addWidget(self.test_call_page)
        self.reports_page = QWidget()
        self.reports_page.setObjectName(u"reports_page")
        self.reports_layout = QVBoxLayout(self.reports_page)
        self.reports_layout.setObjectName(u"reports_layout")
        self.reports_title = QLabel(self.reports_page)
        self.reports_title.setObjectName(u"reports_title")
        self.reports_title.setAlignment(Qt.AlignCenter)

        self.reports_layout.addWidget(self.reports_title)

        self.stacked_widget.addWidget(self.reports_page)
        self.settings_page = QWidget()
        self.settings_page.setObjectName(u"settings_page")
        self.settings_layout = QVBoxLayout(self.settings_page)
        self.settings_layout.setObjectName(u"settings_layout")
        self.settings_title = QLabel(self.settings_page)
        self.settings_title.setObjectName(u"settings_title")
        self.settings_title.setAlignment(Qt.AlignCenter)

        self.settings_layout.addWidget(self.settings_title)

        self.stacked_widget.addWidget(self.settings_page)

        self.main_layout.addWidget(self.stacked_widget)

        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)

        self.stacked_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0633\u0627\u0645\u0627\u0646\u0647 \u0633\u0641\u0627\u0631\u0634\u200c\u06af\u06cc\u0631\u06cc \u0647\u0648\u0634\u0645\u0646\u062f", None))
        self.logo_label.setText(QCoreApplication.translate("MainWindow", u"\U0001f354 \U00000633\U000006a9\U00000647 \U00000637\U00000644\U00000627", None))
        self.btn_dashboard.setText(QCoreApplication.translate("MainWindow", u"\U0001f4ca  \U0000062f\U00000627\U00000634\U00000628\U00000648\U00000631\U0000062f", None))
        self.btn_products.setText(QCoreApplication.translate("MainWindow", u"\U0001f355  \U00000645\U0000062d\U00000635\U00000648\U00000644\U00000627\U0000062a", None))
        self.btn_orders.setText(QCoreApplication.translate("MainWindow", u"\U0001f4cb  \U00000633\U00000641\U00000627\U00000631\U00000634\U00000627\U0000062a", None))
        self.btn_test_call.setText(QCoreApplication.translate("MainWindow", u"\U0001f4de  \U0000062a\U00000633\U0000062a \U0000062a\U00000645\U00000627\U00000633", None))
        self.btn_reports.setText(QCoreApplication.translate("MainWindow", u"\U0001f4c8  \U000006af\U00000632\U00000627\U00000631\U00000634\U00000627\U0000062a", None))
        self.btn_settings.setText(QCoreApplication.translate("MainWindow", u"\u2699\ufe0f  \u062a\u0646\u0638\u06cc\u0645\u0627\u062a", None))
        self.version_label.setText(QCoreApplication.translate("MainWindow", u"\u0646\u0633\u062e\u0647 0.1.0", None))
        self.dashboard_title.setText(QCoreApplication.translate("MainWindow", u"\U0001f4ca \U0000062f\U00000627\U00000634\U00000628\U00000648\U00000631\U0000062f", None))
        self.products_title.setText(QCoreApplication.translate("MainWindow", u"\U0001f355 \U00000645\U0000062f\U000006cc\U00000631\U000006cc\U0000062a \U00000645\U0000062d\U00000635\U00000648\U00000644\U00000627\U0000062a", None))
        self.orders_title.setText(QCoreApplication.translate("MainWindow", u"\U0001f4cb \U00000633\U00000641\U00000627\U00000631\U00000634\U00000627\U0000062a", None))
        self.test_call_title.setText(QCoreApplication.translate("MainWindow", u"\U0001f4de \U0000062a\U00000633\U0000062a \U0000062a\U00000645\U00000627\U00000633", None))
        self.reports_title.setText(QCoreApplication.translate("MainWindow", u"\U0001f4c8 \U000006af\U00000632\U00000627\U00000631\U00000634\U00000627\U0000062a", None))
        self.settings_title.setText(QCoreApplication.translate("MainWindow", u"\u2699\ufe0f \u062a\u0646\u0638\u06cc\u0645\u0627\u062a", None))
    # retranslateUi

