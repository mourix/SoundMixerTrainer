"""Naam: MenuPage.py
Versie:
Beschrijving:

Auteurs: Jos van Mourik
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import os


class MenuPage(QtWidgets.QWidget):
    """Menupagina classe.

    Initialiseerd de menupagina en loopt door een array van opties heen.
    """

    uiItems = ("Hoofdmenu", "Kies item", "▼", "▲", "Selecteer", "pass")
    menuItems = ["Snel starten", "Laden uit SD-kaart"]
    menuPos = 0
    DEBUG = True

    def __init__(self, ui, AudioController):
        super().__init__()
        self.UIController = ui
        self.AudioController = AudioController
        self.setObjectName("menuPage")
        self.menuItems = ("Snel starten", "Laden uit SD-kaart")
        self.menuState = 1      # test varaibelen
        self.dirs =[]
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
        self.menuArrow.setGeometry(QtCore.QRect(20, 0, 41, 21))
        self.menuArrow.setFont(font)
        self.menuArrow.setObjectName("menuArrow")

        self.set_menu_items()

    def set_menu_items(self):
        # testcode leegmaken menuItems
        for i in range(8):
            self.menuLabel[i].setText("")

        # vul menu met elementen
        for i in range(len(self.menuItems)):
            self.menuLabel[i].setText(self.menuItems[i])
        self.menuArrow.setText("-->")

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
        elif btnId == 2 or btnId == 5:
            if self.menuState == 1:
                if self.menuPos == 0:
                    self.UIController.next_page()
                    self.AudioController.quick_play()
                    self.UIController.page[2].update_play_stats()
                else:
                    self.update_menu()
            elif self.menuState == 2:
                self.UIController.next_page()
                self.AudioController.dir_play(self.menuItems[self.menuPos])
                self.UIController.page[2].update_play_stats()

        elif btnId == 3:
            pass

        # vorige
        elif btnId == 4:
            if self.menuState == 1:
                self.UIController.previous_page()
            elif self.menuState == 2:
                self.menuItems.clear()
                self.menuItems = ["Snel starten", "Laden uit SD-kaart"]
                self.set_menu_items()
                self.menuPos = 0
                self.set_selector()
                self.menuState = 1

        elif btnId == 6:
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
        self.menuArrow.move(20, (self.menuPos * 30))

    def rotary_rotate(self, RotId, direction):
        pass

    # test functie updaten menu
    def update_menu(self):
        if self.DEBUG: print("Dirs loading")

        try:
            os.listdir("SDMap")
        except:
            os.chdir("..")

        dirnames = []
        for dirs in os.listdir("SDMap"):
            dirnames.append(os.path.join(dirs))
            self.dirs = dirs

        if self.DEBUG: print(dirnames)

        self.menuState = 2
        self.menuItems = dirnames
        self.set_menu_items()
        self.menuPos = 0
        self.set_selector()
        return