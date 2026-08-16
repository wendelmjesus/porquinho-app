APP_STYLE = """
QWidget {
    font-family: "Inter", sans-serif;
    background-color: #FFFFFF;
    color: #18316F;
}

QMainWindow {
    background-color: #ffffff;
}

QStackedWidget {
    background-color: #ffffff;
}

#sidebar {
    background-color: #ffffff;
    border-right: 1px solid #CFDAF7;
}

#content {
    background-color: #ffffff;
}

#pageScrollArea {
    background-color: #FFFFFF;
    border: none;
}

QAbstractScrollArea::viewport,
QTableWidget,
QListWidget {
    background-color: #FFFFFF;
}

QScrollBar:vertical,
QScrollBar:horizontal {
    background-color: #F7F9FF;
    border: none;
}

QScrollBar::handle:vertical,
QScrollBar::handle:horizontal {
    background-color: #CFDAF7;
    border-radius: 4px;
    min-height: 28px;
    min-width: 28px;
}

QScrollBar::handle:vertical:hover,
QScrollBar::handle:horizontal:hover {
    background-color: #AFC1F5;
}

#menuButton {
    background-color: transparent;
    color: #1145D6;

    border: 1px solid transparent;
    border-radius: 8px;

    text-align: left;

    padding: 0 14px;

    font-size: 14px;
    font-weight: 600;
}

#menuButton:hover {
    background-color: #D4DFFF;
    color: #245DFF;
    border-color: #CFDAF7;
}

#menuButton:checked {
    background-color: #D4DFFF;
    color: #1145D6;
    border-color: #CFDAF7;
}

#menuButton:pressed {
    background-color: #CFDAF7;
    color: #1145D6;
}

#pageTitle {
    color: #1145D6;
    font-size: 30px;
    font-weight: 700;
}

#pageSubtitle {
    color: #1D4CD1;
    font-size: 16px;
    font-weight: 500;
}

#balanceCard,
#incomeCard,
#expenseCard {
    background-color: #F7F9FF;
    border: 1px solid #CFDAF7;
    border-radius: 14px;
}

#balanceCard:hover,
#incomeCard:hover,
#expenseCard:hover {
    background-color: #F0F4FF;
    border-color: #AFC1F5;
}

#cardTitle {
    color: #5E72A8;
    font-size: 14px;
    font-weight: 600;
}

#cardValue {
    color: #1145D6;
    font-size: 25px;
    font-weight: 700;
}

#dashboardPanel {
    background-color: #FDFEFF;
    border: 1px solid #CFDAF7;
    border-radius: 14px;
}

#panelTitle {
    color: #18316F;
    font-size: 17px;
    font-weight: 700;
}

#chartPlaceholder {
    color: #7790CC;
    background-color: #F7F9FF;
    border-radius: 10px;
    font-size: 14px;
}

#transactionDescription {
    color: #334B84;
    font-size: 14px;
    font-weight: 500;
}

#transactionValue {
    color: #1145D6;
    font-size: 14px;
    font-weight: 700;
}

#smallMutedText {
    color: #5E72A8;
    font-size: 12px;
    font-weight: 600;
}

#dashboardRow {
    background-color: #F7F9FF;
    border: 1px solid #E8EDFA;
    border-radius: 8px;
}

#smallButton {
    background-color: #FFFFFF;
    color: #1145D6;

    border: 1px solid #CFDAF7;
    border-radius: 7px;

    padding: 0 10px;

    font-size: 12px;
    font-weight: 700;
}

#smallButton:hover {
    background-color: #D4DFFF;
    border-color: #1145D6;
}

#goalProgressBar {
    background-color: #E8EDFA;
    color: #1145D6;

    border: none;
    border-radius: 4px;

    min-height: 22px;

    font-size: 13px;
    font-weight: 700;
    text-align: center;
}

#goalProgressBar::chunk {
    background-color: #1145D6;
    border-radius: 4px;
}

#primaryButton {
    background-color: #1145D6;
    color: #FFFFFF;

    border: none;
    border-radius: 10px;

    padding: 0 18px;

    font-size: 14px;
    font-weight: 600;
}

#primaryButton:hover {
    background-color: #245DFF;
}

#primaryButton:pressed {
    background-color: #0D38B5;
}

#secondaryButton {
    background-color: #FFFFFF;
    color: #1145D6;

    border: 1px solid #CFDAF7;
    border-radius: 8px;

    padding: 0 14px;

    font-size: 14px;
    font-weight: 600;
}

#secondaryButton:hover {
    background-color: #D4DFFF;
    border-color: #1145D6;
}

#secondaryButton:pressed {
    background-color: #CFDAF7;
}

#dangerButton {
    background-color: #FFFFFF;
    color: #1D4CD1;

    border: 1px solid #CFDAF7;
    border-radius: 8px;

    padding: 0 14px;

    font-size: 14px;
    font-weight: 600;
}

#dangerButton:hover {
    background-color: #D4DFFF;
    border-color: #1145D6;
}

#dangerButton:pressed {
    background-color: #CFDAF7;
}

#dangerButton:disabled {
    color: #AFC1F5;
    background-color: #F7F9FF;
    border-color: #CFDAF7;
}

#filtersFrame {
    background-color: #F7F9FF;

    border: 1px solid #CFDAF7;
    border-radius: 12px;
}

#searchInput {
    background-color: #FFFFFF;
    color: #18316F;

    border: 1px solid #CFDAF7;
    border-radius: 8px;

    padding: 0 12px;

    font-size: 14px;
}

#searchInput::placeholder {
    color: #7790CC;
}

#searchInput:focus {
    border: 1px solid #1145D6;
}

#filterCombo {
    background-color: #FFFFFF;
    color: #18316F;

    border: 1px solid #CFDAF7;
    border-radius: 8px;

    padding: 0 12px;

    min-width: 160px;

    font-size: 14px;
    font-weight: 500;
}

#filterCombo:hover {
    border-color: #1145D6;
}

#filterCombo:focus {
    border-color: #1145D6;
}

#filterCombo::drop-down {
    border: none;
    width: 28px;
}

#filterCombo QAbstractItemView {
    background-color: #FFFFFF;
    color: #18316F;

    border: 1px solid #CFDAF7;
    selection-background-color: #D4DFFF;
    selection-color: #1145D6;

    outline: none;
}

#filterCombo QAbstractItemView::item {
    min-height: 30px;
    padding: 6px 10px;
}

#dateInput,
#amountInput {
    background-color: #FFFFFF;
    color: #18316F;

    border: 1px solid #CFDAF7;
    border-radius: 8px;

    padding: 0 12px;

    font-size: 14px;
    font-weight: 500;
}

#dateInput:focus,
#amountInput:focus {
    border-color: #1145D6;
}

QCalendarWidget QWidget {
    background-color: #FFFFFF;
    color: #18316F;
}

QCalendarWidget QToolButton {
    background-color: #FFFFFF;
    color: #1145D6;
    border: none;
    border-radius: 6px;
    padding: 4px;
}

QCalendarWidget QMenu {
    background-color: #FFFFFF;
    color: #18316F;
    border: 1px solid #CFDAF7;
}

QCalendarWidget QAbstractItemView {
    background-color: #FFFFFF;
    color: #18316F;
    selection-background-color: #D4DFFF;
    selection-color: #1145D6;
}

QDialog {
    background-color: #FFFFFF;
    color: #18316F;
}

QDialog QLabel {
    background-color: #FFFFFF;
    color: #18316F;
}

QDialogButtonBox QPushButton {
    background-color: #FFFFFF;
    color: #1145D6;

    border: 1px solid #CFDAF7;
    border-radius: 8px;

    padding: 8px 14px;

    font-size: 14px;
    font-weight: 600;
}

QDialogButtonBox QPushButton:hover {
    background-color: #D4DFFF;
    border-color: #1145D6;
}

#filtersStatus {
    color: #5E72A8;
    font-size: 13px;
    font-weight: 600;
}

#transactionsTable {
    background-color: #FFFFFF;
    alternate-background-color: #F7F9FF;

    border: 1px solid #CFDAF7;
    border-radius: 12px;

    color: #18316F;

    font-size: 14px;

    outline: none;
    gridline-color: #E8EDFA;
}

#transactionsTable QTableViewport,
#categoriesList QListViewport,
QAbstractScrollArea,
QAbstractScrollArea QWidget {
    background-color: transparent;
}

#transactionsTable::item {
    padding: 12px;
    border-bottom: 1px solid #E8EDFA;
}

#transactionsTable::item:selected {
    background-color: #E5ECFF;
    color: #1145D6;
}

#categoriesList {
    background-color: #FFFFFF;
    color: #18316F;

    border: 1px solid #CFDAF7;
    border-radius: 8px;

    font-size: 14px;

    outline: none;
}

#categoriesList::item {
    min-height: 34px;
    padding: 8px 10px;
    border-bottom: 1px solid #E8EDFA;
}

#categoriesList::item:selected {
    background-color: #E5ECFF;
    color: #1145D6;
}

#settingsCheckBox {
    background-color: transparent;
    color: #18316F;
    font-size: 14px;
    font-weight: 600;
}

QHeaderView::section {
    background-color: #F7F9FF;
    color: #5E72A8;

    border: none;
    border-bottom: 1px solid #CFDAF7;

    padding: 12px;

    font-size: 13px;
    font-weight: 700;
}

QTableCornerButton::section {
    background-color: #F7F9FF;
    border: none;
    border-bottom: 1px solid #CFDAF7;
}

"""

DARK_APP_STYLE = APP_STYLE + """
QWidget {
    background-color: #101624;
    color: #EAF0FF;
}

QMainWindow,
QStackedWidget,
#content,
#pageScrollArea,
QDialog,
QDialog QLabel {
    background-color: #101624;
    color: #EAF0FF;
}

#sidebar {
    background-color: #0B1020;
    border-right: 1px solid #263653;
}

#menuButton {
    color: #BFD0FF;
}

#menuButton:hover,
#menuButton:checked {
    background-color: #1B2A46;
    color: #FFFFFF;
    border-color: #355386;
}

#pageTitle,
#cardValue,
#transactionValue {
    color: #8FB2FF;
}

#pageSubtitle,
#transactionDescription,
#smallMutedText {
    color: #BFD0FF;
}

#balanceCard,
#incomeCard,
#expenseCard,
#dashboardPanel,
#filtersFrame,
#dashboardRow {
    background-color: #151E31;
    border-color: #263653;
}

#balanceCard:hover,
#incomeCard:hover,
#expenseCard:hover {
    background-color: #1B2A46;
    border-color: #355386;
}

#cardTitle,
#filtersStatus {
    color: #AAB8D8;
}

#panelTitle {
    color: #EAF0FF;
}

#chartPlaceholder,
#transactionsTable,
#categoriesList,
QAbstractScrollArea::viewport,
QTableWidget,
QListWidget,
#searchInput,
#filterCombo,
#dateInput,
#amountInput,
#goalProgressBar {
    background-color: #0F1728;
    color: #EAF0FF;
    border-color: #263653;
}

#goalProgressBar::chunk {
    background-color: #8FB2FF;
    border-radius: 4px;
}

#searchInput::placeholder {
    color: #7D8CAE;
}

#searchInput:focus,
#filterCombo:focus,
#filterCombo:hover,
#dateInput:focus,
#amountInput:focus {
    border-color: #8FB2FF;
}

#filterCombo QAbstractItemView,
QCalendarWidget QWidget,
QCalendarWidget QMenu,
QCalendarWidget QAbstractItemView {
    background-color: #0F1728;
    color: #EAF0FF;
    border-color: #263653;
    selection-background-color: #1B2A46;
    selection-color: #FFFFFF;
}

QCalendarWidget QToolButton {
    background-color: #151E31;
    color: #EAF0FF;
}

#transactionsTable {
    alternate-background-color: #151E31;
    gridline-color: #263653;
}

#transactionsTable::item,
#categoriesList::item {
    border-bottom: 1px solid #263653;
}

#transactionsTable::item:selected,
#categoriesList::item:selected {
    background-color: #243B68;
    color: #FFFFFF;
}

QHeaderView::section,
QTableCornerButton::section {
    background-color: #151E31;
    color: #BFD0FF;
    border-bottom: 1px solid #263653;
}

#primaryButton {
    background-color: #5B85FF;
    color: #FFFFFF;
}

#primaryButton:hover {
    background-color: #789BFF;
}

#primaryButton:pressed {
    background-color: #416DDB;
}

#secondaryButton,
#dangerButton,
#smallButton,
QDialogButtonBox QPushButton {
    background-color: #101624;
    color: #BFD0FF;
    border-color: #263653;
}

#secondaryButton:hover,
#dangerButton:hover,
#smallButton:hover,
QDialogButtonBox QPushButton:hover {
    background-color: #1B2A46;
    border-color: #8FB2FF;
}

#dangerButton:disabled {
    color: #5E6C89;
    background-color: #151E31;
    border-color: #263653;
}

#settingsCheckBox {
    background-color: transparent;
    color: #EAF0FF;
    font-size: 14px;
    font-weight: 600;
}
"""
