from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

class MainApp(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols =1
        self.window.size_hint = (0.6,0.7)
        self.window.pos_hint = {'center_x':0.5,'center_y':0.5}

        #label widget for heading
        self.heading = Label(
            text="[b]DRIVER DROWSINESS DETECTION SYSTEM[/b]",
            markup = True,
            font_size = 24,
            color = '#00FFCE',
            )
        self.window.add_widget(self.heading)

        # Button widget
        self.button1 = Button(
            text="Get Started",
            size_hint=(1,0.5),
            background_color = '#00FFCE',
            )
        self.window.add_widget(self.button1)
        self.button2 = Button(
            text="About",
            size_hint=(1,0.5),
            )
        self.window.add_widget(self.button2)
        return self.window

    def Callback(self, instance):
        pass

MainApp().run()