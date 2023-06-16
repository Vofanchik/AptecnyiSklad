import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
class filedialogdemo(QWidget):
 def __init__(self, parent=None):
     super(filedialogdemo, self).__init__(parent)
     layout = QVBoxLayout()
     self.btn = QPushButton("QFileDialog static method demo")
     self.btn.clicked.connect(self.getfile)
     layout.addWidget(self.btn)
     self.le = QLabel("")
     layout.addWidget(self.le)

     self.setLayout(layout)
     self.setWindowTitle("File Dialog demo")

 def getfile(self):
     fname = QFileDialog.getOpenFileName(self, 'Open file',
     '',"Xlsx files (*.xls *.xlsx)")
     self.le.setPixmap(QPixmap(fname[0]))

def main():
 app = QApplication(sys.argv)
 ex = filedialogdemo()
 ex.show()
 sys.exit(app.exec_())
if __name__ == '__main__':
 main()
