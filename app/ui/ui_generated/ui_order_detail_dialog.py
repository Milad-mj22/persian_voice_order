# -*- coding: utf-8 -*-
# ⚠️ این فایل به صورت خودکار تولید شده است.
# 📄 فایل منبع: app\ui\ui_files\order_detail_dialog.ui
# 🚫 تغییرات دستی در این فایل از بین خواهند رفت.
# 🔧 برای ویرایش، فایل .ui را در Qt Designer باز کنید.
#
# تولید شده توسط: compile_ui.py
# =====================================================

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'order_detail_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QDialog,
    QFormLayout, QFrame, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_OrderDetailDialog(object):
    def setupUi(self, OrderDetailDialog):
        if not OrderDetailDialog.objectName():
            OrderDetailDialog.setObjectName(u"OrderDetailDialog")
        OrderDetailDialog.resize(600, 650)
        OrderDetailDialog.setLayoutDirection(Qt.RightToLeft)
        self.main_layout = QVBoxLayout(OrderDetailDialog)
        self.main_layout.setSpacing(12)
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.title_label = QLabel(OrderDetailDialog)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.title_label)

        self.line = QFrame(OrderDetailDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.main_layout.addWidget(self.line)

        self.info_group = QGroupBox(OrderDetailDialog)
        self.info_group.setObjectName(u"info_group")
        self.info_form = QFormLayout(self.info_group)
        self.info_form.setObjectName(u"info_form")
        self.info_form.setLabelAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.label = QLabel(self.info_group)
        self.label.setObjectName(u"label")

        self.info_form.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.code_value = QLabel(self.info_group)
        self.code_value.setObjectName(u"code_value")

        self.info_form.setWidget(0, QFormLayout.ItemRole.FieldRole, self.code_value)

        self.label1 = QLabel(self.info_group)
        self.label1.setObjectName(u"label1")

        self.info_form.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label1)

        self.phone_value = QLabel(self.info_group)
        self.phone_value.setObjectName(u"phone_value")

        self.info_form.setWidget(1, QFormLayout.ItemRole.FieldRole, self.phone_value)

        self.label2 = QLabel(self.info_group)
        self.label2.setObjectName(u"label2")

        self.info_form.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label2)

        self.order_phone_value = QLabel(self.info_group)
        self.order_phone_value.setObjectName(u"order_phone_value")

        self.info_form.setWidget(2, QFormLayout.ItemRole.FieldRole, self.order_phone_value)

        self.label3 = QLabel(self.info_group)
        self.label3.setObjectName(u"label3")

        self.info_form.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label3)

        self.address_value = QLabel(self.info_group)
        self.address_value.setObjectName(u"address_value")
        self.address_value.setWordWrap(True)

        self.info_form.setWidget(3, QFormLayout.ItemRole.FieldRole, self.address_value)

        self.label4 = QLabel(self.info_group)
        self.label4.setObjectName(u"label4")

        self.info_form.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label4)

        self.date_value = QLabel(self.info_group)
        self.date_value.setObjectName(u"date_value")

        self.info_form.setWidget(4, QFormLayout.ItemRole.FieldRole, self.date_value)

        self.label5 = QLabel(self.info_group)
        self.label5.setObjectName(u"label5")

        self.info_form.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label5)

        self.status_combo = QComboBox(self.info_group)
        self.status_combo.setObjectName(u"status_combo")

        self.info_form.setWidget(5, QFormLayout.ItemRole.FieldRole, self.status_combo)


        self.main_layout.addWidget(self.info_group)

        self.items_group = QGroupBox(OrderDetailDialog)
        self.items_group.setObjectName(u"items_group")
        self.items_layout = QVBoxLayout(self.items_group)
        self.items_layout.setObjectName(u"items_layout")
        self.items_table = QTableWidget(self.items_group)
        if (self.items_table.columnCount() < 4):
            self.items_table.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.items_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.items_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.items_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.items_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.items_table.setObjectName(u"items_table")
        self.items_table.setAlternatingRowColors(True)
        self.items_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.items_layout.addWidget(self.items_table)

        self.total_label = QLabel(self.items_group)
        self.total_label.setObjectName(u"total_label")
        self.total_label.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)

        self.items_layout.addWidget(self.total_label)


        self.main_layout.addWidget(self.items_group)

        self.toggle_transcript_btn = QPushButton(OrderDetailDialog)
        self.toggle_transcript_btn.setObjectName(u"toggle_transcript_btn")
        self.toggle_transcript_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toggle_transcript_btn.setCheckable(True)

        self.main_layout.addWidget(self.toggle_transcript_btn)

        self.transcript_edit = QTextEdit(OrderDetailDialog)
        self.transcript_edit.setObjectName(u"transcript_edit")
        self.transcript_edit.setReadOnly(True)
        self.transcript_edit.setMaximumSize(QSize(16777215, 0))
        self.transcript_edit.setVisible(False)

        self.main_layout.addWidget(self.transcript_edit)

        self.line2 = QFrame(OrderDetailDialog)
        self.line2.setObjectName(u"line2")
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)

        self.main_layout.addWidget(self.line2)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setObjectName(u"buttons_layout")
        self.sp = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttons_layout.addItem(self.sp)

        self.close_btn = QPushButton(OrderDetailDialog)
        self.close_btn.setObjectName(u"close_btn")
        self.close_btn.setMinimumSize(QSize(100, 38))
        self.close_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.buttons_layout.addWidget(self.close_btn)

        self.save_btn = QPushButton(OrderDetailDialog)
        self.save_btn.setObjectName(u"save_btn")
        self.save_btn.setMinimumSize(QSize(150, 38))
        self.save_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.buttons_layout.addWidget(self.save_btn)


        self.main_layout.addLayout(self.buttons_layout)


        self.retranslateUi(OrderDetailDialog)

        QMetaObject.connectSlotsByName(OrderDetailDialog)
    # setupUi

    def retranslateUi(self, OrderDetailDialog):
        OrderDetailDialog.setWindowTitle(QCoreApplication.translate("OrderDetailDialog", u"\u062c\u0632\u0626\u06cc\u0627\u062a \u0633\u0641\u0627\u0631\u0634", None))
        self.title_label.setText(QCoreApplication.translate("OrderDetailDialog", u"\U0001f4cb  \U0000062c\U00000632\U00000626\U000006cc\U00000627\U0000062a \U00000633\U00000641\U00000627\U00000631\U00000634", None))
        self.info_group.setTitle(QCoreApplication.translate("OrderDetailDialog", u"\u0627\u0637\u0644\u0627\u0639\u0627\u062a \u0645\u0634\u062a\u0631\u06cc", None))
        self.label.setText(QCoreApplication.translate("OrderDetailDialog", u"\u06a9\u062f \u0633\u0641\u0627\u0631\u0634:", None))
        self.code_value.setText(QCoreApplication.translate("OrderDetailDialog", u"-", None))
        self.label1.setText(QCoreApplication.translate("OrderDetailDialog", u"\u0634\u0645\u0627\u0631\u0647 \u062a\u0645\u0627\u0633:", None))
        self.phone_value.setText(QCoreApplication.translate("OrderDetailDialog", u"-", None))
        self.label2.setText(QCoreApplication.translate("OrderDetailDialog", u"\u0634\u0645\u0627\u0631\u0647 \u062b\u0628\u062a:", None))
        self.order_phone_value.setText(QCoreApplication.translate("OrderDetailDialog", u"-", None))
        self.label3.setText(QCoreApplication.translate("OrderDetailDialog", u"\u0622\u062f\u0631\u0633:", None))
        self.address_value.setText(QCoreApplication.translate("OrderDetailDialog", u"-", None))
        self.label4.setText(QCoreApplication.translate("OrderDetailDialog", u"\u062a\u0627\u0631\u06cc\u062e:", None))
        self.date_value.setText(QCoreApplication.translate("OrderDetailDialog", u"-", None))
        self.label5.setText(QCoreApplication.translate("OrderDetailDialog", u"\u0648\u0636\u0639\u06cc\u062a:", None))
        self.items_group.setTitle(QCoreApplication.translate("OrderDetailDialog", u"\u0627\u0642\u0644\u0627\u0645 \u0633\u0641\u0627\u0631\u0634", None))
        ___qtablewidgetitem = self.items_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("OrderDetailDialog", u"\u0646\u0627\u0645", None))
        ___qtablewidgetitem1 = self.items_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("OrderDetailDialog", u"\u062a\u0639\u062f\u0627\u062f", None))
        ___qtablewidgetitem2 = self.items_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("OrderDetailDialog", u"\u0642\u06cc\u0645\u062a \u0648\u0627\u062d\u062f", None))
        ___qtablewidgetitem3 = self.items_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("OrderDetailDialog", u"\u062c\u0645\u0639", None))
        self.total_label.setText(QCoreApplication.translate("OrderDetailDialog", u"\U0001f4b0  \U00000645\U0000062c\U00000645\U00000648\U00000639: 0 \U0000062a\U00000648\U00000645\U00000627\U00000646", None))
        self.toggle_transcript_btn.setText(QCoreApplication.translate("OrderDetailDialog", u"\U0001f4dd  \U00000646\U00000645\U00000627\U000006cc\U00000634 \U00000645\U0000062a\U00000646 \U00000645\U000006a9\U00000627\U00000644\U00000645\U00000647", None))
        self.close_btn.setText(QCoreApplication.translate("OrderDetailDialog", u"\u0628\u0633\u062a\u0646", None))
        self.save_btn.setText(QCoreApplication.translate("OrderDetailDialog", u"\U0001f4be  \U00000630\U0000062e\U000006cc\U00000631\U00000647 \U0000062a\U0000063a\U000006cc\U000006cc\U00000631\U00000627\U0000062a", None))
    # retranslateUi

