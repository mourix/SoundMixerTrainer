"""Naam:
Versie:
Beschrijving:

Auteurs:
"""


class Preset(object):
    """
    class voor de preset instellingen van  de equalizer.
    """
    eqBanden = [0,0,0,0,0]
    volume = 100
    preamp = 0
    DEBUG = True

    # Zet de verschillende waardes in de classen bij het aanmaken van een pre-set.
    def __init__(self, eqBanden, volume, preamp, preset_id):
        self.eqBanden = eqBanden
        self.volume = volume
        self.preamp = preamp
        self.id = preset_id

    # Zet de gain voor een bepaalde equalizer band
    def set_eq_band(self, band, gain):
        if (band > 4) or (band < 0):
            if self.DEBUG: print("Preset: band out of range")
        elif (gain > 20) or (gain < -20):
            if self.DEBUG: print("Preset: gain out of range")
        else:
            self.eqBanden[band] = gain
        return

    # Vraag de ingestelde equalizer setting van een bepaalde band.
    def get_eq_band(self, band):
        if (band > 4) or (band < 0):
            if self.DEBUG: print("Preset: band out of range")
            return 0
        else:
            return self.eqBanden[band]

    # Zet de volume op een bepaalde equalizer band.
    def set_volume(self, volume):
        if (volume > 100) or (volume < 0):
            if self.DEBUG: print("Preset: volume out of range")
        else:
            self.volume = volume
        return

    # Return de volume van een bepaalde band.
    def get_volume(self):
            return self.volume

    # Zet de pre-amp op een bepaalde equalizer band.
    def set_amp(self, amp):
        if (amp > 20) or (amp < -20):
            if self.DEBUG: print("Preset: preamp out of range")
        else:
            self.preamp = amp
        return

    # Return de amp van een bepaalde band.
    def get_amp(self):
            return self.preamp

    # Zet de amp op een bepaalde equalizer band.
    def set_id(self, bandId):
        self.id = bandId
        return

    # Return de amp van een bepaalde band.
    def get_id(self):
        return self.id

    # Return het Preset object
    def get_preset(self):
        return self
