# -*- coding: utf-8 -*-
# ⚠️ این فایل به صورت خودکار تولید شده است.
# 📄 فایل منبع: app\ui\ui_files\settings_page.ui
# 🚫 تغییرات دستی در این فایل از بین خواهند رفت.
# 🔧 برای ویرایش، فایل .ui را در Qt Designer باز کنید.
#
# تولید شده توسط: compile_ui.py
# =====================================================

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_page.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QFrame, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QSlider, QSpacerItem, QSpinBox, QTextEdit,
    QTimeEdit, QVBoxLayout, QWidget)

class Ui_SettingsPage(object):
    def setupUi(self, SettingsPage):
        if not SettingsPage.objectName():
            SettingsPage.setObjectName(u"SettingsPage")
        SettingsPage.resize(950, 700)
        SettingsPage.setLayoutDirection(Qt.RightToLeft)
        self.main_layout = QVBoxLayout(SettingsPage)
        self.main_layout.setSpacing(12)
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.page_title = QLabel(SettingsPage)
        self.page_title.setObjectName(u"page_title")
        self.page_title.setAlignment(Qt.AlignRight|Qt.AlignVCenter)

        self.main_layout.addWidget(self.page_title)

        self.scroll_area = QScrollArea(SettingsPage)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName(u"scroll_content")
        self.scroll_content.setGeometry(QRect(0, 0, 910, 1200))
        self.content_layout = QVBoxLayout(self.scroll_content)
        self.content_layout.setSpacing(14)
        self.content_layout.setObjectName(u"content_layout")
        self.group_business = QGroupBox(self.scroll_content)
        self.group_business.setObjectName(u"group_business")
        self.form_business = QFormLayout(self.group_business)
        self.form_business.setObjectName(u"form_business")
        self.form_business.setLabelAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.form_business.setHorizontalSpacing(12)
        self.form_business.setVerticalSpacing(10)
        self.label_business_name = QLabel(self.group_business)
        self.label_business_name.setObjectName(u"label_business_name")

        self.form_business.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_business_name)

        self.business_name_edit = QLineEdit(self.group_business)
        self.business_name_edit.setObjectName(u"business_name_edit")

        self.form_business.setWidget(0, QFormLayout.ItemRole.FieldRole, self.business_name_edit)

        self.label_business_goal = QLabel(self.group_business)
        self.label_business_goal.setObjectName(u"label_business_goal")

        self.form_business.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_business_goal)

        self.business_goal_edit = QTextEdit(self.group_business)
        self.business_goal_edit.setObjectName(u"business_goal_edit")
        self.business_goal_edit.setMaximumSize(QSize(16777215, 70))

        self.form_business.setWidget(1, QFormLayout.ItemRole.FieldRole, self.business_goal_edit)

        self.label_welcome = QLabel(self.group_business)
        self.label_welcome.setObjectName(u"label_welcome")

        self.form_business.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_welcome)

        self.welcome_message_edit = QTextEdit(self.group_business)
        self.welcome_message_edit.setObjectName(u"welcome_message_edit")
        self.welcome_message_edit.setMaximumSize(QSize(16777215, 70))

        self.form_business.setWidget(2, QFormLayout.ItemRole.FieldRole, self.welcome_message_edit)

        self.label_goodbye = QLabel(self.group_business)
        self.label_goodbye.setObjectName(u"label_goodbye")

        self.form_business.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_goodbye)

        self.goodbye_message_edit = QTextEdit(self.group_business)
        self.goodbye_message_edit.setObjectName(u"goodbye_message_edit")
        self.goodbye_message_edit.setMaximumSize(QSize(16777215, 70))

        self.form_business.setWidget(3, QFormLayout.ItemRole.FieldRole, self.goodbye_message_edit)


        self.content_layout.addWidget(self.group_business)

        self.group_persona = QGroupBox(self.scroll_content)
        self.group_persona.setObjectName(u"group_persona")
        self.form_persona = QFormLayout(self.group_persona)
        self.form_persona.setObjectName(u"form_persona")
        self.form_persona.setLabelAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.form_persona.setHorizontalSpacing(12)
        self.form_persona.setVerticalSpacing(10)
        self.label_tone = QLabel(self.group_persona)
        self.label_tone.setObjectName(u"label_tone")

        self.form_persona.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_tone)

        self.tone_layout = QVBoxLayout()
        self.tone_layout.setSpacing(4)
        self.tone_layout.setObjectName(u"tone_layout")
        self.tone_slider = QSlider(self.group_persona)
        self.tone_slider.setObjectName(u"tone_slider")
        self.tone_slider.setMinimum(0)
        self.tone_slider.setMaximum(10)
        self.tone_slider.setValue(5)
        self.tone_slider.setOrientation(Qt.Horizontal)
        self.tone_slider.setTickPosition(QSlider.TicksBelow)
        self.tone_slider.setTickInterval(1)

        self.tone_layout.addWidget(self.tone_slider)

        self.tone_label = QLabel(self.group_persona)
        self.tone_label.setObjectName(u"tone_label")
        self.tone_label.setAlignment(Qt.AlignCenter)

        self.tone_layout.addWidget(self.tone_label)


        self.form_persona.setLayout(0, QFormLayout.ItemRole.FieldRole, self.tone_layout)

        self.label_humor = QLabel(self.group_persona)
        self.label_humor.setObjectName(u"label_humor")

        self.form_persona.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_humor)

        self.humor_combo = QComboBox(self.group_persona)
        self.humor_combo.addItem("")
        self.humor_combo.addItem("")
        self.humor_combo.addItem("")
        self.humor_combo.setObjectName(u"humor_combo")

        self.form_persona.setWidget(1, QFormLayout.ItemRole.FieldRole, self.humor_combo)

        self.label_language = QLabel(self.group_persona)
        self.label_language.setObjectName(u"label_language")

        self.form_persona.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_language)

        self.language_combo = QComboBox(self.group_persona)
        self.language_combo.addItem("")
        self.language_combo.addItem("")
        self.language_combo.addItem("")
        self.language_combo.setObjectName(u"language_combo")

        self.form_persona.setWidget(2, QFormLayout.ItemRole.FieldRole, self.language_combo)


        self.content_layout.addWidget(self.group_persona)

        self.group_hours = QGroupBox(self.scroll_content)
        self.group_hours.setObjectName(u"group_hours")
        self.form_hours = QFormLayout(self.group_hours)
        self.form_hours.setObjectName(u"form_hours")
        self.form_hours.setLabelAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.form_hours.setHorizontalSpacing(12)
        self.form_hours.setVerticalSpacing(10)
        self.label_open = QLabel(self.group_hours)
        self.label_open.setObjectName(u"label_open")

        self.form_hours.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_open)

        self.open_time_edit = QTimeEdit(self.group_hours)
        self.open_time_edit.setObjectName(u"open_time_edit")

        self.form_hours.setWidget(0, QFormLayout.ItemRole.FieldRole, self.open_time_edit)

        self.label_close = QLabel(self.group_hours)
        self.label_close.setObjectName(u"label_close")

        self.form_hours.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_close)

        self.close_time_edit = QTimeEdit(self.group_hours)
        self.close_time_edit.setObjectName(u"close_time_edit")

        self.form_hours.setWidget(1, QFormLayout.ItemRole.FieldRole, self.close_time_edit)


        self.content_layout.addWidget(self.group_hours)

        self.group_phone = QGroupBox(self.scroll_content)
        self.group_phone.setObjectName(u"group_phone")
        self.form_phone = QFormLayout(self.group_phone)
        self.form_phone.setObjectName(u"form_phone")
        self.form_phone.setLabelAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.form_phone.setHorizontalSpacing(12)
        self.form_phone.setVerticalSpacing(10)
        self.ask_phone_confirmation_check = QCheckBox(self.group_phone)
        self.ask_phone_confirmation_check.setObjectName(u"ask_phone_confirmation_check")
        self.ask_phone_confirmation_check.setChecked(True)

        self.form_phone.setWidget(0, QFormLayout.ItemRole.SpanningRole, self.ask_phone_confirmation_check)

        self.label_phone_confirm = QLabel(self.group_phone)
        self.label_phone_confirm.setObjectName(u"label_phone_confirm")

        self.form_phone.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_phone_confirm)

        self.phone_confirm_msg_edit = QLineEdit(self.group_phone)
        self.phone_confirm_msg_edit.setObjectName(u"phone_confirm_msg_edit")

        self.form_phone.setWidget(1, QFormLayout.ItemRole.FieldRole, self.phone_confirm_msg_edit)

        self.label_phone_again = QLabel(self.group_phone)
        self.label_phone_again.setObjectName(u"label_phone_again")

        self.form_phone.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_phone_again)

        self.ask_phone_again_msg_edit = QLineEdit(self.group_phone)
        self.ask_phone_again_msg_edit.setObjectName(u"ask_phone_again_msg_edit")

        self.form_phone.setWidget(2, QFormLayout.ItemRole.FieldRole, self.ask_phone_again_msg_edit)

        self.label_phone_invalid = QLabel(self.group_phone)
        self.label_phone_invalid.setObjectName(u"label_phone_invalid")

        self.form_phone.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_phone_invalid)

        self.invalid_phone_msg_edit = QLineEdit(self.group_phone)
        self.invalid_phone_msg_edit.setObjectName(u"invalid_phone_msg_edit")

        self.form_phone.setWidget(3, QFormLayout.ItemRole.FieldRole, self.invalid_phone_msg_edit)

        self.label_phone_retry = QLabel(self.group_phone)
        self.label_phone_retry.setObjectName(u"label_phone_retry")

        self.form_phone.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_phone_retry)

        self.max_phone_retry_spin = QSpinBox(self.group_phone)
        self.max_phone_retry_spin.setObjectName(u"max_phone_retry_spin")
        self.max_phone_retry_spin.setMinimum(1)
        self.max_phone_retry_spin.setMaximum(10)
        self.max_phone_retry_spin.setValue(3)

        self.form_phone.setWidget(4, QFormLayout.ItemRole.FieldRole, self.max_phone_retry_spin)


        self.content_layout.addWidget(self.group_phone)

        self.group_company = QGroupBox(self.scroll_content)
        self.group_company.setObjectName(u"group_company")
        self.form_company = QFormLayout(self.group_company)
        self.form_company.setObjectName(u"form_company")
        self.form_company.setLabelAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.form_company.setHorizontalSpacing(12)
        self.form_company.setVerticalSpacing(10)
        self.label_address = QLabel(self.group_company)
        self.label_address.setObjectName(u"label_address")

        self.form_company.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_address)

        self.address_edit = QLineEdit(self.group_company)
        self.address_edit.setObjectName(u"address_edit")

        self.form_company.setWidget(0, QFormLayout.ItemRole.FieldRole, self.address_edit)

        self.label_phone = QLabel(self.group_company)
        self.label_phone.setObjectName(u"label_phone")

        self.form_company.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_phone)

        self.phone_edit = QLineEdit(self.group_company)
        self.phone_edit.setObjectName(u"phone_edit")

        self.form_company.setWidget(1, QFormLayout.ItemRole.FieldRole, self.phone_edit)

        self.label_delivery_area = QLabel(self.group_company)
        self.label_delivery_area.setObjectName(u"label_delivery_area")

        self.form_company.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_delivery_area)

        self.delivery_area_edit = QLineEdit(self.group_company)
        self.delivery_area_edit.setObjectName(u"delivery_area_edit")

        self.form_company.setWidget(2, QFormLayout.ItemRole.FieldRole, self.delivery_area_edit)

        self.label_payment = QLabel(self.group_company)
        self.label_payment.setObjectName(u"label_payment")

        self.form_company.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_payment)

        self.payment_methods_edit = QLineEdit(self.group_company)
        self.payment_methods_edit.setObjectName(u"payment_methods_edit")

        self.form_company.setWidget(3, QFormLayout.ItemRole.FieldRole, self.payment_methods_edit)

        self.label_discount = QLabel(self.group_company)
        self.label_discount.setObjectName(u"label_discount")

        self.form_company.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_discount)

        self.discount_policy_edit = QTextEdit(self.group_company)
        self.discount_policy_edit.setObjectName(u"discount_policy_edit")
        self.discount_policy_edit.setMaximumSize(QSize(16777215, 70))

        self.form_company.setWidget(4, QFormLayout.ItemRole.FieldRole, self.discount_policy_edit)

        self.label_brand = QLabel(self.group_company)
        self.label_brand.setObjectName(u"label_brand")

        self.form_company.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_brand)

        self.brand_story_edit = QTextEdit(self.group_company)
        self.brand_story_edit.setObjectName(u"brand_story_edit")
        self.brand_story_edit.setMaximumSize(QSize(16777215, 90))

        self.form_company.setWidget(5, QFormLayout.ItemRole.FieldRole, self.brand_story_edit)


        self.content_layout.addWidget(self.group_company)

        self.vertical_spacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.content_layout.addItem(self.vertical_spacer)

        self.scroll_area.setWidget(self.scroll_content)

        self.main_layout.addWidget(self.scroll_area)

        self.button_bar = QFrame(SettingsPage)
        self.button_bar.setObjectName(u"button_bar")
        self.button_bar.setFrameShape(QFrame.StyledPanel)
        self.button_bar_layout = QHBoxLayout(self.button_bar)
        self.button_bar_layout.setObjectName(u"button_bar_layout")
        self.button_bar_layout.setContentsMargins(0, 10, 0, 0)
        self.status_label = QLabel(self.button_bar)
        self.status_label.setObjectName(u"status_label")

        self.button_bar_layout.addWidget(self.status_label)

        self.button_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.button_bar_layout.addItem(self.button_spacer)

        self.reset_btn = QPushButton(self.button_bar)
        self.reset_btn.setObjectName(u"reset_btn")
        self.reset_btn.setMinimumSize(QSize(160, 38))
        self.reset_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.button_bar_layout.addWidget(self.reset_btn)

        self.save_btn = QPushButton(self.button_bar)
        self.save_btn.setObjectName(u"save_btn")
        self.save_btn.setMinimumSize(QSize(160, 38))
        self.save_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.button_bar_layout.addWidget(self.save_btn)


        self.main_layout.addWidget(self.button_bar)


        self.retranslateUi(SettingsPage)

        QMetaObject.connectSlotsByName(SettingsPage)
    # setupUi

    def retranslateUi(self, SettingsPage):
        self.page_title.setText(QCoreApplication.translate("SettingsPage", u"\u2699\ufe0f  \u062a\u0646\u0638\u06cc\u0645\u0627\u062a \u0633\u0627\u0645\u0627\u0646\u0647", None))
        self.group_business.setTitle(QCoreApplication.translate("SettingsPage", u"\U0001f3ea  \U00000627\U00000637\U00000644\U00000627\U00000639\U00000627\U0000062a \U000006a9\U00000633\U00000628\U0000200c\U00000648\U000006a9\U00000627\U00000631", None))
        self.label_business_name.setText(QCoreApplication.translate("SettingsPage", u"\u0646\u0627\u0645 \u06a9\u0633\u0628\u200c\u0648\u06a9\u0627\u0631:", None))
        self.business_name_edit.setPlaceholderText(QCoreApplication.translate("SettingsPage", u"\u0645\u062b\u0627\u0644: \u0641\u0633\u062a\u200c\u0641\u0648\u062f \u0633\u06a9\u0647 \u0637\u0644\u0627", None))
        self.label_business_goal.setText(QCoreApplication.translate("SettingsPage", u"\u0627\u0647\u062f\u0627\u0641 \u0686\u062a\u200c\u0628\u0627\u062a:", None))
        self.business_goal_edit.setPlaceholderText(QCoreApplication.translate("SettingsPage", u"\u062f\u0631\u06cc\u0627\u0641\u062a \u0633\u0641\u0627\u0631\u0634\u060c \u062a\u0631\u063a\u06cc\u0628 \u0645\u0634\u062a\u0631\u06cc\u060c \u0622\u067e\u200c\u0633\u0644\u0627...", None))
        self.label_welcome.setText(QCoreApplication.translate("SettingsPage", u"\u067e\u06cc\u0627\u0645 \u062e\u0648\u0634\u200c\u0622\u0645\u062f\u06af\u0648\u06cc\u06cc:", None))
        self.label_goodbye.setText(QCoreApplication.translate("SettingsPage", u"\u067e\u06cc\u0627\u0645 \u062e\u062f\u0627\u062d\u0627\u0641\u0638\u06cc:", None))
        self.group_persona.setTitle(QCoreApplication.translate("SettingsPage", u"\U0001f3ad  \U00000634\U0000062e\U00000635\U000006cc\U0000062a \U00000648 \U00000644\U0000062d\U00000646 \U00000686\U0000062a\U0000200c\U00000628\U00000627\U0000062a", None))
        self.label_tone.setText(QCoreApplication.translate("SettingsPage", u"\u0644\u062d\u0646 (\u06f0=\u0631\u0633\u0645\u06cc\u060c \u06f1\u06f0=\u0635\u0645\u06cc\u0645\u06cc):", None))
        self.tone_label.setText(QCoreApplication.translate("SettingsPage", u"\u06f5 - \u0645\u062a\u0639\u0627\u062f\u0644", None))
        self.label_humor.setText(QCoreApplication.translate("SettingsPage", u"\u0645\u06cc\u0632\u0627\u0646 \u0634\u0648\u062e\u200c\u0637\u0628\u0639\u06cc:", None))
        self.humor_combo.setItemText(0, QCoreApplication.translate("SettingsPage", u"\u06a9\u0645", None))
        self.humor_combo.setItemText(1, QCoreApplication.translate("SettingsPage", u"\u0645\u062a\u0648\u0633\u0637", None))
        self.humor_combo.setItemText(2, QCoreApplication.translate("SettingsPage", u"\u0632\u06cc\u0627\u062f", None))

        self.label_language.setText(QCoreApplication.translate("SettingsPage", u"\u0632\u0628\u0627\u0646 \u0686\u062a\u200c\u0628\u0627\u062a:", None))
        self.language_combo.setItemText(0, QCoreApplication.translate("SettingsPage", u"\u0641\u0627\u0631\u0633\u06cc", None))
        self.language_combo.setItemText(1, QCoreApplication.translate("SettingsPage", u"\u0627\u0646\u06af\u0644\u06cc\u0633\u06cc", None))
        self.language_combo.setItemText(2, QCoreApplication.translate("SettingsPage", u"\u062f\u0648\u0632\u0628\u0627\u0646\u0647", None))

        self.group_hours.setTitle(QCoreApplication.translate("SettingsPage", u"\U0001f550  \U00000633\U00000627\U00000639\U00000627\U0000062a \U000006a9\U00000627\U00000631\U000006cc", None))
        self.label_open.setText(QCoreApplication.translate("SettingsPage", u"\u0633\u0627\u0639\u062a \u0634\u0631\u0648\u0639:", None))
        self.open_time_edit.setDisplayFormat(QCoreApplication.translate("SettingsPage", u"HH:mm", None))
        self.label_close.setText(QCoreApplication.translate("SettingsPage", u"\u0633\u0627\u0639\u062a \u067e\u0627\u06cc\u0627\u0646:", None))
        self.close_time_edit.setDisplayFormat(QCoreApplication.translate("SettingsPage", u"HH:mm", None))
        self.group_phone.setTitle(QCoreApplication.translate("SettingsPage", u"\U0001f4de  \U0000062a\U00000627\U000006cc\U000006cc\U0000062f \U00000634\U00000645\U00000627\U00000631\U00000647 \U0000062a\U00000645\U00000627\U00000633", None))
        self.ask_phone_confirmation_check.setText(QCoreApplication.translate("SettingsPage", u"\u067e\u0631\u0633\u06cc\u062f\u0646 \u062a\u0627\u06cc\u06cc\u062f \u0634\u0645\u0627\u0631\u0647 \u0641\u0639\u0627\u0644 \u0628\u0627\u0634\u062f", None))
        self.label_phone_confirm.setText(QCoreApplication.translate("SettingsPage", u"\u067e\u06cc\u0627\u0645 \u062a\u0627\u06cc\u06cc\u062f \u0634\u0645\u0627\u0631\u0647:", None))
        self.label_phone_again.setText(QCoreApplication.translate("SettingsPage", u"\u067e\u06cc\u0627\u0645 \u062f\u0631\u062e\u0648\u0627\u0633\u062a \u0634\u0645\u0627\u0631\u0647 \u062c\u062f\u06cc\u062f:", None))
        self.label_phone_invalid.setText(QCoreApplication.translate("SettingsPage", u"\u067e\u06cc\u0627\u0645 \u0634\u0645\u0627\u0631\u0647 \u0646\u0627\u0645\u0639\u062a\u0628\u0631:", None))
        self.label_phone_retry.setText(QCoreApplication.translate("SettingsPage", u"\u062d\u062f\u0627\u06a9\u062b\u0631 \u062a\u0644\u0627\u0634:", None))
        self.group_company.setTitle(QCoreApplication.translate("SettingsPage", u"\U0001f3e2  \U00000627\U00000637\U00000644\U00000627\U00000639\U00000627\U0000062a \U00000634\U00000631\U000006a9\U0000062a (Knowledge Base)", None))
        self.label_address.setText(QCoreApplication.translate("SettingsPage", u"\u0622\u062f\u0631\u0633 \u0641\u06cc\u0632\u06cc\u06a9\u06cc:", None))
        self.label_phone.setText(QCoreApplication.translate("SettingsPage", u"\u0634\u0645\u0627\u0631\u0647 \u062a\u0645\u0627\u0633 \u0634\u0631\u06a9\u062a:", None))
        self.label_delivery_area.setText(QCoreApplication.translate("SettingsPage", u"\u0645\u062d\u062f\u0648\u062f\u0647 \u0627\u0631\u0633\u0627\u0644:", None))
        self.label_payment.setText(QCoreApplication.translate("SettingsPage", u"\u0631\u0648\u0634\u200c\u0647\u0627\u06cc \u067e\u0631\u062f\u0627\u062e\u062a:", None))
        self.label_discount.setText(QCoreApplication.translate("SettingsPage", u"\u0633\u06cc\u0627\u0633\u062a \u062a\u062e\u0641\u06cc\u0641:", None))
        self.label_brand.setText(QCoreApplication.translate("SettingsPage", u"\u0645\u0639\u0631\u0641\u06cc \u0628\u0631\u0646\u062f:", None))
        self.status_label.setText("")
        self.reset_btn.setText(QCoreApplication.translate("SettingsPage", u"\u21ba  \u0628\u0627\u0632\u0646\u0634\u0627\u0646\u06cc \u0628\u0647 \u067e\u06cc\u0634\u200c\u0641\u0631\u0636", None))
        self.save_btn.setText(QCoreApplication.translate("SettingsPage", u"\U0001f4be  \U00000630\U0000062e\U000006cc\U00000631\U00000647 \U0000062a\U00000646\U00000638\U000006cc\U00000645\U00000627\U0000062a", None))
        pass
    # retranslateUi

