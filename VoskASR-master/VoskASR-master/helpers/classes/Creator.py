import win32api
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.factory import Factory

from helpers.sort import sort


class Creator(Widget):

    def __init__(self, main_parent, popup, trial_no, trial_list_no, **kwargs):
        super().__init__(**kwargs)

        self.main_parent = main_parent
        self.popup = popup
        self.trial_number = trial_no
        self.trial_list_number = trial_list_no

        self.new_word = {'word': "", 'conf': 1.0, 'start': "", 'end': "", 'from_session': "", 'from_trial': "", 'trial_number': str(self.trial_number)}

        self.run_creator()

    def refresh(self):
        self.main_parent.result_screen.remove_widget(self.main_parent.result_screen.audio_player)
        self.main_parent.result_screen.show_audio_player()

    def change(self, instance, text):
        try:
            if str(instance.label) == 'start' or str(instance.label) == 'end':
                self.new_word[str(instance.label)] = float(text)
            else:
                self.new_word[str(instance.label)] = text
        except ValueError:
            self.new_word[str(instance.label)] = ""

    def add_new(self):
        not_empty = True
        for key in self.new_word:
            if not self.new_word[key]:
                win32api.MessageBox(0, 'No field can be empty!', 'Warning', 0x00001000)
                not_empty = False
                break

        if not_empty:
            self.main_parent.data.recordings[str(self.trial_list_number)].trial_list.append(self.new_word)
            self.main_parent.restore_data.recordings[str(self.trial_list_number)].trial_list.append(self.new_word)

            print(self.main_parent.data.recordings[str(self.trial_list_number)].trial_list)
            print(self.main_parent.restore_data.recordings[str(self.trial_list_number)].trial_list)

            self.main_parent.data.recordings[str(self.trial_list_number)].trial_list = sort(self.main_parent.data.recordings[str(self.trial_list_number)].trial_list)
            self.main_parent.restore_data.recordings[str(self.trial_list_number)].trial_list = sort(self.main_parent.restore_data.recordings[str(self.trial_list_number)].trial_list)

            print('sorted: ', self.main_parent.data.recordings[str(self.trial_list_number)].trial_list)
            print('sorted: ', self.main_parent.restore_data.recordings[str(self.trial_list_number)].trial_list)

            self.popup.dismiss()
            self.refresh()

    def run_creator(self):
        for idx, key in enumerate(['word', 'conf', 'start', 'end', 'from_session', 'from_trial', 'trial_number']):

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
                text="",
                size_hint=(1, 1),
                halign="center",
                # height=max(self.minimum_height, self.audio_player.ids.scroll_words.height),
                # padding_y=(30, 30),
                font_size=18,
                size_hint_y=None,
                height=35
            )
            if key == 'conf':
                word_value.text = "1.0"
                word_value.readonly = True

            if key == 'trial_number':
                word_value.text = self.trial_number
                word_value.readonly = True

            word_value.label = key
            word_value.bind(text=self.change)

            word_box.add_widget(word_value)
            self.ids.creator_layout.add_widget(word_box)
