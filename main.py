import sys

from PyQt5 import QtWidgets, Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QAction, QDialog, QTableWidgetItem, QInputDialog, QMessageBox

from DataBase import DataBase
from maiwindo import Ui_MainWindow
from group_select import Ui_Form

class SelectGroupDlg(QDialog):                                              # класс диалога с группами
    def __init__(self, root, **kwargs): # def __init__(self, parent=None):
        super().__init__(root, **kwargs) #     super().__init__(parent)
        self.root = root
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.fill_dialog(db.show_data_of_groups())
        self.ui.pushButton.clicked.connect(self.push_btn)
        self.ui.pushButton_2.clicked.connect(self.create_new_group)
        self.ui.pushButton_3.clicked.connect(self.delete_group)

    def fill_dialog(self, lst):                                                     # заполняет виджет таблицы группами из бд
        for co, it in enumerate(lst):
            self.ui.tableWidget.setRowCount(co + 1)
            self.ui.tableWidget.setItem(co, 0, QTableWidgetItem(f"{it[0]}"))
            self.ui.tableWidget.setItem(co, 1, QTableWidgetItem(f"{it[1]}"))

    def create_new_group(self):                                                     # Диалог создания новой группы
        text, ok = QInputDialog.getText(self, 'Новая группа', 'Введите название: ')
        if ok:
            db.create_group(text)
            self.fill_dialog(db.show_data_of_groups())

    def delete_group(self): # Диалог создания новой группы
        self.createDB()
        db.delete_group(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())
        self.fill_dialog(db.show_data_of_groups())


    def push_btn(self):
        print(db.show_data_of_groups())

    def createDB(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setText("Error in Database Creation")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        if self.msg == QMessageBox.Ok:
            print('ok')
        elif self.msg == QMessageBox.Cancel:
            print('no')



class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()

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
        # self.dlg = SelectGroupDlg(self)
        # self.dlg.exec()
        sgd.exec()





app = QApplication(sys.argv)
db = DataBase()
db.id = 1
ex = mywindow()
sgd = SelectGroupDlg(root=ex)
ex.show()
sys.exit(app.exec_())