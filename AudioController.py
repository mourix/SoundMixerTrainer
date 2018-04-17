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
from PyQt5 import QtTest


class AudioController(object):
    """Audio controller classe.

    Omvat alle instellingen en functies van de 8 audiokanalen.
    """
    PIK = "presets.dat"
    PIK2 = "8chpreset.dat"
    playerType = 0
    if os.name == "posix":
        ROOT = "/home/pi/SoundMixerTrainer"
        QUICK = "/home/pi/QuickPlay"
        SDRoot = "/media/pi"
    else:
        #ROOT = "C:/SoundMixerTrainer"
        #QUICK = "C:/SoundMixerTrainer/QuickPlay"
        #SDRoot = "C:/SoundMixerTrainer/SD"
        ROOT = "C:/Users/M/Documents/GitHub/SoundMixerTrainer"
        QUICK = "C:/Users/M/Documents/GitHub/SoundMixerTrainer/Quickplay"
        SDRoot = "C:/Users/M/Documents/GitHub/SoundMixerTrainer/SDMap"
    DEBUG = True

    def __init__(self):
        self.audioPlayers = []
        self.currentChannelIndex = 0
        self.channelAmount = 8
        self.presets = self.load_presets(self.PIK)
        self.multiChannelPresets = self.load_presets(self.PIK2)
        os.chdir(self.ROOT)  # open de SD kaart

        # maak VLC kanalen aan
        for c in range(8):
            if self.DEBUG: print("Channel " + str(c) + ":")
            self.audioPlayers.append(AudioPlayer(self.presets[0]))

        self.currentChannel = self.audioPlayers[self.currentChannelIndex]  # zet huidige kanaal op currentChannel

        # raspberry pi: zet elke speler op een eigen kanaal van de 7.1 USB sound card
        if os.name == "posix":
            # lees alle geluidskanalen uit
            device = self.audioPlayers[0].emum_audiodevices()

            # stel audiokanalen in
            # Indien de geluidskaart MET HDMI wordt gebruike, beginnen de MONO channels op ID 6
            # Indien de geluidskaart ZONDER HDMI wordt gebruike, beginnen de MONO channels op ID 7
            for d in range(8):
                if self.DEBUG: print("Set device: " + str(device[7+d]))
                self.audioPlayers[d].set_audiodevice(device[7+d])

    # zet alle kanalen gelijk aan kanaal 1, of een gekozen tijd
    def sync_channels(self, setTime=None):
        if setTime is not None:
            self.audioPlayers[0].set_time(setTime)
            if self.DEBUG: print("Set time for channel 1")

        a = self.audioPlayers[0].get_time()

        QtTest.QTest.qWait(300)
        for i in range(self.channelAmount):
            self.audioPlayers[i].set_time(a)

        if self.DEBUG: print("Synced channel " + str(i + 2) + " to channel 1")
        if self.DEBUG: print("Synced all channels to channel 1")

    # laad een nummer in een audiospeller
    def set_channel_song(self, channel, song):
        self.audioPlayers[channel].set_media(song)

    # zet alle kanalen op afspelen en synchroniseer
    def play_all(self):
        for c in range(self.channelAmount):
            self.audioPlayers[c].play_song()
        if self.DEBUG: print("Playing all")
        #QtTest.QTest.qWait(200)
        #self.sync_channels()

    # stop alle kanalen
    def stop_all(self):
        for c in range(self.channelAmount):
            self.audioPlayers[c].stop_song()
        if self.DEBUG: print("Stopping all")

    # pauzeer alle kanalen of speel af
    def toggle_pause_all(self):
        if self.audioPlayers[0].get_playback_state() != 6:
            for c in range(self.channelAmount):
                self.audioPlayers[c].toggle_pause()
        else:
            self.play_all()
            self.sync_channels()
            if self.DEBUG: print("Replaying all")
        QtTest.QTest.qWait(300)

    # open volgende kanaal in menu
    def prev_channel(self):
        if self.currentChannelIndex < (self.channelAmount-1):
            self.currentChannelIndex += 1
            self.currentChannel = self.audioPlayers[self.currentChannelIndex]
        else:
            self.currentChannelIndex = 0
            self.currentChannel = self.audioPlayers[self.currentChannelIndex]

    # open vorige kanaal in menu
    def next_channel(self):
        if self.currentChannelIndex > 0:
            self.currentChannelIndex -= 1
            self.currentChannel = self.audioPlayers[self.currentChannelIndex]
        else:
            self.currentChannelIndex = (self.channelAmount-1)
            self.currentChannel = self.audioPlayers[self.currentChannelIndex]

    # kies kanaal in menu
    def set_current_channel(self, channel):
        self.currentChannelIndex = channel
        self.currentChannel = self.audioPlayers[self.currentChannelIndex]

    # geef huidige kanaal terug
    def get_current_channel(self):
        return self.currentChannelIndex

    # zet een EQ band op 0dB
    def reset_eq_band(self, band):
        self.audioPlayers[self.currentChannelIndex].set_eq_band_amp(0, band)

    # zet alle EQ banden van een kanaal op 0dB
    def reset_eq_channel(self, channel):
        for b in range(5):
            self.audioPlayers[channel].set_eq_band_amp(0, b)

    # zet alle EQ banden in de speler op 0dB
    def reset_eq_all(self):
        for c in range(self.channelAmount):
            self.reset_eq_channel(c)

    # zoek preset file, of maak deze aan
    def load_presets(self, PIK):
        try:
            with open(PIK, "rb") as f:
                if self.DEBUG: print("AudioController presets geladen")
                return pickle.load(f)
        except FileNotFoundError:
            if self.DEBUG: print("AudioController: Geen presets gevonden")
            if PIK == self.PIK:
                return self.create_presets(PIK)
            else:
                return self.create_8ch_presets(PIK)

    # sla presets op in file
    def save_presets(self, PIK, presets):
        prevPath = 0
        if os.getcwd() == self.QUICK:
            prevPath = os.getcwd()
        elif os.getcwd() != self.ROOT:
            prevPath = os.getcwd()

        # aanpassen aan de dir die gevolgd moet worden
        os.chdir(self.ROOT)

        with open(PIK, "wb") as f:
            pickle.dump(presets, f)
            if self.DEBUG: print("AudioController: presets opgeslagen")

        if prevPath != 0:
            os.chdir(prevPath)

    # maak een preset file aan met voorgekozen standen
    def create_presets(self, PIK):
        volume = 100
        preamp = 0
        eqBanden1 = [0, 0, 0, 0, 0]
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

        if self.DEBUG: print("Presets zijn aangemaakt")
        self.save_presets(PIK, presets)
        return presets

    # maak een 8-kanaals preset aan
    def create_8ch_presets(self, PIK):
        multiChannelPreset = []
        multiChannelPresets = []

        for i in range(8):
            multiChannelPreset.append(self.presets[0])

        for j in range (10):
            multiChannelPresets.append(multiChannelPreset)

        self.save_presets(PIK, multiChannelPresets)

        return multiChannelPresets

    # sla een 8-kanaals preset op
    def save_8ch_presets(self, index):
        multiChannelPreset = []

        for i in range(self.channelAmount):
            multiChannelPreset.append(self.audioPlayers[i].get_preset())

        self.multiChannelPresets[index] = multiChannelPreset

        self.save_presets(self.PIK2, self.multiChannelPresets)

    def load_8ch_presets(self, index):
        try:
            for i in range(self.channelAmount):
                self.audioPlayers[i].set_preset(self.multiChannelPresets[index][i])
        except IndexError:
            print("ERROR: Preset does not exist")

    def set_channel_preset(self, id):
        self.currentChannel.set_preset(self.presets[id])

    def get_channel_preset(self, channel):
        #return preset
        pass

    # vul de frequentiebanden met willekeurige waarden
    def set_random_preset(self):
        banden = [0, 0, 0, 0, 0]
        volume = randint(0, 100)
        preamp = 0

        if self.DEBUG: print(randint(-20, 20))

        for i in range(5):
            banden[i] = randint(-20, 20)

        self.presets[5] = Preset(banden, volume, preamp, 6)
        self.set_channel_preset(5)

    # laad de alle nummers uit de quickplay map
    def quick_play(self):
        """Quickplay

        Laad alle nummers uit de QuickPlay map in.
        """

        if self.DEBUG: print("Quick Play initializing")
        files = []

        # open Quickplay map
        try:
            if not os.getcwd().endswith("QuickPlay"):
                os.chdir(self.QUICK)

            for filename in os.listdir('.'):
                if filename.endswith(".mp3") or filename.endswith(".wav"):
                    files.append(filename)

            self.stop_all()
            self.channelAmount = len(files)

            for c in range(self.channelAmount):
                self.set_channel_song(c, files[c])
                if self.DEBUG: print("Channel " + str(c+1) + ": " + files[c])

            self.play_all()

        except FileNotFoundError:
            if self.DEBUG: print("QuickPlay ERROR: Can't find path. No songs have been loaded.")

    # laad de eerste 8 nummers uit een map
    def dir_play(self, playDir):
        """Dirplay

        Laad alle nummers uit de gekozen map in.
        """
        files = []
        files.clear()

        # zoek naar SD-kaart
        dirList = os.listdir(self.SDRoot)
        SD = self.SDRoot + "/" + dirList[0]
        os.chdir(SD)
        os.chdir(playDir)

        # laad nummers lijst
        for filename in os.listdir("."):
            if filename.endswith(".mp3") or filename.endswith(".wav"):
                files.append(filename)

        self.stop_all()
        self.channelAmount = len(files)

        for c in range(self.channelAmount):
            try:
                self.set_channel_song(c, files[c])
                if self.DEBUG: print("Channel " + str(c+1) + ": " + files[c])
            except:
                if self.DEBUG: print("dir_play: fout in het laden van de bestanden")

        self.play_all()
