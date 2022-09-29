import win32api
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.factory import Factory

from helpers.sort import sort


class Editor(Widget):

    def __init__(self, main_parent, popup, word, word_index, trial_list_no, **kwargs):
        super().__init__(**kwargs)

        self.main_parent = main_parent
        self.popup = popup
        self.word = word
        self.word_index = word_index
        self.trial_list_number = trial_list_no

        self.changes = self.word.copy()

        #self.ids.test_label.text = str(word['word'])
        self.show_params()

    def refresh(self):
        self.main_parent.result_screen.remove_widget(self.main_parent.result_screen.audio_player)
        self.main_parent.result_screen.show_audio_player()

    def save_changes(self):
        not_empty = True
        for key in self.changes:
            if not self.changes[key]:
                win32api.MessageBox(0, 'No field can be empty!', 'Warning', 0x00001000)
                not_empty = False
                break

        if not_empty:
            self.main_parent.data.recordings[str(self.trial_list_number)].trial_list[self.word_index] = self.changes

            print(self.main_parent.data.recordings[str(self.trial_list_number)].trial_list)
            self.main_parent.data.recordings[str(self.trial_list_number)].trial_list = sort(self.main_parent.data.recordings[str(self.trial_list_number)].trial_list)
            print('sorted: ', self.main_parent.data.recordings[str(self.trial_list_number)].trial_list)

            self.popup.dismiss()
            self.refresh()

    def change(self, instance, text):
        #print(text)
        #print(instance.param_index)
        key = list(self.changes.keys())[instance.param_index]
        try:
            if key == 'start' or key == 'end':
                self.changes[str(key)] = float(text)
            else:
                self.changes[str(key)] = text
        except ValueError:
            self.changes[str(key)] = ""

    """"
    def restore(self):
        print(self.main_parent.data.recordings[str(5)].trial_list[self.word_index])
        self.main_parent.data.recordings[str(5)].trial_list[self.word_index] = self.main_parent.restore_data.recordings[str(5)].trial_list[self.word_index]
        print(self.main_parent.data.recordings[str(5)].trial_list[self.word_index])
        self.popup.dismiss()
        self.refresh()
        """

    def show_params(self):

        for idx, key in enumerate(self.word):

            word_box = BoxLayout(
                orientation="horizontal",
                padding="20dp",
                spacing=10,
                pos_hint=(1, None),
                size_hint_y=None,
                height=50
            )

            word_label = Factory.MyLabel2(
                text=str(key),
                font_size=18,
                size=(100, 35),
                color="#ffffff",
                halign="center",
                valign="middle",
                size_hint=(1, 1),
                bold=True,
                size_hint_y=None,
                height=35,
            )
            word_box.add_widget(word_label)

            word_value = TextInput(
                multiline=False,
                text=str(self.word[key]),
                size_hint=(1, 1),
                halign="center",
                # height=max(self.minimum_height, self.audio_player.ids.scroll_words.height),
                # padding_y=(30, 30),
                font_size=18,
                size_hint_y=None,
                height=35
            )
            if key == 'trial_number':
                word_value.readonly = True

            word_value.param_index = idx
            word_value.bind(text=self.change)

            word_box.add_widget(word_value)
            self.ids.editor_layout.add_widget(word_box)
