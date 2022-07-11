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

class LoginScreen(Screen): #welcomeScreen subclass
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs) #init parent
        loginPage = GridLayout()
        loginPage.cols =1
        loginPage.size_hint = (0.6,0.8)
        loginPage.pos_hint= {'center_x':0.5,'center_y':0.5}
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
        loginPage.add_widget(Image(source="icon.jpg"))
        heading = Label(
            text="[b]LOG-IN[/b]",
            markup = True,
            font_size = 32,
            color = '#1663e0',
            )
        loginPage.add_widget(heading)

        #Email Section
        emailSection = BoxLayout()
        email = Label(
            text="[b]Email:[/b]",
            markup = True,
            color = '#000000',
            size_hint=(0.4,0.3),
            )
        emailSection.add_widget(email)
        emailInput = TextInput(
            multiline = False,
            font_size= 18,
            padding_y=(10,10),
            size_hint=(1,0.5)
            )
        emailSection.add_widget(emailInput)
        loginPage.add_widget(emailSection)

        #Password Section
        pswdSection = BoxLayout()
        pswd = Label(
            text="[b]Password:[/b]",
            markup = True,
            color = '#000000',
            size_hint=(0.4,0.3),
            )
        pswdSection.add_widget(pswd)

        pswdInput = TextInput(
            multiline = False,
            font_size= 18,
            padding_y=(10,10),
            size_hint=(1,0.5)
            )
        pswdSection.add_widget(pswdInput)
        loginPage.add_widget(pswdSection)

       

        buttonSection = BoxLayout()
        blank2 = Label(
            font_size= 18,
            size_hint=(0.4,0.3),
            pos_hint = {"x" : 0.45, "top" : 0.9}
            )
        buttonSection.add_widget(blank2)

        button2 = Button(
            text="login",
            size = (100,50),
            size_hint=(0.4,0.3),
            pos_hint = {'center_x':0.5,'center_y':0.5},
            background_color = '#1663e0',
            on_press = self.callback
            
            )
        buttonSection.add_widget(button2)

        blank3 = Label(
            font_size= 18,
            size_hint=(0.4,0.4),
            pos_hint = {"x" : 0.45, "top" : 0.9}
            )
        buttonSection.add_widget(blank3)
        loginPage.add_widget(buttonSection)
        self.add_widget(loginPage)
          
    def callback(self, instance):
        self.manager.current = 'welcomeScreen'

    def _update_rect(self, instance, value):
            self.rect.pos = instance.pos
            self.rect.size = instance.size