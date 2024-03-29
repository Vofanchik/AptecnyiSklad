# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'residue_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogResidue(object):
    def setupUi(self, DialogResidue):
        DialogResidue.setObjectName("DialogResidue")
        DialogResidue.resize(846, 574)
        self.gridLayout_2 = QtWidgets.QGridLayout(DialogResidue)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(DialogResidue)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(158)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_4 = QtWidgets.QPushButton(DialogResidue)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.pushButton = QtWidgets.QPushButton(DialogResidue)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(DialogResidue)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(DialogResidue)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.checkBox = QtWidgets.QCheckBox(DialogResidue)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout.addWidget(self.checkBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogResidue)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(DialogResidue)
        self.buttonBox.accepted.connect(DialogResidue.accept)
        self.buttonBox.rejected.connect(DialogResidue.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogResidue)

    def retranslateUi(self, DialogResidue):
        _translate = QtCore.QCoreApplication.translate
        DialogResidue.setWindowTitle(_translate("DialogResidue", "Остатки"))
        self.tableWidget.setSortingEnabled(True)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("DialogResidue", "Наименование"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("DialogResidue", "Ед. измерения"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("DialogResidue", "Остаток"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("DialogResidue", "МНН"))
        self.pushButton_4.setText(_translate("DialogResidue", "Расход/приход"))
        self.pushButton.setText(_translate("DialogResidue", "Сохранить в формате word"))
        self.pushButton_2.setText(_translate("DialogResidue", "Сохранить в формате odt"))
        self.pushButton_3.setText(_translate("DialogResidue", "Удаление товара"))
        self.checkBox.setText(_translate("DialogResidue", "Показывать нулевые значения"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogResidue = QtWidgets.QDialog()
    ui = Ui_DialogResidue()
    ui.setupUi(DialogResidue)
    DialogResidue.show()
    sys.exit(app.exec_())
