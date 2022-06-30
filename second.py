from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.logger import Logger
import cv2

class DrowsinessApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        layout.cols =1
        self.img1 = Image(size_hint=(1,.8))
        layout.add_widget(self.img1)
        
        #capture video
        self.camera = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update,1.0/33.0)

        return layout

    #Run continuously to get webcam feed
    def update(self,*args):
        #Read frame from openCV
        ret,frame = self.camera.read()
        
        #Convert img to texture
        buf = cv2.flip(frame,0).tostring()
        img_texture = Texture.create(size=(frame.shape[1],frame.shape[0]),colorfmt='bgr')
        img_texture.blit_buffer(buf,colorfmt='bgr',bufferfmt='ubyte')
        self.img1.texture = img_texture


DrowsinessApp().run()