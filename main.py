import sys
from datetime import date

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QDate
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QAction, QDialog, QTableWidgetItem, QInputDialog, QMessageBox, \
    QFileDialog, QCompleter

from DataBase import DataBase
from UI_files.maiwindo import Ui_MainWindow
from UI_files.group_select import Ui_Form
from UI_files.Change_item import Ui_AddItemDialog
from UI_files.oper_dialog import Ui_OperationDialog

class InputOperationDialogItem(QDialog):                                             # класс диалога с созданием нового товара
    def __init__(self,  **kwargs):                                      # def __init__(self, parent=None):
        super().__init__(**kwargs)
        self.ui = Ui_OperationDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.accept_clicked)
        self.ui.dateEdit.setDisplayFormat("yyyy-MM-dd")
        self.ui.dateEdit.setDate(QDate.currentDate())
        self.set_comleter()

    def get_item_quantyties(self):
        id = db.get_id_from_items(ex.chosen_item)[0]
        return db.show_quantyty_by_id_date(id, ex.ui.dateEdit.text(), ex.ui.dateEdit_2.text())


    def set_comleter(self):
        self.strList = [i[0] for i in db.show_division()]
        completer = QCompleter(self.strList, self.ui.lineEdit)
        completer.setCaseSensitivity(False)
        completer.setFilterMode(QtCore.Qt.MatchContains)
        # completer.activated.connect(self.onActivated_competer)
        self.ui.lineEdit.setCompleter(completer)



    def accept_clicked(self):
        if self.ui.comboBox.currentIndex() == 0:
            oper = True
        else:
            oper = False

        quant = self.ui.doubleSpinBox.value()
        date = self.ui.dateEdit.text()
        who = self.ui.lineEdit.text()
        self.set_comleter()

        db.add_quantity(db.get_id_from_items(ex.ui.label_2.text())[0], quant, oper, date, who)
        try:
            ex.fill_table_operations(ex.get_item_quantyties())
        except:
            pass

        ex.ui.label_5.setText(str(db.calculate_items(db.get_id_from_items(ex.chosen_item)[0])))

        self.hide()


class InputDialogItem(QDialog):                                             # класс диалога с созданием нового товара
    def __init__(self, change_item=False, **kwargs):                                      # def __init__(self, parent=None):
        super().__init__(**kwargs)
        self.ui = Ui_AddItemDialog()
        self.ui.setupUi(self)
        # if change_item == False:
        #     self.compl_iniit()
        # else:
        #     pass


    def compl_iniit(self):
        self.strList = [i[0] for i in db.show_package()]
        completer = QCompleter(self.strList, self.ui.lineEdit_2)
        completer.setCaseSensitivity(False)
        completer.setFilterMode(QtCore.Qt.MatchContains)
        # completer.activated.connect(self.onActivated_competer)
        self.ui.lineEdit_2.setCompleter(completer)

        self.strList2 = [i[0] for i in db.show_mnn()]
        completer2 = QCompleter(self.strList2, self.ui.lineEdit_3)
        completer2.setCaseSensitivity(False)
        completer2.setFilterMode(QtCore.Qt.MatchContains)
        # completer.activated.connect(self.onActivated_competer)
        self.ui.lineEdit_3.setCompleter(completer2)

        self.ui.buttonBox.accepted.connect(self.accept_clicked)

    def accept_clicked(self):
        db.add_items(self.ui.lineEdit.text(), self.ui.lineEdit_2.text(), self.ui.lineEdit_3.text())
        ex.completer_items()
        self.compl_iniit()
        self.hide()

    def accept_clicked_2(self):
        id = db.get_id_from_items(ex.ui.label_2.text())[0]
        db.change_item(self.ui.lineEdit.text(), self.ui.lineEdit_2.text(), self.ui.lineEdit_3.text(), id)
        ex.chosen_item = self.ui.lineEdit.text()
        ex.ui.label_2.setText(ex.chosen_item)
        ex.ui.label_3.setText(db.show_item_by_id(db.get_id_from_items(ex.chosen_item)[0])[1])
        ex.completer_items()
        self.hide()


    def change_item(self):
        id_it = db.get_id_from_items(ex.ui.label_2.text())
        ls = db.show_item_by_id(id_it[0])
        self.ui.lineEdit.setText(ls[0])
        self.ui.lineEdit_2.setText(ls[1])
        self.ui.lineEdit_3.setText(ls[2])
        self.ui.buttonBox.accepted.connect(self.accept_clicked_2)



class SelectGroupDlg(QDialog):                                              # класс диалога с группами
    def __init__(self, root, **kwargs): # def __init__(self, parent=None):
        super().__init__(root, **kwargs) #     super().__init__(parent)
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
        db.id = int(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())
        ex.ui.label.setText(list(filter(lambda x: x[0] == db.id, db.show_data_of_groups()))[0][1])
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
        self.ui.label.setText(list(filter(lambda x: x[0] == db.id, db.show_data_of_groups()))[0][1])
        self.ui.dateEdit.setDisplayFormat("yyyy-MM-dd")
        self.ui.dateEdit_2.setDisplayFormat("yyyy-MM-dd")
        self.ui.dateEdit.setDate(QDate.currentDate().addDays(-31))
        self.ui.dateEdit_2.setDate(QDate.currentDate())
        self.ui.dateEdit.dateChanged.connect(lambda: self.if_date_changed())
        self.ui.dateEdit_2.dateChanged.connect(lambda: self.if_date_changed())

        self.ui.pushButton_5.clicked.connect(self.add_item)
        self.ui.pushButton.clicked.connect(self.change_item)
        self.ui.pushButton_3.clicked.connect(self.add_operation)



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

    def add_operation(self):
        iodi.ui.label.setText(self.ui.label_2.text())
        iodi.show()

    def change_item(self):
        idi_change.change_item()
        idi_change.show()

    def add_item(self):
        idi.ui.lineEdit.setText(self.ui.lineEdit.text())
        idi.show()

    def if_date_changed(self):
        try:
            self.fill_table_operations(self.get_item_quantyties())
        except:
            pass

    def menu_bar_triggered(self, press):
        if press.text() == "Открыть группы":
            sgd.exec()
        elif press.text() == "Импортировать товары из .xlsx файла":
            fname = QFileDialog.getOpenFileName(self, 'Open file',
                                                '', "Xlsx files (*.xls *.xlsx)")
            db.import_from_xls(fname[0], date.today())

    def completer_items(self):
        self.strList = [i[1] for i in db.show_data()] # Создаём список слов
        # Создаём QCompleter, в который устанавливаем список, а также указатель на родителя
        completer = QCompleter(self.strList, self.ui.lineEdit)
        completer.setCaseSensitivity(False)
        completer.setFilterMode(QtCore.Qt.MatchContains)
        completer.activated.connect(self.onActivated_competer)
        self.ui.lineEdit.setCompleter(completer)

    def get_item_quantyties(self):
        id = db.get_id_from_items(self.chosen_item)[0]
        return db.show_quantyty_by_id_date(id, self.ui.dateEdit.text(), self.ui.dateEdit_2.text())

    def onActivated_competer(self):
        self.chosen_item = self.ui.lineEdit.text()

        self.ui.label_2.setText(self.chosen_item)
        self.ui.label_3.setText(db.show_item_by_id(db.get_id_from_items(ex.chosen_item)[0])[1]) # вставляет остаток товара
        self.fill_table_operations(self.get_item_quantyties())                                  # заполняет таблицу операциями
        self.ui.label_5.setText(str(db.calculate_items(db.get_id_from_items(self.chosen_item)[0])))
        QTimer.singleShot(0, self.ui.lineEdit.clear)

    def fill_table_operations(self, lst):                                                     # заполняет виджет таблицы группами из бд
        if lst == []:
            self.ui.tableWidget_2.setRowCount(0)
        else:
            for co, it in enumerate(lst):
                self.ui.tableWidget_2.setRowCount(co + 1)
                if it[2] > 0:
                    self.ui.tableWidget_2.setItem(co, 0, QTableWidgetItem(f"Приход"))
                    self.ui.tableWidget_2.setItem(co, 1, QTableWidgetItem(f"{it[2]}"))
                else:
                    self.ui.tableWidget_2.setItem(co, 0, QTableWidgetItem(f"Расход"))
                    self.ui.tableWidget_2.setItem(co, 1, QTableWidgetItem(f"{it[2]}"))

                self.ui.tableWidget_2.setItem(co, 2, QTableWidgetItem(f"{it[3]}"))
                self.ui.tableWidget_2.setItem(co, 3, QTableWidgetItem(f"{it[4]}"))



app = QApplication(sys.argv)
db = DataBase()
db.id = 1
ex = mywindow()
ex.chosen_item = 'Наименование'
sgd = SelectGroupDlg(root=ex)
idi = InputDialogItem()
idi_change = InputDialogItem(True)
iodi = InputOperationDialogItem()
ex.show()
sys.exit(app.exec_())