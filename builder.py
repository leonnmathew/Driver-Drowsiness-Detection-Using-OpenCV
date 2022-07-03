from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager, Screen
from scipy.spatial import distance as dist
from imutils import face_utils
import numpy as np
import dlib
import cv2
import playsound
from threading import Thread


class BuilderApp(App): # display the welcome screen
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcomeScreen'))
        sm.add_widget(MainScreen(name='mainScreen'))
        return sm


class WelcomeScreen(Screen): #welcomeScreen subclass
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs) #init parent
        welcomePage = GridLayout()
        welcomePage.cols =1
        welcomePage.size_hint = (0.6,0.7)
        welcomePage.pos_hint= {'center_x':0.5,'center_y':0.5}

        #label widget for heading
        heading = Label(
            text="[b]DRIVER DROWSINESS DETECTION SYSTEM[/b]",
            markup = True,
            font_size = 24,
            color = '#00FFCE',
            )
        welcomePage.add_widget(heading)

        # Button widget
        button1 = Button(
            text="Get Started",
            size_hint=(1,0.5),
            background_color = '#00FFCE',
            on_press = self.callback
            )
        welcomePage.add_widget(button1)

        button2 = Button(
            text="About",
            size_hint=(1,0.5),
            )
        welcomePage.add_widget(button2)
        self.add_widget(welcomePage)

    def callback(self, instance):
        self.manager.current = 'mainScreen'



class MainScreen(Screen): #mainScreen subclass
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs) #init parent
        layout = BoxLayout(orientation='vertical')
        layout.cols =1
        self.img1 = Image(size_hint=(1,.8))
        layout.add_widget(self.img1)
        
        #capture video
        self.camera = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update,1.0/33.0)
        self.add_widget(layout)

    def update(self,*args):
        #Read frame from openCV
        ret,frame = self.camera.read()
        #Convert img to texture
        buf = cv2.flip(frame,0).tostring()
        img_texture = Texture.create(size=(frame.shape[1],frame.shape[0]),colorfmt='bgr')
        img_texture.blit_buffer(buf,colorfmt='bgr',bufferfmt='ubyte')
        self.img1.texture = img_texture



if __name__ == '__main__':
    BuilderApp().run()