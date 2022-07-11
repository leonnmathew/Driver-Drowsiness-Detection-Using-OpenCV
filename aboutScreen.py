from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color

class AboutScreen(Screen): #AboutScreen subclass
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__(**kwargs) #init parent
        aboutPage = GridLayout()
        aboutPage.cols =1
        aboutPage.size_hint = (0.6,0.7)
        aboutPage.pos_hint= {'center_x':0.5,'center_y':0.5}
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
            text="[b]SEMESTER 2 MINI PROJECT BY-[/b]",
            markup = True,
            font_size = 26,
            color = '#1663e0',
            )
        aboutPage.add_widget(heading)
        name1 = Label(
            text="Roll No: 4 - Itika Bhattacharjee",
            markup = True,
            font_size = 20,
            color = '#1663e0',
            )
        aboutPage.add_widget(name1)
        name2 = Label(
            text="Roll No: 54 - Shubham Singh",
            markup = True,
            font_size = 20,
            color = '#1663e0',
            )
        aboutPage.add_widget(name2)
        name3 = Label(
            text="Roll No: 58 - Leon Mathew",
            markup = True,
            font_size = 20,
            color = '#1663e0',
            )
        aboutPage.add_widget(name3)

        # Button widget
        buttonSection = BoxLayout()
        blank2 = Label(
            font_size= 18,
            size_hint=(0.4,0.3),
            pos_hint = {"x" : 0.45, "top" : 0.9}
            )
        buttonSection.add_widget(blank2)
        button1 = Button(
            text="Go Back",
            size_hint=(0.4,0.4),
            on_press = self.callback
            )
        buttonSection.add_widget(button1)
        blank3 = Label(
            font_size= 18,
            size_hint=(0.4,0.3),
            pos_hint = {"x" : 0.45, "top" : 0.9}
            )
        buttonSection.add_widget(blank3)
        aboutPage.add_widget(buttonSection)
        self.add_widget(aboutPage)

    def callback(self, instance):
        self.manager.current = 'welcomeScreen'
        
    def _update_rect(self, instance, value):
            self.rect.pos = instance.pos
            self.rect.size = instance.size