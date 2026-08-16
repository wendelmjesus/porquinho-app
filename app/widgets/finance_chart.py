from PySide6.QtCore import QDate, QPointF, Qt
from PySide6.QtGui import QBrush, QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget


class FinanceChartWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.transactions = []
        self.dark_mode_enabled = False
        self.setObjectName("financeChart")
        self.setMinimumHeight(220)

    def set_transactions(self, transactions):
        self.transactions = list(transactions)
        self.update()

    def set_dark_mode(self, enabled):
        self.dark_mode_enabled = enabled
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect().adjusted(18, 18, -18, -18)
        painter.setPen(Qt.PenStyle.NoPen)
        background_color = QColor("#0F1728" if self.dark_mode_enabled else "#F7F9FF")
        grid_color = QColor("#263653" if self.dark_mode_enabled else "#CFDAF7")
        text_color = QColor("#BFD0FF" if self.dark_mode_enabled else "#7790CC")
        line_color = QColor("#8FB2FF" if self.dark_mode_enabled else "#1145D6")

        painter.setBrush(QBrush(background_color))
        painter.drawRoundedRect(rect, 10, 10)

        if not self.transactions:
            painter.setPen(text_color)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Sem dados para o gráfico")
            return

        points = self.get_balance_points()

        if len(points) == 1:
            points.append((points[0][0].addDays(1), points[0][1]))

        chart_rect = rect.adjusted(44, 22, -24, -42)
        min_value = min(value for date, value in points)
        max_value = max(value for date, value in points)

        if min_value == max_value:
            min_value -= 1
            max_value += 1

        painter.setPen(QPen(grid_color, 1))
        painter.drawLine(chart_rect.bottomLeft(), chart_rect.bottomRight())
        painter.drawLine(chart_rect.bottomLeft(), chart_rect.topLeft())

        start_date = points[0][0]
        end_date = points[-1][0]
        days_range = max(1, start_date.daysTo(end_date))

        line_points = []

        for date, value in points:
            x_position = chart_rect.left() + (
                start_date.daysTo(date) / days_range
            ) * chart_rect.width()
            y_position = chart_rect.bottom() - (
                (value - min_value) / (max_value - min_value)
            ) * chart_rect.height()
            line_points.append(QPointF(x_position, y_position))

        painter.setPen(QPen(line_color, 3))

        for index in range(len(line_points) - 1):
            painter.drawLine(line_points[index], line_points[index + 1])

        painter.setBrush(QBrush(line_color))

        for point in line_points:
            painter.drawEllipse(point, 4, 4)

        painter.setPen(text_color)
        painter.drawText(
            rect.adjusted(12, 0, -12, -8),
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom,
            f"Inicial: {self.format_currency(points[0][1])}",
        )
        painter.drawText(
            rect.adjusted(12, 0, -12, -8),
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom,
            f"Atual: {self.format_currency(points[-1][1])}",
        )

    def get_balance_points(self):
        transactions_by_date = {}

        for transaction in self.transactions:
            date = QDate.fromString(transaction["date"], "dd/MM/yyyy")

            if not date.isValid():
                date = QDate.currentDate()

            transactions_by_date[date] = transactions_by_date.get(date, 0) + transaction["amount"]

        balance = 0
        points = []

        for date in sorted(transactions_by_date.keys()):
            balance += transactions_by_date[date]
            points.append((date, balance))

        return points

    def format_currency(self, amount):
        formatted = f"R$ {abs(amount):,.2f}"
        formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")

        if amount < 0:
            return f"-{formatted}"

        return formatted
