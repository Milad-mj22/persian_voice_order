# -*- coding: utf-8 -*-
# ⚠️ این فایل به صورت خودکار تولید شده است.
# 📄 فایل منبع: app\ui\ui_files\reports_page.ui
# 🚫 تغییرات دستی در این فایل از بین خواهند رفت.
# 🔧 برای ویرایش، فایل .ui را در Qt Designer باز کنید.
#
# تولید شده توسط: compile_ui.py
# =====================================================

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'reports_page.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_ReportsPage(object):
    def setupUi(self, ReportsPage):
        if not ReportsPage.objectName():
            ReportsPage.setObjectName(u"ReportsPage")
        ReportsPage.resize(950, 700)
        ReportsPage.setLayoutDirection(Qt.RightToLeft)
        self.main_layout = QVBoxLayout(ReportsPage)
        self.main_layout.setSpacing(14)
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.page_title = QLabel(ReportsPage)
        self.page_title.setObjectName(u"page_title")
        self.page_title.setAlignment(Qt.AlignRight|Qt.AlignVCenter)

        self.main_layout.addWidget(self.page_title)

        self.cards_layout = QHBoxLayout()
        self.cards_layout.setSpacing(12)
        self.cards_layout.setObjectName(u"cards_layout")
        self.card_today_count = QFrame(ReportsPage)
        self.card_today_count.setObjectName(u"card_today_count")
        self.card_today_count.setFrameShape(QFrame.StyledPanel)
        self.card_today_count.setMinimumSize(QSize(180, 100))
        self.c1 = QVBoxLayout(self.card_today_count)
        self.c1.setObjectName(u"c1")
        self.label_today_count = QLabel(self.card_today_count)
        self.label_today_count.setObjectName(u"label_today_count")
        self.label_today_count.setAlignment(Qt.AlignCenter)

        self.c1.addWidget(self.label_today_count)

        self.value_today_count = QLabel(self.card_today_count)
        self.value_today_count.setObjectName(u"value_today_count")
        self.value_today_count.setAlignment(Qt.AlignCenter)

        self.c1.addWidget(self.value_today_count)


        self.cards_layout.addWidget(self.card_today_count)

        self.card_today_sum = QFrame(ReportsPage)
        self.card_today_sum.setObjectName(u"card_today_sum")
        self.card_today_sum.setFrameShape(QFrame.StyledPanel)
        self.card_today_sum.setMinimumSize(QSize(180, 100))
        self.c2 = QVBoxLayout(self.card_today_sum)
        self.c2.setObjectName(u"c2")
        self.label_today_sum = QLabel(self.card_today_sum)
        self.label_today_sum.setObjectName(u"label_today_sum")
        self.label_today_sum.setAlignment(Qt.AlignCenter)

        self.c2.addWidget(self.label_today_sum)

        self.value_today_sum = QLabel(self.card_today_sum)
        self.value_today_sum.setObjectName(u"value_today_sum")
        self.value_today_sum.setAlignment(Qt.AlignCenter)

        self.c2.addWidget(self.value_today_sum)


        self.cards_layout.addWidget(self.card_today_sum)

        self.card_total_count = QFrame(ReportsPage)
        self.card_total_count.setObjectName(u"card_total_count")
        self.card_total_count.setFrameShape(QFrame.StyledPanel)
        self.card_total_count.setMinimumSize(QSize(180, 100))
        self.c3 = QVBoxLayout(self.card_total_count)
        self.c3.setObjectName(u"c3")
        self.label_total_count = QLabel(self.card_total_count)
        self.label_total_count.setObjectName(u"label_total_count")
        self.label_total_count.setAlignment(Qt.AlignCenter)

        self.c3.addWidget(self.label_total_count)

        self.value_total_count = QLabel(self.card_total_count)
        self.value_total_count.setObjectName(u"value_total_count")
        self.value_total_count.setAlignment(Qt.AlignCenter)

        self.c3.addWidget(self.value_total_count)


        self.cards_layout.addWidget(self.card_total_count)

        self.card_total_sum = QFrame(ReportsPage)
        self.card_total_sum.setObjectName(u"card_total_sum")
        self.card_total_sum.setFrameShape(QFrame.StyledPanel)
        self.card_total_sum.setMinimumSize(QSize(180, 100))
        self.c4 = QVBoxLayout(self.card_total_sum)
        self.c4.setObjectName(u"c4")
        self.label_total_sum = QLabel(self.card_total_sum)
        self.label_total_sum.setObjectName(u"label_total_sum")
        self.label_total_sum.setAlignment(Qt.AlignCenter)

        self.c4.addWidget(self.label_total_sum)

        self.value_total_sum = QLabel(self.card_total_sum)
        self.value_total_sum.setObjectName(u"value_total_sum")
        self.value_total_sum.setAlignment(Qt.AlignCenter)

        self.c4.addWidget(self.value_total_sum)


        self.cards_layout.addWidget(self.card_total_sum)


        self.main_layout.addLayout(self.cards_layout)

        self.charts_layout = QHBoxLayout()
        self.charts_layout.setSpacing(12)
        self.charts_layout.setObjectName(u"charts_layout")
        self.chart_group = QGroupBox(ReportsPage)
        self.chart_group.setObjectName(u"chart_group")
        self.chart_outer = QVBoxLayout(self.chart_group)
        self.chart_outer.setObjectName(u"chart_outer")
        self.chart_container = QWidget(self.chart_group)
        self.chart_container.setObjectName(u"chart_container")
        self.chart_container.setMinimumSize(QSize(500, 300))

        self.chart_outer.addWidget(self.chart_container)


        self.charts_layout.addWidget(self.chart_group)

        self.top_group = QGroupBox(ReportsPage)
        self.top_group.setObjectName(u"top_group")
        self.top_group.setMinimumSize(QSize(320, 0))
        self.top_layout = QVBoxLayout(self.top_group)
        self.top_layout.setObjectName(u"top_layout")
        self.top_products_list = QListWidget(self.top_group)
        self.top_products_list.setObjectName(u"top_products_list")

        self.top_layout.addWidget(self.top_products_list)


        self.charts_layout.addWidget(self.top_group)


        self.main_layout.addLayout(self.charts_layout)

        self.bottom_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.main_layout.addItem(self.bottom_spacer)


        self.retranslateUi(ReportsPage)

        QMetaObject.connectSlotsByName(ReportsPage)
    # setupUi

    def retranslateUi(self, ReportsPage):
        self.page_title.setText(QCoreApplication.translate("ReportsPage", u"\U0001f4c8  \U000006af\U00000632\U00000627\U00000631\U00000634\U00000627\U0000062a", None))
        self.label_today_count.setText(QCoreApplication.translate("ReportsPage", u"\u0633\u0641\u0627\u0631\u0634\u0627\u062a \u0627\u0645\u0631\u0648\u0632", None))
        self.value_today_count.setText(QCoreApplication.translate("ReportsPage", u"0", None))
        self.label_today_sum.setText(QCoreApplication.translate("ReportsPage", u"\u0641\u0631\u0648\u0634 \u0627\u0645\u0631\u0648\u0632 (\u062a\u0648\u0645\u0627\u0646)", None))
        self.value_today_sum.setText(QCoreApplication.translate("ReportsPage", u"0", None))
        self.label_total_count.setText(QCoreApplication.translate("ReportsPage", u"\u06a9\u0644 \u0633\u0641\u0627\u0631\u0634\u0627\u062a", None))
        self.value_total_count.setText(QCoreApplication.translate("ReportsPage", u"0", None))
        self.label_total_sum.setText(QCoreApplication.translate("ReportsPage", u"\u06a9\u0644 \u0641\u0631\u0648\u0634 (\u062a\u0648\u0645\u0627\u0646)", None))
        self.value_total_sum.setText(QCoreApplication.translate("ReportsPage", u"0", None))
        self.chart_group.setTitle(QCoreApplication.translate("ReportsPage", u"\U0001f4ca  \U00000641\U00000631\U00000648\U00000634 \U000006f7 \U00000631\U00000648\U00000632 \U00000627\U0000062e\U000006cc\U00000631", None))
        self.top_group.setTitle(QCoreApplication.translate("ReportsPage", u"\U0001f3c6  \U0000067e\U00000631 \U00000641\U00000631\U00000648\U00000634\U0000200c\U0000062a\U00000631\U000006cc\U00000646\U0000200c\U00000647\U00000627", None))
        pass
    # retranslateUi

