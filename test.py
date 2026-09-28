import sys
from PySide6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
label = QLabel("سلام! PySide6 کار می‌کنه ✅")
label.setLayoutDirection(label.layoutDirection().RightToLeft)
label.resize(400, 100)
label.show()
sys.exit(app.exec())