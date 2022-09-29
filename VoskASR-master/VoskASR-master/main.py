from kivy.app import App
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

from pages.DirPathPage import DirPathPage
from pages.FilePathPage import FilePathPage
from pages.FinishPage import FinishPage
from pages.ResultPage import ResultPage

Window.size = 1200, 800


class MainWindow(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.finish_screen = None
        self.result_screen = None
        self.file_path_screen = None
        self.screen_manager = None
        self.dir_path_screen = None
        self.data = None
        self.restore_data = None

    def build(self):
        """
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.window.add_widget(Image(source="resources/images/logo_image.jpg"))


        self.date = TextInput(
            multiline=False,
            # padding_y=(30, 30),
            size_hint=(1, 0.7),
            font_size=30
        )
        self.window.add_widget(self.date)
        """
        self.title = 'ASR System'

        # self.theme_cls.theme_style = "Dark"
        self.screen_manager = ScreenManager()
        Builder.load_file('resources/screen_elements.kv')

        self.dir_path_screen = DirPathPage(main_parent=self)
        screen = Screen(name="Directory")
        screen.add_widget(self.dir_path_screen)
        self.screen_manager.add_widget(screen)

        self.file_path_screen = FilePathPage(main_parent=self)
        screen = Screen(name="File")
        screen.add_widget(self.file_path_screen)
        self.screen_manager.add_widget(screen)

        self.result_screen = ResultPage(main_parent=self)
        screen = Screen(name="Result")
        screen.add_widget(self.result_screen)
        self.screen_manager.add_widget(screen)

        self.finish_screen = FinishPage(main_parent=self)
        screen = Screen(name="Finish")
        screen.add_widget(self.finish_screen)
        self.screen_manager.add_widget(screen)

        # self.file_path_screen = ResultPage(main_parent=self)
        # screen = Screen(name="Result")
        # screen.add_widget(self.file_path_screen)
        # self.screen_manager.add_widget(screen)

        return self.screen_manager

    def restart(self):
        self.root.clear_widgets()
        self.stop()
        return MainWindow().run()


if __name__ == "__main__":
    MainWindow().run()
