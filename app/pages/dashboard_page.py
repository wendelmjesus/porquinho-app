from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QPushButton, QVBoxLayout


class DashboardPage(QFrame):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setObjectName("content")
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 35, 40, 35)
        layout.setSpacing(0)

        title = QLabel("Dashboard")
        title.setObjectName("pageTitle")
        title.setMinimumHeight(40)
        title.setWordWrap(True)

        subtitle = QLabel("Acompanhe sua vida financeira.")
        subtitle.setObjectName("pageSubtitle")
        subtitle.setMinimumHeight(24)
        subtitle.setWordWrap(True)

        header_layout = QGridLayout()
        self.controller.dashboard_header_layout = header_layout
        header_layout.setHorizontalSpacing(12)
        header_layout.setVerticalSpacing(12)

        title_container = QVBoxLayout()
        title_container.setSpacing(0)
        title_container.addWidget(title)
        title_container.addWidget(subtitle)

        quick_income_button = QPushButton("Nova receita")
        quick_income_button.setObjectName("primaryButton")
        quick_income_button.setFixedHeight(40)
        quick_income_button.setCursor(Qt.CursorShape.PointingHandCursor)
        quick_income_button.clicked.connect(
            lambda: self.controller.open_transaction_dialog("Receita")
        )

        quick_expense_button = QPushButton("Nova despesa")
        quick_expense_button.setObjectName("secondaryButton")
        quick_expense_button.setFixedHeight(40)
        quick_expense_button.setCursor(Qt.CursorShape.PointingHandCursor)
        quick_expense_button.clicked.connect(
            lambda: self.controller.open_transaction_dialog("Despesa")
        )

        header_layout.addLayout(title_container, 0, 0, 2, 1)
        header_layout.addWidget(quick_income_button, 0, 1)
        header_layout.addWidget(quick_expense_button, 1, 1)
        header_layout.setColumnStretch(0, 1)

        layout.addLayout(header_layout)
        layout.addSpacing(30)

        self.controller.cards_layout = QGridLayout()
        self.controller.cards_layout.setHorizontalSpacing(18)
        self.controller.cards_layout.setVerticalSpacing(18)

        balance_card = self.controller.create_finance_card(
            "Saldo",
            "R$ 0,00",
            "balanceCard",
        )
        income_card = self.controller.create_finance_card(
            "Receitas",
            "R$ 0,00",
            "incomeCard",
        )
        expense_card = self.controller.create_finance_card(
            "Despesas",
            "R$ 0,00",
            "expenseCard",
        )

        self.controller.finance_cards = [
            balance_card,
            income_card,
            expense_card,
        ]
        self.controller.refresh_dashboard_summary()
        self.controller.update_cards_layout()

        layout.addLayout(self.controller.cards_layout)
        layout.addSpacing(30)

        self.controller.dashboard_bottom_layout = QGridLayout()
        self.controller.dashboard_bottom_layout.setHorizontalSpacing(18)
        self.controller.dashboard_bottom_layout.setVerticalSpacing(18)

        chart_panel = self.controller.create_chart_panel()
        transactions_panel = self.controller.create_transactions_panel()
        goals_panel = self.controller.create_dashboard_goals_panel()

        self.controller.dashboard_panels = [
            chart_panel,
            transactions_panel,
            goals_panel,
        ]
        self.controller.update_dashboard_panels_layout()

        layout.addLayout(self.controller.dashboard_bottom_layout)
        layout.addStretch()
