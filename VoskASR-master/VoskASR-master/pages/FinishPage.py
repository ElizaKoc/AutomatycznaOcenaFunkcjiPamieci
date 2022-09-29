from kivy.uix.gridlayout import GridLayout
from kivy.app import App


class FinishPage(GridLayout):
    def __init__(self, main_parent, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1
        self.size = (self.width, self.height)
        self.pos = [0.5, 0.5]

        self.audio_player = None
        self.index = 1
        self.main_parent = main_parent

        self.ids.restart_button.bind(on_press=self.button_clicked)

        import subprocess
        #subprocess.Popen(r'explorer /select,"C:\path\of\folder\file"')

    def button_clicked(self, *args):
        App.get_running_app().restart()
