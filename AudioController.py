"""Naam: AudioController.py
Versie:
Beschrijving:

Auteurs: Jos van Mourik & Matthijs Daggelders
"""
import os
from AudioPlayer import *
import pickle
from Preset import Preset
from random import randint


class AudioController(object):
    """Audio controller classe.

    Omvat alle instellingen en functies van de 8 audiokanalen.
    """
    PIK = "presets.dat"
    DEBUG = True

    def __init__(self):
        self.audioPlayers = []
        self.currentChannel = 0
        self.presets = self.load_presets(self.PIK)

        # maak VLC kanalen aan
        for c in range(8):
            if self.DEBUG: print("Channel " + str(c) + ":")
            self.audioPlayers.append(AudioPlayer(self.presets[0]))

        self.cChannel = self.audioPlayers[self.currentChannel]  # zet huidige kanaal op cCurrent

        # raspberry pi: zet elke speler op een eigen kanaal
        if os.name == "posix":
            # lees alle geluidskanalen uit
            device = self.audioPlayers[0].emum_audiodevices()

            # stel audiokanalen in
            for d in range(8):
                if self.DEBUG: print("Set device: " + str(device[6+d]))
                self.audioPlayers[d].set_audiodevice(device[6+d])

    # zet alle kanalen gelijk aan kanaal 1
    def sync_channels(self,):
        for i in range(7):
            self.audioPlayers[i+1].set_time(self.audioPlayers[0].get_time())
        if self.DEBUG: print("Synced all channels to channel 1")

    def set_channel_song(self, channel, song):
        self.audioPlayers[channel].set_media(song)

    def play_all(self):
        for c in range(8):
            self.audioPlayers[c].play_song()
        if self.DEBUG: print("Playing all")
        #self.sync_channels()

    def stop_all(self):
        if self.DEBUG: print("Stopping all")
        for c in range(8):
            self.audioPlayers[c].stop_song()

    def prev_channel(self):
        if self.currentChannel < 7:
            self.currentChannel += 1
            self.cChannel = self.audioPlayers[self.currentChannel]
        else:
            self.currentChannel = 0
            self.cChannel = self.audioPlayers[self.currentChannel]

    def next_channel(self):
        if self.currentChannel > 0:
            self.currentChannel -= 1
            self.cChannel = self.audioPlayers[self.currentChannel]
        else:
            self.currentChannel = 7
            self.cChannel = self.audioPlayers[self.currentChannel]

    def set_current_channel(self, channel):
        self.currentChannel = channel
        self.cChannel = self.audioPlayers[self.currentChannel]

    def get_current_channel(self):
        return self.currentChannel

    def reset_eq_band(self, band):
        self.audioPlayers[self.currentChannel].set_eq_band_amp(0, band)

    def reset_eq_channel(self, channel):
        for b in range(5):
            self.audioPlayers[channel].set_eq_band_amp(0, b)

    def reset_eq_all(self):
        for c in range(8):
            self.reset_eq_channel(c)

    def load_presets(self, PIK):
        try:
            with open(PIK, "rb") as f:
                if self.DEBUG: print("AudioController presets geladen")
                return pickle.load(f)
        except:
            if self.DEBUG: print("AudioController: Geen presets gevonden")
            return self.create_presets(PIK)

    def save_presets(self, PIK, presets):
        with open(PIK, "wb") as f:
            pickle.dump(presets, f)
            if self.DEBUG: print("AudioController: presets opgeslagen")

    def create_presets(self, PIK):
        eqBanden1 = [0, 0, 0, 0, 0]
        volume = 100
        preamp = 0
        eqBanden2 = [20, 20, 20, 20, 20]
        eqBanden3 = [-20, -20, -20, -20, -20]
        eqBanden4 = [-20, -20, 0, 20, 20]
        eqBanden5 = [20, 20, 0, -20, -20]
        eqBanden6 = [0, 0, 0, 0, 0]

        presets = []
        presets.append(Preset(eqBanden1, volume, preamp, 1))
        presets.append(Preset(eqBanden2, volume, preamp, 2))
        presets.append(Preset(eqBanden3, volume, preamp, 3))
        presets.append(Preset(eqBanden4, volume, preamp, 4))
        presets.append(Preset(eqBanden5, volume, preamp, 5))
        presets.append(Preset(eqBanden6, volume, preamp, 6))

        if self.DEBUG: print("presets zijn aangemaakt")
        self.save_presets(PIK, presets)
        return presets

    def set_channel_preset(self, id):
        self.cChannel.set_preset(self.presets[id])

    def get_channel_preset(self, channel):
        #return preset
        pass

    def set_random_preset(self):
        banden = [0, 0, 0, 0, 0]
        volume = randint(0, 100)
        preamp = 0

        if self.DEBUG: print(randint(-20, 20))

        for i in range(5):
            banden[i] = randint(-20, 20)

        self.presets[5] = Preset(banden, volume, preamp, 6)

        self.set_channel_preset(5)

    def quick_play(self):
        """Quickplay

        Laad alle nummers uit de QuickPlay amp in.
        """

        if self.DEBUG: print("Quick Play initializing")
        files = []

        try:
            try:
                if not os.getcwd().endswith("QuickPlay"):
                    os.chdir("QuickPlay")

            except:
                os.chdir("..")
                os.chdir("..")
                if not os.getcwd().endswith("QuickPlay"):
                    os.chdir("QuickPlay")

            for filename in os.listdir('.'):
                if filename.endswith(".mp3") or filename.endswith(".wav"):
                    files.append(filename)

            for c in range(8):
                self.set_channel_song(c, files[c])
                if self.DEBUG: print("Channel " + str(c) + ": " + files[c])

        except:
            if self.DEBUG: print("QuickPlay ERROR: Can't find path. No songs have been loaded.")

    # laadt de eerste 8 nummers uit een map. test code
    def dir_play(self, playDir):
        files = []
        files.clear()

        try:
            if not os.getcwd().endswith("SDMap"):
                os.chdir("SDMap")
                os.chdir(playDir)
                if self.DEBUG: print("a")
        except:
            os.chdir("..")
            os.chdir("..")
            try:
                if not os.getcwd().endswith("SDMap"):
                    os.chdir("SDMap")
                    os.chdir(playDir)
                    if self.DEBUG: print("b")
            except:
                if self.DEBUG: print("dir_play: foute bestandslocatie")

        for filename in os.listdir("."):
            if filename.endswith(".mp3") or filename.endswith(".wav"):
                files.append(filename)

        for c in range(8):
            try:
                self.set_channel_song(c, files[c])
                if self.DEBUG: print("Channel " + str(c) + ": " + files[c])
            except:
                if self.DEBUG: print("dir_play: fout in het laden van de bestanden")

    def play_last(self, audioPlayersLast):
        pass

    def save_last_played(self, audioPlayersLast):
        pass

    def load_last_played(self):
        #return audioPlayersLast
        pass
