from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QVBoxLayout,
)


class TransactionsPage(QFrame):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setObjectName("content")
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        self.controller.transaction_content_layout = layout
        layout.setContentsMargins(40, 35, 40, 35)
        layout.setSpacing(0)

        header_layout = QGridLayout()
        self.controller.transaction_header_layout = header_layout
        header_layout.setHorizontalSpacing(12)
        header_layout.setVerticalSpacing(12)

        title_container = QVBoxLayout()
        self.controller.transaction_title_layout = title_container
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
        new_transaction_button.clicked.connect(self.controller.open_new_transaction_dialog)
        self.controller.new_transaction_button = new_transaction_button

        header_layout.addLayout(title_container, 0, 0)
        header_layout.addWidget(new_transaction_button, 0, 1)
        header_layout.setColumnStretch(0, 1)

        layout.addLayout(header_layout)
        layout.addSpacing(28)

        filters_frame = QFrame()
        filters_frame.setObjectName("filtersFrame")

        filters_layout = QGridLayout(filters_frame)
        self.controller.transaction_filters_layout = filters_layout
        filters_layout.setContentsMargins(18, 14, 18, 14)
        filters_layout.setHorizontalSpacing(12)
        filters_layout.setVerticalSpacing(12)

        search_input = QLineEdit()
        search_input.setObjectName("searchInput")
        search_input.setPlaceholderText("Buscar transação...")
        search_input.setMinimumWidth(160)
        search_input.setFixedHeight(40)
        search_input.textChanged.connect(self.controller.apply_transaction_filters)

        type_filter = QComboBox()
        type_filter.setObjectName("filterCombo")
        type_filter.setFixedHeight(40)
        type_filter.addItems([
            "Todos os tipos",
            "Receitas",
            "Despesas",
        ])
        type_filter.currentTextChanged.connect(self.controller.apply_transaction_filters)

        category_filter = QComboBox()
        category_filter.setObjectName("filterCombo")
        category_filter.setFixedHeight(40)
        category_filter.addItem("Todas as categorias")
        category_filter.addItems(self.controller.get_all_categories())
        category_filter.currentTextChanged.connect(self.controller.apply_transaction_filters)

        clear_filters_button = QPushButton("Limpar filtros")
        clear_filters_button.setObjectName("secondaryButton")
        clear_filters_button.setFixedHeight(40)
        clear_filters_button.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_filters_button.clicked.connect(self.controller.clear_transaction_filters)
        self.controller.clear_filters_button = clear_filters_button

        edit_transaction_button = QPushButton("Editar selecionada")
        edit_transaction_button.setObjectName("secondaryButton")
        edit_transaction_button.setFixedHeight(40)
        edit_transaction_button.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_transaction_button.clicked.connect(self.controller.edit_selected_transaction)
        self.controller.edit_transaction_button = edit_transaction_button

        remove_transaction_button = QPushButton("Remover selecionada")
        remove_transaction_button.setObjectName("dangerButton")
        remove_transaction_button.setFixedHeight(40)
        remove_transaction_button.setCursor(Qt.CursorShape.PointingHandCursor)
        remove_transaction_button.clicked.connect(self.controller.remove_selected_transaction)
        self.controller.remove_transaction_button = remove_transaction_button

        results_label = QLabel()
        results_label.setObjectName("filtersStatus")
        results_label.setFixedHeight(40)

        filters_layout.addWidget(search_input, 0, 0, 1, 2)
        filters_layout.addWidget(type_filter, 0, 2)
        filters_layout.addWidget(category_filter, 0, 3)
        filters_layout.addWidget(clear_filters_button, 1, 0)
        filters_layout.addWidget(edit_transaction_button, 1, 1)
        filters_layout.addWidget(remove_transaction_button, 1, 2)
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
        self.controller.transactions_table = table
        self.controller.transaction_search_input = search_input
        self.controller.transaction_type_filter = type_filter
        self.controller.transaction_category_filter = category_filter
        self.controller.transaction_results_label = results_label

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
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.itemSelectionChanged.connect(self.controller.update_remove_button_state)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(table)
        self.controller.populate_transactions_table(self.controller.transactions)
        self.controller.update_remove_button_state()
        self.controller.update_transactions_layout()
