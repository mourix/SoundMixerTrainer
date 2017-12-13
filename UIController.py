"""Naam: UIController.py
Versie:
Beschrijving:

Auteurs: Jos van Mourik (& Matthijs Daggelders)
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PlayPage import PlayPage
from MenuPage import MenuPage
from IntroPage import IntroPage
from AudioController import AudioController


class UIController(object):
    """Hoofd UI classe.

    Initialiseert en update de vaste UI elementen en roept widgets aan.
    """
    DEBUG = True

    def __init__(self, MainWindow, AudioController):
        self.AudioController = AudioController
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 320)  # vergroot voor debugknoppen

        # Zet achtergrond op zwart en text op wit
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255), QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        MainWindow.setPalette(palette)

        # main widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # bovenbalk
        font = QtGui.QFont("Arial", 14, QtGui.QFont.Bold)
        self.topLabel = [0 for i in range(2)]
        self.topLabel[0] = QtWidgets.QLabel(self.centralwidget)
        self.topLabel[0].setGeometry(QtCore.QRect(10, 0, 340, 30))
        self.topLabel[0].setFont(font)
        self.topLabel[0].setObjectName("topLabelLeft")
        self.topLabel[1] = QtWidgets.QLabel(self.centralwidget)
        self.topLabel[1].setGeometry(QtCore.QRect(350, 0, 120, 30))
        self.topLabel[1].setFont(font)
        self.topLabel[1].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.topLabel[1].setObjectName("topLabelRight")

        # bovenbalk lijn
        self.topLine = QtWidgets.QFrame(self.centralwidget)
        self.topLine.setGeometry(QtCore.QRect(0, 30, 480, 3))
        self.topLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.topLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.topLine.setObjectName("topLine")

        # OSD knoppen
        self.pushButton = [0 for i in range(4)]
        for i in range(4):
            def make_lambda(j): return lambda b: self.page[self.stackedWidget.currentIndex()].action_button_pushed(j)
            self.pushButton[i] = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton[i].setGeometry(QtCore.QRect(i*120, 290, 120, 30))
            self.pushButton[i].setFont(font)
            self.pushButton[i].setObjectName("pushButton_" + str(i))
            self.pushButton[i].clicked.connect(make_lambda(i))

        # knoppen voor debug: play, stop, terug
        self.debugActionLabel = ("TERUG", "PLAY", "STOP" )
        self.debugActionbutton = [0 for i in range(3)]
        for i in range(3):
            def make_lambda(j): return lambda b: self.page[self.stackedWidget.currentIndex()].action_button_pushed(j+4)
            self.debugActionbutton[i] = QtWidgets.QPushButton(self.centralwidget)
            self.debugActionbutton[i].setGeometry(QtCore.QRect(i*120, 330, 120, 30))
            self.debugActionbutton[i].setObjectName("pushButton_" + str(i))
            self.debugActionbutton[i].setText(self.debugActionLabel[i])
            self.debugActionbutton[i].clicked.connect(make_lambda(i))

        # knoppen voor debug: preset
        self.debugPresetButton = [0 for i in range(6)]
        for i in range(6):
            def make_lambda(j): return lambda b: self.page[self.stackedWidget.currentIndex()].preset_button_pushed(j)
            self.debugPresetButton[i] = QtWidgets.QPushButton(self.centralwidget)
            self.debugPresetButton[i].setGeometry(QtCore.QRect(i*60, 360, 60, 30))
            self.debugPresetButton[i].setObjectName("pushButton_" + str(i))
            self.debugPresetButton[i].setText("PR" + str(i+1))
            self.debugPresetButton[i].clicked.connect(make_lambda(i))

        # knoppen voor debug: getallen/kanalen
        self.debugChannelButton = [0 for i in range(8)]
        for i in range(8):
            def make_lambda(j): return lambda b: self.page[self.stackedWidget.currentIndex()].channel_button_pushed(j)
            self.debugChannelButton[i] = QtWidgets.QPushButton(self.centralwidget)
            self.debugChannelButton[i].setGeometry(QtCore.QRect(i*60, 390, 60, 30))
            self.debugChannelButton[i].setObjectName("pushButton_" + str(i))
            self.debugChannelButton[i].setText("CH" + str(i+1))
            self.debugChannelButton[i].clicked.connect(make_lambda(i))

        # knoppen voor debug: eq/volume reset
        self.debugRotaryButton = [0 for i in range(6)]
        for i in range(6):
            def make_lambda(j): return lambda b: self.page[self.stackedWidget.currentIndex()].rotary_button_pushed(j)
            self.debugRotaryButton[i] = QtWidgets.QPushButton(self.centralwidget)
            self.debugRotaryButton[i].setGeometry(QtCore.QRect(i * 80, 430, 80, 30))
            self.debugRotaryButton[i].setObjectName("pushButton_" + str(i))
            if i != 5:
                self.debugRotaryButton[i].setText("Reset Band" + str(i + 1))
            else:
                self.debugRotaryButton[i].setText("Mute")
            self.debugRotaryButton[i].clicked.connect(make_lambda(i))

        # maak widget met schakelbare pagina's
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 40, 481, 251))
        self.stackedWidget.setObjectName("stackedWidget")

        # maak pagina's van widget aan in losse classes
        self.page = [0 for i in range(3)]
        self.page[0] = IntroPage(self)
        self.stackedWidget.addWidget(self.page[0])
        self.page[1] = MenuPage(self, self.AudioController)
        self.stackedWidget.addWidget(self.page[1])
        self.page[2] = PlayPage(self, self.AudioController)
        self.stackedWidget.addWidget(self.page[2])

        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setWindowTitle("Sound Mixer Tool Demo UI")
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # open volgende pagina van widget en update labels
    def next_page(self):
        if self.stackedWidget.currentIndex() < self.stackedWidget.count() - 1:
            self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() + 1)
        else:
            self.stackedWidget.setCurrentIndex(0)
        self.update_main_texts(self.stackedWidget.currentIndex())

    # open vorige pagina van widget en update labels
    def previous_page(self):
        if self.stackedWidget.currentIndex() > 0:
            self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() - 1)
        else:
            self.stackedWidget.setCurrentIndex(self.stackedWidget.count() - 1)
        self.update_main_texts(self.stackedWidget.currentIndex())

    # update de bovenbalk en knoppen op basis van de array in de subclasse
    def update_main_texts(self, id):
        for i in range(2):
            self.topLabel[i].setText(self.page[id].uiItems[i])
        for i in range(4):
            self.pushButton[i].setText(self.page[id].uiItems[i + 2])

    def button_pressed(self, id, port, btnId):
        if id == 0:
            if port == 0:
                self.page[self.stackedWidget.currentIndex()].action_button_pushed(btnId)
            else:
                self.page[self.stackedWidget.currentIndex()].channel_button_pushed(btnId)
        else:
            if port == 0:
                self.page[self.stackedWidget.currentIndex()].preset_button_pushed(btnId)
            else:
                self.page[self.stackedWidget.currentIndex()].rotary_button_pushed(btnId)

        if self.DEBUG: print("UIController: button pressed" + id + port + btnId)
