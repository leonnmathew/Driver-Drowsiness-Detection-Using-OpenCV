from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import  Screen
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from numpy import size

from mainScreen import MainScreen

class StatsScreen(Screen): #welcomeScreen subclass
    def __init__(self, **kwargs):
        super(StatsScreen, self).__init__(**kwargs) #init parent
        self.ms=MainScreen()
        statsPage = GridLayout()
        statsPage.cols =1
        statsPage.size_hint = (0.9,0.8)
        statsPage.pos_hint= {'center_x':0.5,'center_y':0.5}
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

        
        self.table = MDDataTable(
			pos_hint = {'center_x': 0.5, 'center_y': 0.5},
			size_hint =(0.9, 0.8),
			column_data = [
                ("Sr. No.", dp(30)),
				("Date", dp(30)),
				("No. of Alarms (Eyes)", dp(40)),
				("No. of Alarms (Yawns)", dp(40))
			],
			row_data = [
                ("1","2022-06-30", "4", "1")
                ]
			)
        
        self.add_row(self.ms)
        statsPage.add_widget(self.table)
        btnSection = BoxLayout()
        btn1 = Button(
            text="Show Latest Visualization",
            size_hint =(.5, .25),
            pos =(20, 20),
            background_color = '#1663e0',
            # on_press = self.dataShow()
            )
        btnSection.add_widget(btn1)

        button1 = Button(
            text="Go Back",
            size_hint =(.5, .25),
            pos =(20, 20),
            on_press = self.callback
            )
        btnSection.add_widget(button1)
        statsPage.add_widget(btnSection)     
        self.add_widget(statsPage)


    def callback(self, instance):
        self.manager.current = 'welcomeScreen'

    def add_row(self,ms) -> None:
        last_num_row = int(self.table.row_data[-1][0])
        self.val = ms.fetchData("all")
        for dict in self.val:
            row=((str(last_num_row + 1),dict["date"],dict["eyes"],dict["yawn"]))
            self.table.row_data.insert(len(self.table.row_data),row)

    def dataShow(self):
        pass

    def _update_rect(self, instance, value):
            self.rect.pos = instance.pos
            self.rect.size = instance.size