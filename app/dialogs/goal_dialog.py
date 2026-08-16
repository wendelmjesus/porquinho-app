from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
)


class GoalDialog(QDialog):
    def __init__(self, parent, goal):
        super().__init__(parent)
        self.setWindowTitle("Editar meta")
        self.setObjectName("transactionDialog")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(16)

        form_layout = QFormLayout()
        form_layout.setSpacing(12)

        self.name_input = QLineEdit()
        self.name_input.setObjectName("searchInput")
        self.name_input.setFixedHeight(40)
        self.name_input.setText(goal["name"])

        self.current_input = QDoubleSpinBox()
        self.current_input.setObjectName("amountInput")
        self.current_input.setFixedHeight(40)
        self.current_input.setPrefix("R$ ")
        self.current_input.setDecimals(2)
        self.current_input.setMaximum(9999999.99)
        self.current_input.setValue(goal["current"])

        self.target_input = QDoubleSpinBox()
        self.target_input.setObjectName("amountInput")
        self.target_input.setFixedHeight(40)
        self.target_input.setPrefix("R$ ")
        self.target_input.setDecimals(2)
        self.target_input.setMaximum(9999999.99)
        self.target_input.setValue(goal["target"])

        form_layout.addRow("Nome", self.name_input)
        form_layout.addRow("Guardado", self.current_input)
        form_layout.addRow("Objetivo", self.target_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(buttons)

    def get_goal_data(self):
        return {
            "name": self.name_input.text().strip() or "Meta sem nome",
            "current": self.current_input.value(),
            "target": self.target_input.value(),
        }
