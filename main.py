import sqlite3

from PyQt5 import QtWidgets, uic
import sys


class CoffeeWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        self.connection = sqlite3.connect("coffee.sqlite")
        self.sql_cursor = self.connection.cursor()

        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(
            ["id", "Сорт", "Обжарка (°)", "Консистенция", "Вкус", "Цена", "Объём"]
        )

        self.update()
        self.update_button.clicked.connect(self.update)

    def update(self):
        data = self.sql_cursor.execute("""
            SELECT * FROM coffee
        """).fetchall()

        self.table_widget.clearContents()
        self.table_widget.setRowCount(len(data))

        row = -1
        for i in data:
            row = row + 1

            column = -1
            for j in i:
                column += 1
                self.table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(str(j)))

    def closeEvent(self, event):
        self.connection.close()


# Запуск Виджета
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
    sys.exit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = CoffeeWidget()
    widget.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())