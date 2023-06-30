from itertools import chain
from json import load

from PyQt5.QtCore import QRect, QSize, QMetaObject, QCoreApplication, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout, QPushButton, \
    QTabWidget, QGridLayout, QCheckBox, QScrollArea

from file_dilog import FileDialog
from converter import get_path


class FileTypeBrowser(QTabWidget):
    with open(get_path("fileTypesData.json")) as f:
        buttonsText = load(f)

    def __init__(self, root):
        super().__init__(root)
        self.setMinimumSize(QSize(260, 90))
        self.setObjectName("selectResultTypeTab")

        self.tabs = []
        self.layouts = []
        self.buttons = []
        self.activeButton: QPushButton = None
        for i, (name, tab) in enumerate(self.buttonsText.items()):
            self.tabs.append(QWidget())
            self.tabs[-1].setObjectName(name.lower() + "Select")
            self.layouts.append(QGridLayout(self.tabs[-1]))
            self.layouts[-1].setGeometry(QRect(10, 10, 239, 54))
            self.layouts[-1].setObjectName(name.lower() + "GridLayout")
            self.buttons.append([])
            for y, row in enumerate(tab):
                for x, text in enumerate(row):
                    button = QPushButton()
                    button.setObjectName(text.lower() + "Button")
                    button.setCheckable(True)
                    button.clicked.connect(self.clickButton(button))
                    button.setText(text)
                    self.buttons[-1].append(button)
                    self.layouts[-1].addWidget(button, y, x)
            self.addTab(self.tabs[-1], "")
            self.setTabText(i, name)

    def clickButton(self, button):
        def change(toggle):
            if self.activeButton is not None:
                self.activeButton.setChecked(False)
            if toggle:
                self.activeButton = button
                self.activeButton.setChecked(True)
            else:
                self.activeButton = None

        return change

    def retranslateUI(self):
        _translate = QCoreApplication.translate
        for i, name in enumerate(self.buttonsText.keys()):
            self.setTabText(i, _translate("MainWindow", name))


class FileBrowser(QWidget):
    def __init__(self, types, parent=None):
        super().__init__(parent)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.types = types

        self.horizontalLayout_6 = QHBoxLayout(self)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        self.browsePathLabel = QLabel(self)
        self.browsePathLabel.setMinimumSize(QSize(50, 16))
        self.browsePathLabel.setMaximumSize(QSize(16777215, 80))
        self.browsePathLabel.setObjectName("browsePathLabel")

        self.horizontalLayout.addWidget(self.browsePathLabel)

        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem)

        self.BrowseButton = QPushButton(self)
        self.BrowseButton.setObjectName("BrowseButton")
        self.horizontalLayout.addWidget(self.BrowseButton)
        self.BrowseButton.clicked.connect(self.browse)

    def browse(self):
        self.browsePathLabel.setText(FileDialog(fmt=self.types))

    def getPath(self):
        return self.browsePathLabel.text()

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.browsePathLabel.setText(_translate("MainWindow", "<html><head/><body><p>--browse--</p></body></html>"))
        self.BrowseButton.setText(_translate("MainWindow", "Browse"))


# noinspection PyAttributeOutsideInit
class Ui_MainWindow:
    horizontalLayout: QHBoxLayout
    fromLabel: QLabel
    verticalLayout: QVBoxLayout
    horizontalLayout_3: QHBoxLayout
    title: QLabel
    verticalLayout_3: QVBoxLayout
    centralwidget: QWidget

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(622, 324)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.title = QLabel(self.centralwidget)
        self.title.setMinimumSize(QSize(310, 30))
        self.title.setMaximumSize(QSize(16777215, 100))
        self.title.setObjectName("title")
        self.verticalLayout_3.addWidget(self.title)

        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.fromLabel = QLabel(self.centralwidget)
        self.fromLabel.setMinimumSize(QSize(60, 40))
        self.fromLabel.setMaximumSize(QSize(16777215, 41))
        self.fromLabel.setObjectName("fromLabel")
        self.verticalLayout.addWidget(self.fromLabel)

        fileTypes = {v: v.lower() for v in chain.from_iterable(chain.from_iterable(FileTypeBrowser.buttonsText.values()))}
        fileTypes["ZIP"] = "zip"
        fileTypes[""] = "*"
        self.browserIn = FileBrowser(fileTypes, self.centralwidget)

        self.verticalLayout.addLayout(self.browserIn.horizontalLayout)
        self.verticalLayout.addWidget(self.browserIn)

        self.horizontalLayout_3.addLayout(self.verticalLayout)

        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.toLabel = QLabel(self.centralwidget)
        self.toLabel.setMinimumSize(QSize(20, 19))
        self.toLabel.setObjectName("toLabel")
        self.verticalLayout_2.addWidget(self.toLabel)
        #
        # self.selectResultTypeTab = FileTypeBrowser(self.centralwidget)
        # self.verticalLayout_2.addWidget(self.selectResultTypeTab)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.doZipButton = QCheckBox(self.centralwidget)
        self.doZipButton.setMinimumSize(QSize(80, 30))
        self.doZipButton.setObjectName("doZipButton")
        self.horizontalLayout_2.addWidget(self.doZipButton)

        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.browserOut = FileBrowser(fileTypes, self.centralwidget)
        self.verticalLayout_2.addLayout(self.browserOut.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setMaximumSize(QSize(51, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_4.addWidget(self.pushButton)

        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)

        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        spacerItem5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem5)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title.setText(_translate("MainWindow",
                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Image and Video Converter</span></p></body></html>"))
        self.fromLabel.setText(_translate("MainWindow",
                                          "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">From</span></p></body></html>"))

        self.toLabel.setText(_translate("MainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">To</span></p></body></html>"))

        self.doZipButton.setText(_translate("MainWindow", "zip result (work in progres)"))
        self.pushButton.setText(_translate("MainWindow", "Convert"))

        self.browserIn.retranslateUi()
        self.browserOut.retranslateUi()
