from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
)


class TransactionDialog(QDialog):
    def __init__(self, parent, get_categories, default_type="Receita", transaction=None):
        super().__init__(parent)
        self.get_categories = get_categories
        self.transaction = transaction
        self.setWindowTitle("Editar transação" if transaction else "Nova transação")
        self.setObjectName("transactionDialog")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(16)

        form_layout = QFormLayout()
        form_layout.setSpacing(12)

        self.description_input = QLineEdit()
        self.description_input.setObjectName("searchInput")
        self.description_input.setPlaceholderText("Ex: Mercado")
        self.description_input.setFixedHeight(40)

        self.category_input = QComboBox()
        self.category_input.setObjectName("filterCombo")
        self.category_input.setFixedHeight(40)

        self.type_input = QComboBox()
        self.type_input.setObjectName("filterCombo")
        self.type_input.setFixedHeight(40)
        self.type_input.addItems(["Receita", "Despesa"])
        self.type_input.setCurrentText(transaction["type"] if transaction else default_type)
        self.type_input.currentTextChanged.connect(self.update_categories)
        self.update_categories()

        if transaction:
            self.description_input.setText(transaction["description"])
            self.category_input.setCurrentText(transaction["category"])

        self.date_input = QDateEdit()
        self.date_input.setObjectName("dateInput")
        self.date_input.setFixedHeight(40)
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd/MM/yyyy")
        self.date_input.setDate(QDate.currentDate())

        if transaction:
            transaction_date = QDate.fromString(transaction["date"], "dd/MM/yyyy")

            if transaction_date.isValid():
                self.date_input.setDate(transaction_date)

        self.amount_input = QDoubleSpinBox()
        self.amount_input.setObjectName("amountInput")
        self.amount_input.setFixedHeight(40)
        self.amount_input.setPrefix("R$ ")
        self.amount_input.setDecimals(2)
        self.amount_input.setMaximum(9999999.99)

        if transaction:
            self.amount_input.setValue(abs(transaction["amount"]))

        form_layout.addRow("Descrição", self.description_input)
        form_layout.addRow("Categoria", self.category_input)
        form_layout.addRow("Tipo", self.type_input)
        form_layout.addRow("Data", self.date_input)
        form_layout.addRow("Valor", self.amount_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(buttons)

    def update_categories(self):
        current_category = self.category_input.currentText()
        self.category_input.clear()
        self.category_input.addItems(self.get_categories(self.type_input.currentText()))

        if current_category:
            self.category_input.setCurrentText(current_category)

    def get_transaction_data(self):
        description = self.description_input.text().strip()

        if not description:
            description = "Sem descrição"

        amount = self.amount_input.value()

        if self.type_input.currentText() == "Despesa":
            amount = -amount

        return {
            "description": description,
            "category": self.category_input.currentText(),
            "type": self.type_input.currentText(),
            "date": self.date_input.date().toString("dd/MM/yyyy"),
            "amount": amount,
        }
