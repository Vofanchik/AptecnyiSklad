# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DivisionOperationsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogDivisionOperations(object):
    def setupUi(self, DialogDivisionOperations):
        DialogDivisionOperations.setObjectName("DialogDivisionOperations")
        DialogDivisionOperations.resize(759, 519)
        self.gridLayout = QtWidgets.QGridLayout(DialogDivisionOperations)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(DialogDivisionOperations)
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(145)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(49)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.tableWidget, 4, 1, 1, 2)
        self.lineEdit = QtWidgets.QLineEdit(DialogDivisionOperations)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 2)
        self.label = QtWidgets.QLabel(DialogDivisionOperations)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 1, 1, 2)
        self.dateEdit_3 = QtWidgets.QDateEdit(DialogDivisionOperations)
        self.dateEdit_3.setCalendarPopup(True)
        self.dateEdit_3.setCurrentSectionIndex(0)
        self.dateEdit_3.setObjectName("dateEdit_3")
        self.gridLayout.addWidget(self.dateEdit_3, 2, 2, 1, 1)
        self.dateEdit_2 = QtWidgets.QDateEdit(DialogDivisionOperations)
        self.dateEdit_2.setCalendarPopup(True)
        self.dateEdit_2.setCurrentSectionIndex(0)
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.gridLayout.addWidget(self.dateEdit_2, 2, 1, 1, 1)

        self.retranslateUi(DialogDivisionOperations)
        QtCore.QMetaObject.connectSlotsByName(DialogDivisionOperations)

    def retranslateUi(self, DialogDivisionOperations):
        _translate = QtCore.QCoreApplication.translate
        DialogDivisionOperations.setWindowTitle(_translate("DialogDivisionOperations", "Выдача"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("DialogDivisionOperations", "Наименование"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("DialogDivisionOperations", "ед. измерения"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("DialogDivisionOperations", "Выдано за период"))
        self.label.setText(_translate("DialogDivisionOperations", "<html><head/><body><p><span style=\" font-size:16pt;\">Отделение</span></p></body></html>"))
        self.dateEdit_3.setDisplayFormat(_translate("DialogDivisionOperations", "yyyy-MM-dd"))
        self.dateEdit_2.setDisplayFormat(_translate("DialogDivisionOperations", "yyyy-MM-dd"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogDivisionOperations = QtWidgets.QDialog()
    ui = Ui_DialogDivisionOperations()
    ui.setupUi(DialogDivisionOperations)
    DialogDivisionOperations.show()
    sys.exit(app.exec_())
