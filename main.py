import sys
from datetime import date

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QAction, QDialog, QTableWidgetItem, QInputDialog, QMessageBox, \
    QFileDialog, QVBoxLayout, QWidget, QPushButton, QLabel, QCompleter

from DataBase import DataBase
from UI_files.maiwindo import Ui_MainWindow
from UI_files.group_select import Ui_Form


class SelectGroupDlg(QDialog):                                              # класс диалога с группами
    def __init__(self, root, **kwargs): # def __init__(self, parent=None):
        super().__init__(root, **kwargs) #     super().__init__(parent)
        self.root = root
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.fill_dialog(db.show_data_of_groups())
        self.ui.pushButton.clicked.connect(self.checkout_group)
        self.ui.pushButton_2.clicked.connect(self.create_new_group)
        self.ui.pushButton_3.clicked.connect(self.delete_group)

    def fill_dialog(self, lst):                                                     # заполняет виджет таблицы группами из бд
        if lst == []:
            self.ui.tableWidget.setRowCount(0)
        else:
            for co, it in enumerate(lst):
                self.ui.tableWidget.setRowCount(co + 1)
                self.ui.tableWidget.setItem(co, 0, QTableWidgetItem(f"{it[0]}"))
                self.ui.tableWidget.setItem(co, 1, QTableWidgetItem(f"{it[1]}"))

    def create_new_group(self):                                                     # Диалог создания новой группы
        text, ok = QInputDialog.getText(self, 'Новая группа', 'Введите название: ')
        if ok:
            db.create_group(text)
            self.fill_dialog(db.show_data_of_groups())

    def delete_group(self):                            # Удаляет группу и её содержимое
        check = self.critical_warning()
        if check == True:
            db.delete_group(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())
            self.fill_dialog(db.show_data_of_groups())
        else:
            return

    def checkout_group(self):
        db.id = self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text()
        self.hide()
        ex.completer_items()

    def critical_warning(self): # Предупреждение об удалении
        qm = QMessageBox()
        ret = qm.critical(self, 'Предупреждение', "Данное действие удалит всю группу и все входящие в нёё записи",  qm.Ok | qm.Cancel)

        if ret == qm.Ok:
            return True
        else:
            return False



class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.completer_items()

        def add_menu():
            layout = QHBoxLayout()
            bar = self.menuBar()
            file = bar.addMenu("Действия")
            file.addAction("Открыть группы")
            file.addAction("Импортировать товары из .xlsx файла")

            # open_groups = QAction("Open groups", self)

            file.triggered[QAction].connect(self.menu_bar_triggered)
            self.setLayout(layout)

        add_menu()

    def menu_bar_triggered(self, press):
        if press.text() == "Открыть группы":
            self.dialog_group()
        elif press.text() == "Импортировать товары из .xlsx файла":
            fname = QFileDialog.getOpenFileName(self, 'Open file',
                                                '', "Xlsx files (*.xls *.xlsx)")
            db.import_from_xls(fname[0], date.today())

    def dialog_group(self):
        sgd.exec()

    def completer_items(self):
        strList = [i[1] for i in db.show_data()] # Создаём список слов
        # Создаём QCompleter, в который устанавливаем список, а также указатель на родителя
        completer = QCompleter(strList, self.ui.lineEdit)
        completer.setCaseSensitivity(False)
        completer.setFilterMode(QtCore.Qt.MatchContains)
        self.ui.lineEdit.setCompleter(completer)


app = QApplication(sys.argv)
db = DataBase()
db.id = 1
ex = mywindow()
sgd = SelectGroupDlg(root=ex)
ex.show()
sys.exit(app.exec_())