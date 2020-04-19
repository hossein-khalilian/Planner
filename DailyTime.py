#!/home/hse/henv/bin/python
import os
os.environ["KIVY_NO_FILELOG"] = "1"
os.environ["KIVY_NO_CONSOLELOG"] = "1"
import kivy
import pause
import pandas as pd
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import  Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from datetime import datetime
from kivy.input import motionevent
from kivy.config import Config
from datetime import timedelta
from kivy.logger import Logger
Logger.disabled = True
Config.set('kivy','log_enable', '0')
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '200')
# Config.write()


class Title(TextInput):
    def on_parent(self, widget, parent):
        self.focus = True

class Daily(App):

    def build(self):
        self.csvpath = '/home/hse/DailyPlan/DailyTime.csv'
        if not os.path.exists(self.csvpath):
            data = {
                'time': [str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))], 
                'type': ['start'],
                'title': ['start'],
                'description': ['start']
                }
            df = pd.DataFrame(data=data)
            df.to_csv( self.csvpath, mode='w',index=False, sep=',')
            
        df1 = pd.read_csv( self.csvpath, sep=',')
        self.previous = df1.iloc[0]['time']
        now = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        FMT = "%Y-%m-%d %H:%M:%S"
        tdelta = datetime.strptime(now, FMT) - datetime.strptime(self.previous, FMT)

        self.boxl = BoxLayout(orientation='horizontal', spacing=.1, size_hint=(1, .55))
        self.lbl = Label(text='What have you been up to since ' + str(self.previous), size_hint=(1, 1))
        self.boxl.add_widget(self.lbl)

        self.boxt = BoxLayout(orientation='horizontal', spacing=.1, size_hint=(1, .45),)
        self.time = Label(text='Time:' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), size_hint=(1, 1))
        self.delta = Label(text='Spend time: ' + str(tdelta), size_hint=(1, 1))
        self.boxt.add_widget(self.time)
        self.boxt.add_widget(self.delta)

        self.box1 = BoxLayout(orientation='vertical', spacing=1, size_hint=(1,.25))
        self.box1.add_widget(self.boxl)
        self.box1.add_widget(self.boxt)


        self.btnbox = BoxLayout(orientation='vertical', spacing=.1, size_hint=(.2,1))
        self.btn1 = Button(text='Efficient', on_press=self.store, size_hint=(1, 1), background_color=(0,1,0,1))
        self.btn2 = Button(text='Shallow', on_press=self.store, size_hint=(1, 1), background_color=(1,1,1,1))
        self.btn3 = Button(text='Inefficient', on_press=self.store, size_hint=(1, 1), background_color=(1,0,0,1))
        self.btn4 = Button(text='Daily Habits', on_press=self.store, size_hint=(1, 1), background_color=(1,1,0,1))
        self.btnbox.add_widget(self.btn1)
        self.btnbox.add_widget(self.btn2)
        self.btnbox.add_widget(self.btn3)
        self.btnbox.add_widget(self.btn4)

        self.txtbox = BoxLayout(orientation='vertical', spacing=1, size_hint=(.8,1))
        self.title1 = Title(hint_text='Title', multiline=False, write_tab=False, size_hint=(1,.2))
        self.txt = TextInput(hint_text='Description', write_tab=False, size_hint=(1,.8))
        self.txtbox.add_widget(self.title1)
        self.txtbox.add_widget(self.txt)

        self.box2 = BoxLayout(orientation='horizontal', spacing=.1, size_hint=(1,.7))
        self.box2.add_widget(self.txtbox)
        self.box2.add_widget(self.btnbox)

        self.box = BoxLayout(orientation='vertical', spacing=0.1,)
        self.box.add_widget(self.box1)
        self.box.add_widget(self.box2)

        Clock.schedule_interval(self.clock_callback, 1)

        return self.box


    def store(self, instance):
        data = {
        	'time': [str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))], 
         	'type': [instance.text],
            'title': [self.title1.text],
         	'description': [self.txt.text]
         	}
        df = pd.DataFrame(data=data)
        df1 = pd.read_csv( self.csvpath, sep=',')
        df = pd.concat([df, df1], keys=['time', 'type', 'title', 'description'])
        df.to_csv( self.csvpath, mode='w',index=False, sep=',')
        App.get_running_app().stop()
    

    def clock_callback(self, dt):
        now = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        FMT = "%Y-%m-%d %H:%M:%S"
        tdelta = datetime.strptime(now, FMT) - datetime.strptime(self.previous, FMT)
        self.time.text = 'Time: ' + now
        self.delta.text = 'Spend time: ' + str(tdelta)



Daily().run()
