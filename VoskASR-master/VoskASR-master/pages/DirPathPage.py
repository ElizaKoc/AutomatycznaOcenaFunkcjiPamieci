import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
# to use buttons:
from kivy.uix.button import Button
from kivy.uix.image import Image

import helpers.dialog as dialog


class DirPathPage(GridLayout):
    def __init__(self, main_parent, **kwargs):
        super().__init__(**kwargs)

        self.dir_path = None
        self.main_parent = main_parent

        self.cols = 1
        self.size_hint = (0.6, 0.7)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.add_widget(Image(source="resources/images/logo_image.jpg"))

        self.button_rec_directory = None
        self.optionRequest = None

        self.load_label()
        self.load_buttons()

    def do_action(self, event):
        self.main_parent.dir_path = dialog.show_dialog_directory()
        self.main_parent.screen_manager.current = 'File'

    def load_label(self):
        self.optionRequest = Label(
            text="Choose recordings directory",
            font_size=25,
            color="#ffffff",
            bold=True
        )
        self.add_widget(self.optionRequest)

    def load_buttons(self):
        self.button_rec_directory = Button(
            text="Select Directory",
            size_hint=(0.5, 0.5),
            bold=True,
            font_size=25
        )

        self.button_rec_directory.bind(on_press=self.do_action)
        self.add_widget(self.button_rec_directory)
