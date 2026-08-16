import sys

from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication
from app.main_window import MainWindow
from app.styles import APP_STYLE

def main():
    app = QApplication(sys.argv)
    
    app.setApplicationName ("Porquinho")
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#18316F"))
    palette.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#F7F9FF"))
    palette.setColor(QPalette.ColorRole.Text, QColor("#18316F"))
    palette.setColor(QPalette.ColorRole.Button, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#1145D6"))
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#D4DFFF"))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#1145D6"))
    app.setPalette(palette)

    app.setStyleSheet(APP_STYLE)

    window=MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
