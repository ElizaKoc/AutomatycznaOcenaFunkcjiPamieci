import win32api
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
# to use buttons:
from kivy.uix.button import Button

import helpers.dialog as dialog
from helpers.classes.Data import Data


class FilePathPage(GridLayout):
    def __init__(self, main_parent, **kwargs):
        super().__init__(**kwargs)

        self.main_parent = main_parent
        self.cols = 1
        self.size_hint = (0.6, 0.7)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.button_rec_file = None
        self.option_request = None

        self.load_label()
        self.load_buttons()

    def do_action(self, event):
        self.main_parent.file_path = dialog.show_dialog_file()
        if self.main_parent.file_path.endswith('.csv'):
            self.option_request.text = "Data file uploaded correctly"
            self.main_parent.data = Data(self.main_parent.dir_path, self.main_parent.file_path)
            self.main_parent.restore_data = Data(self.main_parent.dir_path, self.main_parent.file_path)
            self.main_parent.screen_manager.current = 'Result'
            self.main_parent.result_screen.show_audio_player()
        else:
            win32api.MessageBox(0, 'Incorrect data format!', 'Error', 0x00001000)
        #self.main_parent.screen_manager.current = 'File'

    def load_label(self):
        self.option_request = Label(
            #text="Choose recording file",
            text="Select a csv file with a list of words \nfrom a given session for a given patient",
            font_size=25,
            color="#ffffff",
            halign="center",
            bold=True
        )
        self.add_widget(self.option_request)

    def load_buttons(self):
        self.button_rec_file = Button(
            text="Upload File",
            size_hint=(0.5, 0.5),
            bold=True,
            font_size=25
        )

        self.button_rec_file.bind(on_press=self.do_action)
        self.add_widget(self.button_rec_file)
