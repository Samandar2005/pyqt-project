from dis import dis
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import PyQt5

from models import Region, District


class DistrictWindow(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        # self.fillTable()

    def onAdd(self):
        region = Region.get_by_id(self.cbb_region.currentData())

        dist = District(self.le_dist.text(), region.id)
        dist.save()

        row_count = self.table.rowCount()
        self.table.setRowCount(row_count + 1)
        self.table.setItem(row_count, 0,
                           QTableWidgetItem(str(region.id)))
        self.table.setItem(row_count, 1,
                           QTableWidgetItem(str(region.name)))
        self.table.setItem(row_count, 2,
                           QTableWidgetItem(str(dist.id)))
        self.table.setItem(row_count, 3,
                           QTableWidgetItem(str(dist.name)))

    def onUpd(self):
        dist_name = self.le_dist.text()
        reg_id = self.cbb_region.currentData()
        dist_id = int(self.table.item(self.sel_row, 2).text())

        dist = District(dist_name, reg_id, dist_id)
        dist.save()

        self.fillTable()

    def onDel(self):
        dist_name = self.le_dist.text()
        reg_id = self.cbb_region.currentData()
        dist_id = int(self.table.item(self.sel_row, 2).text())

        dist = District(dist_name, reg_id, dist_id)
        dist.delete()

        self.fillTable()

    def onClicked(self):
        self.sel_row = self.table.currentRow()
        dist_name = self.table.item(self.sel_row, 3).text()
        self.le_dist.setText(dist_name)

    def initUI(self):

        self.setGeometry(200, 200, 680, 400)
        self.resize(680, 400)

        self.qlb_region = QLabel("Region", self)
        self.qlb_region.move(30, 30)

        self.cbb_region = QComboBox(self)
        self.cbb_region.move(80, 30)

        self.qlb_dist = QLabel("District name", self)
        self.qlb_dist.move(280, 30)

        self.le_dist = QLineEdit(self)
        self.le_dist.move(380, 30)

        self.btn_add = QPushButton("Add", self)
        self.btn_add.move(530, 30)
        self.btn_add.clicked.connect(self.onAdd)

        self.btn_upd = QPushButton("Update", self)
        self.btn_upd.move(530, 60)
        self.btn_upd.clicked.connect(self.onUpd)

        self.btn_del = QPushButton("Delete", self)
        self.btn_del.move(530, 90)
        self.btn_del.clicked.connect(self.onDel)

        self.table = QTableWidget(self)
        self.table.setGeometry(30, 60, 480, 300)
        self.table.setColumnCount(4)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        self.table.clicked.connect(self.onClicked)

        self.cbb_region.currentIndexChanged.connect(self.fillTable)
        for reg in Region.objects():
            self.cbb_region.addItem(reg.name, reg.id)

    def fillTable(self):
        self.table.clear()
        self.table.setHorizontalHeaderLabels(
            ["Reg id", 'Region name', 'dist id', 'District name'])
        self.table.setRowCount(0)
        self.table.hideColumn(0)
        self.table.hideColumn(2)
        current_id = self.cbb_region.currentData()
        for dist in District.objects():
            dist.regionId
            if current_id == dist.regionId:
                region = dist.region
                row_count = self.table.rowCount()
                self.table.setRowCount(row_count + 1)
                self.table.setItem(row_count, 0,
                                   QTableWidgetItem(str(region.id)))
                self.table.setItem(row_count, 1,
                                   QTableWidgetItem(str(region.name)))
                self.table.setItem(row_count, 2,
                                   QTableWidgetItem(str(dist.id)))
                self.table.setItem(row_count, 3,
                                   QTableWidgetItem(str(dist.name)))
        self.table.resizeColumnsToContents()
