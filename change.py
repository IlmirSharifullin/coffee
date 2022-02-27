import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class ChangeWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.select_data()
        self.search.editingFinished.connect(self.searching)
        self.rbtn_id.pressed.connect(self.id_pressed)
        self.rbtn_name.pressed.connect(self.name_pressed)
        self.save.clicked.connect(self.save_info)
        self.by_id = True
        self.new = True

    def select_data(self):
        query = 'Select * from coffee'
        a = ['ID', 'Название']
        res = self.con.cursor().execute(query).fetchall()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        for i in range(2):
            self.tableWidget.setHorizontalHeaderItem(i, QTableWidgetItem(a[i]))
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def searching(self):
        text = self.search.text()
        if text:
            self.save.setEnabled(True)
        else:
            return
        if self.by_id:
            query = f'SELECT * FROM coffee WHERE id == {text}'
        else:
            query = f'SELECT * FROM coffee WHERE name like "%{text}%"'
        try:
            res = self.con.cursor().execute(query).fetchone()
        except Exception:
            res = None
        if res:
            self.name.setText(res[1])
            self.roastlevel.setText(res[2])
            self.condition.setValue(res[3])
            self.description.setPlainText(res[4])
            self.price.setText(str(res[5]))
            self.volume.setText(str(res[6]))
            self.new = False
        else:
            self.new = True
            self.name.setText('')
            self.roastlevel.setText('')
            self.condition.setValue(0)
            self.description.setPlainText('')
            self.price.setText('')
            self.volume.setText('')

    def id_pressed(self):
        self.by_id = True

    def name_pressed(self):
        self.by_id = False

    def save_info(self):
        if self.new:
            try:
                query = f'''INSERT INTO coffee(name, [roast level], condition, description, price, [packing volume]) VALUES('{self.name.text()}', '{self.roastlevel.text()}',
                                                        {self.condition.value()}, '{self.description.toPlainText()}',
                                                        {float(self.price.text())}, {float(self.volume.text())})'''
                self.con.cursor().execute(query)
            except Exception as e:
                raise e
        else:
            try:
                query = f'''UPDATE coffee SET name='{self.name.text()}', [roast level]='{self.roastlevel.text()}', condition={self.condition.value()}, description='{self.description.toPlainText()}', price={float(self.price.text())}, [packing volume]={float(self.volume.text())}'''
                if self.by_id:
                    query += f''' WHERE id={self.search.text()} '''
                else:
                    query += f''' WHERE name like '%{self.search.text()}%' '''
                self.con.cursor().execute(query)
            except Exception as e:
                raise e
        self.con.commit()
        self.select_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChangeWidget()
    ex.show()
    sys.exit(app.exec())
