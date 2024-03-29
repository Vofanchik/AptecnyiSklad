# -*- coding: utf-8 -*-
import datetime
import os, sys
sys.path.append(os.getcwd()+'/venv/lib/python3.5/site-packages')

print(sys.path)
import sys
from datetime import date

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QDate
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QAction, QDialog, QTableWidgetItem, QInputDialog, QMessageBox, \
    QFileDialog, QCompleter, QWidget, QTableWidget, QPushButton

from ODF_import_expor import OdtImport, OdsExport
from  XlsxImport import Word_export
from DataBase import DataBase
from UI_files.maiwindo import Ui_MainWindow
from UI_files.group_select import Ui_Form
from UI_files.Change_item import Ui_AddItemDialog
from UI_files.oper_dialog import Ui_OperationDialog
from UI_files.residue_dialog import Ui_DialogResidue
from UI_files.DivisionOperationsDialog import Ui_DialogDivisionOperations



class OperationsDivisionDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_DialogDivisionOperations()
        self.ui.setupUi(self)
        self.ui.dateEdit_2.setDate(QDate.currentDate().addDays(-31))
        self.ui.dateEdit_3.setDate(QDate.currentDate())
        self.ui.dateEdit_2.dateChanged.connect(lambda: self.if_date_changed())
        self.ui.dateEdit_3.dateChanged.connect(lambda: self.if_date_changed())
        self.set_comleter()

    def fill_table_operations(self, sums):  # заполняет виджет таблицы группами из бд
        if not sums:
            self.ui.tableWidget.setRowCount(0)
        else:
            for co, it in enumerate(sums.values()):
                self.ui.tableWidget.setRowCount(co + 1)
                self.ui.tableWidget.setItem(co, 0, QTableWidgetItem("{}".format(it[1])))
                self.ui.tableWidget.setItem(co, 1, QTableWidgetItem("{}".format(it[2])))
                self.ui.tableWidget.setItem(co, 2, QTableWidgetItem("{}".format(it[0])))

    def if_date_changed(self):
        try:
            lst = db.show_quantyty_by_division_date(str(self.chosen_item), self.ui.dateEdit_2.text(),
                                                    self.ui.dateEdit_3.text())
            sums = {}
            for i in lst:
                if i[0] not in sums.keys():
                    sums[i[0]] = [0, i[1], i[2]]
                    sums[i[0]][0] += i[3]
                else:
                    sums[i[0]][0] += i[3]

            self.fill_table_operations(sums)
        except:
            pass

    def set_comleter(self):
        self.strList = [i[0] for i in db.show_division()]
        completer = QCompleter(self.strList, self.ui.lineEdit)
        completer.setCaseSensitivity(False)
        completer.setFilterMode(QtCore.Qt.MatchContains)
        completer.activated.connect(self.onActivated_competer)
        self.ui.lineEdit.setCompleter(completer)

    def onActivated_competer(self):
        self.chosen_item = self.ui.lineEdit.text()
        self.ui.label.setText(self.chosen_item)
        QTimer.singleShot(0, self.ui.lineEdit.clear)  # очищаем изменение текста
        lst = db.show_quantyty_by_division_date(str(self.chosen_item), self.ui.dateEdit_2.text(),
                                                self.ui.dateEdit_3.text())
        sums = {}
        for i in lst:
            if i[0] not in sums.keys():
                sums[i[0]] = [0, i[1], i[2]]
                sums[i[0]][0] += i[3]
            else:
                sums[i[0]][0] += i[3]

        self.fill_table_operations(sums)

class InputOperationDialogItem(QDialog):  # класс диалога с созданием новой операции
    def __init__(self, **kwargs):  # def __init__(self, parent=None):
        super().__init__(**kwargs)
        self.strList = None
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

class InputDialogItem(QDialog):  # класс диалога с созданием нового товара
    def __init__(self, change_item=False, **kwargs):  # def __init__(self, parent=None):
        super().__init__(**kwargs)
        self.ui = Ui_AddItemDialog()
        self.ui.setupUi(self)
        if not change_item:
            self.compl_iniit()
        else:
            pass

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

    def accept_clicked(self): # Скрипт при добавлении нового товара
        db.add_items(str(self.ui.lineEdit.text()), self.ui.lineEdit_2.text(), self.ui.lineEdit_3.text())
        ex.completer_items()
        self.compl_iniit()
        ex.chosen_item = self.ui.lineEdit.text()
        ex.ui.label_2.setText(ex.chosen_item)
        ui = ex.ui
        buttons = [ui.pushButton, ui.pushButton_2, ui.pushButton_3]  # включаем кнопки
        [i.setEnabled(True) for i in buttons]
        # rd.fill_residue_table()
        ex.fill_table_operations(lst=False)
        ex.ui.label_5.setText("0.0")
        ex.ui.label_3.setText(db.show_item_by_id(db.get_id_from_items(ex.chosen_item)[0])[1])
        self.hide()

    def accept_clicked_2(self): # скрипт для изменения названия товара
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

class ResidueDialog(QDialog):  # класс диалога с остатками
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ui = Ui_DialogResidue()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.on_ok_clicked)
        self.ui.pushButton.clicked.connect(self.on_add_clicked)
        self.ui.pushButton_2.clicked.connect(self.on_add_clicked_odf)
        self.ui.buttonBox.rejected.connect(self.on_cancell_clicked)
        self.ui.checkBox.stateChanged.connect(self.fill_residue_table)
        self.ui.pushButton_3.clicked.connect(self.delete_item)
        self.ui.pushButton_4.clicked.connect(self.IO_items)
        # self.ui.tableWidget.setColumnHidden(0, True)  # Скрывает поле id из таблицы

    def critical_warning(self):  # Предупреждение об удалении
        qm = QMessageBox()
        ret = qm.critical(self, 'Предупреждение', "Данное действие товар и все записи с ним связанные",
                          qm.Ok | qm.Cancel)

        if ret == qm.Ok:
            return True
        else:
            return False

    def IO_items(self):
        item_name = self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text()
        IO = QDialog()
        IO.setMinimumWidth(300)
        IO_layout = QtWidgets.QGridLayout()
        IO.setWindowTitle("Остатки за период")
        IO.setLayout(IO_layout)
        from_date_area_label = QtWidgets.QLabel("С")
        from_date_area = QtWidgets.QDateEdit()
        to_date_area_label = QtWidgets.QLabel("По")
        to_date_area = QtWidgets.QDateEdit()
        name = QtWidgets.QLabel(item_name)
        in_count = QtWidgets.QLabel()
        in_label = QtWidgets.QLabel("Приход")
        out_count = QtWidgets.QLabel()
        out_label = QtWidgets.QLabel("Расход")
        widgets = [name,from_date_area_label, from_date_area,to_date_area_label, to_date_area,in_label,
                   in_count,out_label,out_count]

        date_widgets = [from_date_area, to_date_area]
        [[i.setDate(datetime.datetime.now()), i.setCalendarPopup(True), i.setDisplayFormat("yyyy-MM-dd"),
          i.dateChanged.connect(lambda : [in_count.setText(str
                                                           (db.select_quant_by_date_name
                                                            (item_name, from_date_area.text(),
                                                             to_date_area.text())[0][1])),
        out_count.setText(str(db.select_quant_by_date_name(item_name, from_date_area.text(),
                                                           to_date_area.text())[0][0]))])] for i in date_widgets]
        from_date_area.setDate(QDate.currentDate().addDays(-31))

        for c, w in enumerate(widgets):
            IO_layout.addWidget(w)

        IO.exec_()



    def delete_item(self):
        id = db.get_id_from_items(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())[0]

        check = self.critical_warning()
        try:
            if check == True:
                db.delete_item(id)
                self.fill_residue_table()
                ex.completer_items()
                ex.ui.label_2.setText('')
                ex.ui.label_3.setText('')  # вставляет еденицу измерения товара
                ex.ui.label_5.setText('')
                # ex.ui.
                ex.ui.pushButton.setEnabled(False)
                ex.ui.pushButton_2.setEnabled(True)
                ex.ui.pushButton_3.setEnabled(False)
                ex.fill_table_operations(lst=[])
            else:
                return
        except:
            pass


        db.delete_item(id)
        self.fill_residue_table()
    def on_add_clicked(self): # импорт в word
        if self.ui.checkBox.checkState() == 0:
            lst = list(filter(lambda x: x[3] != '0.0' and x[3] != 'None', db.return_residue()))
        else:
            lst = list(db.return_residue())
        fname = QFileDialog.getSaveFileName(self, 'Save file',
                                            '', "Word files (*.docx *.doc)")

        import_word.form_docx(lst, fname[0])

    def on_add_clicked_odf(self): # импорт в odt
        if self.ui.checkBox.checkState() == 0:
            lst = list(filter(lambda x: x[3] != '0.0' and x[3] != 'None', db.return_residue()))
        else:
            lst = list(db.return_residue())
        fname = QFileDialog.getSaveFileName(self, 'Save file',
                                            '', "Open Office Document text files (*.odt)")

        import_odt.form_odt(lst, fname[0])

    def fill_residue_table(self):
        if self.ui.checkBox.checkState() == 0:
            lst = list(filter(lambda x : x[3] != '0.0' and x[3] != 'None', db.return_residue()))
        else:
            lst = list(db.return_residue())
        if not lst:
            self.ui.tableWidget.setRowCount(0)
        else:
            for co, it in enumerate(lst):
                self.ui.tableWidget.setRowCount(co + 1)
                self.ui.tableWidget.setItem(co, 0, QTableWidgetItem("{}".format(it[0])))
                self.ui.tableWidget.setItem(co, 1, QTableWidgetItem("{}".format(it[1])))
                self.ui.tableWidget.setItem(co, 2, QTableWidgetItem("{}".format(it[3])))
                self.ui.tableWidget.setItem(co, 3, QTableWidgetItem("{}".format(it[2])))


    def on_ok_clicked(self):
        ex.chosen_item = self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text()
        # db.get_id_from_items(ex.chosen_item)[0])[1]
        ex.ui.label_2.setText(ex.chosen_item)
        ex.ui.label_3.setText(
            db.show_item_by_id(db.get_id_from_items(ex.chosen_item)[0])[1])  # вставляет еденицу измерения товара
        ex.ui.label_5.setText(str(db.calculate_items(db.get_id_from_items(ex.chosen_item)[0])))
        ex.fill_table_operations(ex.get_item_quantyties())  # заполняет таблицу операциями
        ex.ui.pushButton.setEnabled(True)
        ex.ui.pushButton_2.setEnabled(True)
        ex.ui.pushButton_3.setEnabled(True)
        rd.hide()

    def on_cancell_clicked(self):
        rd.hide()

class SelectGroupDlg(QDialog):  # класс диалога с группами
    def __init__(self, root, **kwargs):  # def __init__(self, parent=None):
        super().__init__(root, **kwargs)  # super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.fill_dialog(db.show_data_of_groups())
        self.ui.pushButton.clicked.connect(self.checkout_group)
        self.ui.pushButton_2.clicked.connect(self.create_new_group)
        self.ui.pushButton_3.clicked.connect(self.delete_group)
        self.ui.tableWidget.setColumnHidden(0, True)  # Скрывает поле id из таблицы

    def fill_dialog(self, lst):  # заполняет виджет таблицы группами из бд
        if lst == []:
            self.ui.tableWidget.setRowCount(0)
        else:
            for co, it in enumerate(lst):
                self.ui.tableWidget.setRowCount(co + 1)
                self.ui.tableWidget.setItem(co, 0, QTableWidgetItem("{}".format(it[0])))
                self.ui.tableWidget.setItem(co, 1, QTableWidgetItem("{}".format(it[1])))

    def create_new_group(self):  # Диалог создания новой группы
        text, ok = QInputDialog.getText(self, 'Новая группа', 'Введите название: ')
        if ok:
            db.create_group(text)
            self.fill_dialog(db.show_data_of_groups())

    def delete_group(self):  # Удаляет группу и её содержимое
        check = self.critical_warning()
        try:
            if check == True:
                db.delete_group(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())
                self.fill_dialog(db.show_data_of_groups())
            else:
                return
        except:
            pass

    def checkout_group(self):
        try:
            db.id = int(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())
            ex.ui.label.setText(list(filter(lambda x: x[0] == db.id, db.show_data_of_groups()))[0][1])
            ui = ex.ui
            buttons = [ui.pushButton, ui.pushButton_2, ui.pushButton_3]  # выключаем кнопки
            [i.setEnabled(False) for i in buttons]
            ex.ui.pushButton_4.setEnabled(True)
            ex.ui.pushButton_5.setEnabled(True)
            self.hide()
            ex.completer_items()
        except:
            pass

    def critical_warning(self):  # Предупреждение об удалении
        qm = QMessageBox()
        ret = qm.critical(self, 'Предупреждение', "Данное действие удалит всю группу и все входящие в нёё записи",
                          qm.Ok | qm.Cancel)

        if ret == qm.Ok:
            return True
        else:
            return False

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()

        self.chosen_item = None
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.completer_items()
        try:
            self.ui.label.setText(list(filter(lambda x: x[0] == db.id, db.show_data_of_groups()))[0][1])
        except:
            pass
        self.ui.dateEdit.setDisplayFormat("yyyy-MM-dd")
        self.ui.dateEdit_2.setDisplayFormat("yyyy-MM-dd")
        self.ui.dateEdit.setDate(QDate.currentDate().addDays(-31))
        self.ui.dateEdit_2.setDate(QDate.currentDate())
        self.ui.dateEdit.dateChanged.connect(lambda: self.if_date_changed())
        self.ui.dateEdit_2.dateChanged.connect(lambda: self.if_date_changed())

        self.ui.pushButton_5.clicked.connect(self.add_item)
        self.ui.pushButton.clicked.connect(self.change_item)
        self.ui.pushButton_3.clicked.connect(self.add_operation)
        self.ui.pushButton_2.clicked.connect(self.delete_quantity_row)
        self.ui.pushButton_4.clicked.connect(self.open_residue_dialog)

        self.ui.tableWidget_2.setColumnHidden(4, True)  # Скрывает поле id из таблицы

        def add_menu():
            layout = QHBoxLayout()
            bar = self.menuBar()
            file = bar.addMenu("Действия")
            file.addAction("Открыть группы")
            file.addAction("Импортировать товары из .xlsx файла")
            file.addAction("Импортировать товары из .ods файла")
            file.addAction("Открыть расход по отделениям")
            file.addAction("Редактировать получателей")

            # open_groups = QAction("Open groups", self)

            file.triggered[QAction].connect(self.menu_bar_triggered)
            self.setLayout(layout)

        add_menu()

    def delete_quantity_row(self):
        db.delete_quantity(self.ui.tableWidget_2.item(self.ui.tableWidget_2.currentRow(), 4).text())
        self.ui.label_5.setText(str(db.calculate_items(db.get_id_from_items(self.chosen_item)[0])))
        self.fill_table_operations(self.get_item_quantyties())

    def add_operation(self):
        iodi.ui.label.setText(self.ui.label_2.text())
        iodi.show()

    def change_item(self):
        idi_change.change_item()
        idi_change.show()

    def open_residue_dialog(self):
        rd.fill_residue_table()
        rd.show()

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
            sgd.exec_()
        elif press.text() == "Импортировать товары из .xlsx файла":
            fname = QFileDialog.getOpenFileName(self, 'Open file',
                                                '', "Xlsx files (*.xls *.xlsx)")
            try:
                db.import_from_xls(fname[0], date.today())
                ex.completer_items()
            except:
                pass

        elif press.text() == "Импортировать товары из .ods файла":
            fname = QFileDialog.getOpenFileName(self, 'Open file',
                                                '', "Ods files (*.ods)")
            try:
                db.import_from_ods(fname[0], date.today())
                ex.completer_items()
            except:
                pass

        elif press.text() == "Открыть расход по отделениям":
            dod.show()

        elif press.text() == "Редактировать получателей":
            del_recivier = QDialog()
            del_recivier.setWindowTitle('Редактировать получателей')

            del_button = QPushButton()
            del_button.setText("Удалить")

            recivier_layout = QtWidgets.QVBoxLayout()
            recivier_table = QTableWidget()
            recivier_table.setColumnCount(2)
            recivier_table.horizontalHeader().setStretchLastSection(True)

            for co, it in enumerate(db.show_division_and_id()):
                recivier_table.setRowCount(co + 1)

                recivier_table.setItem(co, 0, QTableWidgetItem(str(it[0])))
                recivier_table.setItem(co, 1, QTableWidgetItem(it[1]))


            recivier_table.setHorizontalHeaderLabels(['id',"Получатели"])
            # recivier_table.setColumnHidden(0, True)
            recivier_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)

            del_recivier.setLayout(recivier_layout)
            recivier_layout.addWidget(recivier_table)
            recivier_layout.addWidget(del_button)

            del_button.clicked.connect(lambda: db.delete_division(recivier_table.item(recivier_table.currentRow(), 0).
                                                                   text()))

            if del_recivier.exec_():
                pass



    def completer_items(self):
        self.strList = [i[1] for i in db.show_data()]  # Создаём список слов
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
        self.ui.label_3.setText(
            db.show_item_by_id(db.get_id_from_items(ex.chosen_item)[0])[1])  # вставляет остаток товара
        self.fill_table_operations(self.get_item_quantyties())  # заполняет таблицу операциями
        self.ui.label_5.setText(str(db.calculate_items(db.get_id_from_items(self.chosen_item)[0])))

        ui = self.ui
        buttons = [ui.pushButton, ui.pushButton_2, ui.pushButton_3]  # включаем кнопки
        [i.setEnabled(True) for i in buttons]

        QTimer.singleShot(0, self.ui.lineEdit.clear)  # очищаем изменение текста

    def fill_table_operations(self, lst):  # заполняет виджет таблицы группами из бд
        if not lst:
            self.ui.tableWidget_2.setRowCount(0)
        else:
            for co, it in enumerate(lst):
                self.ui.tableWidget_2.setRowCount(co + 1)
                if it[2] > 0:
                    self.ui.tableWidget_2.setItem(co, 0, QTableWidgetItem("Приход"))
                    self.ui.tableWidget_2.setItem(co, 1, QTableWidgetItem("{}".format(it[2])))
                else:
                    self.ui.tableWidget_2.setItem(co, 0, QTableWidgetItem("Расход"))
                    self.ui.tableWidget_2.setItem(co, 1, QTableWidgetItem("{}".format(it[2])))

                self.ui.tableWidget_2.setItem(co, 2, QTableWidgetItem("{}".format(it[3])))
                self.ui.tableWidget_2.setItem(co, 3, QTableWidgetItem("{}".format(it[4])))
                self.ui.tableWidget_2.setItem(co, 4, QTableWidgetItem("{}".format(it[0])))


app = QApplication(sys.argv)
db = DataBase()
db.id = None
ex = mywindow()
# print(ex.ui.gridLayout)

ex.chosen_item = 'Наименование'
sgd = SelectGroupDlg(root=ex)
idi = InputDialogItem()
idi_change = InputDialogItem(True)
iodi = InputOperationDialogItem()
rd = ResidueDialog()
import_word = Word_export()
import_odt = OdtImport()
dod = OperationsDivisionDialog()

ex.show()
sgd.show()
sys.exit(app.exec_())
