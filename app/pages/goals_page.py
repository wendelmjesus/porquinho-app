from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
)


class GoalsPage(QFrame):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setObjectName("content")
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        self.controller.goals_content_layout = layout
        layout.setContentsMargins(40, 35, 40, 35)
        layout.setSpacing(0)

        title = QLabel("Metas")
        title.setObjectName("pageTitle")
        title.setMinimumHeight(40)
        title.setWordWrap(True)

        subtitle = QLabel("Defina metas financeiras e acompanhe seu progresso.")
        subtitle.setObjectName("pageSubtitle")
        subtitle.setMinimumHeight(24)
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(28)

        form_frame = QFrame()
        form_frame.setObjectName("filtersFrame")

        form_layout = QGridLayout(form_frame)
        self.controller.goal_form_layout = form_layout
        form_layout.setContentsMargins(18, 14, 18, 14)
        form_layout.setHorizontalSpacing(12)
        form_layout.setVerticalSpacing(12)

        goal_name_input = QLineEdit()
        goal_name_input.setObjectName("searchInput")
        goal_name_input.setPlaceholderText("Ex: Reserva de emergência")
        goal_name_input.setFixedHeight(40)

        goal_target_input = QDoubleSpinBox()
        goal_target_input.setObjectName("amountInput")
        goal_target_input.setFixedHeight(40)
        goal_target_input.setPrefix("R$ ")
        goal_target_input.setDecimals(2)
        goal_target_input.setMaximum(9999999.99)

        goal_current_input = QDoubleSpinBox()
        goal_current_input.setObjectName("amountInput")
        goal_current_input.setFixedHeight(40)
        goal_current_input.setPrefix("R$ ")
        goal_current_input.setDecimals(2)
        goal_current_input.setMaximum(9999999.99)

        add_goal_button = QPushButton("Adicionar meta")
        add_goal_button.setObjectName("primaryButton")
        add_goal_button.setFixedHeight(40)
        add_goal_button.setCursor(Qt.CursorShape.PointingHandCursor)
        add_goal_button.clicked.connect(self.controller.add_goal_from_form)

        edit_goal_button = QPushButton("Editar selecionada")
        edit_goal_button.setObjectName("secondaryButton")
        edit_goal_button.setFixedHeight(40)
        edit_goal_button.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_goal_button.clicked.connect(self.controller.edit_selected_goal)

        remove_goal_button = QPushButton("Remover selecionada")
        remove_goal_button.setObjectName("dangerButton")
        remove_goal_button.setFixedHeight(40)
        remove_goal_button.setCursor(Qt.CursorShape.PointingHandCursor)
        remove_goal_button.clicked.connect(self.controller.remove_selected_goal)

        goal_status_label = QLabel("")
        goal_status_label.setObjectName("filtersStatus")
        goal_status_label.setFixedHeight(40)

        self.controller.goal_name_input = goal_name_input
        self.controller.goal_target_input = goal_target_input
        self.controller.goal_current_input = goal_current_input
        self.controller.add_goal_button = add_goal_button
        self.controller.edit_goal_button = edit_goal_button
        self.controller.remove_goal_button = remove_goal_button
        self.controller.goal_status_label = goal_status_label

        form_layout.addWidget(goal_name_input, 0, 0)
        form_layout.addWidget(goal_target_input, 0, 1)
        form_layout.addWidget(goal_current_input, 0, 2)
        form_layout.addWidget(add_goal_button, 0, 3)
        form_layout.addWidget(edit_goal_button, 1, 0)
        form_layout.addWidget(remove_goal_button, 1, 1)
        form_layout.addWidget(goal_status_label, 1, 2, 1, 2)
        form_layout.setColumnStretch(0, 2)
        form_layout.setColumnStretch(1, 1)
        form_layout.setColumnStretch(2, 1)
        form_layout.setColumnStretch(3, 1)

        layout.addWidget(form_frame)
        layout.addSpacing(20)

        deposit_frame = QFrame()
        deposit_frame.setObjectName("filtersFrame")

        deposit_layout = QGridLayout(deposit_frame)
        self.controller.goal_deposit_layout = deposit_layout
        deposit_layout.setContentsMargins(18, 14, 18, 14)
        deposit_layout.setHorizontalSpacing(12)
        deposit_layout.setVerticalSpacing(12)

        goal_deposit_select = QComboBox()
        goal_deposit_select.setObjectName("filterCombo")
        goal_deposit_select.setFixedHeight(40)

        goal_deposit_input = QDoubleSpinBox()
        goal_deposit_input.setObjectName("amountInput")
        goal_deposit_input.setFixedHeight(40)
        goal_deposit_input.setPrefix("R$ ")
        goal_deposit_input.setDecimals(2)
        goal_deposit_input.setMaximum(9999999.99)

        add_goal_deposit_button = QPushButton("Adicionar valor guardado")
        add_goal_deposit_button.setObjectName("primaryButton")
        add_goal_deposit_button.setFixedHeight(40)
        add_goal_deposit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        add_goal_deposit_button.clicked.connect(self.controller.add_goal_deposit)

        self.controller.goal_deposit_select = goal_deposit_select
        self.controller.goal_deposit_input = goal_deposit_input
        self.controller.add_goal_deposit_button = add_goal_deposit_button

        deposit_layout.addWidget(goal_deposit_select, 0, 0)
        deposit_layout.addWidget(goal_deposit_input, 0, 1)
        deposit_layout.addWidget(add_goal_deposit_button, 0, 2)
        deposit_layout.setColumnStretch(0, 2)
        deposit_layout.setColumnStretch(1, 1)
        deposit_layout.setColumnStretch(2, 1)

        layout.addWidget(deposit_frame)
        layout.addSpacing(20)

        goals_table = QTableWidget()
        goals_table.setObjectName("transactionsTable")
        goals_table.setMinimumHeight(360)
        goals_table.setColumnCount(4)
        goals_table.setHorizontalHeaderLabels([
            "Meta",
            "Guardado",
            "Objetivo",
            "Progresso",
        ])
        goals_table.verticalHeader().setVisible(False)
        goals_table.setShowGrid(False)
        goals_table.setAlternatingRowColors(True)
        goals_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        goals_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        goals_table.itemSelectionChanged.connect(self.controller.update_remove_goal_button_state)
        goals_table.verticalHeader().setDefaultSectionSize(54)

        goals_header = goals_table.horizontalHeader()
        goals_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        goals_header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        goals_header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        goals_header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        self.controller.goals_table = goals_table

        layout.addWidget(goals_table)
        layout.addStretch()

        goal_name_input.returnPressed.connect(self.controller.add_goal_from_form)
        self.controller.populate_goals_table()
        self.controller.update_remove_goal_button_state()
        self.controller.update_goals_layout()
