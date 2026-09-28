"""
حباب چت برای نمایش پیام‌ها
"""
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt


class ChatBubble(QFrame):
    """
    حباب چت - پیام بات سمت راست، پیام کاربر سمت چپ
    """

    def __init__(self, text: str, role: str = "bot",
                 timestamp: str = "", parent=None):
        """
        Args:
            text: متن پیام
            role: "bot" | "user" | "system"
            timestamp: زمان به صورت رشته
        """
        super().__init__(parent)

        self.role = role
        self._setup_ui(text, timestamp)

    def _setup_ui(self, text: str, timestamp: str):
        # --- استایل بر اساس نقش ---
        if self.role == "user":
            bg = "#3b82f6"      # آبی
            fg = "#ffffff"
            align = Qt.AlignLeft
            icon = "👤"
            border_radius = "14px 14px 14px 4px"
        elif self.role == "system":
            bg = "#f1f5f9"      # خاکستری روشن
            fg = "#64748b"
            align = Qt.AlignCenter
            icon = "⚙️"
            border_radius = "8px"
        else:  # bot
            bg = "#ffffff"      # سفید
            fg = "#1e293b"
            align = Qt.AlignRight
            icon = "🤖"
            border_radius = "14px 14px 4px 14px"

        # --- ساخت حباب ---
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg};
                border-radius: {border_radius};
                border: 1px solid #e2e8f0;
            }}
        """)

        self.setMaximumWidth(420)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)

        # --- متن ---
        text_label = QLabel(f"{icon}  {text}")
        text_label.setWordWrap(True)
        text_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        text_label.setStyleSheet(f"""
            color: {fg};
            font-size: 13px;
            background: transparent;
            border: none;
        """)
        layout.addWidget(text_label)

        # --- زمان ---
        if timestamp:
            time_label = QLabel(timestamp)
            time_label.setStyleSheet(f"""
                color: {fg};
                font-size: 10px;
                background: transparent;
                border: none;
                opacity: 0.7;
            """)
            time_label.setAlignment(Qt.AlignLeft)
            layout.addWidget(time_label)


class ChatContainer(QWidget):
    """نگهدارنده حباب‌ها با چیدمان درست"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(8)
        self._layout.addStretch()

    def add_message(self, text: str, role: str = "bot",
                    timestamp: str = ""):
        """افزودن حباب جدید"""
        bubble = ChatBubble(text, role, timestamp)

        # ساخت ردیف با تراز مناسب
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)

        if role == "user":
            row_layout.addWidget(bubble, 0, Qt.AlignLeft)
            row_layout.addStretch()
        elif role == "system":
            row_layout.addStretch()
            row_layout.addWidget(bubble, 0, Qt.AlignCenter)
            row_layout.addStretch()
        else:  # bot
            row_layout.addStretch()
            row_layout.addWidget(bubble, 0, Qt.AlignRight)

        # درج قبل از stretch
        self._layout.insertWidget(self._layout.count() - 1, row)
        return bubble

    def clear(self):
        """پاک کردن همه پیام‌ها"""
        while self._layout.count() > 1:
            item = self._layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()