"""Naam: MenuPage.py
Versie:
Beschrijving:

Auteurs: Jos van Mourik (& Matthijs Daggelders)
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import os


class MenuPage(QtWidgets.QWidget):
    """Menupagina classe.

    Initialiseerd de menupagina en loopt door een array van opties heen.
    """

    uiItems = ("Main menu", "Choose item", "▼", "▲", "Select", "Back")
    menuItems = ["Quick start", "Load from SD card"]
    menuPos = 0
    DEBUG = True

    def __init__(self, ui, AudioController):
        super().__init__()
        self.UIController = ui
        self.AudioController = AudioController
        self.setObjectName("menuPage")
        self.menuState = 1      # test variabelen
        font = QtGui.QFont("Arial", 14, QtGui.QFont.Bold)

        # menu labels
        self.menuLabel = [0 for i in range(8)]
        for i in range(8):
            self.menuLabel[i] = QtWidgets.QLabel(self)
            self.menuLabel[i].setGeometry(QtCore.QRect(60, i * 30, 400, 21))
            self.menuLabel[i].setFont(font)
            self.menuLabel[i].setObjectName("menuLabel_" + str(i))

        # menupijl
        self.menuArrow = QtWidgets.QLabel(self)
        self.menuArrow.setGeometry(QtCore.QRect(35, 0, 45, 21))
        self.menuArrow.setFont(font)
        self.menuArrow.setObjectName("menuArrow")
        self.menuArrow.setText("➔")

        self.set_menu_items()

    def set_menu_items(self):
        # testcode leegmaken menuItems
        for i in range(8):
            self.menuLabel[i].setText("")

        # vul menu met elementen
        for i in range(len(self.menuItems)):
            self.menuLabel[i].setText(str(i+1) + ". " + self.menuItems[i])

    # play, stop, terug
    def action_button_pushed(self, btnId):
        # pijl omlaag
        if btnId == 0:
            if self.menuPos < (len(self.menuItems) - 1):
                self.menuPos += 1
            else:
                self.menuPos = 0
            self.set_selector()

        # pijl onhoog
        elif btnId == 1:
            if self.menuPos > 0:
                self.menuPos -= 1
            else:
                self.menuPos = len(self.menuItems) - 1
            self.set_selector()

        # volgende/play
        elif btnId == 2 or btnId == 4:
            if self.menuState == 1:
                if self.menuPos == 0:
                    self.UIController.next_page()
                    self.AudioController.quick_play()
                else:
                    self.update_menu()
            elif self.menuState == 2:
                self.UIController.next_page()
                self.AudioController.dir_play(self.menuItems[self.menuPos])
            self.AudioController.set_current_channel(0)
            self.UIController.page[2].update_play_stats()

        # vorige
        elif btnId == 3:
            if self.menuState == 1:
                self.UIController.previous_page()
            elif self.menuState == 2:
                self.menuItems.clear()
                self.menuItems = ["Quick start", "Load from SD card"]
                self.set_menu_items()
                self.menuPos = 0
                self.set_selector()
                self.menuState = 1

        elif btnId == 5:
            self.AudioController.stop_all()

    # preset hardwareknoppen
    def preset_button_pushed(self, btnId):
        if btnId <= (len(self.menuItems) - 1):
            self.menuPos = btnId
            self.set_selector()

    # kanaal hardwareknoppen
    def channel_button_pushed(self, btnId):
        if btnId <= (len(self.menuItems) - 1):
            self.menuPos = btnId
            self.set_selector()

    def rotary_button_pushed(self, btnId):
        pass

    # verplaats menupijl
    def set_selector(self):
        self.menuArrow.move(35, (self.menuPos * 30))

    def rotary_rotate(self, RotId, direction):
        pass

    # test functie updaten menu
    def update_menu(self):
        if self.DEBUG: print("Dirs loading")

        try:
            os.listdir("SDMap")
        except FileNotFoundError:
            os.chdir("..")

        dirNames = []
        for dirs in os.listdir("SDMap"):
            dirNames.append(os.path.join(dirs))

        if self.DEBUG: print(dirNames)

        self.menuState = 2
        self.menuItems = dirNames
        self.set_menu_items()
        self.menuPos = 0
        self.set_selector()
