import os
import threading
import time

from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.uix.widget import Widget

SLIDER_UPDATE_FRENQUENCY = 0.05

if os.name == 'posix':
    AUDIO_DIR = '/storage/emulated/0/Download/Audiobooks/Various/'
else:
    AUDIO_DIR = 'C:/Users/user/PycharmProjects/VoskASR/vosk-api/python/example/'

Builder.load_string('''
<MyLayout>:
    BoxLayout:
        orientation: "vertical"
        size: root.width, root.height
        pos_hint: {'top': 10}
        spacing: 10
        padding: 50

        Label:
            id: song_title
            text: "Song title!"
            text_size: self.size
            font_size: 32
            valign: "middle"
            halign: "center"
            
        Label:
            id: timestamp
            text: ""
            text_size: self.size
            font_size: 25
            valign: "middle"
            halign: "center"

        Slider:
            id: slider
            min: 0
            max: 1
            step: 1
            value: 0
            on_value: root.change_pos(self.value)

        Button:
            id: button
            text: "Play"
            font_size: 32
            size_hint: (0.5, 0.5)
            pos_hint: {"center_x": 0.5}
            on_release: root.start_song()''')


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
            time.sleep(SLIDER_UPDATE_FRENQUENCY)
            music_pos = self.music_obj.get_pos()
            self.timestamp.text = str(round(music_pos, 1)) + '/' + str(music_length)
            if music_pos + (SLIDER_UPDATE_FRENQUENCY * 2) < music_length:
                self.slider.value = music_pos
            else:
                self.stop = True
                self.button.text = "Play"
                #music_pos = 0
                #self.timestamp.text = str(round(music_pos, 2)) + '/' + str(music_length)
                #self.slider.value = music_pos
                #self.slider.value = 0
                #self.music_obj.seek(self.slider.value)


class MyLayout(Widget):
    """
    WARNING

    Only works if ffpyplayer is installed !
    (C:\Program Files\Python39> ./python -m pip install ffpyplayer
    Successfully installed ffpyplayer-4.3.2)

    NOT WORKING ON ANDROID SINCE INSTALLING FFPYPLAYER FAILS !
    """

    music_file = AUDIO_DIR + "sound_08.wav"
    music_obj = None

    def init_song(self):
        self.music_obj = SoundLoader.load(self.music_file)
        if self.music_obj:
            print(self.music_obj.source)
            print(self.music_obj.length)
            x = self.music_obj.source.split('\\')
            self.ids.song_title.text = x[-2] + ": " + x[-1]
            self.ids.slider.max = self.music_obj.length

            self.sliderAsynchUpdater = AsynchSliderUpdater(self.music_obj, self.ids.slider, self.ids.timestamp, self.ids.button)
            t = threading.Thread(target=self.sliderAsynchUpdater.updateSlider, args=())
            t.daemon = True
            t.start()

            self.music_obj.play()
            self.ids.button.text = "Stop"

    def restart_song(self):
        self.sliderAsynchUpdater = AsynchSliderUpdater(self.music_obj, self.ids.slider, self.ids.timestamp, self.ids.button)
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
            if abs(self.music_obj.get_pos() - value) > SLIDER_UPDATE_FRENQUENCY:
                print(value)
                self.music_obj.seek(value)
                self.ids.timestamp.text = str(value) + '/' + str(self.music_obj.length)


class Awesome(App):
    def build(self):
        self.title = "Hello!"
        return MyLayout()


if __name__ == "__main__":
    Awesome().run()