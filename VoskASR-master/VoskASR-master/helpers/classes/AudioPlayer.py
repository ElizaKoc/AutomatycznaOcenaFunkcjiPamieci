from kivy.core.audio import SoundLoader
import threading
import time

from kivy.core.audio import SoundLoader
from kivy.uix.widget import Widget

SLIDER_UPDATE_FREQUENCY = 0.05


class AsynchSliderUpdater:
    def __init__(self, music_obj, slider, timestamp, button):
        self.music_obj = music_obj
        self.slider = slider
        self.timestamp = timestamp
        self.button = button

    def updateSlider(self):
        music_length = self.music_obj.length
        self.stop = False

        while not self.stop:
            time.sleep(SLIDER_UPDATE_FREQUENCY)
            music_pos = self.music_obj.get_pos()
            self.timestamp.text = str(round(music_pos, 1)) + '/' + str(music_length)
            if music_pos + (SLIDER_UPDATE_FREQUENCY * 2) < music_length:
                self.slider.value = music_pos
            else:
                self.stop = True
                self.button.text = "Play"


class AudioPlayer(Widget):
    """
    WARNING

    Only works if ffpyplayer is installed !
    (C:\Program Files\Python39> ./python -m pip install ffpyplayer
    Successfully installed ffpyplayer-4.3.2)

    NOT WORKING ON ANDROID SINCE INSTALLING FFPYPLAYER FAILS !
    """

    def __init__(self, path):
        super().__init__()

        self.box = None
        self.music_file = None
        self.path = path
        self.music_obj = None

        self.title = self.path.split('\\')
        self.ids.song_title.text = ((self.title[0]).split('/'))[-1] + ": " + self.title[-1]

    def init_song(self):
        self.music_file = self.path
        self.music_obj = SoundLoader.load(self.music_file)
        if self.music_obj:
            #print(self.music_obj.source)
            #print(self.music_obj.length)
            #sample = self.music_obj.source.split('\\')
            #self.ids.song_title.text = sample[-2] + ": " + sample[-1]
            self.ids.slider.max = self.music_obj.length

            self.sliderAsynchUpdater = AsynchSliderUpdater(self.music_obj, self.ids.slider, self.ids.timestamp, self.ids.button)
            t = threading.Thread(target=self.sliderAsynchUpdater.updateSlider, args=())
            t.daemon = True
            t.start()

            self.music_obj.play()
            self.ids.button.text = "Stop"

    def restart_song(self):
        self.sliderAsynchUpdater = AsynchSliderUpdater(self.music_obj, self.ids.slider, self.ids.timestamp,
                                                       self.ids.button)
        t = threading.Thread(target=self.sliderAsynchUpdater.updateSlider, args=())
        t.daemon = True
        t.start()

        self.music_obj.play()
        self.ids.button.text = "Stop"

    def start_song(self):
        if self.music_obj is None:
            self.init_song()
        elif not self.sliderAsynchUpdater.stop:
            self.sliderAsynchUpdater.stop = True
            self.music_obj.stop()
            self.ids.button.text = "Play"
        else:
            self.restart_song()

    def change_pos(self, value):
        if self.music_obj is not None:
            # test required to avoid mp3 playing perturbation
            if abs(self.music_obj.get_pos() - value) > SLIDER_UPDATE_FREQUENCY:
                #print(value)
                self.music_obj.seek(value)
                self.ids.timestamp.text = str(value) + '/' + str(self.music_obj.length)
