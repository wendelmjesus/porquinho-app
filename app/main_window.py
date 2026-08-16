import os
import sys

from PySide6.QtCore import QDate, Qt, QTimer
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.is_compact_layout = None
        self.setWindowTitle("Porquinho")
        self.resize(1200,760)
        self.setMinimumSize(360, 640)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.pages = QStackedWidget()
        self.menu_buttons = []
        self.sidebar_labels = []
        self.transactions = []
        self.next_transaction_id = 1

        self.dashboard_page = self.create_scroll_page(self.create_content())

        self.transactions_page = self.create_scroll_page(self.create_transactions_page())

        self.categories_page = self.create_scroll_page(
            self.create_simple_page(
                "Categorias",
                "Organize suas transações em categorias."
            )
        )

        self.goals_page = self.create_scroll_page(
            self.create_simple_page(
                "Metas",
                "Defina metas financeiras e acompanhe seu progresso."
            )
        )

        self.reports_page = self.create_scroll_page(
            self.create_simple_page(
                "Relatórios",
                "Visualize e exporte seus relatórios detalhados sobre suas finanças."
            )
        )

        self.settings_page = self.create_scroll_page(
            self.create_simple_page(
                "Configurações",
                "Personalize sua experiência."
            )
        )

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.transactions_page)
        self.pages.addWidget(self.categories_page)
        self.pages.addWidget(self.goals_page)
        self.pages.addWidget(self.reports_page)
        self.pages.addWidget(self.settings_page)

        self.sidebar = self.create_sidebar()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.pages, 1)
        self.update_responsive_layout()

    def create_scroll_page(self, page):
        scroll_area = QScrollArea()
        scroll_area.setObjectName("pageScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setWidget(page)

        return scroll_area

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_responsive_layout()

    def update_responsive_layout(self):
        if not hasattr(self, "sidebar"):
            return

        compact_layout = self.width() < 760

        if compact_layout != self.is_compact_layout:
            self.is_compact_layout = compact_layout

            if compact_layout:
                self.sidebar.setFixedWidth(92)
                self.sidebar.layout().setContentsMargins(12, 20, 12, 20)

                for button, full_text, compact_text in self.sidebar_labels:
                    button.setText(compact_text)
            else:
                self.sidebar.setFixedWidth(250)
                self.sidebar.layout().setContentsMargins(22, 28, 22, 24)

                for button, full_text, compact_text in self.sidebar_labels:
                    button.setText(full_text)

        self.update_cards_layout()
        self.update_dashboard_panels_layout()
        self.update_transactions_layout()

    def clear_layout(self, layout):
        while layout.count():
            layout.takeAt(0)

    def update_cards_layout(self):
        if not hasattr(self, "cards_layout"):
            return

        compact_layout = self.width() < 900
        self.clear_layout(self.cards_layout)

        for index, card in enumerate(self.finance_cards):
            if compact_layout:
                self.cards_layout.addWidget(card, index, 0)
            else:
                self.cards_layout.addWidget(card, 0, index)

        self.cards_layout.setColumnStretch(0, 1)
        self.cards_layout.setColumnStretch(1, 1 if not compact_layout else 0)
        self.cards_layout.setColumnStretch(2, 1 if not compact_layout else 0)

    def update_dashboard_panels_layout(self):
        if not hasattr(self, "dashboard_bottom_layout"):
            return

        compact_layout = self.width() < 980
        self.clear_layout(self.dashboard_bottom_layout)

        if compact_layout:
            self.dashboard_bottom_layout.addWidget(self.dashboard_panels[0], 0, 0)
            self.dashboard_bottom_layout.addWidget(self.dashboard_panels[1], 1, 0)
            self.dashboard_bottom_layout.setColumnStretch(0, 1)
            return

        self.dashboard_bottom_layout.addWidget(self.dashboard_panels[0], 0, 0)
        self.dashboard_bottom_layout.addWidget(self.dashboard_panels[1], 0, 1)
        self.dashboard_bottom_layout.setColumnStretch(0, 2)
        self.dashboard_bottom_layout.setColumnStretch(1, 1)

    def update_transactions_layout(self):
        if not hasattr(self, "transaction_filters_layout"):
            return

        compact_layout = self.width() < 760
        medium_layout = self.width() < 1040

        self.transaction_content_layout.setContentsMargins(
            18 if compact_layout else 40,
            24 if compact_layout else 35,
            18 if compact_layout else 40,
            24 if compact_layout else 35,
        )

        self.clear_layout(self.transaction_header_layout)

        if compact_layout:
            self.transaction_header_layout.addLayout(self.transaction_title_layout, 0, 0)
            self.transaction_header_layout.addWidget(self.new_transaction_button, 1, 0)
            self.transaction_header_layout.setColumnStretch(0, 1)
            self.transaction_header_layout.setColumnStretch(1, 0)
        else:
            self.transaction_header_layout.addLayout(self.transaction_title_layout, 0, 0)
            self.transaction_header_layout.addWidget(self.new_transaction_button, 0, 1)
            self.transaction_header_layout.setColumnStretch(0, 1)
            self.transaction_header_layout.setColumnStretch(1, 0)

        self.clear_layout(self.transaction_filters_layout)

        if compact_layout:
            self.transaction_filters_layout.addWidget(self.transaction_search_input, 0, 0)
            self.transaction_filters_layout.addWidget(self.transaction_type_filter, 1, 0)
            self.transaction_filters_layout.addWidget(self.transaction_category_filter, 2, 0)
            self.transaction_filters_layout.addWidget(self.clear_filters_button, 3, 0)
            self.transaction_filters_layout.addWidget(self.remove_transaction_button, 4, 0)
            self.transaction_filters_layout.addWidget(self.transaction_results_label, 5, 0)
            self.transaction_filters_layout.setColumnStretch(0, 1)
        elif medium_layout:
            self.transaction_filters_layout.addWidget(self.transaction_search_input, 0, 0, 1, 2)
            self.transaction_filters_layout.addWidget(self.transaction_type_filter, 1, 0)
            self.transaction_filters_layout.addWidget(self.transaction_category_filter, 1, 1)
            self.transaction_filters_layout.addWidget(self.clear_filters_button, 2, 0)
            self.transaction_filters_layout.addWidget(self.remove_transaction_button, 2, 1)
            self.transaction_filters_layout.addWidget(self.transaction_results_label, 3, 0, 1, 2)
            self.transaction_filters_layout.setColumnStretch(0, 1)
            self.transaction_filters_layout.setColumnStretch(1, 1)
        else:
            self.transaction_filters_layout.addWidget(self.transaction_search_input, 0, 0, 1, 2)
            self.transaction_filters_layout.addWidget(self.transaction_type_filter, 0, 2)
            self.transaction_filters_layout.addWidget(self.transaction_category_filter, 0, 3)
            self.transaction_filters_layout.addWidget(self.clear_filters_button, 1, 0)
            self.transaction_filters_layout.addWidget(self.remove_transaction_button, 1, 1)
            self.transaction_filters_layout.addWidget(self.transaction_results_label, 1, 3)
            self.transaction_filters_layout.setColumnStretch(0, 2)
            self.transaction_filters_layout.setColumnStretch(1, 1)
            self.transaction_filters_layout.setColumnStretch(2, 1)
            self.transaction_filters_layout.setColumnStretch(3, 1)

        if hasattr(self, "transactions_table"):
            self.transactions_table.setColumnHidden(1, compact_layout)
            self.transactions_table.setColumnHidden(3, compact_layout)

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
            ("Dashboard", "Dash", 0),
            ("Transações", "Trans.", 1),
            ("Categorias", "Cat.", 2),
            ("Metas", "Metas", 3),
            ("Relatórios", "Relat.", 4)
        ]

        for button_name, compact_name, page_index in buttons:
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
            self.sidebar_labels.append((button, button_name, compact_name))

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
        self.sidebar_labels.append((settings_button, "Configurações", "Config."))

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
        title.setMinimumHeight(40)
        title.setWordWrap(True)

        subtitle = QLabel(subtitle_text)
        subtitle.setObjectName("pageSubtitle")
        subtitle.setMinimumHeight(24)
        subtitle.setWordWrap(True)

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
        title.setMinimumHeight(40)
        title.setWordWrap(True)

        subtitle = QLabel("Acompanhe sua vida financeira.")
        subtitle.setObjectName("pageSubtitle")
        subtitle.setMinimumHeight(24)
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(30)

        self.cards_layout = QGridLayout()
        self.cards_layout.setHorizontalSpacing(18)
        self.cards_layout.setVerticalSpacing(18)

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

        self.finance_cards = [
            balance_card,
            income_card,
            expense_card,
        ]
        self.update_cards_layout()

        layout.addLayout(self.cards_layout)

        layout.addSpacing(30)

        self.dashboard_bottom_layout = QGridLayout()
        self.dashboard_bottom_layout.setHorizontalSpacing(18)
        self.dashboard_bottom_layout.setVerticalSpacing(18)

        chart_panel = self.create_chart_panel()
        transactions_panel = self.create_transactions_panel()

        self.dashboard_panels = [
            chart_panel,
            transactions_panel,
        ]
        self.update_dashboard_panels_layout()

        layout.addLayout(self.dashboard_bottom_layout)

        layout.addStretch()

        return content
    
    def create_finance_card(self, title_text, value_text, object_name):
        card = QFrame () 
        card.setObjectName(object_name)
        card.setMinimumWidth(150)
        card.setFixedHeight(132)
        card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

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
        self.transaction_content_layout = layout
        layout.setContentsMargins(40, 35, 40, 35)
        layout.setSpacing(0)

        header_layout = QGridLayout()
        self.transaction_header_layout = header_layout
        header_layout.setHorizontalSpacing(12)
        header_layout.setVerticalSpacing(12)

        title_container = QVBoxLayout()
        self.transaction_title_layout = title_container
        title_container.setSpacing(0)

        title = QLabel("Transações")
        title.setObjectName("pageTitle")
        title.setMinimumHeight(40)
        title.setWordWrap(True)

        subtitle = QLabel("Gerencie suas receitas e despesas.")
        subtitle.setObjectName("pageSubtitle")
        subtitle.setMinimumHeight(24)
        subtitle.setWordWrap(True)

        title_container.addWidget(title)
        title_container.addWidget(subtitle)

        new_transaction_button = QPushButton("Nova transação")
        new_transaction_button.setObjectName("primaryButton")
        new_transaction_button.setFixedHeight(42)
        new_transaction_button.setCursor(Qt.CursorShape.PointingHandCursor)
        new_transaction_button.clicked.connect(self.open_new_transaction_dialog)
        self.new_transaction_button = new_transaction_button

        header_layout.addLayout(title_container, 0, 0)
        header_layout.addWidget(new_transaction_button, 0, 1)
        header_layout.setColumnStretch(0, 1)

        layout.addLayout(header_layout)

        layout.addSpacing(28)

        filters_frame = QFrame()
        filters_frame.setObjectName("filtersFrame")

        filters_layout = QGridLayout(filters_frame)
        self.transaction_filters_layout = filters_layout
        filters_layout.setContentsMargins(18, 14, 18, 14)
        filters_layout.setHorizontalSpacing(12)
        filters_layout.setVerticalSpacing(12)

        search_input = QLineEdit()
        search_input.setObjectName("searchInput")
        search_input.setPlaceholderText("Buscar transação...")
        search_input.setMinimumWidth(160)
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
        self.clear_filters_button = clear_filters_button

        remove_transaction_button = QPushButton("Remover selecionada")
        remove_transaction_button.setObjectName("dangerButton")
        remove_transaction_button.setFixedHeight(40)
        remove_transaction_button.setCursor(Qt.CursorShape.PointingHandCursor)
        remove_transaction_button.clicked.connect(self.remove_selected_transaction)
        self.remove_transaction_button = remove_transaction_button

        results_label = QLabel()
        results_label.setObjectName("filtersStatus")
        results_label.setFixedHeight(40)

        filters_layout.addWidget(search_input, 0, 0, 1, 2)
        filters_layout.addWidget(type_filter, 0, 2)
        filters_layout.addWidget(category_filter, 0, 3)
        filters_layout.addWidget(clear_filters_button, 1, 0)
        filters_layout.addWidget(remove_transaction_button, 1, 1)
        filters_layout.addWidget(results_label, 1, 3)
        filters_layout.setColumnStretch(0, 2)
        filters_layout.setColumnStretch(1, 1)
        filters_layout.setColumnStretch(2, 1)
        filters_layout.setColumnStretch(3, 1)

        layout.addWidget(filters_frame)

        layout.addSpacing(20)

        table = QTableWidget()
        table.setObjectName("transactionsTable")
        table.setMinimumHeight(360)
        table.setMinimumWidth(0)
        table.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
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
        self.update_transactions_layout()

        return page

    def clear_transaction_filters(self):
        self.transaction_search_input.clear()
        self.transaction_type_filter.setCurrentIndex(0)
        self.transaction_category_filter.setCurrentIndex(0)
        self.apply_transaction_filters()

    def open_new_transaction_dialog(self):
        self.open_transaction_dialog()

    def open_transaction_dialog(self, default_type="Receita"):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nova transação")
        dialog.setObjectName("transactionDialog")

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(16)

        form_layout = QFormLayout()
        form_layout.setSpacing(12)

        description_input = QLineEdit()
        description_input.setObjectName("searchInput")
        description_input.setPlaceholderText("Ex: Mercado")
        description_input.setFixedHeight(40)

        category_input = QComboBox()
        category_input.setObjectName("filterCombo")
        category_input.setFixedHeight(40)
        category_input.addItems([
            "Alimentação",
            "Transporte",
            "Lazer",
            "Moradia",
            "Saúde",
            "Salário",
            "Outros",
        ])

        type_input = QComboBox()
        type_input.setObjectName("filterCombo")
        type_input.setFixedHeight(40)
        type_input.addItems(["Receita", "Despesa"])
        type_input.setCurrentText(default_type)

        date_input = QDateEdit()
        date_input.setObjectName("dateInput")
        date_input.setFixedHeight(40)
        date_input.setCalendarPopup(True)
        date_input.setDisplayFormat("dd/MM/yyyy")
        date_input.setDate(QDate.currentDate())

        amount_input = QDoubleSpinBox()
        amount_input.setObjectName("amountInput")
        amount_input.setFixedHeight(40)
        amount_input.setPrefix("R$ ")
        amount_input.setDecimals(2)
        amount_input.setMaximum(9999999.99)

        form_layout.addRow("Descrição", description_input)
        form_layout.addRow("Categoria", category_input)
        form_layout.addRow("Tipo", type_input)
        form_layout.addRow("Data", date_input)
        form_layout.addRow("Valor", amount_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        layout.addLayout(form_layout)
        layout.addWidget(buttons)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        description = description_input.text().strip()

        if not description:
            description = "Sem descrição"

        amount = amount_input.value()

        if type_input.currentText() == "Despesa":
            amount = -amount

        self.add_transaction(
            description,
            category_input.currentText(),
            type_input.currentText(),
            date_input.date().toString("dd/MM/yyyy"),
            amount,
        )

    def add_expense(self, description, category, transaction_date, amount):
        self.add_transaction(
            description,
            category,
            "Despesa",
            transaction_date,
            -abs(amount),
        )

    def add_transaction(self, description, category, transaction_type, transaction_date, amount):
        transaction_id = self.next_transaction_id
        self.next_transaction_id += 1

        self.transactions.insert(
            0,
            {
                "id": transaction_id,
                "description": description,
                "category": category,
                "type": transaction_type,
                "date": transaction_date,
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
