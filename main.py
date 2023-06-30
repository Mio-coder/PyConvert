import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from converter import convert
from ui import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.pushButton.clicked.connect(self.convert)

    def convert(self):
        convert(self.browserIn.getPath(), self.browserOut.getPath(), self.doZipButton.isChecked())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
