# -*- coding: utf-8 -*-
# ⚠️ این فایل به صورت خودکار تولید شده است.
# 📄 فایل منبع: app\ui\ui_files\test_call_page.ui
# 🚫 تغییرات دستی در این فایل از بین خواهند رفت.
# 🔧 برای ویرایش، فایل .ui را در Qt Designer باز کنید.
#
# تولید شده توسط: compile_ui.py
# =====================================================

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test_call_page.ui'
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
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_TestCallPage(object):
    def setupUi(self, TestCallPage):
        if not TestCallPage.objectName():
            TestCallPage.setObjectName(u"TestCallPage")
        TestCallPage.resize(950, 700)
        TestCallPage.setLayoutDirection(Qt.RightToLeft)
        self.main_layout = QVBoxLayout(TestCallPage)
        self.main_layout.setSpacing(12)
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.page_title = QLabel(TestCallPage)
        self.page_title.setObjectName(u"page_title")
        self.page_title.setAlignment(Qt.AlignRight|Qt.AlignVCenter)

        self.main_layout.addWidget(self.page_title)

        self.control_bar = QFrame(TestCallPage)
        self.control_bar.setObjectName(u"control_bar")
        self.control_bar.setFrameShape(QFrame.StyledPanel)
        self.control_layout = QHBoxLayout(self.control_bar)
        self.control_layout.setSpacing(10)
        self.control_layout.setObjectName(u"control_layout")
        self.label_caller = QLabel(self.control_bar)
        self.label_caller.setObjectName(u"label_caller")

        self.control_layout.addWidget(self.label_caller)

        self.caller_phone_edit = QLineEdit(self.control_bar)
        self.caller_phone_edit.setObjectName(u"caller_phone_edit")
        self.caller_phone_edit.setMinimumSize(QSize(180, 38))
        self.caller_phone_edit.setMaximumSize(QSize(180, 16777215))
        self.caller_phone_edit.setMaxLength(13)

        self.control_layout.addWidget(self.caller_phone_edit)

        self.start_call_btn = QPushButton(self.control_bar)
        self.start_call_btn.setObjectName(u"start_call_btn")
        self.start_call_btn.setMinimumSize(QSize(160, 38))
        self.start_call_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.control_layout.addWidget(self.start_call_btn)

        self.end_call_btn = QPushButton(self.control_bar)
        self.end_call_btn.setObjectName(u"end_call_btn")
        self.end_call_btn.setMinimumSize(QSize(140, 38))
        self.end_call_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.end_call_btn.setEnabled(False)

        self.control_layout.addWidget(self.end_call_btn)

        self.control_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.control_layout.addItem(self.control_spacer)

        self.timer_label = QLabel(self.control_bar)
        self.timer_label.setObjectName(u"timer_label")
        self.timer_label.setMinimumSize(QSize(90, 0))
        self.timer_label.setAlignment(Qt.AlignCenter)

        self.control_layout.addWidget(self.timer_label)

        self.status_indicator = QLabel(self.control_bar)
        self.status_indicator.setObjectName(u"status_indicator")
        self.status_indicator.setMinimumSize(QSize(140, 0))
        self.status_indicator.setAlignment(Qt.AlignCenter)

        self.control_layout.addWidget(self.status_indicator)


        self.main_layout.addWidget(self.control_bar)

        self.content_layout = QHBoxLayout()
        self.content_layout.setSpacing(12)
        self.content_layout.setObjectName(u"content_layout")
        self.chat_frame = QFrame(TestCallPage)
        self.chat_frame.setObjectName(u"chat_frame")
        self.chat_frame.setFrameShape(QFrame.StyledPanel)
        self.chat_layout = QVBoxLayout(self.chat_frame)
        self.chat_layout.setSpacing(8)
        self.chat_layout.setObjectName(u"chat_layout")
        self.chat_layout.setContentsMargins(10, 10, 10, 10)
        self.chat_header = QLabel(self.chat_frame)
        self.chat_header.setObjectName(u"chat_header")

        self.chat_layout.addWidget(self.chat_header)

        self.chat_scroll = QScrollArea(self.chat_frame)
        self.chat_scroll.setObjectName(u"chat_scroll")
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chat_container = QWidget()
        self.chat_container.setObjectName(u"chat_container")
        self.chat_container.setGeometry(QRect(0, 0, 580, 400))
        self.chat_messages_layout = QVBoxLayout(self.chat_container)
        self.chat_messages_layout.setSpacing(8)
        self.chat_messages_layout.setObjectName(u"chat_messages_layout")
        self.chat_messages_layout.setContentsMargins(6, 6, 6, 6)
        self.chat_bottom_spacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.chat_messages_layout.addItem(self.chat_bottom_spacer)

        self.chat_scroll.setWidget(self.chat_container)

        self.chat_layout.addWidget(self.chat_scroll)

        self.input_layout = QHBoxLayout()
        self.input_layout.setSpacing(6)
        self.input_layout.setObjectName(u"input_layout")
        self.user_input_edit = QLineEdit(self.chat_frame)
        self.user_input_edit.setObjectName(u"user_input_edit")
        self.user_input_edit.setMinimumSize(QSize(0, 42))
        self.user_input_edit.setEnabled(False)

        self.input_layout.addWidget(self.user_input_edit)

        self.send_btn = QPushButton(self.chat_frame)
        self.send_btn.setObjectName(u"send_btn")
        self.send_btn.setMinimumSize(QSize(90, 42))
        self.send_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.send_btn.setEnabled(False)

        self.input_layout.addWidget(self.send_btn)


        self.chat_layout.addLayout(self.input_layout)


        self.content_layout.addWidget(self.chat_frame)

        self.info_frame = QFrame(TestCallPage)
        self.info_frame.setObjectName(u"info_frame")
        self.info_frame.setMinimumSize(QSize(270, 0))
        self.info_frame.setMaximumSize(QSize(270, 16777215))
        self.info_frame.setFrameShape(QFrame.StyledPanel)
        self.info_layout = QVBoxLayout(self.info_frame)
        self.info_layout.setSpacing(10)
        self.info_layout.setObjectName(u"info_layout")
        self.cart_header = QLabel(self.info_frame)
        self.cart_header.setObjectName(u"cart_header")

        self.info_layout.addWidget(self.cart_header)

        self.cart_list = QListWidget(self.info_frame)
        self.cart_list.setObjectName(u"cart_list")
        self.cart_list.setMinimumSize(QSize(0, 180))

        self.info_layout.addWidget(self.cart_list)

        self.cart_total_label = QLabel(self.info_frame)
        self.cart_total_label.setObjectName(u"cart_total_label")
        self.cart_total_label.setAlignment(Qt.AlignRight|Qt.AlignVCenter)

        self.info_layout.addWidget(self.cart_total_label)

        self.line1 = QFrame(self.info_frame)
        self.line1.setObjectName(u"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)

        self.info_layout.addWidget(self.line1)

        self.customer_header = QLabel(self.info_frame)
        self.customer_header.setObjectName(u"customer_header")

        self.info_layout.addWidget(self.customer_header)

        self.customer_phone_label = QLabel(self.info_frame)
        self.customer_phone_label.setObjectName(u"customer_phone_label")
        self.customer_phone_label.setWordWrap(True)

        self.info_layout.addWidget(self.customer_phone_label)

        self.customer_address_label = QLabel(self.info_frame)
        self.customer_address_label.setObjectName(u"customer_address_label")
        self.customer_address_label.setWordWrap(True)

        self.info_layout.addWidget(self.customer_address_label)

        self.info_spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.info_layout.addItem(self.info_spacer)

        self.save_order_btn = QPushButton(self.info_frame)
        self.save_order_btn.setObjectName(u"save_order_btn")
        self.save_order_btn.setMinimumSize(QSize(0, 42))
        self.save_order_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.save_order_btn.setEnabled(False)

        self.info_layout.addWidget(self.save_order_btn)

        self.download_transcript_btn = QPushButton(self.info_frame)
        self.download_transcript_btn.setObjectName(u"download_transcript_btn")
        self.download_transcript_btn.setMinimumSize(QSize(0, 36))
        self.download_transcript_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.download_transcript_btn.setEnabled(False)

        self.info_layout.addWidget(self.download_transcript_btn)


        self.content_layout.addWidget(self.info_frame)


        self.main_layout.addLayout(self.content_layout)


        self.retranslateUi(TestCallPage)

        QMetaObject.connectSlotsByName(TestCallPage)
    # setupUi

    def retranslateUi(self, TestCallPage):
        self.page_title.setText(QCoreApplication.translate("TestCallPage", u"\U0001f4de  \U0000062a\U00000633\U0000062a \U0000062a\U00000645\U00000627\U00000633", None))
        self.label_caller.setText(QCoreApplication.translate("TestCallPage", u"\U0001f4f1  \U00000634\U00000645\U00000627\U00000631\U00000647 \U0000062a\U00000645\U00000627\U00000633\U0000200c\U000006af\U000006cc\U00000631\U00000646\U0000062f\U00000647:", None))
        self.caller_phone_edit.setText(QCoreApplication.translate("TestCallPage", u"09123456789", None))
        self.caller_phone_edit.setPlaceholderText(QCoreApplication.translate("TestCallPage", u"09xxxxxxxxx", None))
        self.start_call_btn.setText(QCoreApplication.translate("TestCallPage", u"\U0001f399\U0000fe0f  \U00000634\U00000631\U00000648\U00000639 \U0000062a\U00000645\U00000627\U00000633", None))
        self.end_call_btn.setText(QCoreApplication.translate("TestCallPage", u"\U0001f534  \U0000067e\U00000627\U000006cc\U00000627\U00000646 \U0000062a\U00000645\U00000627\U00000633", None))
        self.timer_label.setText(QCoreApplication.translate("TestCallPage", u"\u23f1\ufe0f  00:00", None))
        self.status_indicator.setText(QCoreApplication.translate("TestCallPage", u"\u26aa  \u0622\u0645\u0627\u062f\u0647", None))
        self.chat_header.setText(QCoreApplication.translate("TestCallPage", u"\U0001f4dd  \U00000645\U000006a9\U00000627\U00000644\U00000645\U00000647", None))
        self.user_input_edit.setPlaceholderText(QCoreApplication.translate("TestCallPage", u"\u067e\u06cc\u0627\u0645 \u062e\u0648\u062f \u0631\u0627 \u062a\u0627\u06cc\u067e \u06a9\u0646\u06cc\u062f \u0648 Enter \u0628\u0632\u0646\u06cc\u062f...", None))
        self.send_btn.setText(QCoreApplication.translate("TestCallPage", u"\u0627\u0631\u0633\u0627\u0644 \u27a4", None))
        self.cart_header.setText(QCoreApplication.translate("TestCallPage", u"\U0001f6d2  \U00000633\U00000628\U0000062f \U0000062e\U00000631\U000006cc\U0000062f", None))
        self.cart_total_label.setText(QCoreApplication.translate("TestCallPage", u"\U0001f4b0  \U00000645\U0000062c\U00000645\U00000648\U00000639: 0 \U0000062a\U00000648\U00000645\U00000627\U00000646", None))
        self.customer_header.setText(QCoreApplication.translate("TestCallPage", u"\U0001f464  \U00000627\U00000637\U00000644\U00000627\U00000639\U00000627\U0000062a \U00000645\U00000634\U0000062a\U00000631\U000006cc", None))
        self.customer_phone_label.setText(QCoreApplication.translate("TestCallPage", u"\U0001f4de  \U00000634\U00000645\U00000627\U00000631\U00000647 \U0000062b\U00000628\U0000062a: -", None))
        self.customer_address_label.setText(QCoreApplication.translate("TestCallPage", u"\U0001f4cd  \U00000622\U0000062f\U00000631\U00000633: -", None))
        self.save_order_btn.setText(QCoreApplication.translate("TestCallPage", u"\U0001f4be  \U0000062b\U00000628\U0000062a \U00000633\U00000641\U00000627\U00000631\U00000634 \U00000646\U00000647\U00000627\U000006cc\U000006cc", None))
        self.download_transcript_btn.setText(QCoreApplication.translate("TestCallPage", u"\U0001f4e5  \U0000062f\U00000627\U00000646\U00000644\U00000648\U0000062f \U00000645\U0000062a\U00000646 \U00000645\U000006a9\U00000627\U00000644\U00000645\U00000647", None))
        pass
    # retranslateUi

