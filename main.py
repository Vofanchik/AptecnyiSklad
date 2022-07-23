import sys

from PyQt5 import QtWidgets, Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QAction, QDialog, QTableWidgetItem

from DataBase import DataBase
from maiwindo import Ui_MainWindow
from group_select import Ui_Form

class SelectGroupDlg(QDialog):
    def __init__(self, root, **kwargs): # def __init__(self, parent=None):
        super().__init__(root, **kwargs) #     super().__init__(parent)
        self.mywindow = root
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.push_btn)

    # def fill_dialog(self, lst):
    #     for co, it in enumerate(lst):
    #         self.ui.tableWidget.setRowCount(co + 1)
    #         self.ui.tableWidget.setItem(co, 0, QTableWidgetItem(f"{it[0]}"))
    #         self.ui.tableWidget.setItem(co, 1, QTableWidgetItem(f"{it[1]}"))


    def push_btn(self):
        print(self.root)


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()

        db = DataBase()
        db.id = 1
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        def add_menu():
            layout = QHBoxLayout()
            bar = self.menuBar()
            file = bar.addMenu("Действия")
            file.addAction("Открыть группы")
            open_groups = QAction("Open groups", self)

            file.triggered[QAction].connect(self.menu_bar_triggered)
            self.setLayout(layout)

        add_menu()

    def menu_bar_triggered(self, press):
        if press.text() == "Открыть группы":
            self.dialog_group()

    def dialog_group(self):
        self.dlg = SelectGroupDlg(self)
        self.dlg.exec()






app = QApplication(sys.argv)
ex = mywindow()
ex.show()
sys.exit(app.exec_())