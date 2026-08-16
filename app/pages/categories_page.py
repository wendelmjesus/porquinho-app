from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QVBoxLayout,
)


class CategoriesPage(QFrame):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setObjectName("content")
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        self.controller.categories_content_layout = layout
        layout.setContentsMargins(40, 35, 40, 35)
        layout.setSpacing(0)

        title = QLabel("Categorias")
        title.setObjectName("pageTitle")
        title.setMinimumHeight(40)
        title.setWordWrap(True)

        subtitle = QLabel("Organize suas transações em categorias.")
        subtitle.setObjectName("pageSubtitle")
        subtitle.setMinimumHeight(24)
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(28)

        form_frame = QFrame()
        form_frame.setObjectName("filtersFrame")

        form_layout = QGridLayout(form_frame)
        self.controller.category_form_layout = form_layout
        form_layout.setContentsMargins(18, 14, 18, 14)
        form_layout.setHorizontalSpacing(12)
        form_layout.setVerticalSpacing(12)

        category_name_input = QLineEdit()
        category_name_input.setObjectName("searchInput")
        category_name_input.setPlaceholderText("Nome da categoria")
        category_name_input.setFixedHeight(40)

        category_type_input = QComboBox()
        category_type_input.setObjectName("filterCombo")
        category_type_input.setFixedHeight(40)
        category_type_input.addItems(["Despesa", "Receita"])

        add_category_button = QPushButton("Adicionar")
        add_category_button.setObjectName("primaryButton")
        add_category_button.setFixedHeight(40)
        add_category_button.setCursor(Qt.CursorShape.PointingHandCursor)
        add_category_button.clicked.connect(self.controller.add_category_from_form)

        remove_category_button = QPushButton("Remover selecionada")
        remove_category_button.setObjectName("dangerButton")
        remove_category_button.setFixedHeight(40)
        remove_category_button.setCursor(Qt.CursorShape.PointingHandCursor)
        remove_category_button.clicked.connect(self.controller.remove_selected_category)

        category_status_label = QLabel("")
        category_status_label.setObjectName("filtersStatus")
        category_status_label.setFixedHeight(40)

        self.controller.category_name_input = category_name_input
        self.controller.category_type_input = category_type_input
        self.controller.category_status_label = category_status_label
        self.controller.remove_category_button = remove_category_button

        form_layout.addWidget(category_name_input, 0, 0)
        form_layout.addWidget(category_type_input, 0, 1)
        form_layout.addWidget(add_category_button, 0, 2)
        form_layout.addWidget(remove_category_button, 1, 0)
        form_layout.addWidget(category_status_label, 1, 1, 1, 2)
        form_layout.setColumnStretch(0, 2)
        form_layout.setColumnStretch(1, 1)
        form_layout.setColumnStretch(2, 1)

        layout.addWidget(form_frame)
        layout.addSpacing(20)

        self.controller.categories_lists_layout = QGridLayout()
        self.controller.categories_lists_layout.setHorizontalSpacing(18)
        self.controller.categories_lists_layout.setVerticalSpacing(18)

        self.controller.income_categories_list = QListWidget()
        self.controller.income_categories_list.setObjectName("categoriesList")
        self.controller.income_categories_list.itemSelectionChanged.connect(
            self.controller.handle_income_category_selection
        )

        self.controller.expense_categories_list = QListWidget()
        self.controller.expense_categories_list.setObjectName("categoriesList")
        self.controller.expense_categories_list.itemSelectionChanged.connect(
            self.controller.handle_expense_category_selection
        )

        self.controller.income_categories_panel = self.controller.create_category_panel(
            "Receitas",
            self.controller.income_categories_list,
        )
        self.controller.expense_categories_panel = self.controller.create_category_panel(
            "Despesas",
            self.controller.expense_categories_list,
        )

        layout.addLayout(self.controller.categories_lists_layout)
        layout.addStretch()

        category_name_input.returnPressed.connect(self.controller.add_category_from_form)

        self.controller.populate_categories_lists()
        self.controller.update_remove_category_button_state()
        self.controller.update_categories_layout()
