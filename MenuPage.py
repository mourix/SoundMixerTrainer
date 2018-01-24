"""Naam: MenuPage.py
Versie:
Beschrijving:

Auteurs: Jos van Mourik (& Matthijs Daggelders)
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import os


class MenuPage(QtWidgets.QWidget):
    """Menupagina classe.

    Initialiseert de menupagina en loopt door een array van opties heen.
    """

    uiItems0 = ["Main menu", "Choose item", "▼", "▲", "Select", "Back"]
    menuItems = ["Quick start", "Load from SD card"]
    menuPos = 0
    DEBUG = True

    def __init__(self, ui, AudioController):
        super().__init__()
        self.UIController = ui
        self.AudioController = AudioController
        self.setObjectName("menuPage")
        self.menuState = 1      # testvariabelen
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

    # vul menu met lijst
    def set_menu_items(self):
        # leegmaken menuItems
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
                # Quick Play
                if self.menuPos == 0:
                    self.UIController.next_page()
                    self.AudioController.quick_play()
                    self.AudioController.set_current_channel(0)
                    self.AudioController.playerType = 0
                    self.UIController.page[2].update_play_stats()
                # menu voor SD mappen
                elif self.menuPos == 1:
                    self.update_dir_menu()
                    self.uiItems0[0] = "Load from SD card"
                    self.UIController.topLabel[0].setText(self.uiItems0[0])

            # speel gekozen SD map, controleer aanwezigheid kaart
            elif self.menuState == 2:
                try:
                    self.AudioController.dir_play(self.menuItems[self.menuPos])
                    self.UIController.next_page()
                    self.AudioController.set_current_channel(0)
                    self.AudioController.playerType = 1
                    self.UIController.page[2].update_play_stats()
                except:
                    self.UIController.page[self.UIController.stackedWidget.currentIndex()].action_button_pushed(3)
                    print("ERROR: No SD card found!!")

        # vorige
        elif btnId == 3:
            if self.menuState == 1:
                self.UIController.previous_page()
            elif self.menuState == 2:
                self.menuItems.clear()
                self.menuItems = ["Quick start", "Load from SD card"]
                self.set_menu_items()
                self.uiItems0[0] = "Main menu"
                self.UIController.topLabel[0].setText(self.uiItems0[0])
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

    # update menu met alle mappen in de SD kaart
    def update_dir_menu(self):
        if self.DEBUG: print("Dirs loading")

        # mount sd-kaart
        try:
            dirList = os.listdir(self.AudioController.SDRoot)
            SD = self.AudioController.SDRoot + "/" + dirList[0]
        except:
            print("ERROR: No SD card found!!")

        # lees sd-kaart uit
        try:
            os.listdir(SD)
        except:
            os.chdir("..")
            try:
                os.listdir(SD)
            except FileNotFoundError:
                os.chdir("..")

        dirNames = []
        for dirs in os.listdir(SD):
            if not dirs.startswith("System Volume"):
                dirNames.append(os.path.join(dirs))

        if self.DEBUG: print(dirNames)

        self.menuState = 2
        self.menuItems = dirNames[0:8]  # stop maar 8 mappen in het menu!
        self.set_menu_items()
        self.menuPos = 0
        self.set_selector()
