from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout


class FinanceCard(QFrame):
    def __init__(self, title_text, value_text, object_name):
        super().__init__()
        self.setObjectName(object_name)
        self.setMinimumWidth(150)
        self.setFixedHeight(132)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)

        title = QLabel(title_text)
        title.setObjectName("cardTitle")
        title.setMinimumHeight(20)

        self.value_label = QLabel(value_text)
        self.value_label.setObjectName("cardValue")
        self.value_label.setMinimumHeight(34)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        layout.addWidget(title)
        layout.addWidget(self.value_label)
        layout.addStretch()

    def set_value(self, value_text):
        self.value_label.setText(value_text)
