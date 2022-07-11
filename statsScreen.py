from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from numpy import source

class StatsScreen(Screen): #welcomeScreen subclass
    def __init__(self, **kwargs):
        super(StatsScreen, self).__init__(**kwargs) #init parent
        