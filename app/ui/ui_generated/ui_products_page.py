# -*- coding: utf-8 -*-
# ⚠️ این فایل به صورت خودکار تولید شده است.
# 📄 فایل منبع: app\ui\ui_files\products_page.ui
# 🚫 تغییرات دستی در این فایل از بین خواهند رفت.
# 🔧 برای ویرایش، فایل .ui را در Qt Designer باز کنید.
#
# تولید شده توسط: compile_ui.py
# =====================================================

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'products_page.ui'
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

class Ui_ProductsPage(object):
    def setupUi(self, ProductsPage):
        if not ProductsPage.objectName():
            ProductsPage.setObjectName(u"ProductsPage")
        ProductsPage.resize(950, 700)
        ProductsPage.setLayoutDirection(Qt.RightToLeft)
        self.main_layout = QVBoxLayout(ProductsPage)
        self.main_layout.setSpacing(12)
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.page_title = QLabel(ProductsPage)
        self.page_title.setObjectName(u"page_title")
        self.page_title.setAlignment(Qt.AlignRight|Qt.AlignVCenter)

        self.main_layout.addWidget(self.page_title)

        self.toolbar = QFrame(ProductsPage)
        self.toolbar.setObjectName(u"toolbar")
        self.toolbar.setFrameShape(QFrame.StyledPanel)
        self.toolbar_layout = QHBoxLayout(self.toolbar)
        self.toolbar_layout.setSpacing(8)
        self.toolbar_layout.setObjectName(u"toolbar_layout")
        self.add_btn = QPushButton(self.toolbar)
        self.add_btn.setObjectName(u"add_btn")
        self.add_btn.setMinimumSize(QSize(140, 36))
        self.add_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.toolbar_layout.addWidget(self.add_btn)

        self.refresh_btn = QPushButton(self.toolbar)
        self.refresh_btn.setObjectName(u"refresh_btn")
        self.refresh_btn.setMinimumSize(QSize(110, 36))
        self.refresh_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.toolbar_layout.addWidget(self.refresh_btn)

        self.toolbar_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.toolbar_layout.addItem(self.toolbar_spacer)

        self.category_combo = QComboBox(self.toolbar)
        self.category_combo.setObjectName(u"category_combo")
        self.category_combo.setMinimumSize(QSize(160, 36))

        self.toolbar_layout.addWidget(self.category_combo)

        self.search_edit = QLineEdit(self.toolbar)
        self.search_edit.setObjectName(u"search_edit")
        self.search_edit.setMinimumSize(QSize(240, 36))
        self.search_edit.setClearButtonEnabled(True)

        self.toolbar_layout.addWidget(self.search_edit)


        self.main_layout.addWidget(self.toolbar)

        self.products_table = QTableWidget(ProductsPage)
        if (self.products_table.columnCount() < 7):
            self.products_table.setColumnCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        self.products_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.products_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.products_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.products_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.products_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.products_table.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.products_table.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.products_table.setObjectName(u"products_table")
        self.products_table.setAlternatingRowColors(True)
        self.products_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.products_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.products_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.products_table.setSortingEnabled(True)

        self.main_layout.addWidget(self.products_table)

        self.actions_bar = QFrame(ProductsPage)
        self.actions_bar.setObjectName(u"actions_bar")
        self.actions_bar.setFrameShape(QFrame.StyledPanel)
        self.actions_layout = QHBoxLayout(self.actions_bar)
        self.actions_layout.setObjectName(u"actions_layout")
        self.stats_label = QLabel(self.actions_bar)
        self.stats_label.setObjectName(u"stats_label")

        self.actions_layout.addWidget(self.stats_label)

        self.actions_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.actions_layout.addItem(self.actions_spacer)

        self.delete_btn = QPushButton(self.actions_bar)
        self.delete_btn.setObjectName(u"delete_btn")
        self.delete_btn.setMinimumSize(QSize(100, 36))
        self.delete_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.actions_layout.addWidget(self.delete_btn)

        self.edit_btn = QPushButton(self.actions_bar)
        self.edit_btn.setObjectName(u"edit_btn")
        self.edit_btn.setMinimumSize(QSize(100, 36))
        self.edit_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.actions_layout.addWidget(self.edit_btn)


        self.main_layout.addWidget(self.actions_bar)


        self.retranslateUi(ProductsPage)

        QMetaObject.connectSlotsByName(ProductsPage)
    # setupUi

    def retranslateUi(self, ProductsPage):
        self.page_title.setText(QCoreApplication.translate("ProductsPage", u"\U0001f355  \U00000645\U0000062f\U000006cc\U00000631\U000006cc\U0000062a \U00000645\U0000062d\U00000635\U00000648\U00000644\U00000627\U0000062a", None))
        self.add_btn.setText(QCoreApplication.translate("ProductsPage", u"\u2795  \u0627\u0641\u0632\u0648\u062f\u0646 \u0645\u062d\u0635\u0648\u0644", None))
        self.refresh_btn.setText(QCoreApplication.translate("ProductsPage", u"\U0001f504  \U00000628\U00000631\U00000648\U00000632\U00000631\U00000633\U00000627\U00000646\U000006cc", None))
        self.search_edit.setPlaceholderText(QCoreApplication.translate("ProductsPage", u"\U0001f50d  \U0000062c\U00000633\U0000062a\U0000062c\U00000648\U000006cc \U00000645\U0000062d\U00000635\U00000648\U00000644...", None))
        ___qtablewidgetitem = self.products_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("ProductsPage", u"\u0634\u0646\u0627\u0633\u0647", None))
        ___qtablewidgetitem1 = self.products_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("ProductsPage", u"\u0646\u0627\u0645 \u0645\u062d\u0635\u0648\u0644", None))
        ___qtablewidgetitem2 = self.products_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("ProductsPage", u"\u062f\u0633\u062a\u0647\u200c\u0628\u0646\u062f\u06cc", None))
        ___qtablewidgetitem3 = self.products_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("ProductsPage", u"\u0642\u06cc\u0645\u062a (\u062a\u0648\u0645\u0627\u0646)", None))
        ___qtablewidgetitem4 = self.products_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("ProductsPage", u"\u0645\u0648\u062c\u0648\u062f\u06cc", None))
        ___qtablewidgetitem5 = self.products_table.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("ProductsPage", u"\u0648\u0636\u0639\u06cc\u062a", None))
        ___qtablewidgetitem6 = self.products_table.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("ProductsPage", u"\u0648\u06cc\u0698\u0647", None))
        self.stats_label.setText(QCoreApplication.translate("ProductsPage", u"\u062f\u0631 \u062d\u0627\u0644 \u0628\u0627\u0631\u06af\u0630\u0627\u0631\u06cc...", None))
        self.delete_btn.setText(QCoreApplication.translate("ProductsPage", u"\U0001f5d1\U0000fe0f  \U0000062d\U00000630\U00000641", None))
        self.edit_btn.setText(QCoreApplication.translate("ProductsPage", u"\u270f\ufe0f  \u0648\u06cc\u0631\u0627\u06cc\u0634", None))
        pass
    # retranslateUi

