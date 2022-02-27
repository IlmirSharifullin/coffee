import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

from UI.main_design import Ui_MainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connection = sqlite3.connect("data/coffee.sqlite")
        self.ui.pushButton.clicked.connect(self.select_data)
        self.ui.textEdit.setPlainText("SELECT * FROM coffee")
        self.select_data()

    def select_data(self):
        query = self.ui.textEdit.toPlainText()
        a = ['ID', 'Название', 'Степень обжарки', 'Состояние', 'Описание', 'Цена (руб.)', 'Объем упаковки (г.)']
        res = self.connection.cursor().execute(query).fetchall()
        self.ui.tableWidget.setColumnCount(7)
        self.ui.tableWidget.setRowCount(0)
        for i in range(7):
            self.ui.tableWidget.setHorizontalHeaderItem(i, QTableWidgetItem(a[i]))
        for i, row in enumerate(res):
            self.ui.tableWidget.setRowCount(
                self.ui.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                if j == 3:
                    if elem == 1:
                        elem = 'В зернах'
                    elif elem == 0:
                        elem = 'Растворимый'
                self.ui.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
