from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QLineEdit, QCompleter
from PyQt5.QtCore import QSize
from DataBase import DataBase


# Наследуемся от QMainWindow
class MainWindow(QMainWindow):
    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(480, 80))  # Устанавливаем размеры
        self.setWindowTitle("Проверка автодополнения")  # Устанавливаем заголовок окна
        central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(central_widget)  # Устанавливаем центральный виджет

        grid_layout = QGridLayout()  # Создаём QGridLayout
        central_widget.setLayout(grid_layout)  # Устанавливаем данное размещение в центральный виджет

        grid_layout.addWidget(QLabel("Проверка автодополнения", self), 0, 0)

        # Создаём поле ввода
        lineEdit = QLineEdit(self)
        db = DataBase()
        strList = [i[1] for i in db.show_data_of_groups()] # Создаём список слов
        # Создаём QCompleter, в который устанавливаем список, а также указатель на родителя
        completer = QCompleter(strList, lineEdit)
        completer.setCaseSensitivity(False)
        completer.setFilterMode(QtCore.Qt.MatchContains)
        lineEdit.setCompleter(completer)  # Устанавливает QCompleter в поле ввода
        grid_layout.addWidget(lineEdit, 0, 1)  # Добавляем поле ввода в сетку


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())