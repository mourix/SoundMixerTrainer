"""Naam:
Versie:
Beschrijving:

Auteurs: Jos van Mourik & Matthijs Daggelders
"""

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


if __name__ == "__main__":
    import sys
    aController = AudioController()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UIController(MainWindow, aController)

    #setup_input_controllers(ui)

    # fullscreen op Raspberry Pi (linux)
    if os.name == "posix":
        MainWindow.showFullScreen()
    else:
        MainWindow.show()

    sys.excepthook = except_hook  # pyqt5 verbergt foutmeldingen, dus vang deze
    sys.exit(app.exec_())
