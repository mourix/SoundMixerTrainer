"""Naam: Audioplayer.py
Versie:
Beschrijving:

Auteurs: Jos van Mourik
"""

import vlc
from Preset import Preset


class AudioPlayer(object):
    """vlc media player class

    Omvat alle functies en variabelen van de muziekspelers die voor de kanalen gebruikt worden.
    """
    song = ""
    DEBUG = True

    def __init__(self, preset=None):
        # zet speler aan
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.preset = preset

        # zet equalizer aan
        self.equalizer = vlc.libvlc_audio_equalizer_new()
        if (vlc.libvlc_media_player_set_equalizer(self.player, self.equalizer) == 0) and (self.player is not None):
            if self.DEBUG: print("Initialized Player and EQ successfully")

        if preset is not None:
            for i in range(len(self.preset.eqBanden)):
                self.set_eq_band_amp(self.preset.eqBanden[i], i)
                self.set_volume(self.preset.volume)

    # zet nummer in speler
    def set_media(self, s):
        self.song = s

    # speel nummer
    def play_song(self):
        self.player.set_media(self.instance.media_new(self.song))
        self.player.play()

    # pauzeer nummer en zet tijd op 0s
    def stop_song(self):
        if self.get_playback_state() == 3:
            self.player.pause()
            self.set_time(0)
        # self.player.stop() # werkt niet met pi sound devices

    # lees afspeelvolume uit
    def get_volume(self):
        return vlc.libvlc_audio_get_volume(self.player)

    #  stel afspeelvolume in
    def set_volume(self, volume):
        vlc.libvlc_audio_set_volume(self.player, volume)
        if self.DEBUG: print("AudioPlayer: Volume " + str(self.get_volume()))

    # geef een tik aan volume
    def bump_volume(self, direction):
        vol = self.get_volume()

        if direction == 0:
            vol -= 2
            if vol < 0:
                vol = 0

        elif direction == 1:
            vol += 2
            if vol > 100:
                vol = 100

        vlc.libvlc_audio_set_volume(self.player, vol)
        if self.DEBUG: print("AudioPlayer: Volume " + str(self.get_volume()))
        return vol

    # lees nummerlengte uit
    def get_lenght(self):
        return vlc.libvlc_media_player_get_length(self.player)

    # lees afspeeltijd uit
    def get_time(self):
        return vlc.libvlc_media_player_get_time(self.player)

    # stel afspeeltijd in
    def set_time(self, time):
        vlc.libvlc_media_player_set_time(self.player, time)

    # geef lijst van beschikbare afspeelapparaten terug
    def emum_audiodevices(self):
        self.devices = []

        # open linkedlist van apparaten
        self.outputs = vlc.libvlc_audio_output_device_enum(self.player)
        self.output = self.outputs

        # lees linkedlist uit
        while self.output:
            self.output = self.output.contents
            self.devices.append(self.output.device)
            self.output = self.output.next

        # geef linkedlist vrij
        vlc.libvlc_audio_output_device_list_release(self.outputs)
        return self.devices

    # stel afspeelapparaat in
    def set_audiodevice(self, device):
        vlc.libvlc_audio_output_device_set(self.player, None, device)

    # lees equalizer gain uit
    def get_eq_preamp(self):
        return vlc.libvlc_audio_equalizer_get_preamp(self.equalizer)

    #  stel equalizer gain in
    def set_eq_preamp(self, amp):
        vlc.libvlc_audio_equalizer_set_preamp(self.equalizer, amp)
        vlc.libvlc_media_player_set_equalizer(self.player, self.equalizer)
        if self.DEBUG: print("EQ gain " + str(self.get_eq_preamp()) + "dB")

    # geef een tik aan preamp
    def bump_eq_preamp(self, direction):
        preamp = self.get_volume()

        if direction == 0 and preamp > -20:
            preamp -= 1

        elif direction == 1 and preamp < 20:
            preamp += 1

        else:
            if self.DEBUG: print("EQ gain " + str(self.get_eq_preamp()) + "dB")
            return preamp

        vlc.libvlc_audio_equalizer_set_preamp(self.equalizer, preamp)
        vlc.libvlc_media_player_set_equalizer(self.player, self.equalizer)
        if self.DEBUG: print("EQ gain " + str(self.get_eq_preamp()) + "dB")

        return preamp

    # lees EQ-band gain uit
    def get_eq_band_amp(self, band):
        return vlc.libvlc_audio_equalizer_get_amp_at_index(self.equalizer, band * 2)

    #  stel EQ-band gain in
    def set_eq_band_amp(self, amp, band):
        vlc.libvlc_audio_equalizer_set_amp_at_index(self.equalizer, amp, band*2)
        vlc.libvlc_audio_equalizer_set_amp_at_index(self.equalizer, amp, (band*2)+1)
        vlc.libvlc_media_player_set_equalizer(self.player, self.equalizer)
        if self.DEBUG: print("EQ " + str(vlc.libvlc_audio_equalizer_get_band_frequency(band))
              + " Hz " + str(self.get_eq_band_amp(band)) + "dB")

    def get_playback_state(self):
        return vlc.libvlc_media_player_get_state(self.player)

    # geef een tik aan EQ band amp
    def bump_eq_band_amp(self, band, direction):
        bandAmp = self.get_eq_band_amp(band)

        if direction == 0 and bandAmp > -20:
            bandAmp -= 1

        elif direction == 1 and bandAmp < 20:
            bandAmp += 1

        else:
            if self.DEBUG: print("EQ gain " + str(self.get_eq_band_amp(band)) + "dB")
            return bandAmp

        vlc.libvlc_audio_equalizer_set_amp_at_index(self.equalizer, bandAmp, band)
        vlc.libvlc_media_player_set_equalizer(self.player, self.equalizer)
        if self.DEBUG: print("EQ " + str(vlc.libvlc_audio_equalizer_get_band_frequency(band))
              + " Hz " + str(self.get_eq_band_amp(band)) + "dB")

        return bandAmp

    # zet preset op de speler
    def set_preset(self, preset):
        self.preset = preset

        for i in range(len(self.preset.eqBanden)):
            self.set_eq_band_amp(self.preset.eqBanden[i], i)

        #self.set_volume(self.preset.volume)
        return

    # returnt de huidige preset??????
    def get_preset(self):
        return self.preset

    # mute de player
    def toggle_mute(self):
        vlc.libvlc_audio_toggle_mute(self.player)

    # vraag de mutestatus op
    def get_mute(self):
        return vlc.libvlc_audio_get_mute(self.player)
