# Kivy imports
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen

#user defined classes import
from loginScreen import LoginScreen
from welcomeScreen import WelcomeScreen
from aboutScreen import AboutScreen
from mainScreen import MainScreen


class BuilderApp(App): # display the welcome screen
    def build(self):
        self.title = "Driver Drowsiness Detection System"
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='loginScreen'))
        sm.add_widget(WelcomeScreen(name='welcomeScreen'))
        sm.add_widget(MainScreen(name='mainScreen'))
        sm.add_widget(AboutScreen(name='aboutScreen'))
        return sm

if __name__ == '__main__':
    BuilderApp().run()
