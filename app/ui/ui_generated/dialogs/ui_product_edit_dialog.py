# -*- coding: utf-8 -*-
# ⚠️ این فایل به صورت خودکار تولید شده است.
# 📄 فایل منبع: app\ui\ui_files\dialogs\product_edit_dialog.ui
# 🚫 تغییرات دستی در این فایل از بین خواهند رفت.
# 🔧 برای ویرایش، فایل .ui را در Qt Designer باز کنید.
#
# تولید شده توسط: compile_ui.py
# =====================================================

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'product_edit_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFormLayout, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTextEdit, QVBoxLayout, QWidget)

class Ui_ProductEditDialog(object):
    def setupUi(self, ProductEditDialog):
        if not ProductEditDialog.objectName():
            ProductEditDialog.setObjectName(u"ProductEditDialog")
        ProductEditDialog.resize(520, 560)
        ProductEditDialog.setLayoutDirection(Qt.RightToLeft)
        self.main_layout = QVBoxLayout(ProductEditDialog)
        self.main_layout.setSpacing(12)
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.dialog_title = QLabel(ProductEditDialog)
        self.dialog_title.setObjectName(u"dialog_title")
        self.dialog_title.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.dialog_title)

        self.line = QFrame(ProductEditDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.main_layout.addWidget(self.line)

        self.form_layout = QFormLayout()
        self.form_layout.setObjectName(u"form_layout")
        self.form_layout.setLabelAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.form_layout.setHorizontalSpacing(12)
        self.form_layout.setVerticalSpacing(10)
        self.label_name = QLabel(ProductEditDialog)
        self.label_name.setObjectName(u"label_name")

        self.form_layout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_name)

        self.name_edit = QLineEdit(ProductEditDialog)
        self.name_edit.setObjectName(u"name_edit")

        self.form_layout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.name_edit)

        self.label_category = QLabel(ProductEditDialog)
        self.label_category.setObjectName(u"label_category")

        self.form_layout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_category)

        self.category_combo = QComboBox(ProductEditDialog)
        self.category_combo.setObjectName(u"category_combo")
        self.category_combo.setEditable(True)

        self.form_layout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.category_combo)

        self.label_price = QLabel(ProductEditDialog)
        self.label_price.setObjectName(u"label_price")

        self.form_layout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_price)

        self.price_spin = QSpinBox(ProductEditDialog)
        self.price_spin.setObjectName(u"price_spin")
        self.price_spin.setMaximum(999999999)
        self.price_spin.setSingleStep(1000)
        self.price_spin.setGroupSeparatorShown(True)

        self.form_layout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.price_spin)

        self.label_stock = QLabel(ProductEditDialog)
        self.label_stock.setObjectName(u"label_stock")

        self.form_layout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_stock)

        self.stock_spin = QSpinBox(ProductEditDialog)
        self.stock_spin.setObjectName(u"stock_spin")
        self.stock_spin.setMaximum(999999)

        self.form_layout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.stock_spin)

        self.label_order = QLabel(ProductEditDialog)
        self.label_order.setObjectName(u"label_order")

        self.form_layout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_order)

        self.display_order_spin = QSpinBox(ProductEditDialog)
        self.display_order_spin.setObjectName(u"display_order_spin")
        self.display_order_spin.setMaximum(9999)

        self.form_layout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.display_order_spin)

        self.label_description = QLabel(ProductEditDialog)
        self.label_description.setObjectName(u"label_description")

        self.form_layout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_description)

        self.description_edit = QTextEdit(ProductEditDialog)
        self.description_edit.setObjectName(u"description_edit")
        self.description_edit.setMaximumSize(QSize(16777215, 100))

        self.form_layout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.description_edit)


        self.main_layout.addLayout(self.form_layout)

        self.checks_layout = QHBoxLayout()
        self.checks_layout.setObjectName(u"checks_layout")
        self.is_active_check = QCheckBox(ProductEditDialog)
        self.is_active_check.setObjectName(u"is_active_check")
        self.is_active_check.setChecked(True)

        self.checks_layout.addWidget(self.is_active_check)

        self.is_featured_check = QCheckBox(ProductEditDialog)
        self.is_featured_check.setObjectName(u"is_featured_check")

        self.checks_layout.addWidget(self.is_featured_check)

        self.checks_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.checks_layout.addItem(self.checks_spacer)


        self.main_layout.addLayout(self.checks_layout)

        self.error_label = QLabel(ProductEditDialog)
        self.error_label.setObjectName(u"error_label")
        self.error_label.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.error_label)

        self.line_2 = QFrame(ProductEditDialog)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.main_layout.addWidget(self.line_2)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setObjectName(u"buttons_layout")
        self.buttons_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttons_layout.addItem(self.buttons_spacer)

        self.cancel_btn = QPushButton(ProductEditDialog)
        self.cancel_btn.setObjectName(u"cancel_btn")
        self.cancel_btn.setMinimumSize(QSize(100, 38))
        self.cancel_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.buttons_layout.addWidget(self.cancel_btn)

        self.save_btn = QPushButton(ProductEditDialog)
        self.save_btn.setObjectName(u"save_btn")
        self.save_btn.setMinimumSize(QSize(120, 38))
        self.save_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.buttons_layout.addWidget(self.save_btn)


        self.main_layout.addLayout(self.buttons_layout)


        self.retranslateUi(ProductEditDialog)

        QMetaObject.connectSlotsByName(ProductEditDialog)
    # setupUi

    def retranslateUi(self, ProductEditDialog):
        ProductEditDialog.setWindowTitle(QCoreApplication.translate("ProductEditDialog", u"\u0645\u062d\u0635\u0648\u0644", None))
        self.dialog_title.setText(QCoreApplication.translate("ProductEditDialog", u"\u0627\u0641\u0632\u0648\u062f\u0646 \u0645\u062d\u0635\u0648\u0644 \u062c\u062f\u06cc\u062f", None))
        self.label_name.setText(QCoreApplication.translate("ProductEditDialog", u"\u0646\u0627\u0645 \u0645\u062d\u0635\u0648\u0644: *", None))
        self.name_edit.setPlaceholderText(QCoreApplication.translate("ProductEditDialog", u"\u0645\u062b\u0627\u0644: \u067e\u06cc\u062a\u0632\u0627 \u0645\u062e\u0635\u0648\u0635", None))
        self.label_category.setText(QCoreApplication.translate("ProductEditDialog", u"\u062f\u0633\u062a\u0647\u200c\u0628\u0646\u062f\u06cc: *", None))
        self.label_price.setText(QCoreApplication.translate("ProductEditDialog", u"\u0642\u06cc\u0645\u062a (\u062a\u0648\u0645\u0627\u0646): *", None))
        self.label_stock.setText(QCoreApplication.translate("ProductEditDialog", u"\u0645\u0648\u062c\u0648\u062f\u06cc:", None))
        self.label_order.setText(QCoreApplication.translate("ProductEditDialog", u"\u062a\u0631\u062a\u06cc\u0628 \u0646\u0645\u0627\u06cc\u0634:", None))
        self.label_description.setText(QCoreApplication.translate("ProductEditDialog", u"\u062a\u0648\u0636\u06cc\u062d\u0627\u062a:", None))
        self.description_edit.setPlaceholderText(QCoreApplication.translate("ProductEditDialog", u"\u062a\u0648\u0636\u06cc\u062d\u0627\u062a \u0627\u062e\u062a\u06cc\u0627\u0631\u06cc...", None))
        self.is_active_check.setText(QCoreApplication.translate("ProductEditDialog", u"\u0641\u0639\u0627\u0644", None))
        self.is_featured_check.setText(QCoreApplication.translate("ProductEditDialog", u"\u067e\u06cc\u0634\u0646\u0647\u0627\u062f \u0648\u06cc\u0698\u0647 \u2b50", None))
        self.error_label.setText("")
        self.cancel_btn.setText(QCoreApplication.translate("ProductEditDialog", u"\u0627\u0646\u0635\u0631\u0627\u0641", None))
        self.save_btn.setText(QCoreApplication.translate("ProductEditDialog", u"\U0001f4be  \U00000630\U0000062e\U000006cc\U00000631\U00000647", None))
    # retranslateUi

