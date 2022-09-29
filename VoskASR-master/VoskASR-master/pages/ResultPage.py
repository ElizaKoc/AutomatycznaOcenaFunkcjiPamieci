from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button

from helpers.classes.AudioPlayer import *
from kivy.factory import Factory
from kivy.uix.screenmanager import Screen

from helpers.classes.Editor import Editor
from helpers.classes.Creator import Creator
from helpers.csv_generator import generate_csv
from helpers.folder_generator import clear_directory


class ResultPage(GridLayout):
    def __init__(self, main_parent, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1
        self.size = (self.width, self.height)
        self.pos = [0.5, 0.5]

        self.audio_player = None
        self.index = 1
        self.main_parent = main_parent

    def move_to_finish_screen(self, *args):
        generate_csv(self.main_parent.data.recordings)
        clear_directory('resources/preprocessed/')
        self.main_parent.screen_manager.current = 'Finish'

    def refresh(self):
        self.main_parent.result_screen.remove_widget(self.main_parent.result_screen.audio_player)
        self.main_parent.result_screen.show_audio_player()

    def previous_recording(self, *args):
        self.index = self.index - 1
        self.refresh()

    def next_recording(self, *args):
        self.index = self.index + 1
        self.refresh()

    def remove_word(self, *args):
        word_index = (args[0].word_index)
        self.main_parent.data.recordings[str(self.index)].trial_list.pop(word_index)
        self.refresh()

    def open_editor(self, *args):
        screen = Screen(name="Editor")

        self.popup = Popup(title='Edit recognized word',
                           content=screen,
                           size_hint=(None, None), size=(800, 600))

        word_index = (args[0].word_index)

        editor_screen = Editor(main_parent=self.main_parent, popup=self.popup,
                               word=(self.main_parent.data.recordings[str(self.index)].trial_list[word_index]),
                               word_index=word_index, trial_list_no=self.index)
        screen.add_widget(editor_screen)

        self.popup.open()

    def open_creator(self, *args):
        screen = Screen(name="Creator")

        self.popup = Popup(title='Add recognized word',
                           content=screen,
                           size_hint=(None, None), size=(800, 600))

        if not self.main_parent.data.recordings[str(self.index)].trial_list:
            self.main_parent.data.recordings[str(self.index)].trial_list = []

        trial_number = str(self.index)

        creator_screen = Creator(main_parent=self.main_parent, popup=self.popup, trial_no=trial_number, trial_list_no=self.index)
        screen.add_widget(creator_screen)

        self.popup.open()

    def add_empty_fields(self, col_num, word_box):

        for i in range(col_num):
            word_label = Label(
                text="",
                font_size=16,
                text_size=(self.width, None),
                color="#ffffff",
                halign="center",
                valign="middle",
                size_hint=(1, 0.5),
                bold=True,
                size_hint_y=None,
                height=25
            )
            word_box.add_widget(word_label)

    def show_labels(self):
        labels = self.main_parent.data.recordings[str(self.index)].trial_list[0]

        word_box = BoxLayout(
            orientation="horizontal",
            padding="20dp",
            spacing=25,
            pos_hint=(1, None),
            size_hint_y=None,
            height=30
        )

        for key in labels:
            word_label = Label(
                text=str(key),
                font_size=16,
                text_size=(self.width, None),
                color="#ffffff",
                halign="center",
                valign="middle",
                size_hint=(1, 0.5),
                bold=True,
                size_hint_y=None,
                height=25,
            )
            word_box.add_widget(word_label)

        self.add_empty_fields(2, word_box)
        self.audio_player.ids.words_list_params.add_widget(word_box)

    def show_values(self):
        for idx, word in enumerate(self.main_parent.data.recordings[str(self.index)].trial_list):
            # print(word)

            word_box = BoxLayout(
                orientation="horizontal",
                padding="20dp",
                spacing=25,
                pos_hint=(1, None),
                size_hint_y=None,
                height=30
            )

            for key in word:
                word_value = Factory.MyLabel(
                    text=str(word[key]),
                    font_size=16,
                    text_size=(self.width, None),
                    color="#ffffff",
                    halign="center",
                    valign="middle",
                    size_hint=(1, 0.5),
                    bold=False,
                    size_hint_y=None,
                    height=25
                )
                word_box.add_widget(word_value)

            word_button = Button(
                text="Edit",
                padding_y="20dp",
                padding_x="20dp",
                font_size=16,
                size_hint=(1, 0.5),
                pos_hint={"center_x": 0.5},
                size_hint_y=None,
                height=25,
                on_release=self.open_editor
            )
            word_button.word_index = idx
            word_box.add_widget(word_button)

            word_remove_button = Button(
                text="Remove",
                padding_y="20dp",
                padding_x="20dp",
                font_size=16,
                size_hint=(1, 0.5),
                pos_hint={"center_x": 0.5},
                size_hint_y=None,
                height=25,
                on_release=self.remove_word
            )
            word_remove_button.word_index = idx
            word_box.add_widget(word_remove_button)

            self.audio_player.ids.words_list_params.add_widget(word_box)
            # self.ids.words_list.add_widget(self.word_label)

    def add_control_buttons(self):
        word_box_button = BoxLayout(
            orientation="horizontal",
            padding="20dp",
            spacing=25,
            pos_hint=(1, None),
            size_hint_y=None,
            height=30
        )

        add_button = Button(
            text="Add new",
            padding_y="20dp",
            padding_x="20dp",
            font_size=16,
            size_hint=(None, None),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            width=200,
            height=50,
            size_hint_y=None,
            on_release=self.open_creator
        )
        word_box_button.add_widget(add_button)

        if self.index > (int(list(self.main_parent.data.recordings.keys())[0])):
            previous_button = Button(
                text="Previous recording",
                padding_y="20dp",
                padding_x="20dp",
                font_size=16,
                size_hint=(None, None),
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                width=200,
                height=50,
                size_hint_y=None,
                on_release=self.previous_recording
            )
            word_box_button.add_widget(previous_button)

        if self.index < (int(list(self.main_parent.data.recordings.keys())[-1])):
            next_button = Button(
                text="Next recording",
                padding_y="20dp",
                padding_x="20dp",
                font_size=16,
                size_hint=(None, None),
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                width=200,
                height=50,
                size_hint_y=None,
                on_release=self.next_recording
            )
            word_box_button.add_widget(next_button)

        final_button = Button(
            text="Finish",
            padding_y="20dp",
            padding_x="20dp",
            font_size=16,
            size_hint=(None, None),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            width=200,
            height=50,
            size_hint_y=None,
            on_release=self.move_to_finish_screen
        )
        word_box_button.add_widget(final_button)

        self.audio_player.ids.words_list_params.add_widget(word_box_button)

    def show_results(self):
        if self.main_parent.data.recordings[str(self.index)].trial_list:
            self.show_labels()
            self.show_values()

        self.add_control_buttons()

    def show_audio_player(self):
        print(self.main_parent.data.recordings[str(self.index)].filepath)
        self.audio_player = AudioPlayer(self.main_parent.data.recordings[str(self.index)].filepath)
        # self.ids.audio_player_box.add_widget(self.audio_player)
        self.add_widget(self.audio_player)

        self.show_results()
