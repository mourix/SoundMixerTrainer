"""Naam: App.py
Versie:
Beschrijving:

Auteurs: Jos van Mourik & Matthijs Daggelders
"""
from random import randint
from PyQt5 import QtTest
import os
from UIController import *
from AudioController import AudioController
from RotaryEncoder import RotaryEncoder
from ButtonController import ButtonController
from IOExpander import IOExpander
#import RPi.GPIO as GPIO
#import smbus


def except_hook(type, value, tback):
    # Vang foutmeldingen voordat app afsluit en geef deze weer
    sys.__excepthook__(type, value, tback)


def setup_input_controllers(ui):
    intA1 = 19
    intB1 = 26  # interrupts voor 2 ontbreken
    intA2 = 16
    intB2 = 20

    # Zet GPIO
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)  # Gebruik BCM voor GPIO nummering

    bus = smbus.SMBus(1)
    mcp1 = IOExpander(0x20, bus, "input")
    mcp2 = IOExpander(0x24, bus, "input")

    ButtonController(mcp1, ui, intA1, intB1, 0)
    ButtonController(mcp2, ui, intA2, intB2, 1)

    # Setup rotary encoders
    rotaryencoders = []
    rotaryencoders.append(RotaryEncoder(4, 14, 0, ui))
    rotaryencoders.append(RotaryEncoder(17, 15, 1, ui))
    rotaryencoders.append(RotaryEncoder(27, 18, 2, ui))
    rotaryencoders.append(RotaryEncoder(22, 23, 3, ui))
    rotaryencoders.append(RotaryEncoder(5, 24, 4, ui))
    rotaryencoders.append(RotaryEncoder(6, 25, 5, ui))


# DEBUG: open Quickplay
def debug_quickplay():
    while ui.stackedWidget.currentIndex() != 0:  # introscherm
        ui.page[ui.stackedWidget.currentIndex()].action_button_pushed(3)

    for j in range(2):
        ui.page[ui.stackedWidget.currentIndex()].action_button_pushed(4)
        QtTest.QTest.qWait(300)
        if ui.stackedWidget.currentIndex() == 2 and os.getcwd().endswith("QuickPlay") and aController.audioPlayers[0].get_playback_state() == 3:
            print("DEBUG: QUICKPLAY PASS")
        else:
            print("DEBUG: ERROR OPENING QUICKPLAY")


# DEBUG: open alle folders
def debug_folders():
    for folders in range(3):
        while ui.stackedWidget.currentIndex() != 0:# introscherm
            ui.page[ui.stackedWidget.currentIndex()].action_button_pushed(3)
            QtTest.QTest.qWait(200)
        ui.page[ui.stackedWidget.currentIndex()].action_button_pushed(4)  # menuscherm
        QtTest.QTest.qWait(200)
        ui.page[ui.stackedWidget.currentIndex()].action_button_pushed(1)  # pijl omlaag
        QtTest.QTest.qWait(200)
        ui.page[ui.stackedWidget.currentIndex()].action_button_pushed(4)  # folder menu
        QtTest.QTest.qWait(200)
        for steps in range(folders):  # scroll door alle mappen
            ui.page[ui.stackedWidget.currentIndex()].action_button_pushed(0)
            QtTest.QTest.qWait(200)
        ui.page[ui.stackedWidget.currentIndex()].action_button_pushed(4) # press play
        QtTest.QTest.qWait(200)
        if ui.stackedWidget.currentIndex() == 2 and not os.getcwd().endswith("QuickPlay") and aController.audioPlayers[0].get_playback_state() == 3:
            print("DEBUG: FOLDER " + os.getcwd()  + " PASS")
        else:
            print("DEBUG: ERROR OPENING FOLDER")


# DEBUG: open alle kanalen, pas alle presets toe, reset alle presets
def debug_all_playback_options():
    for i in range(8):  # kanalen
        ui.page[2].channel_button_pushed(i)
        print("DEBUG: SETTING CHANNEL " + str(i+1))
        if aController.currentChannelIndex == i:
            print("DEBUG: CHANNEL" + str(i+1) + " SET PASS")
        elif aController.currentChannelIndex != i and i < (aController.channelAmount-1):
            print("DEBUG: ERROR SETTING CHANNEL" + str(i+1))

        for j in range(6):  # presets
            ui.page[2].preset_button_pushed(j)
            QtTest.QTest.qWait(100)

        for k in range(6):  # EQ
            ui.page[2].rotary_button_pushed(k)
            QtTest.QTest.qWait(50)
        ui.page[2].rotary_button_pushed(5)

        print("DEBUG: PLAYING, STOPPING, STOPPING PASS TESTING")
        for l in range(2):  # test afspelen, pauzeren en stoppen
            ui.page[2].action_button_pushed(4) # play
            QtTest.QTest.qWait(100)
            ui.page[2].action_button_pushed(4) # play
            QtTest.QTest.qWait(100)
            ui.page[2].action_button_pushed(4)  # stop
            QtTest.QTest.qWait(100)
            ui.page[2].action_button_pushed(4) # play
            QtTest.QTest.qWait(100)
        if aController.audioPlayers[0].get_playback_state() == 3:
            print("DEBUG: PLAYING, STOPPING, STOPPING PASS")
        else:
            print("DEBUG: ERROR PLAYING, STOPPING, STOPPING")

        print("DEBUG: SYNC TEST")
        for i in range(6):  # open time menu en druk driemaal op sync
            ui.page[2].action_button_pushed(0)
            QtTest.QTest.qWait(100)
        if aController.audioPlayers[0].get_playback_state() == 3:
            print("DEBUG: SYNC PASS")
        else:
            print("DEBUG: ERROR SYNC FAILED")

        print("DEBUG: PRESET TEST")
        for i in range(3):
            ui.page[2].action_button_pushed(1)  # open preset menu
            QtTest.QTest.qWait(100)
            ui.page[2].action_button_pushed(i)  # alle 3 de opties
            QtTest.QTest.qWait(100)
            ui.page[2].action_button_pushed(2)  # select
            QtTest.QTest.qWait(100)

        print("DEBUG: REPEAT TEST")
        for i in range(6):
            ui.page[2].action_button_pushed(2)
            QtTest.QTest.qWait(100)

    QtTest.QTest.qWait(2000)


# DEBUG: druk op willekeurige toetsen
def debug_random_input(times):
    print("DEBUG RANDOM FOR " + str(times) + " TIMES")
    for i in range(times):
        fId = randint(0, 4)
        if fId == 0:
            ui.page[2].action_button_pushed(randint(0, 6))
        elif fId == 1:
            ui.page[2].channel_button_pushed(randint(0, 7))
        elif fId == 2:
            ui.page[2].preset_button_pushed(randint(0,5))
        elif fId == 3:
            ui.page[2].rotary_button_pushed(randint(0, 5))
        QtTest.QTest.qWait(100)
    print("DEBUG RANDOM: FINISHED")


if __name__ == "__main__":
    import sys
    aController = AudioController()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UIController(MainWindow, aController)

    # fullscreen op Raspberry Pi (linux)
    if os.name == "posix":
        MainWindow.showFullScreen()
        setup_input_controllers(ui)
    else:
        MainWindow.show()

    #debug_quickplay()
    #debug_folders()
    #debug_random_input(100)
    #debug_all_playback_options()

    sys.excepthook = except_hook  # pyqt5 verbergt foutmeldingen, dus vang deze
    sys.exit(app.exec_())
