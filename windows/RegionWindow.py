from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import PyQt5

from models import Region


class RegionWindow(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(PyQt5.QtCore.Qt.Window)

        self.setWindowTitle('Viloyatlar')
        self.row_count = 0

        self.initUI()

        self.sel_region = None

    def initUI(self):
        self.setGeometry(100, 100, 400, 400)

        self.ql_region_name = QLabel(self)
        self.ql_region_name.setText("Region Name: ")
        self.ql_region_name.move(30, 30)

        self.qle_region_name = QLineEdit(self)
        self.qle_region_name.move(120, 30)

        self.btn_add = QPushButton('Add', self)
        self.btn_add.move(300, 30)
        self.btn_add.clicked.connect(self.onAdd)

        self.btn_update = QPushButton('Update', self)
        self.btn_update.move(300, 60)
        self.btn_update.clicked.connect(self.onUpdate)

        self.btn_del = QPushButton('Delete', self)
        self.btn_del.move(300, 90)
        self.btn_del.clicked.connect(self.onDel)

        self.table = QTableWidget(self)  # Создаём таблицу
        self.table.move(30, 60)
        self.table.setColumnCount(2)     # Устанавливаем три колонки

        # Устанавливаем заголовки таблицы
        self.table.setHorizontalHeaderLabels(['Id', "Region name"])

        # Устанавливаем всплывающие подсказки на заголовки
        self.table.horizontalHeaderItem(0).setToolTip("This is Region name")

        self.table.hideColumn(0)

        # Устанавливаем выравнивание на заголовки
        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)

        # заполняем первую строку
        for region in Region.objects():
            self.table.setRowCount(self.row_count + 1)
            self.table.setItem(self.row_count, 0,
                               QTableWidgetItem(str(region.id)))
            self.table.setItem(self.row_count, 1,
                               QTableWidgetItem(str(region)))
            self.row_count += 1

        # делаем ресайз колонок по содержимому
        self.table.resizeColumnsToContents()
        self.table.clicked.connect(self.onClicked)

    def onAdd(self):
        reg = Region(self.qle_region_name.text())
        reg.save()
        self.table.setRowCount(self.row_count + 1)

        self.table.setItem(self.row_count, 0,
                           QTableWidgetItem(str(reg.id)))
        self.table.setItem(self.row_count, 1,
                           QTableWidgetItem(reg.name))
        self.row_count += 1

    def onUpdate(self):
        if self.sel_region is not None:
            self.sel_region.name = self.qle_region_name.text()
            self.sel_region.save()
            self.table.setItem(
                self.sel_row, 1, QTableWidgetItem(str(self.sel_region)))

    def onDel(self):
        if self.sel_region is not None:
            self.sel_region.delete()
            self.sel_region = None
            self.table.removeRow(self.sel_row)

    def onClicked(self, item):
        self.sel_row = self.table.currentRow()
        self.qle_region_name.setText(self.table.item(self.sel_row, 1).text())

        self.sel_region = Region(self.table.item(
            self.sel_row, 1).text(), self.table.item(self.sel_row, 0).text())
