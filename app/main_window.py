import os
import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QProgressBar,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.database import DatabaseManager
from app.dialogs import GoalDialog, TransactionDialog
from app.pages import (
    CategoriesPage,
    DashboardPage,
    GoalsPage,
    ReportsPage,
    SettingsPage,
    TransactionsPage,
)
from app.services import (
    export_transactions_to_csv,
    format_currency,
    format_summary_currency,
    get_all_categories,
    get_category_totals,
    get_goal_progress,
    get_next_id,
    get_totals,
)
from app.styles import APP_STYLE, DARK_APP_STYLE
from app.widgets import FinanceCard, FinanceChartWidget


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
        self.goals = []
        self.next_goal_id = 1
        self.dark_mode_enabled = False
        self.selected_category = None
        self.database_path = os.environ.get(
            "PORQUINHO_DATABASE_PATH",
            os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "data",
                "porquinho.db",
            ),
        )
        self.categories = {
            "Receita": [
                "Salário",
                "Freelance",
                "Investimentos",
                "Presente",
                "Outros",
            ],
            "Despesa": [
                "Alimentação",
                "Transporte",
                "Moradia",
                "Saúde",
                "Educação",
                "Lazer",
                "Assinaturas",
                "Outros",
            ],
        }
        self.database = DatabaseManager(self.database_path, self.categories)
        self.database.initialize()
        self.load_database_data()

        self.dashboard_page = self.create_scroll_page(DashboardPage(self))

        self.transactions_page = self.create_scroll_page(TransactionsPage(self))

        self.categories_page = self.create_scroll_page(CategoriesPage(self))

        self.goals_page = self.create_scroll_page(GoalsPage(self))

        self.reports_page = self.create_scroll_page(ReportsPage(self))

        self.settings_page = self.create_scroll_page(SettingsPage(self))

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

    def load_database_data(self):
        self.categories, self.transactions, self.goals = self.database.load_data()
        self.next_transaction_id = self.get_next_id(self.transactions)
        self.next_goal_id = self.get_next_id(self.goals)

    def get_next_id(self, records):
        return get_next_id(records)

    def save_category_to_database(self, category_type, category_name):
        self.database.save_category(category_type, category_name)

    def delete_category_from_database(self, category_type, category_name):
        self.database.delete_category(category_type, category_name)

    def save_transaction_to_database(self, transaction):
        self.database.save_transaction(transaction)

    def update_transaction_in_database(self, transaction):
        self.database.update_transaction(transaction)

    def delete_transactions_from_database(self, transaction_ids):
        self.database.delete_transactions(transaction_ids)

    def save_goal_to_database(self, goal):
        self.database.save_goal(goal)

    def update_goal_in_database(self, goal):
        self.database.update_goal(goal)

    def delete_goals_from_database(self, goal_ids):
        self.database.delete_goals(goal_ids)

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
        self.update_categories_layout()
        self.update_goals_layout()
        self.update_reports_layout()
        self.update_settings_layout()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.setParent(None)

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
            self.dashboard_bottom_layout.addWidget(self.dashboard_panels[2], 2, 0)
            self.dashboard_bottom_layout.setColumnStretch(0, 1)
            return

        self.dashboard_bottom_layout.addWidget(self.dashboard_panels[0], 0, 0)
        self.dashboard_bottom_layout.addWidget(self.dashboard_panels[1], 0, 1)
        self.dashboard_bottom_layout.addWidget(self.dashboard_panels[2], 1, 0, 1, 2)
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
            self.transaction_filters_layout.addWidget(self.edit_transaction_button, 4, 0)
            self.transaction_filters_layout.addWidget(self.remove_transaction_button, 5, 0)
            self.transaction_filters_layout.addWidget(self.transaction_results_label, 6, 0)
            self.transaction_filters_layout.setColumnStretch(0, 1)
        elif medium_layout:
            self.transaction_filters_layout.addWidget(self.transaction_search_input, 0, 0, 1, 2)
            self.transaction_filters_layout.addWidget(self.transaction_type_filter, 1, 0)
            self.transaction_filters_layout.addWidget(self.transaction_category_filter, 1, 1)
            self.transaction_filters_layout.addWidget(self.clear_filters_button, 2, 0)
            self.transaction_filters_layout.addWidget(self.edit_transaction_button, 2, 1)
            self.transaction_filters_layout.addWidget(self.remove_transaction_button, 3, 0)
            self.transaction_filters_layout.addWidget(self.transaction_results_label, 3, 1)
            self.transaction_filters_layout.setColumnStretch(0, 1)
            self.transaction_filters_layout.setColumnStretch(1, 1)
        else:
            self.transaction_filters_layout.addWidget(self.transaction_search_input, 0, 0, 1, 2)
            self.transaction_filters_layout.addWidget(self.transaction_type_filter, 0, 2)
            self.transaction_filters_layout.addWidget(self.transaction_category_filter, 0, 3)
            self.transaction_filters_layout.addWidget(self.clear_filters_button, 1, 0)
            self.transaction_filters_layout.addWidget(self.edit_transaction_button, 1, 1)
            self.transaction_filters_layout.addWidget(self.remove_transaction_button, 1, 2)
            self.transaction_filters_layout.addWidget(self.transaction_results_label, 1, 3)
            self.transaction_filters_layout.setColumnStretch(0, 2)
            self.transaction_filters_layout.setColumnStretch(1, 1)
            self.transaction_filters_layout.setColumnStretch(2, 1)
            self.transaction_filters_layout.setColumnStretch(3, 1)

        if hasattr(self, "transactions_table"):
            self.transactions_table.setColumnHidden(1, compact_layout)
            self.transactions_table.setColumnHidden(3, compact_layout)

    def update_categories_layout(self):
        if not hasattr(self, "categories_content_layout"):
            return

        compact_layout = self.width() < 760

        self.categories_content_layout.setContentsMargins(
            18 if compact_layout else 40,
            24 if compact_layout else 35,
            18 if compact_layout else 40,
            24 if compact_layout else 35,
        )

        self.clear_layout(self.categories_lists_layout)

        if compact_layout:
            self.categories_lists_layout.addWidget(self.income_categories_panel, 0, 0)
            self.categories_lists_layout.addWidget(self.expense_categories_panel, 1, 0)
            self.categories_lists_layout.setColumnStretch(0, 1)
            return

        self.categories_lists_layout.addWidget(self.income_categories_panel, 0, 0)
        self.categories_lists_layout.addWidget(self.expense_categories_panel, 0, 1)
        self.categories_lists_layout.setColumnStretch(0, 1)
        self.categories_lists_layout.setColumnStretch(1, 1)

    def update_goals_layout(self):
        if not hasattr(self, "goals_content_layout"):
            return

        compact_layout = self.width() < 760
        self.goals_content_layout.setContentsMargins(
            18 if compact_layout else 40,
            24 if compact_layout else 35,
            18 if compact_layout else 40,
            24 if compact_layout else 35,
        )

        self.clear_layout(self.goal_form_layout)
        self.clear_layout(self.goal_deposit_layout)

        if compact_layout:
            self.goal_form_layout.addWidget(self.goal_name_input, 0, 0)
            self.goal_form_layout.addWidget(self.goal_target_input, 1, 0)
            self.goal_form_layout.addWidget(self.goal_current_input, 2, 0)
            self.goal_form_layout.addWidget(self.add_goal_button, 3, 0)
            self.goal_form_layout.addWidget(self.edit_goal_button, 4, 0)
            self.goal_form_layout.addWidget(self.remove_goal_button, 5, 0)
            self.goal_form_layout.addWidget(self.goal_status_label, 6, 0)
            self.goal_form_layout.setColumnStretch(0, 1)

            self.goal_deposit_layout.addWidget(self.goal_deposit_select, 0, 0)
            self.goal_deposit_layout.addWidget(self.goal_deposit_input, 1, 0)
            self.goal_deposit_layout.addWidget(self.add_goal_deposit_button, 2, 0)
            self.goal_deposit_layout.setColumnStretch(0, 1)
            return

        self.goal_form_layout.addWidget(self.goal_name_input, 0, 0)
        self.goal_form_layout.addWidget(self.goal_target_input, 0, 1)
        self.goal_form_layout.addWidget(self.goal_current_input, 0, 2)
        self.goal_form_layout.addWidget(self.add_goal_button, 0, 3)
        self.goal_form_layout.addWidget(self.edit_goal_button, 1, 0)
        self.goal_form_layout.addWidget(self.remove_goal_button, 1, 1)
        self.goal_form_layout.addWidget(self.goal_status_label, 1, 2, 1, 2)
        self.goal_form_layout.setColumnStretch(0, 2)
        self.goal_form_layout.setColumnStretch(1, 1)
        self.goal_form_layout.setColumnStretch(2, 1)
        self.goal_form_layout.setColumnStretch(3, 1)

        self.goal_deposit_layout.addWidget(self.goal_deposit_select, 0, 0)
        self.goal_deposit_layout.addWidget(self.goal_deposit_input, 0, 1)
        self.goal_deposit_layout.addWidget(self.add_goal_deposit_button, 0, 2)
        self.goal_deposit_layout.setColumnStretch(0, 2)
        self.goal_deposit_layout.setColumnStretch(1, 1)
        self.goal_deposit_layout.setColumnStretch(2, 1)

    def update_reports_layout(self):
        if not hasattr(self, "reports_content_layout"):
            return

        compact_layout = self.width() < 760
        self.reports_content_layout.setContentsMargins(
            18 if compact_layout else 40,
            24 if compact_layout else 35,
            18 if compact_layout else 40,
            24 if compact_layout else 35,
        )

        self.clear_layout(self.report_actions_layout)
        self.clear_layout(self.report_summary_layout)

        if compact_layout:
            self.report_actions_layout.addWidget(self.export_report_button, 0, 0)
            self.report_actions_layout.addWidget(self.refresh_report_button, 1, 0)
            self.report_actions_layout.addWidget(self.report_status_label, 2, 0)
            self.report_actions_layout.setColumnStretch(0, 1)

            self.report_summary_layout.addWidget(self.report_income_card, 0, 0)
            self.report_summary_layout.addWidget(self.report_expense_card, 1, 0)
            self.report_summary_layout.addWidget(self.report_balance_card, 2, 0)
            self.report_summary_layout.setColumnStretch(0, 1)
            return

        self.report_actions_layout.addWidget(self.export_report_button, 0, 0)
        self.report_actions_layout.addWidget(self.refresh_report_button, 0, 1)
        self.report_actions_layout.addWidget(self.report_status_label, 0, 2)
        self.report_actions_layout.setColumnStretch(0, 1)
        self.report_actions_layout.setColumnStretch(1, 1)
        self.report_actions_layout.setColumnStretch(2, 2)

        self.report_summary_layout.addWidget(self.report_income_card, 0, 0)
        self.report_summary_layout.addWidget(self.report_expense_card, 0, 1)
        self.report_summary_layout.addWidget(self.report_balance_card, 0, 2)
        self.report_summary_layout.setColumnStretch(0, 1)
        self.report_summary_layout.setColumnStretch(1, 1)
        self.report_summary_layout.setColumnStretch(2, 1)

    def update_settings_layout(self):
        if not hasattr(self, "settings_content_layout"):
            return

        compact_layout = self.width() < 760
        self.settings_content_layout.setContentsMargins(
            18 if compact_layout else 40,
            24 if compact_layout else 35,
            18 if compact_layout else 40,
            24 if compact_layout else 35,
        )

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

    def create_category_panel(self, title_text, categories_list):
        panel = QFrame()
        panel.setObjectName("dashboardPanel")
        panel.setMinimumHeight(280)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(12)

        title = QLabel(title_text)
        title.setObjectName("panelTitle")

        layout.addWidget(title)
        layout.addWidget(categories_list, 1)

        return panel

    def change_page(self, index, clicked_button):
        self.pages.setCurrentIndex(index)

        for button in self.menu_buttons:
            button.setChecked(False)

        clicked_button.setChecked(True)

    def create_finance_card(self, title_text, value_text, object_name):
        return FinanceCard(title_text, value_text, object_name)
    
    def create_chart_panel(self):
        panel = QFrame()
        panel.setObjectName("dashboardPanel")
        panel.setMinimumHeight(300)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(22, 20, 22, 20)

        title = QLabel("Evolução financeira")
        title.setObjectName("panelTitle")

        self.finance_chart = FinanceChartWidget()
        self.finance_chart.set_transactions(self.transactions)

        layout.addWidget(title)
        layout.addSpacing(15)
        layout.addWidget(self.finance_chart, 1)

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

        self.dashboard_recent_transactions_layout = QVBoxLayout()
        self.dashboard_recent_transactions_layout.setSpacing(10)
        layout.addLayout(self.dashboard_recent_transactions_layout)

        layout.addStretch()

        self.populate_dashboard_recent_transactions()

        return panel

    def create_dashboard_goals_panel(self):
        panel = QFrame()
        panel.setObjectName("dashboardPanel")
        panel.setMinimumHeight(220)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(12)

        title = QLabel("Metas em andamento")
        title.setObjectName("panelTitle")

        self.dashboard_goals_layout = QVBoxLayout()
        self.dashboard_goals_layout.setSpacing(12)

        layout.addWidget(title)
        layout.addLayout(self.dashboard_goals_layout)
        layout.addStretch()

        self.populate_dashboard_goals()

        return panel

    def populate_dashboard_recent_transactions(self):
        if not hasattr(self, "dashboard_recent_transactions_layout"):
            return

        self.clear_layout(self.dashboard_recent_transactions_layout)

        if not self.transactions:
            empty_label = QLabel("Nenhuma transação cadastrada")
            empty_label.setObjectName("transactionDescription")
            self.dashboard_recent_transactions_layout.addWidget(empty_label)
            return

        for transaction in self.transactions[:4]:
            row_widget = QFrame()
            row_widget.setObjectName("dashboardRow")

            row = QGridLayout(row_widget)
            row.setContentsMargins(10, 8, 10, 8)
            row.setHorizontalSpacing(10)
            row.setVerticalSpacing(4)

            description_label = QLabel(transaction["description"])
            description_label.setObjectName("transactionDescription")

            category_label = QLabel(transaction["category"])
            category_label.setObjectName("smallMutedText")

            value_label = QLabel(self.format_currency(transaction["amount"]))
            value_label.setObjectName("transactionValue")
            value_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

            edit_button = QPushButton("Editar")
            edit_button.setObjectName("smallButton")
            edit_button.setFixedHeight(30)
            edit_button.setCursor(Qt.CursorShape.PointingHandCursor)
            edit_button.clicked.connect(
                lambda checked=False, transaction_id=transaction["id"]:
                self.open_edit_transaction_dialog(transaction_id)
            )

            row.addWidget(description_label, 0, 0)
            row.addWidget(category_label, 1, 0)
            row.addWidget(value_label, 0, 1)
            row.addWidget(edit_button, 1, 1)
            row.setColumnStretch(0, 1)

            self.dashboard_recent_transactions_layout.addWidget(row_widget)

    def populate_dashboard_goals(self):
        if not hasattr(self, "dashboard_goals_layout"):
            return

        self.clear_layout(self.dashboard_goals_layout)

        if not self.goals:
            empty_label = QLabel("Nenhuma meta cadastrada")
            empty_label.setObjectName("transactionDescription")
            self.dashboard_goals_layout.addWidget(empty_label)
            return

        for goal in self.goals[:3]:
            goal_widget = QFrame()
            goal_widget.setObjectName("dashboardRow")
            goal_widget.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed,
            )

            layout = QVBoxLayout(goal_widget)
            layout.setContentsMargins(10, 8, 10, 8)
            layout.setSpacing(6)

            header = QHBoxLayout()

            name_label = QLabel(goal["name"])
            name_label.setObjectName("transactionDescription")
            name_label.setWordWrap(True)

            progress = self.get_goal_progress(goal)
            progress_label = QLabel(f"{progress}%")
            progress_label.setObjectName("transactionValue")

            progress_bar = QProgressBar()
            progress_bar.setObjectName("goalProgressBar")
            progress_bar.setRange(0, 100)
            progress_bar.setValue(progress)
            progress_bar.setFormat(f"{progress}%")
            progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
            progress_bar.setTextVisible(True)
            progress_bar.setFixedHeight(20)

            details_label = QLabel(
                f"{self.format_currency(goal['current'])} de {self.format_currency(goal['target'])}"
            )
            details_label.setObjectName("smallMutedText")
            details_label.setWordWrap(True)

            header.addWidget(name_label)
            header.addStretch()
            header.addWidget(progress_label)

            layout.addLayout(header)
            layout.addWidget(progress_bar)
            layout.addWidget(details_label)

            self.dashboard_goals_layout.addWidget(goal_widget)

    def add_category_from_form(self):
        category_name = self.category_name_input.text().strip()
        category_type = self.category_type_input.currentText()

        if not category_name:
            self.category_status_label.setText("Digite um nome para a categoria.")
            return

        if self.add_category(category_type, category_name):
            self.category_name_input.clear()
            self.category_status_label.setText("Categoria adicionada.")
            return

        self.category_status_label.setText("Essa categoria já existe.")

    def add_category(self, category_type, category_name):
        categories = self.get_categories(category_type)

        if category_name.lower() in [category.lower() for category in categories]:
            return False

        categories.append(category_name)
        categories.sort(key=str.lower)
        self.save_category_to_database(category_type, category_name)
        self.refresh_category_views()

        return True

    def remove_selected_category(self):
        selected_category = self.get_selected_category()

        if selected_category is None:
            self.category_status_label.setText("Selecione uma categoria para remover.")
            return

        category_type, category_name = selected_category

        if category_name == "Outros":
            self.category_status_label.setText("A categoria Outros não pode ser removida.")
            return

        if category_name not in self.get_categories(category_type):
            self.category_status_label.setText("Selecione uma categoria válida.")
            return

        self.categories[category_type].remove(category_name)
        self.selected_category = None
        self.delete_category_from_database(category_type, category_name)

        for transaction in self.transactions:
            if transaction["category"] == category_name:
                transaction["category"] = "Outros"
                self.update_transaction_in_database(transaction)

        self.category_status_label.setText("Categoria removida.")
        self.refresh_category_views()
        self.refresh_after_transactions_change()

    def get_selected_category_item(self):
        selected_items = (
            self.income_categories_list.selectedItems()
            + self.expense_categories_list.selectedItems()
        )

        if not selected_items:
            return None

        return selected_items[0]

    def get_selected_category(self):
        selected_item = self.get_selected_category_item()

        if selected_item is not None:
            return (
                selected_item.data(Qt.ItemDataRole.UserRole),
                selected_item.text(),
            )

        return self.selected_category

    def handle_income_category_selection(self):
        selected_items = self.income_categories_list.selectedItems()

        if selected_items:
            self.selected_category = ("Receita", selected_items[0].text())
            self.expense_categories_list.blockSignals(True)
            self.expense_categories_list.clearSelection()
            self.expense_categories_list.blockSignals(False)

        self.update_remove_category_button_state()

    def handle_expense_category_selection(self):
        selected_items = self.expense_categories_list.selectedItems()

        if selected_items:
            self.selected_category = ("Despesa", selected_items[0].text())
            self.income_categories_list.blockSignals(True)
            self.income_categories_list.clearSelection()
            self.income_categories_list.blockSignals(False)

        self.update_remove_category_button_state()

    def update_remove_category_button_state(self):
        selected_category = self.get_selected_category()
        can_remove = (
            selected_category is not None
            and selected_category[1] != "Outros"
            and selected_category[1] in self.get_categories(selected_category[0])
        )
        self.remove_category_button.setEnabled(can_remove)

    def refresh_category_views(self):
        self.populate_categories_lists()
        self.populate_category_filter()

    def populate_categories_lists(self):
        self.selected_category = None
        self.income_categories_list.clear()
        self.expense_categories_list.clear()

        for category_type, categories_list in [
            ("Receita", self.income_categories_list),
            ("Despesa", self.expense_categories_list),
        ]:
            for category in self.get_categories(category_type):
                item = QListWidgetItem(category)
                item.setData(Qt.ItemDataRole.UserRole, category_type)
                categories_list.addItem(item)

        self.update_remove_category_button_state()

    def populate_category_filter(self):
        if not hasattr(self, "transaction_category_filter"):
            return

        current_category = self.transaction_category_filter.currentText()
        all_categories = self.get_all_categories()

        self.transaction_category_filter.blockSignals(True)
        self.transaction_category_filter.clear()
        self.transaction_category_filter.addItem("Todas as categorias")
        self.transaction_category_filter.addItems(all_categories)

        if current_category in all_categories:
            self.transaction_category_filter.setCurrentText(current_category)

        self.transaction_category_filter.blockSignals(False)

    def get_categories(self, category_type):
        return self.categories.get(category_type, [])

    def get_all_categories(self):
        return get_all_categories(self.categories)

    def add_goal_from_form(self):
        goal_name = self.goal_name_input.text().strip()
        target_amount = self.goal_target_input.value()
        current_amount = self.goal_current_input.value()

        if not goal_name:
            self.goal_status_label.setText("Digite um nome para a meta.")
            return

        if target_amount <= 0:
            self.goal_status_label.setText("Defina um objetivo maior que zero.")
            return

        goal = {
            "id": None,
            "name": goal_name,
            "target": target_amount,
            "current": current_amount,
        }
        self.save_goal_to_database(goal)
        self.goals.insert(0, goal)
        self.next_goal_id = self.get_next_id(self.goals)

        self.goal_name_input.clear()
        self.goal_target_input.setValue(0)
        self.goal_current_input.setValue(0)
        self.goal_status_label.setText("Meta adicionada.")
        self.populate_goals_table()

    def remove_selected_goal(self):
        selected_rows = self.goals_table.selectionModel().selectedRows()

        if not selected_rows:
            return

        if not self.confirm_action("Remover meta", "Remover a meta selecionada?"):
            return

        goal_ids = []

        for selected_row in selected_rows:
            item = self.goals_table.item(selected_row.row(), 0)

            if item is not None:
                goal_ids.append(item.data(Qt.ItemDataRole.UserRole))

        self.goals = [
            goal for goal in self.goals
            if goal["id"] not in goal_ids
        ]
        self.delete_goals_from_database(goal_ids)

        self.goal_status_label.setText("Meta removida.")
        self.populate_goals_table()

    def update_remove_goal_button_state(self):
        has_selection = bool(self.goals_table.selectionModel().selectedRows())
        self.remove_goal_button.setEnabled(has_selection)
        self.edit_goal_button.setEnabled(has_selection)

    def populate_goals_table(self):
        self.goals_table.setRowCount(len(self.goals))

        for row, goal in enumerate(self.goals):
            progress = self.get_goal_progress(goal)
            self.goals_table.setRowHeight(row, 54)

            values = [
                goal["name"],
                self.format_currency(goal["current"]),
                self.format_currency(goal["target"]),
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

                if column == 0:
                    item.setData(Qt.ItemDataRole.UserRole, goal["id"])

                if column in [1, 2, 3]:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )
                else:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
                    )

                self.goals_table.setItem(row, column, item)

            progress_bar = QProgressBar()
            progress_bar.setObjectName("goalProgressBar")
            progress_bar.setRange(0, 100)
            progress_bar.setValue(progress)
            progress_bar.setFormat(f"{progress}%")
            progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
            progress_bar.setTextVisible(True)
            progress_bar.setFixedHeight(24)
            self.goals_table.setCellWidget(row, 3, progress_bar)

        self.populate_goal_deposit_select()
        self.populate_dashboard_goals()
        QTimer.singleShot(0, self.update_remove_goal_button_state)

    def populate_goal_deposit_select(self):
        if not hasattr(self, "goal_deposit_select"):
            return

        current_goal_id = self.goal_deposit_select.currentData()

        self.goal_deposit_select.blockSignals(True)
        self.goal_deposit_select.clear()

        if not self.goals:
            self.goal_deposit_select.addItem("Nenhuma meta cadastrada", None)
        else:
            for goal in self.goals:
                self.goal_deposit_select.addItem(goal["name"], goal["id"])

        if current_goal_id is not None:
            index = self.goal_deposit_select.findData(current_goal_id)

            if index >= 0:
                self.goal_deposit_select.setCurrentIndex(index)

        self.goal_deposit_select.blockSignals(False)

    def add_goal_deposit(self):
        goal_id = self.goal_deposit_select.currentData()
        deposit_amount = self.goal_deposit_input.value()

        if goal_id is None:
            self.goal_status_label.setText("Crie uma meta antes de adicionar valor.")
            return

        if deposit_amount <= 0:
            self.goal_status_label.setText("Digite um valor guardado maior que zero.")
            return

        goal = self.find_goal_by_id(goal_id)

        if goal is None:
            return

        goal["current"] += deposit_amount
        self.update_goal_in_database(goal)
        self.goal_deposit_input.setValue(0)
        self.goal_status_label.setText("Valor guardado adicionado.")
        self.populate_goals_table()

    def edit_selected_goal(self):
        goal = self.get_selected_goal()

        if goal is None:
            return

        dialog = GoalDialog(self, goal)

        if dialog.exec() != GoalDialog.DialogCode.Accepted:
            return

        goal_data = dialog.get_goal_data()

        if goal_data["target"] <= 0:
            self.goal_status_label.setText("O objetivo precisa ser maior que zero.")
            return

        goal["name"] = goal_data["name"]
        goal["current"] = goal_data["current"]
        goal["target"] = goal_data["target"]
        self.update_goal_in_database(goal)

        self.goal_status_label.setText("Meta editada.")
        self.populate_goals_table()

    def get_selected_goal(self):
        selected_rows = self.goals_table.selectionModel().selectedRows()

        if not selected_rows:
            return None

        item = self.goals_table.item(selected_rows[0].row(), 0)

        if item is None:
            return None

        return self.find_goal_by_id(item.data(Qt.ItemDataRole.UserRole))

    def find_goal_by_id(self, goal_id):
        for goal in self.goals:
            if goal["id"] == goal_id:
                return goal

        return None

    def get_goal_progress(self, goal):
        return get_goal_progress(goal)

    def refresh_reports(self):
        if not hasattr(self, "category_report_table"):
            return

        totals = get_totals(self.transactions)

        self.set_card_value(
            self.report_income_card,
            self.format_summary_currency(totals["income"]),
        )
        self.set_card_value(
            self.report_expense_card,
            self.format_summary_currency(totals["expense"]),
        )
        self.set_card_value(
            self.report_balance_card,
            self.format_summary_currency(totals["balance"]),
        )

        sorted_totals = get_category_totals(self.transactions)

        self.category_report_table.setRowCount(len(sorted_totals))

        for row, ((category, transaction_type), total) in enumerate(sorted_totals):
            values = [
                category,
                transaction_type,
                self.format_currency(total),
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

                if column == 2:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )
                    item.setForeground(
                        QColor("#1145D6") if total >= 0 else QColor("#1D4CD1")
                    )
                else:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
                    )

                self.category_report_table.setItem(row, column, item)

        transaction_count = len(self.transactions)
        self.report_status_label.setText(
            f"{transaction_count} transação no relatório"
            if transaction_count == 1
            else f"{transaction_count} transações no relatório"
        )

    def refresh_dashboard_summary(self):
        if not hasattr(self, "finance_cards"):
            return

        totals = get_totals(self.transactions)

        self.set_card_value(self.finance_cards[0], self.format_summary_currency(totals["balance"]))
        self.set_card_value(self.finance_cards[1], self.format_summary_currency(totals["income"]))
        self.set_card_value(self.finance_cards[2], self.format_summary_currency(totals["expense"]))

        if hasattr(self, "finance_chart"):
            self.finance_chart.set_transactions(self.transactions)

    def refresh_summary_cards(self):
        self.refresh_dashboard_summary()
        self.refresh_reports()

    def set_card_value(self, card, value_text):
        if hasattr(card, "set_value"):
            card.set_value(value_text)
            return

        value_label = card.findChild(QLabel, "cardValue")

        if value_label is not None:
            value_label.setText(value_text)

    def export_transactions_to_excel(self):
        if not self.transactions:
            QMessageBox.information(
                self,
                "Exportar relatório",
                "Não há transações para exportar.",
            )
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar para Excel",
            "relatorio_financeiro.csv",
            "Planilha Excel (*.csv)",
        )

        if not file_path:
            return

        if not file_path.lower().endswith(".csv"):
            file_path = f"{file_path}.csv"

        export_transactions_to_csv(file_path, self.transactions)

        self.report_status_label.setText(f"Relatório exportado: {os.path.basename(file_path)}")

    def toggle_dark_mode(self, state=None):
        self.dark_mode_enabled = self.dark_mode_checkbox.isChecked()
        app = QApplication.instance()

        if app is None:
            return

        app.setStyleSheet(DARK_APP_STYLE if self.dark_mode_enabled else APP_STYLE)

        if hasattr(self, "finance_chart"):
            self.finance_chart.set_dark_mode(self.dark_mode_enabled)

    def confirm_action(self, title, message):
        if not hasattr(self, "confirm_delete_checkbox"):
            return True

        if not self.confirm_delete_checkbox.isChecked():
            return True

        result = QMessageBox.question(
            self,
            title,
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        return result == QMessageBox.StandardButton.Yes

    def clear_transaction_filters(self):
        self.transaction_search_input.clear()
        self.transaction_type_filter.setCurrentIndex(0)
        self.transaction_category_filter.setCurrentIndex(0)
        self.apply_transaction_filters()

    def open_new_transaction_dialog(self):
        self.open_transaction_dialog()

    def open_transaction_dialog(self, default_type="Receita"):
        self.open_transaction_editor(default_type=default_type)

    def open_edit_transaction_dialog(self, transaction_id):
        transaction = self.find_transaction_by_id(transaction_id)

        if transaction is None:
            return

        self.open_transaction_editor(transaction=transaction)

    def edit_selected_transaction(self):
        selected_rows = self.transactions_table.selectionModel().selectedRows()

        if not selected_rows:
            return

        item = self.transactions_table.item(selected_rows[0].row(), 0)

        if item is None:
            return

        self.open_edit_transaction_dialog(item.data(Qt.ItemDataRole.UserRole))

    def open_transaction_editor(self, default_type="Receita", transaction=None):
        dialog = TransactionDialog(
            self,
            self.get_categories,
            default_type=default_type,
            transaction=transaction,
        )

        if dialog.exec() != TransactionDialog.DialogCode.Accepted:
            return

        transaction_data = dialog.get_transaction_data()

        if transaction:
            transaction.update(transaction_data)
            self.update_transaction_in_database(transaction)
            self.refresh_after_transactions_change()
            return

        self.add_transaction(
            transaction_data["description"],
            transaction_data["category"],
            transaction_data["type"],
            transaction_data["date"],
            transaction_data["amount"],
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
        transaction = {
            "id": None,
            "description": description,
            "category": category,
            "type": transaction_type,
            "date": transaction_date,
            "amount": amount,
        }
        self.save_transaction_to_database(transaction)
        self.next_transaction_id = self.get_next_id(self.transactions + [transaction])

        self.transactions.insert(
            0,
            transaction,
        )

        self.refresh_after_transactions_change()

    def find_transaction_by_id(self, transaction_id):
        for transaction in self.transactions:
            if transaction["id"] == transaction_id:
                return transaction

        return None

    def refresh_after_transactions_change(self):
        self.apply_transaction_filters()
        self.refresh_dashboard_summary()
        self.refresh_reports()
        self.populate_dashboard_recent_transactions()

    def remove_selected_transaction(self):
        selected_rows = self.transactions_table.selectionModel().selectedRows()

        if not selected_rows:
            return

        if not self.confirm_action("Remover transação", "Remover a transação selecionada?"):
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
        self.delete_transactions_from_database(transaction_ids)

        self.refresh_after_transactions_change()

    def update_remove_button_state(self):
        has_selection = bool(self.transactions_table.selectionModel().selectedRows())
        self.remove_transaction_button.setEnabled(has_selection)
        self.edit_transaction_button.setEnabled(has_selection)

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
        return format_currency(amount)

    def format_summary_currency(self, amount):
        compact = (
            hasattr(self, "compact_values_checkbox")
            and self.compact_values_checkbox.isChecked()
        )
        return format_summary_currency(amount, compact)
