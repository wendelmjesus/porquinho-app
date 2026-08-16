import os
import sys
from datetime import date

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Porquinho")
        self.resize(1200,760)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.pages = QStackedWidget()
        self.menu_buttons = []
        self.transactions = []
        self.next_transaction_id = 1

        self.dashboard_page = self.create_content()

        self.transactions_page = self.create_transactions_page()

        self.categories_page = self.create_simple_page(
            "Categorias", 
            "Organize suas transações em categorias."
        )

        self.goals_page = self.create_simple_page(
            "Metas", 
            "Defina metas financeiras e acompanhe seu progresso."
        )

        self.reports_page = self.create_simple_page(
            "Relatórios", 
            "Visualize e exporte seus relatórios detalhados sobre suas finanças."
        )

        self.settings_page = self.create_simple_page(
            "Configurações", 
            "Personalize sua experiência."
        )

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.transactions_page)
        self.pages.addWidget(self.categories_page)
        self.pages.addWidget(self.goals_page)
        self.pages.addWidget(self.reports_page)
        self.pages.addWidget(self.settings_page)

        sidebar = self.create_sidebar()

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages, 1)

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(250)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(22, 28, 22, 24)
        layout.setSpacing(8)

        logo = QLabel()
        logo.setObjectName("sidebarLogo")
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "porquinho_logo.png")
        logo_pixmap = QPixmap(logo_path)
        logo.setPixmap(
            logo_pixmap.scaled(
                48,
                48,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        logo.setFixedSize(72, 72)
        logo.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        layout.addWidget(logo)
        layout.addSpacing(20)

        buttons = [
            ("Dashboard", 0),
            ("Transações", 1),
            ("Categorias", 2),
            ("Metas", 3),
            ("Relatórios", 4)
        ]

        for button_name, page_index in buttons:
            button = QPushButton(button_name)

            button.setObjectName("menuButton")
            button.setFixedHeight(44)
            button.setCursor(Qt.CursorShape.PointingHandCursor)

            button.setCheckable(True)

            button.clicked.connect(
                lambda checked, index=page_index, btn=button:
                self.change_page(index, btn)
            )

            self.menu_buttons.append(button)

            layout.addWidget(button)

        self.menu_buttons[0].setChecked(True)

        layout.addStretch()

        restart_button = QPushButton("Reiniciar app")
        restart_button.setObjectName("menuButton")
        restart_button.setFixedHeight(44)
        restart_button.setCursor(Qt.CursorShape.PointingHandCursor)
        restart_button.clicked.connect(self.restart_app)

        settings_button = QPushButton("Configurações")
        settings_button.setObjectName("menuButton")
        settings_button.setFixedHeight(44)
        settings_button.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_button.setCheckable(True)

        settings_button.clicked.connect(
            lambda checked, btn=settings_button:
            self.change_page(5, btn)
        )
        self.menu_buttons.append(settings_button)

        layout.addWidget(restart_button)
        layout.addWidget(settings_button)

        return sidebar

    def restart_app(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    def create_simple_page(self, title_text, subtitle_text):
        page = QFrame()
        page.setObjectName("content")

        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 35, 40, 35)
        layout.setSpacing(0)

        title = QLabel(title_text)
        title.setObjectName("pageTitle")
        title.setFixedHeight(40)

        subtitle = QLabel(subtitle_text)
        subtitle.setObjectName("pageSubtitle")
        subtitle.setFixedHeight(24)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addStretch()

        return page

    def change_page(self, index, clicked_button):
        self.pages.setCurrentIndex(index)

        for button in self.menu_buttons:
            button.setChecked(False)

        clicked_button.setChecked(True)

    def create_content(self):
        content = QFrame()
        content.setObjectName("content")

        layout = QVBoxLayout(content)

        layout.setContentsMargins(40, 35, 40, 35)
        layout.setSpacing(0)

        title = QLabel("Dashboard")
        title.setObjectName("pageTitle")
        title.setFixedHeight(40)

        subtitle = QLabel("Acompanhe sua vida financeira.")
        subtitle.setObjectName("pageSubtitle")
        subtitle.setFixedHeight(24)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(30)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(18)

        balance_card = self.create_finance_card(
            "Saldo", 
            "R$ 0,00",
            "balanceCard"
        )

        income_card = self.create_finance_card(
            "Receitas", 
            "R$ 0,00",
            "incomeCard"
        )

        expense_card = self.create_finance_card(
            "Despesas", 
            "R$ 0,00",
            "expenseCard"
        )

        cards_layout.addWidget(balance_card)
        cards_layout.addWidget(income_card)
        cards_layout.addWidget(expense_card)

        layout.addLayout(cards_layout)

        layout.addSpacing(30)

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(18)

        chart_panel = self.create_chart_panel()
        transactions_panel = self.create_transactions_panel()

        bottom_layout.addWidget(chart_panel, 2)
        bottom_layout.addWidget(transactions_panel, 1)

        layout.addLayout(bottom_layout)

        layout.addStretch()

        return content
    
    def create_finance_card(self, title_text, value_text, object_name):
        card = QFrame () 
        card.setObjectName(object_name)
        card.setMinimumWidth(150)
        card.setFixedHeight(132)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)

        title = QLabel(title_text)
        title.setObjectName("cardTitle")
        title.setMinimumHeight(20)

        value = QLabel(value_text)
        value.setObjectName("cardValue")
        value.setMinimumHeight(34)
        value.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        layout.addWidget(title)
        layout.addWidget(value)

        layout.addStretch()

        return card
    
    def create_chart_panel(self):
        panel = QFrame()
        panel.setObjectName("dashboardPanel")
        panel.setMinimumHeight(300)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(22, 20, 22, 20)

        title = QLabel("Evolução financeira")
        title.setObjectName("panelTitle")

        placeholder = QLabel("O gráfico aparecerá aqui")
        placeholder.setObjectName("chartPlaceholder")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)
        layout.addSpacing(15)
        layout.addWidget(placeholder, 1)

        return panel

    def create_transactions_panel(self):
        panel = QFrame()
        panel.setObjectName("dashboardPanel")
        panel.setMinimumHeight(300)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(12)

        title = QLabel("Transações recentes")
        title.setObjectName("panelTitle")

        layout.addWidget(title)
        layout.addSpacing(10)

        if self.transactions:
            for transaction in self.transactions[:4]:
                row = QHBoxLayout()

                description_label = QLabel(transaction["description"])
                description_label.setObjectName("transactionDescription")

                value_label = QLabel(self.format_currency(transaction["amount"]))
                value_label.setObjectName("transactionValue")

                row.addWidget(description_label)
                row.addStretch()
                row.addWidget(value_label)

                layout.addLayout(row)
        else:
            empty_label = QLabel("Nenhuma transação cadastrada")
            empty_label.setObjectName("transactionDescription")
            layout.addWidget(empty_label)

        layout.addStretch()

        return panel

    def create_transactions_page(self):
        page = QFrame()
        page.setObjectName("content")

        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 35, 40, 35)
        layout.setSpacing(0)

        header_layout = QHBoxLayout()

        title_container = QVBoxLayout()
        title_container.setSpacing(0)

        title = QLabel("Transações")
        title.setObjectName("pageTitle")
        title.setFixedHeight(40)

        subtitle = QLabel("Gerencie suas receitas e despesas.")
        subtitle.setObjectName("pageSubtitle")
        subtitle.setFixedHeight(24)

        title_container.addWidget(title)
        title_container.addWidget(subtitle)

        new_transaction_button = QPushButton("Nova transação")
        new_transaction_button.setObjectName("primaryButton")
        new_transaction_button.setFixedHeight(42)
        new_transaction_button.setCursor(Qt.CursorShape.PointingHandCursor)
        new_transaction_button.clicked.connect(self.add_demo_transaction)

        header_layout.addLayout(title_container)
        header_layout.addStretch()
        header_layout.addWidget(new_transaction_button)

        layout.addLayout(header_layout)

        layout.addSpacing(28)

        filters_frame = QFrame()
        filters_frame.setObjectName("filtersFrame")

        filters_layout = QHBoxLayout(filters_frame)
        filters_layout.setContentsMargins(18, 14, 18, 14)
        filters_layout.setSpacing(12)

        search_input = QLineEdit()
        search_input.setObjectName("searchInput")
        search_input.setPlaceholderText("Buscar transação...")
        search_input.setMinimumWidth(250)
        search_input.setFixedHeight(40)
        search_input.textChanged.connect(self.apply_transaction_filters)

        type_filter = QComboBox()
        type_filter.setObjectName("filterCombo")
        type_filter.setFixedHeight(40)
        type_filter.addItems([
            "Todos os tipos",
            "Receitas",
            "Despesas",
        ])
        type_filter.currentTextChanged.connect(self.apply_transaction_filters)

        category_filter = QComboBox()
        category_filter.setObjectName("filterCombo")
        category_filter.setFixedHeight(40)
        category_filter.addItems([
            "Todas as categorias",
            "Alimentação",
            "Transporte",
            "Lazer",
            "Moradia",
            "Saúde",
            "Salário",
            "Outros",
        ])
        category_filter.currentTextChanged.connect(self.apply_transaction_filters)

        clear_filters_button = QPushButton("Limpar filtros")
        clear_filters_button.setObjectName("secondaryButton")
        clear_filters_button.setFixedHeight(40)
        clear_filters_button.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_filters_button.clicked.connect(self.clear_transaction_filters)

        remove_transaction_button = QPushButton("Remover selecionada")
        remove_transaction_button.setObjectName("dangerButton")
        remove_transaction_button.setFixedHeight(40)
        remove_transaction_button.setCursor(Qt.CursorShape.PointingHandCursor)
        remove_transaction_button.clicked.connect(self.remove_selected_transaction)
        self.remove_transaction_button = remove_transaction_button

        results_label = QLabel()
        results_label.setObjectName("filtersStatus")
        results_label.setFixedHeight(40)

        filters_layout.addWidget(search_input)
        filters_layout.addWidget(type_filter)
        filters_layout.addWidget(category_filter)
        filters_layout.addWidget(clear_filters_button)
        filters_layout.addWidget(remove_transaction_button)
        filters_layout.addStretch()
        filters_layout.addWidget(results_label)

        layout.addWidget(filters_frame)

        layout.addSpacing(20)

        table = QTableWidget()
        table.setObjectName("transactionsTable")
        self.transactions_table = table
        self.transaction_search_input = search_input
        self.transaction_type_filter = type_filter
        self.transaction_category_filter = category_filter
        self.transaction_results_label = results_label

        table.setColumnCount(5)

        table.setHorizontalHeaderLabels([
            "Descrição",
            "Categoria",
            "Tipo",
            "Data",
            "Valor",
        ])

        table.setRowCount(0)
        table.setSortingEnabled(True)

        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)

        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        table.itemSelectionChanged.connect(self.update_remove_button_state)

        table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        header = table.horizontalHeader()

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.Stretch
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeMode.ResizeToContents
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeMode.ResizeToContents
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeMode.ResizeToContents
        )

        header.setSectionResizeMode(
            4,
            QHeaderView.ResizeMode.ResizeToContents
        )

        layout.addWidget(table)
        self.populate_transactions_table(self.transactions)
        self.update_remove_button_state()

        return page

    def clear_transaction_filters(self):
        self.transaction_search_input.clear()
        self.transaction_type_filter.setCurrentIndex(0)
        self.transaction_category_filter.setCurrentIndex(0)
        self.apply_transaction_filters()

    def add_demo_transaction(self):
        transaction_id = self.next_transaction_id
        self.next_transaction_id += 1
        amount = 95.00 if transaction_id % 2 == 0 else -35.90

        self.transactions.insert(
            0,
            {
                "id": transaction_id,
                "description": f"Transação {transaction_id}",
                "category": "Outros",
                "type": "Receita" if amount > 0 else "Despesa",
                "date": date.today().strftime("%d/%m/%Y"),
                "amount": amount,
            },
        )

        self.apply_transaction_filters()

    def remove_selected_transaction(self):
        selected_rows = self.transactions_table.selectionModel().selectedRows()

        if not selected_rows:
            return

        transaction_ids = []

        for selected_row in selected_rows:
            item = self.transactions_table.item(selected_row.row(), 0)

            if item is not None:
                transaction_ids.append(item.data(Qt.ItemDataRole.UserRole))

        self.transactions = [
            transaction for transaction in self.transactions
            if transaction["id"] not in transaction_ids
        ]

        self.apply_transaction_filters()

    def update_remove_button_state(self):
        has_selection = bool(self.transactions_table.selectionModel().selectedRows())
        self.remove_transaction_button.setEnabled(has_selection)

    def apply_transaction_filters(self):
        search_text = self.transaction_search_input.text().strip().lower()
        selected_type = self.transaction_type_filter.currentText()
        selected_category = self.transaction_category_filter.currentText()

        filtered_transactions = []

        for transaction in self.transactions:
            text_matches = (
                search_text in transaction["description"].lower()
                or search_text in transaction["category"].lower()
                or search_text in transaction["type"].lower()
            )
            type_matches = (
                selected_type == "Todos os tipos"
                or selected_type[:-1] == transaction["type"]
            )
            category_matches = (
                selected_category == "Todas as categorias"
                or selected_category == transaction["category"]
            )

            if text_matches and type_matches and category_matches:
                filtered_transactions.append(transaction)

        self.populate_transactions_table(filtered_transactions)

    def populate_transactions_table(self, transactions):
        self.transactions_table.setSortingEnabled(False)
        self.transactions_table.setRowCount(len(transactions))
        self.transaction_results_label.setText(
            f"{len(transactions)} transação" if len(transactions) == 1
            else f"{len(transactions)} transações"
        )

        for row, transaction in enumerate(transactions):
            values = [
                transaction["description"],
                transaction["category"],
                transaction["type"],
                transaction["date"],
                self.format_currency(transaction["amount"]),
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

                if column == 0:
                    item.setData(Qt.ItemDataRole.UserRole, transaction["id"])

                if column == 4:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )
                    item.setForeground(
                        QColor("#1145D6")
                        if transaction["amount"] >= 0
                        else QColor("#1D4CD1")
                    )
                else:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
                    )

                self.transactions_table.setItem(row, column, item)

        self.transactions_table.setSortingEnabled(True)
        QTimer.singleShot(0, self.update_remove_button_state)

    def format_currency(self, amount):
        formatted = f"R$ {abs(amount):,.2f}"
        formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")

        if amount < 0:
            return f"-{formatted}"

        return formatted
