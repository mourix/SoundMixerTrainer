"""Naam: IOExpander.py
Versie:
Beschrijving:

Auteurs: Matthijs Daggelders
"""


class IOExpander(object):
    # MCP23017 IO-expander.
    # Er worden 3 bytes uitgestuurd 0x00 0x00 0x00.
    # De eerste byte is het slave adress.
    # De tweede byte is fucntie selectie.
    # De derde byte is pin selectie.

    DEBUG = True

    # Registerwaardes datasheet MCP23017.
    dirA = 0x00  # IO dir A  0x00 0x00 = output, 0x00 0xff = input.
    dirB = 0x01  # IO dir B.
    polA = 0x02  # Polariteit van GPIOA register.
    polB = 0x03  # Polariteit van GPIOB register.
    intA = 0x04  # Zet de interrupt mogelijkheden van elke pin van register A.
    intB = 0x05  # Zet de interrupt mogelijkheden van elke pin van register B.
    intValA = 0x06  # Reg. A. Zet de standaard interrupt waarde. Als de pin waarde anders is.
    intValB = 0x07  # Reg. B. Zet de standaard interrupt waarde. Als de pin waarde anders is.
    intConA = 0x08  # Reg. A. Interrupt control. 1 = zelfde,  0 = bij verandering.
    intConB = 0x09  # Reg. B. Interrupt control. 1 = zelfde,  0 = bij verandering.
    pullA = 0x0C  # Reg. A. zet 100k ohm pull-up resistor.
    pullB = 0x0D  # Reg. B. Zet 100k ohm pull-up resistor.
    INTFA = 0x0E  # Reg. A. reflecteerd de  interrupt conditie op de geven pinnen van Reg. A.
    INTFB = 0x0F  # Reg. B. reflecteerd de  interrupt conditie op de geven pinnen van Reg. A.
    INTCAPA = 0x10  # Reg. A. pakt de GPIOA waarden bij een interrupt.
    INTCAPB = 0x11  # Reg. B. pakt de GPIOA waarden bij een interrupt.
    GPIOA = 0x12  # Reg. A. Zet input.
    GPIOB = 0x13  # Reg. B. Zet input.

    # Variabelen
    # Maak byte array voor elke port
    # IO van A en B 1 = input, 0 = output
    portDirA = 0x00
    portDirB = 0x00
    # Waarde van de verschillende IO
    portValA = 0x00
    portValB = 0x00
    # Puul-up voor de verschillende output
    portPullA = 0x00
    portPullB = 0x00
    # Polariteit van de verschillende IO
    portPolA = 0x00
    portPolB = 0x00
    # interupt control voor de verschillende input
    portIntA = 0x00
    portIntB = 0x00

    def __init__(self, address, bus, name):
        self.address = address
        self.bus = bus
        self.name = name
        return

    # Zet een enkele bit in een byte
    @staticmethod
    def setbit(byte, bit, value):
        mask = 1 << bit
        if value == 0:
            return byte & ~mask
        elif value == 1:
            return byte | mask

    # zoekte de waarde van een enkele bit in een "byte"
    @staticmethod
    def checkbit(bite, bit):
        bt = bytes([0x00])
        bt = bite

        value = 0
        mask = 1 << bit
        if bt & mask:
            value = 1
        return value

    def get_name(self):
        return self.name

    # Zet de directie van een bit. bit = A0-A7 = 1-8, B0-B7 = 9-16, value = 1 = input, 0 = output
    def set_pin_dir(self, pin, value):
        int = pin - 1
        if int < 8:
            self.portDirA = self.setbit(self.portDirA, int, value)
            self.bus.write_byte_data(self.address, self.dirA, self.portDirA)
        elif int > 7:
            int -= 8
            self.portDirB = self.setbit(self.portDirB, int, value)
            self.bus.write_byte_data(self.address, self.dirB, self.portDirB)
        return

    # Zet de directie van een port 0 = A, 1 = B. value 1 = input, 0 = output.
    def set_port_dir(self, port, value):
        if port == 1:
            self.portDirB = value
            self.bus.write_byte_data(self.address, self.dirB, self.portDirB)
        elif port == 0:
            self.portDirA = value
            self.bus.write_byte_data(self.address, self.dirA, self.portDirA)
        return

    # Zet pull-up resistor voor enkele pin 1-8 = A, 9-16 =B
    def set_pin_pullup(self, pin, value):
        int = pin - 1
        if int < 8:
            self.portPullA = self.setbit(self.portPullA, int, value)
            self.bus.write_byte_data(self.address, self.pullA, self.portPullA)
        elif int > 7:
            int -= 8
            self.portPullA = self.setbit(self.portPullB, int, value)
            self.bus.write_byte_data(self.address, self.pullB, self.portPullB)
        return

    # Zet pull-up resistor voor hele port 0 = A, 1 = B
    def set_port_pullups(self, port, value):
        if port == 1:
            self.portPullB = value
            self.bus.write_byte_data(self.address, self.pullB, self.portPullB)
        elif port == 0:
            self.portPullB = value
            self.bus.write_byte_data(self.address, self.pullA, value)
        return

    # schrijf naar een enkele pin pin 1-8 = A, 9-16 =B
    def write_pin(self, pin, value):
        int = pin - 1
        if int < 8:
            self.portValA = self.setbit(self.portValA, int, value)
            self.bus.write_byte_data(self.address, self.GPIOA, self.portValA)
        elif int > 7:
            int -= 8
            self.portValB = self.setbit(self.portValB, int, value)
            self.bus.write_byte_data(self.address, self.GPIOB, self.portValB)
        return

    # schrijf naar hele port 0 = A, 1 = B
    def write_port(self, port, value):
        if port == 1:
            self.portValB = value
            self.bus.write_byte_data(self.address, self.GPIOB, self.portValB)
        elif port == 0:
            self.portValA = value
            self.bus.write_byte_data(self.address, self.GPIOA, self.portValB)
        return

    # Lees enkele pin. 1-8 = A, 9-16 =B
    def read_pin(self, pin):
        value = 0
        int = pin - 1
        if int < 8:
            self.portValA = self.bus.read_byte_data(self.address, self.GPIOA)
            value = self.checkbit(self.portValA, int)
        elif int > 7:
            int -= 8
            self.portValB = self.bus.read_byte_data(self.address, self.GPIOB)
            value = self.checkbit(self.portValB, int)
        return value

    # Lees hele port. 0 = A, 1 = B
    def read_port(self, port):
        value = 0
        if port == 1:
            self.portValB = self.bus.read_byte_data(self.address, self.GPIOB)
            value = self.portValB
        elif port == 0:
            self.portValA = self.bus.read_byte_data(self.address, self.GPIOA)
            value = self.portValA
        return value

    # zet type interrupt 1 = zelfde als register, 0 = onchange
    def set_interrupt_type(self, port, value):
        if port == 0:
            self.bus.write_byte_data(self.address, self.intConA, value)
        elif port == 1:
            self.bus.write_byte_data(self.address, self.intConB, value)
        return

    # zet de vergelijkwaardes voor de interrupt
    def set_interrupt_defaults(self, port, value):
        if port == 0:
            self.portIntA = value
            self.bus.write_byte_data(self.address, self.intValA, self.portIntA)
        elif port == 1:
            self.portIntB = value
            self.bus.write_byte_data(self.address, self.intValA, self.portValB)
        return

    # zet interrupt voor de hele port 0 = A, 1 = B
    def set_interrupt_on_port(self, port, value):

        if port == 0:
            self.bus.write_byte_data(self.address, self.intA, value)
            self.portIntA = value
        elif port == 1:
            self.bus.write_byte_data(self.address, self.intB, value)
            self.portIntB = value
        return

    # zet interrupt voor enekel pin,
    def set_interrupt_on_pin(self, pin, value):
        int = pin - 1
        if int < 8:
            self.portIntA = self.setbit(self.portIntA, pin, value)
            self.bus.write_byte_data(self.address, self.intA, self.portIntA)
        elif int > 7:
            int -= 8
            self.portIntB = self.setbit(self.portIntB, int, value)
            self.bus.write_byte_data(self.address, self.intB, self.portIntB)
        return

    # Lees de waardes op het moment van de interrupt
    def read_interrupt_capture(self, port):
        value = 0
        if port == 0:
            value = self.bus.read_byte_data(self.address, self.INTCAPA)
        else:
            value = self.bus.read_byte_data(self.address, self.INTCAPB)
        return value

    # Reset interrupts door ze uit te lezen
    def reset_interrupts(self):
        self.read_interrupt_capture(0)
        self.read_interrupt_capture(1)
        return
