"""Naam: PlayPage.py
Versie:
Beschrijving:

Auteurs: Jos van Mourik (& Matthijs Daggelders)
"""

from PyQt5 import QtCore, QtGui, QtWidgets


class PlayPage(QtWidgets.QWidget):
    """Afspeelpagina klasse.

    Initialiseerd de afspeelpagina en update de schruifknoppen.
    """

    uiItems0 = ["", "", "Time Options", "Presets", "Repeat", "Back"]
    uiItems1 = ["", "", "Re sync", "Set time", "", "Back"]
    uiItems = []
    uiItems.append(uiItems0)
    uiItems.append(uiItems1)

    taskbarItems0 = ["Time: 0:00", "Repeat: off", "Preset: -"]
    taskbarItems1 = ["1: Re sync", "2: Set time", ""]
    taskbarItems = []
    taskbarItems.append(taskbarItems0)
    taskbarItems.append(taskbarItems1)

    menuState = 0
    repeat = 0
    DEBUG = True

    def __init__(self, ui, AudioController):
        super().__init__()
        self.UIController = ui
        self.AudioController = AudioController
        self.setObjectName("playPage")
        font = QtGui.QFont("Arial", 12, QtGui.QFont.Bold)

        # maak onderbalk lijn
        self.setObjectName("playPage")
        self.bottomLine = QtWidgets.QFrame(self)
        self.bottomLine.setGeometry(QtCore.QRect(0, 220, 480, 3))
        self.bottomLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.bottomLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.bottomLine.setObjectName("bottomLine")

        # maak onderbalk
        self.bottomLabel = [0 for i in range(3)]
        for i in range(3):
            self.bottomLabel[i] = QtWidgets.QLabel(self)
            self.bottomLabel[i].setFont(font)
            self.bottomLabel[i].setObjectName("bottomLabel_" + str(i))
        self.bottomLabel[0].setGeometry(QtCore.QRect(10, 220, 155, 30))
        self.bottomLabel[1].setGeometry(QtCore.QRect(165, 220, 150, 30))
        self.bottomLabel[1].setAlignment(QtCore.Qt.AlignCenter)
        self.bottomLabel[2].setGeometry(QtCore.QRect(315, 220, 155, 30))
        self.bottomLabel[2].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)

        # maak EQ sliders
        self.eqSlider = [0 for i in range(5)]
        for i in range(5):
            def make_lambda(j): return lambda s: self.eq_changed(j, self.eqSlider[j].value())
            self.eqSlider[i] = QtWidgets.QSlider(self)
            self.eqSlider[i].setGeometry(QtCore.QRect(40 + (i * 70), 20, 22, 170))
            self.eqSlider[i].setMinimum(-20)
            self.eqSlider[i].setMaximum(20)
            self.eqSlider[i].setOrientation(QtCore.Qt.Vertical)
            self.eqSlider[i].setObjectName("eqSlider_" + str(i))
            self.eqSlider[i].valueChanged.connect(make_lambda(i))

        # maak volume slider
        self.volSlider = QtWidgets.QSlider(self)
        self.volSlider.setGeometry(QtCore.QRect(410, 20, 22, 170))
        self.volSlider.setMinimum(0)
        self.volSlider.setMaximum(100)
        self.volSlider.setValue(100)
        self.volSlider.setOrientation(QtCore.Qt.Vertical)
        self.volSlider.setObjectName("volSlider")
        self.volSlider.valueChanged.connect(lambda: self.volume_changed(self.volSlider.value()))

        font = QtGui.QFont("Arial", 12)

        # maak slider labels boven
        self.eqAmpLabel = [0 for i in range(5)]
        for i in range(5):
            self.eqAmpLabel[i] = QtWidgets.QLabel(self)
            self.eqAmpLabel[i].setGeometry(QtCore.QRect(30 + (i * 70), 0, 41, 16))
            self.eqAmpLabel[i].setFont(font)
            self.eqAmpLabel[i].setAlignment(QtCore.Qt.AlignCenter)
            self.eqAmpLabel[i].setObjectName("eqAmpLabel_" + str(i))

        self.volLabel = QtWidgets.QLabel(self)
        self.volLabel.setGeometry(QtCore.QRect(400, 0, 41, 16))
        self.volLabel.setFont(font)
        self.volLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.volLabel.setObjectName("volLabel")

        # maak slider labels onder
        self.eqFreqLabel = [0 for i in range(6)]
        for i in range(5):
            self.eqFreqLabel[i] = QtWidgets.QLabel(self)
            self.eqFreqLabel[i].setGeometry(QtCore.QRect(20 + (i * 70), 190, 61, 16))
            self.eqFreqLabel[i].setFont(font)
            self.eqFreqLabel[i].setAlignment(QtCore.Qt.AlignCenter)
            self.eqFreqLabel[i].setObjectName("eqFreqLabel_" + str(i))
        self.eqFreqLabel[5] = QtWidgets.QLabel(self)
        self.eqFreqLabel[5].setGeometry(QtCore.QRect(390, 190, 61, 16))
        self.eqFreqLabel[5].setFont(font)
        self.eqFreqLabel[5].setAlignment(QtCore.Qt.AlignCenter)
        self.eqFreqLabel[5].setObjectName("eqFreqLabel_5")

        # update legenda
        for i in range(5):
            self.eqAmpLabel[i].setText("0dB")
        self.volLabel.setText("100")
        self.eqFreqLabel[0].setText("170Hz")
        self.eqFreqLabel[1].setText("600Hz")
        self.eqFreqLabel[2].setText("3kHz")
        self.eqFreqLabel[3].setText("12kHz")
        self.eqFreqLabel[4].setText("16kHz")
        self.eqFreqLabel[5].setText("Volume")

        # update onderbalk
        for i in range(3):
            self.bottomLabel[i].setText(self.taskbarItems0[i])

        # timer voor afspeeltijd en repeat
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(900)

    # zet milliseconden om naar tijdsformaat string
    def ms_to_time_string(self, ms):
        totalSecs = int(ms/1000)
        minStr = str(int(totalSecs / 60))
        leftSecs = totalSecs % 60

        if leftSecs < 10:
            secStr = "0" + str(leftSecs)
        else:
            secStr = str(leftSecs)

        return minStr + ":" + secStr

    # update afspeeltijd en repeat
    def update_timer(self):
        if self.menuState == 0:
            # update afspeeltijd
            self.taskbarItems0[0] = "Time: " + self.ms_to_time_string(self.AudioController.currentChannel.get_time()) \
                                   + "/" + self.ms_to_time_string(self.AudioController.currentChannel.get_lenght())
            self.bottomLabel[0].setText(self.taskbarItems0[0])

        # Repeat
        if self.AudioController.audioPlayers[0].get_playback_state() == 6 and self.repeat:
            self.AudioController.play_all()

    # play, stop, terug
    def action_button_pushed(self, btnId):
        # tijd opties
        if btnId == 0:
            if self.menuState == 0:
                self.menuState = 1
            elif self.menuState == 1:
                self.AudioController.sync_channels()
                self.menuState = 0

            for i in range (3):
                self.bottomLabel[i].setText(self.taskbarItems[self.menuState][i])
                self.UIController.pushButton[i].setText(self.uiItems[self.menuState][i + 2])
        # Preset opties
        elif btnId == 1:
            if self.menuState == 0:
                pass
            elif self.menuState == 1:
                pass

        # repeat
        elif btnId == 2:
            self.toggle_repeat()

        # vorige
        elif btnId == 3:
            self.UIController.previous_page()

        # play
        if btnId == 4:
            self.AudioController.play_all()
            self.update_play_stats()

        # stop
        elif btnId == 5:
            self.AudioController.stop_all()

    # preset hardwareknoppen
    def preset_button_pushed(self, btnId):
        if btnId != 5:
            self.AudioController.set_channel_preset(btnId)
        else:
            self.AudioController.set_random_preset()

        self.update_play_stats()
        print("Preset " + str(btnId+1) + ": preset selected")

    # kanaal hardwareknoppen
    def channel_button_pushed(self, btnId):
        if btnId <= (self.AudioController.channelAmount-1):
            self.AudioController.set_current_channel(btnId)
            self.update_play_stats()
            print("Channel " + str(btnId+1) + ": set display")
        else:
            print("Channel " + str(btnId+1) + ": not playing")

    # reset de eq banden en toggle geluid.
    def rotary_button_pushed(self, btnId):
        if btnId != 5:
            self.AudioController.reset_eq_band(btnId)
        else:
            self.AudioController.currentChannel.toggle_mute()
        self.update_play_stats()

    # update EQ amp
    def eq_changed(self, sldId, sldValue):
        self.AudioController.currentChannel.set_eq_band_amp(sldValue, sldId)
        self.eqAmpLabel[sldId].setText(str(sldValue) + "dB")

    # update volume
    def volume_changed(self, sldvalue):
        self.AudioController.currentChannel.set_volume(sldvalue)
        self.volLabel.setText(str(sldvalue))

    # zet repeat aan of uit
    def toggle_repeat(self):
        if self.repeat == 0:
            self.repeat = 1
            self.taskbarItems0[1] = "Repeat: on"
        else:
            self.repeat = 0
            self.taskbarItems0[1] = "Repeat: off"
        self.bottomLabel[1].setText(self.taskbarItems0[1])

    def rotary_rotate(self, rotId, direction):
        if rotId is not 6:
            sldvalue = self.AudioController.currentChannel.bump_eq_band_amp(rotId, direction)
            self.eqAmpLabel[rotId].setText(str(sldvalue) + "dB")
        else:
            sldvalue = self.AudioController.currentChannel.bump_volume(direction)
            self.eqAmpLabel[rotId].setText(str(sldvalue) + "dB")

    # update alle labels en sliderposities die van kanaal afhangen
    def update_play_stats(self):
        self.uiItems0[0] = "Song: " + str(self.AudioController.currentChannel.song)
        self.uiItems0[1] = "Channel: " + str(self.AudioController.get_current_channel() + 1) \
                          + "/" + str(self.AudioController.channelAmount)
        self.UIController.update_main_texts(2)

        self.taskbarItems0[2] = "Preset: " + str(self.AudioController.currentChannel.preset.get_id())
        self.bottomLabel[2].setText(self.taskbarItems0[2])

        for i in range(5):
            self.eqSlider[i].setValue(self.AudioController.currentChannel.get_eq_band_amp(i))

        self.volSlider.setValue(self.AudioController.currentChannel.get_volume())

        muteState = self.AudioController.currentChannel.get_mute()
        if muteState == 0:
            self.eqFreqLabel[5].setText("Volume")
        else:
            self.eqFreqLabel[5].setText("Muted")
