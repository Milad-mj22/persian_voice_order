# -*- coding: utf-8 -*-
# ⚠️ این فایل به صورت خودکار تولید شده است.
# 📄 فایل منبع: app\ui\ui_files\orders_page.ui
# 🚫 تغییرات دستی در این فایل از بین خواهند رفت.
# 🔧 برای ویرایش، فایل .ui را در Qt Designer باز کنید.
#
# تولید شده توسط: compile_ui.py
# =====================================================

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'orders_page.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_OrdersPage(object):
    def setupUi(self, OrdersPage):
        if not OrdersPage.objectName():
            OrdersPage.setObjectName(u"OrdersPage")
        OrdersPage.resize(950, 700)
        OrdersPage.setLayoutDirection(Qt.RightToLeft)
        self.main_layout = QVBoxLayout(OrdersPage)
        self.main_layout.setSpacing(12)
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.page_title = QLabel(OrdersPage)
        self.page_title.setObjectName(u"page_title")
        self.page_title.setAlignment(Qt.AlignRight|Qt.AlignVCenter)

        self.main_layout.addWidget(self.page_title)

        self.toolbar = QFrame(OrdersPage)
        self.toolbar.setObjectName(u"toolbar")
        self.toolbar.setFrameShape(QFrame.StyledPanel)
        self.toolbar_layout = QHBoxLayout(self.toolbar)
        self.toolbar_layout.setSpacing(8)
        self.toolbar_layout.setObjectName(u"toolbar_layout")
        self.refresh_btn = QPushButton(self.toolbar)
        self.refresh_btn.setObjectName(u"refresh_btn")
        self.refresh_btn.setMinimumSize(QSize(120, 36))
        self.refresh_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.toolbar_layout.addWidget(self.refresh_btn)

        self.export_btn = QPushButton(self.toolbar)
        self.export_btn.setObjectName(u"export_btn")
        self.export_btn.setMinimumSize(QSize(120, 36))
        self.export_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.toolbar_layout.addWidget(self.export_btn)

        self.sp1 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.toolbar_layout.addItem(self.sp1)

        self.status_combo = QComboBox(self.toolbar)
        self.status_combo.setObjectName(u"status_combo")
        self.status_combo.setMinimumSize(QSize(150, 36))

        self.toolbar_layout.addWidget(self.status_combo)

        self.search_edit = QLineEdit(self.toolbar)
        self.search_edit.setObjectName(u"search_edit")
        self.search_edit.setMinimumSize(QSize(240, 36))
        self.search_edit.setClearButtonEnabled(True)

        self.toolbar_layout.addWidget(self.search_edit)


        self.main_layout.addWidget(self.toolbar)

        self.orders_table = QTableWidget(OrdersPage)
        if (self.orders_table.columnCount() < 7):
            self.orders_table.setColumnCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        self.orders_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.orders_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.orders_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.orders_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.orders_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.orders_table.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.orders_table.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.orders_table.setObjectName(u"orders_table")
        self.orders_table.setAlternatingRowColors(True)
        self.orders_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.orders_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.orders_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.orders_table.setSortingEnabled(True)

        self.main_layout.addWidget(self.orders_table)

        self.actions_bar = QFrame(OrdersPage)
        self.actions_bar.setObjectName(u"actions_bar")
        self.actions_bar.setFrameShape(QFrame.StyledPanel)
        self.actions_layout = QHBoxLayout(self.actions_bar)
        self.actions_layout.setObjectName(u"actions_layout")
        self.stats_label = QLabel(self.actions_bar)
        self.stats_label.setObjectName(u"stats_label")

        self.actions_layout.addWidget(self.stats_label)

        self.sp2 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.actions_layout.addItem(self.sp2)

        self.delete_btn = QPushButton(self.actions_bar)
        self.delete_btn.setObjectName(u"delete_btn")
        self.delete_btn.setMinimumSize(QSize(100, 36))
        self.delete_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.actions_layout.addWidget(self.delete_btn)

        self.view_btn = QPushButton(self.actions_bar)
        self.view_btn.setObjectName(u"view_btn")
        self.view_btn.setMinimumSize(QSize(140, 36))
        self.view_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.actions_layout.addWidget(self.view_btn)


        self.main_layout.addWidget(self.actions_bar)


        self.retranslateUi(OrdersPage)

        QMetaObject.connectSlotsByName(OrdersPage)
    # setupUi

    def retranslateUi(self, OrdersPage):
        self.page_title.setText(QCoreApplication.translate("OrdersPage", u"\U0001f4cb  \U00000633\U00000641\U00000627\U00000631\U00000634\U00000627\U0000062a", None))
        self.refresh_btn.setText(QCoreApplication.translate("OrdersPage", u"\U0001f504  \U00000628\U00000631\U00000648\U00000632\U00000631\U00000633\U00000627\U00000646\U000006cc", None))
        self.export_btn.setText(QCoreApplication.translate("OrdersPage", u"\U0001f4e5  \U0000062e\U00000631\U00000648\U0000062c\U000006cc CSV", None))
        self.search_edit.setPlaceholderText(QCoreApplication.translate("OrdersPage", u"\U0001f50d  \U0000062c\U00000633\U0000062a\U0000062c\U00000648 \U0000062f\U00000631 \U00000634\U00000645\U00000627\U00000631\U00000647\U0000060c \U000006a9\U0000062f \U00000633\U00000641\U00000627\U00000631\U00000634\U0000060c \U00000622\U0000062f\U00000631\U00000633...", None))
        ___qtablewidgetitem = self.orders_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("OrdersPage", u"\u06a9\u062f", None))
        ___qtablewidgetitem1 = self.orders_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("OrdersPage", u"\u062a\u0627\u0631\u06cc\u062e", None))
        ___qtablewidgetitem2 = self.orders_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("OrdersPage", u"\u0634\u0645\u0627\u0631\u0647", None))
        ___qtablewidgetitem3 = self.orders_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("OrdersPage", u"\u0622\u062f\u0631\u0633", None))
        ___qtablewidgetitem4 = self.orders_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("OrdersPage", u"\u0627\u0642\u0644\u0627\u0645", None))
        ___qtablewidgetitem5 = self.orders_table.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("OrdersPage", u"\u0645\u0628\u0644\u063a (\u062a\u0648\u0645\u0627\u0646)", None))
        ___qtablewidgetitem6 = self.orders_table.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("OrdersPage", u"\u0648\u0636\u0639\u06cc\u062a", None))
        self.stats_label.setText(QCoreApplication.translate("OrdersPage", u"\u062f\u0631 \u062d\u0627\u0644 \u0628\u0627\u0631\u06af\u0630\u0627\u0631\u06cc...", None))
        self.delete_btn.setText(QCoreApplication.translate("OrdersPage", u"\U0001f5d1\U0000fe0f  \U0000062d\U00000630\U00000641", None))
        self.view_btn.setText(QCoreApplication.translate("OrdersPage", u"\U0001f441\U0000fe0f  \U00000645\U00000634\U00000627\U00000647\U0000062f\U00000647 \U0000062c\U00000632\U00000626\U000006cc\U00000627\U0000062a", None))
        pass
    # retranslateUi

