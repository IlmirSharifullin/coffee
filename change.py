import sqlite3
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

from UI.addEditCoffeeForm import Ui_MainWindow


class ChangeWidget(QMainWindow):
    def __init__(self):
        super(ChangeWidget, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.con = sqlite3.connect('data/coffee.sqlite')
        self.select_data()
        self.ui.search.editingFinished.connect(self.searching)
        self.ui.rbtn_id.pressed.connect(self.id_pressed)
        self.ui.rbtn_name.pressed.connect(self.name_pressed)
        self.ui.save.clicked.connect(self.save_info)
        self.by_id = True
        self.new = True

    def select_data(self):
        query = 'Select * from coffee'
        a = ['ID', 'Название']
        res = self.con.cursor().execute(query).fetchall()
        self.ui.tableWidget.setColumnCount(2)
        self.ui.tableWidget.setRowCount(0)
        for i in range(2):
            self.ui.tableWidget.setHorizontalHeaderItem(i, QTableWidgetItem(a[i]))
        for i, row in enumerate(res):
            self.ui.tableWidget.setRowCount(
                self.ui.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.ui.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def searching(self):
        text = self.ui.search.text()
        if text:
            self.ui.save.setEnabled(True)
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
            self.ui.name.setText(res[1])
            self.ui.roastlevel.setText(res[2])
            self.ui.condition.setValue(res[3])
            self.ui.description.setPlainText(res[4])
            self.ui.price.setText(str(res[5]))
            self.ui.volume.setText(str(res[6]))
            self.new = False
        else:
            self.new = True
            self.ui.name.setText('')
            self.ui.roastlevel.setText('')
            self.ui.condition.setValue(0)
            self.ui.description.setPlainText('')
            self.ui.price.setText('')
            self.ui.volume.setText('')

    def id_pressed(self):
        self.by_id = True

    def name_pressed(self):
        self.by_id = False

    def save_info(self):
        if self.new:
            try:
                query = f'''INSERT INTO coffee(name, [roast level], condition, description, price, [packing volume]) VALUES('{self.ui.name.text()}', '{self.ui.roastlevel.text()}',
                                                        {self.ui.condition.value()}, '{self.ui.description.toPlainText()}',
                                                        {float(self.ui.price.text())}, {float(self.ui.volume.text())})'''
                self.con.cursor().execute(query)
            except Exception as e:
                raise e
        else:
            try:
                query = f'''UPDATE coffee SET name='{self.ui.name.text()}', [roast level]='{self.ui.roastlevel.text()}', condition={self.ui.condition.value()}, description='{self.ui.description.toPlainText()}', price={float(self.ui.price.text())}, [packing volume]={float(self.ui.volume.text())}'''
                if self.by_id:
                    query += f''' WHERE id={self.ui.search.text()} '''
                else:
                    query += f''' WHERE name like '%{self.ui.search.text()}%' '''
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
