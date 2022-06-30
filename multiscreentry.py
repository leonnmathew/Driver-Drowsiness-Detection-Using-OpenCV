import kivy
kivy.require('1.9.1')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

class PanelBuilderApp(App):  # display the welcome screen
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcomeScreen'))
        sm.add_widget(FunctionScreen(name='functionScreen'))
        return sm

class WelcomeScreen(Screen): #welcomeScreen subclass
    def __init__(self, **kwargs): #constructor method
        super(WelcomeScreen, self).__init__(**kwargs) #init parent
        welcomePage = FloatLayout()
        box = BoxLayout(orientation='vertical', size_hint=(0.4, 0.3),
                                           padding=8, pos_hint={'top': 0.5, 'center_x': 0.5})
        welcomeLabel = Label(text='Hello and welcome to the Panel Builder version 1.0.\nApp by John Vorsten\nClick below to continue',
            halign= 'center', valign= 'center', size_hint= (0.4, 0.2), pos_hint= {'top': 1, 'center_x': 0.5})
        welcomeBox = Button(text= 'Click to continue', on_press=self.callback)
        welcomeBox2 = Button(text='not used')

        welcomePage.add_widget(welcomeLabel)
        box.add_widget(welcomeBox)
        box.add_widget(welcomeBox2)
        welcomePage.add_widget(box)
        self.add_widget(welcomePage)

    def callback(self, instance):
        print('The button has been pressed')
        self.manager.current = 'functionScreen'

class FunctionScreen(Screen):  #For later function navigation
    def __init__(self, **kwargs): #constructor method
        super(FunctionScreen, self).__init__(**kwargs) #init parent
        functionPage = FloatLayout()
        functionLabel = Label(text='Welcome to the function page. Here you will choose what functions to use',
                              halign='center', valign='center', size_hint=(0.4,0.2), pos_hint={'top': 1, 'center_x': 0.5})
        functionPage.add_widget(functionLabel)
        self.add_widget(functionPage)

if __name__ == '__main__':
    PanelBuilderApp().run()
