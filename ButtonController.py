"""Naam:
Versie:
Beschrijving:

Auteurs:
"""

import UIController
#import RPi.GPIO as GPIO


class ButtonController(object):
    
    DEBUG = True
    
    def __init__(self, i2cIO, UIController, intA, intB, btnId):
        self.currVal = 255
        self.mcp = i2cIO
        self.UIController = UIController
        self.intA = intA
        self.intB = intB
        self.id = btnId

        # zet mcp2 port directie naar output
        self.mcp.set_port_dir(0,0xff)
        self.mcp.set_port_dir(1, 0xff)

        # pull-up resistors zodat input laag getrokkenm wordt
        self.mcp.set_port_pullups(0, 0xff)
        self.mcp.set_port_pullups(1, 0xff)

        # zet interrupt op 0 = onchange
        self.mcp.set_interrupt_type(0, 0x00)
        self.mcp.set_interrupt_type(1, 0x00)

        # zet de interrupt vergelijk register
        self.mcp.set_interrupt_defaults(0, 0xff)
        self.mcp.set_interrupt_defaults(1, 0xff)

        # zet de interrupts aan op alle pins
        self.mcp.set_interrupt_on_port(0, 0xff)
        self.mcp.set_interrupt_on_port(1, 0xff)

        GPIO.setup(self.intA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.intB, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(self.intA, GPIO.FALLING,
                              callback=lambda AorB: self.onkeypressed(0))
        GPIO.add_event_detect(self.intB, GPIO.FALLING,
                              callback=lambda AorB: self.onkeypressed(1))

        # reset interrupts voor de start van het programma
        self.mcp.reset_interrupts()

    # Interrupt op een van de interrupt pinnen 19, 16
    def onkeypressed(self, port):
        value = self.mcp.read_interrupt_capture(port)
        # simpele debounce voor nul meting.
        # alleen triggeren als de nieuwe waarde lager is dan de vorige
        # Hierdoor wordt het loslaten van een knop niet als verandering gezien
        if (value < self.currVal):
            # bepaal welke bit er is getriggert
            for i in range(8):
                if self.mcp.checkbit(value, i) != self.mcp.checkbit(self.currVal, i):
                    if self.DEBUG: print(self.mcp.get_name, "port: ", port, "bit: ", i+1)
                    self.output(port, i)
        self.currVal = value
        return

    def output(self, port, bit):
        self.UIController.button_pressed(self.id, port, bit)
        return
