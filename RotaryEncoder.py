"""Naam:
Versie:
Beschrijving:

Auteurs:
"""

import UIController
#import RPi.GPIO as GPIO
from PyQt5 import QtCore, QtGui, QtWidgets


class RotaryEncoder(object):
    rot_counter = 0
    new_counter = 0
    curr_A = 1
    curr_B = 1
    DEBUG = True

    def __init__(self, enc_A, enc_B, id, UIController):
        self.enc_A = enc_A  # encoder A pin BCM
        self.enc_B = enc_B  # encoder B pin BCM
        self.id = id  # identificatie nummer van de encoder
        self.UIController = UIController  # UI voor hetaanroepen van functies
        self.setup()
        return

    def setup(self):
        # Stel GPIO in
        GPIO.setup(self.enc_A, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.enc_B, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Zet interrupt trigger
        GPIO.add_event_detect(self.enc_A, GPIO.RISING,
                              callback=lambda AorB: self.rotary_interrupt(self.enc_A))  # NO bouncetime
        GPIO.add_event_detect(self.enc_B, GPIO.RISING,
                              callback=lambda AorB: self.rotary_interrupt(self.enc_B))  # NO bouncetime

        return

    # Rotary encoder interrupt:
    # Dez functie wordt aangeroepen voor zowel A als B
    def rotary_interrupt(self, enc):

        # Lees switches
        self.switch_A = GPIO.input(self.enc_A)
        self.switch_B = GPIO.input(self.enc_B)

        # Zelfde als vorige interrupt(Bouncing)
        if self.curr_A == self.switch_A and self.curr_B == self.switch_B:
            return

        self.curr_A = self.switch_A  # Zet nieuwe waarde voor debounce check
        self.curr_B = self.switch_B

        if self.switch_A and self.switch_B:  # Beide actief klik sequentie is afgelopen
            if enc == self.enc_B:  # Als B eerst triggert gaat hij naar rechts anders links
                self.UIController.page[self.UIController.stackedWidget.currentIndex()].rotary_rotate(self.id, 0)
            else:
                self.UIController.page[self.UIController.stackedWidget.currentIndex()].rotary_rotate(self.id, 1)
        return
