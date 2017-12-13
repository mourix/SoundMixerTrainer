"""Naam: IntroPage.py
Versie:
Beschrijving:

Auteurs: Jos van Mourik
"""

from PyQt5 import QtCore, QtGui, QtWidgets


class IntroPage(QtWidgets.QWidget):
    """Titelpagina classe.

    Initialiseerd de titelpagina en gaat door als er geklikt wordt.
    """

    uiItems = ("", "", "", "", "", "")
    DEBUG = True

    def __init__(self, ui):
        super().__init__()
        self.UIController = ui
        font = QtGui.QFont("Arial", 24, QtGui.QFont.Bold)
        self.setObjectName("introPage")
        self.infoLabel_0 = QtWidgets.QLabel(self)
        self.infoLabel_0.setGeometry(QtCore.QRect(40, 0, 381, 61))
        self.infoLabel_0.setFont(font)
        self.infoLabel_0.setObjectName("intoLabel_0")

        font = QtGui.QFont("Arial", 14)
        self.introLabel_1 = QtWidgets.QLabel(self)
        self.introLabel_1.setGeometry(QtCore.QRect(40, 70, 381, 141))
        self.introLabel_1.setFont(font)
        self.introLabel_1.setObjectName("introLabel_1")
        self.infoLabel_0.setText("Sound Mixer Trainer V1")
        self.introLabel_1.setText("Made by: \n"
                                  "Matthijs, Jos, Trevor, Rémon en Suzanne\n(c) 2018\n\n\n"
                                  "Press any key to continue.")

    # "press any key"
    def action_button_pushed(self, btnId):
        self.UIController.next_page()

    def preset_button_pushed(self, btnId):
        self.UIController.next_page()

    def channel_button_pushed(self, btnId):
        self.UIController.next_page()

    def rotary_rotate(self, RotId, direction):
        pass
