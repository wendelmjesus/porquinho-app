from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
)


class ReportsPage(QFrame):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setObjectName("content")
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        self.controller.reports_content_layout = layout
        layout.setContentsMargins(40, 35, 40, 35)
        layout.setSpacing(0)

        title = QLabel("Relatórios")
        title.setObjectName("pageTitle")
        title.setMinimumHeight(40)
        title.setWordWrap(True)

        subtitle = QLabel("Visualize e exporte seus relatórios detalhados sobre suas finanças.")
        subtitle.setObjectName("pageSubtitle")
        subtitle.setMinimumHeight(24)
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(28)

        actions_frame = QFrame()
        actions_frame.setObjectName("filtersFrame")

        actions_layout = QGridLayout(actions_frame)
        self.controller.report_actions_layout = actions_layout
        actions_layout.setContentsMargins(18, 14, 18, 14)
        actions_layout.setHorizontalSpacing(12)
        actions_layout.setVerticalSpacing(12)

        export_button = QPushButton("Exportar para Excel")
        export_button.setObjectName("primaryButton")
        export_button.setFixedHeight(40)
        export_button.setCursor(Qt.CursorShape.PointingHandCursor)
        export_button.clicked.connect(self.controller.export_transactions_to_excel)

        refresh_report_button = QPushButton("Atualizar relatório")
        refresh_report_button.setObjectName("secondaryButton")
        refresh_report_button.setFixedHeight(40)
        refresh_report_button.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_report_button.clicked.connect(self.controller.refresh_reports)

        report_status_label = QLabel("")
        report_status_label.setObjectName("filtersStatus")
        report_status_label.setFixedHeight(40)

        self.controller.report_status_label = report_status_label
        self.controller.export_report_button = export_button
        self.controller.refresh_report_button = refresh_report_button

        actions_layout.addWidget(export_button, 0, 0)
        actions_layout.addWidget(refresh_report_button, 0, 1)
        actions_layout.addWidget(report_status_label, 0, 2)
        actions_layout.setColumnStretch(0, 1)
        actions_layout.setColumnStretch(1, 1)
        actions_layout.setColumnStretch(2, 2)

        layout.addWidget(actions_frame)
        layout.addSpacing(20)

        summary_layout = QGridLayout()
        self.controller.report_summary_layout = summary_layout
        summary_layout.setHorizontalSpacing(18)
        summary_layout.setVerticalSpacing(18)

        self.controller.report_income_card = self.controller.create_finance_card(
            "Receitas",
            "R$ 0,00",
            "incomeCard",
        )
        self.controller.report_expense_card = self.controller.create_finance_card(
            "Despesas",
            "R$ 0,00",
            "expenseCard",
        )
        self.controller.report_balance_card = self.controller.create_finance_card(
            "Saldo",
            "R$ 0,00",
            "balanceCard",
        )

        summary_layout.addWidget(self.controller.report_income_card, 0, 0)
        summary_layout.addWidget(self.controller.report_expense_card, 0, 1)
        summary_layout.addWidget(self.controller.report_balance_card, 0, 2)
        summary_layout.setColumnStretch(0, 1)
        summary_layout.setColumnStretch(1, 1)
        summary_layout.setColumnStretch(2, 1)

        layout.addLayout(summary_layout)
        layout.addSpacing(20)

        category_report_table = QTableWidget()
        category_report_table.setObjectName("transactionsTable")
        category_report_table.setMinimumHeight(320)
        category_report_table.setColumnCount(3)
        category_report_table.setHorizontalHeaderLabels([
            "Categoria",
            "Tipo",
            "Total",
        ])
        category_report_table.verticalHeader().setVisible(False)
        category_report_table.setShowGrid(False)
        category_report_table.setAlternatingRowColors(True)
        category_report_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        report_header = category_report_table.horizontalHeader()
        report_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        report_header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        report_header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        self.controller.category_report_table = category_report_table

        layout.addWidget(category_report_table)
        layout.addStretch()

        self.controller.refresh_reports()
        self.controller.update_reports_layout()
