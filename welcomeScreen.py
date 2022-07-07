from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color

class WelcomeScreen(Screen): #welcomeScreen subclass
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs) #init parent
        welcomePage = GridLayout()
        welcomePage.cols =1
        welcomePage.size_hint = (0.6,0.7)
        welcomePage.pos_hint= {'center_x':0.5,'center_y':0.5}
        self.bind(
            size=self._update_rect,
            pos=self._update_rect
        )

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(
                size=self.size,
                pos=self.pos
            )

        #label widget for heading
        heading = Label(
            text="[b]DRIVER DROWSINESS DETECTION SYSTEM[/b]",
            markup = True,
            font_size = 32,
            color = '#1663e0',
            )
        welcomePage.add_widget(heading)

        # Button widget
        button1 = Button(
            text="Get Started",
            size_hint=(0.4,0.3),
            background_color = '#1663e0',
            on_press = self.callback
            )
        welcomePage.add_widget(button1)

        button2 = Button(
            text="About",
            size_hint=(0.4,0.3),
            on_press = self.about
            )
        welcomePage.add_widget(button2)
        self.add_widget(welcomePage)

    def callback(self, instance):
        self.manager.current = 'mainScreen'
    def about(self, instance):
        self.manager.current = 'aboutScreen'
    def _update_rect(self, instance, value):
            self.rect.pos = instance.pos
            self.rect.size = instance.size