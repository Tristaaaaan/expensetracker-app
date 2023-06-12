
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.app import MDApp


import scrHome
import scrViewExpenses
import scrAddExpenses


class WindowManager(ScreenManager):
    pass


class rawApp(MDApp):

    def build(self):

        return WindowManager()


if __name__ == '__main__':
    rawApp().run()
