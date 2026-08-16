from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QFrame, QLabel, QVBoxLayout


class SettingsPage(QFrame):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setObjectName("content")
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        self.controller.settings_content_layout = layout
        layout.setContentsMargins(40, 35, 40, 35)
        layout.setSpacing(0)

        title = QLabel("Configurações")
        title.setObjectName("pageTitle")
        title.setMinimumHeight(40)
        title.setWordWrap(True)

        subtitle = QLabel("Personalize sua experiência.")
        subtitle.setObjectName("pageSubtitle")
        subtitle.setMinimumHeight(24)
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(28)

        appearance_panel = QFrame()
        appearance_panel.setObjectName("dashboardPanel")

        appearance_layout = QVBoxLayout(appearance_panel)
        appearance_layout.setContentsMargins(22, 20, 22, 20)
        appearance_layout.setSpacing(12)

        appearance_title = QLabel("Aparência")
        appearance_title.setObjectName("panelTitle")

        dark_mode_checkbox = QCheckBox("Modo escuro")
        dark_mode_checkbox.setObjectName("settingsCheckBox")
        dark_mode_checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        dark_mode_checkbox.stateChanged.connect(self.controller.toggle_dark_mode)

        appearance_layout.addWidget(appearance_title)
        appearance_layout.addWidget(dark_mode_checkbox)

        preferences_panel = QFrame()
        preferences_panel.setObjectName("dashboardPanel")

        preferences_layout = QVBoxLayout(preferences_panel)
        preferences_layout.setContentsMargins(22, 20, 22, 20)
        preferences_layout.setSpacing(12)

        preferences_title = QLabel("Preferências")
        preferences_title.setObjectName("panelTitle")

        compact_values_checkbox = QCheckBox("Ocultar centavos nos cartões de resumo")
        compact_values_checkbox.setObjectName("settingsCheckBox")
        compact_values_checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        compact_values_checkbox.stateChanged.connect(self.controller.refresh_summary_cards)

        confirm_delete_checkbox = QCheckBox("Manter confirmação visual ao remover itens importantes")
        confirm_delete_checkbox.setObjectName("settingsCheckBox")
        confirm_delete_checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        confirm_delete_checkbox.setChecked(True)

        self.controller.dark_mode_checkbox = dark_mode_checkbox
        self.controller.compact_values_checkbox = compact_values_checkbox
        self.controller.confirm_delete_checkbox = confirm_delete_checkbox

        preferences_layout.addWidget(preferences_title)
        preferences_layout.addWidget(compact_values_checkbox)
        preferences_layout.addWidget(confirm_delete_checkbox)

        layout.addWidget(appearance_panel)
        layout.addSpacing(18)
        layout.addWidget(preferences_panel)
        layout.addStretch()

        self.controller.update_settings_layout()
