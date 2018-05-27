'''
Created on Feb 20, 2018

@created by Nafis Abrar
'''
import glob
import os, sys
import random

import pandas as pd
import os.path

import subprocess
sys.path.insert(0, 'Classifier_2')
sys.path.append(''.join(os.getcwd() + '/Classifier_2/plot_hmm_copy'))
sys.path.append('/Classifier_2/utils')
from Classifier_2.plot_hmmcopy import parse_args, GenHmmPlots
# KIVY IMPORTS#
import kivy
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen,SwapTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, Clock
from kivy.uix.popup import Popup
from kivy.core.window import Window

def load_all_csv():
# Get the csv and concatenate it if it does not exist already
    print (os.getcwd())
    if os.path.isfile("all_csv.csv"):
        os.remove("all_csv.csv")
    all_csv = glob.glob(os.getcwd() + "/*.csv")
    all_csv.sort(key=os.path.getctime)
    df = pd.concat((pd.read_csv(f) for f in all_csv))
    df = df.reset_index(drop=True)
    resultcsv = df.to_csv('all_csv.csv')
    print "Initial Load"

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

def get_pages(df1,arg):
    random_pages = []
    os.chdir("Pdfs")
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    files = filter(lambda f: f.endswith('.png'), files)
    files_count = len(files)
    numberofcells = (float(arg)/100) * files_count
    for page in random.sample(xrange(0, files_count-1),int(numberofcells) ):
       random_pages.append(page)
    return random_pages


class Body(BoxLayout): # capitalize class per convention, and extend FloatLayout instead of BoxLayout
    pass

Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 200
        
        TextInput:
            id: Filenames
            text:
            font_size:10 

        Button:
            text:'Plot'
            on_press: root.add_csv(Filenames.text)
            
    
        Button:
            text:  'Rate Cells!'
            on_press: root.manager.current = 'Cellcount'

""")


# Declare both screens
class MenuScreen(Screen):

    def get_filenames(self,arg):
        input_text = arg.encode("utf-8")
        s = [x for x in input_text.split(',')]
        last_letter = s[-1]
        if last_letter == '':
            del s[-1]
        if len(s) == 3:
            return s
        raise

    def validate_filename(self,arg):
        if '_reads.csv' == ".".join(arg[0].split("_")[1:]):
            print arg[0]
            print ".".join(arg[0].split("_")[1:])
            print "_read.csv not in arg0"
            raise
        elif '_all_metrics_summary.csv' ==".".join(arg[1].split("_")[1:]):
            print "_all_metrics summary not present in filename"
            print arg[1].split("_")[1:]

            raise
        elif '_segments.csv' == ".".join(arg[2].split("_")[1:]):
            print arg[2].split("_")[1:]
            print '_segments.csv not in arg[2]'
            raise

    def match_CSV_id(self,filenames):

        name_check = []
        for x in filenames:
            l = x.split("_")[0].split()
            name_check.append(l)
        print "Name check " + str(name_check)
        if all(name_check[0] == item for item in name_check) == False:
            x=1/0

    input=ObjectProperty()

    def add_csv(self,text):
        try:
            filenames = self.get_filenames(text)
            self.validate_filename(filenames)
            # Check for length of filename and
            self.match_CSV_id(filenames)
            print "All CSV passed"
            corrected_reads = filenames[0].strip()
            quality_metrics = filenames[1].strip()
            segments = filenames[2].strip()

            print corrected_reads,quality_metrics,segments
            print "Adding new csv"
            args = parse_args(corrected_reads,quality_metrics,segments)
            genhmm = GenHmmPlots(args)
            genhmm.main()
            print os.getcwd()
            os.chdir("..")
            # load_all_csv()
        except ValueError as v:
            print v
            print "Index"
            popup = Popup(title='Filename Error',
                          content=Label(text="[size=12]Please enter the correct filenames.[/size]",markup=True),
                          size_hint=(None, None), size=(300, 150))
            popup.open()
        except IndexError as i:
            print "Index"
            popup = Popup(title='Incorrect input',
                          content=Label(text="[size=12]Please enter the csv filenames in the above space.[/size]",markup=True),
                          size_hint=(None, None), size=(300, 150))
            popup.open()
        except IOError as i:
            print i
            print "Index"
            popup = Popup(title='I/O Error',
                          content=Label(text="[size=12]Please check the spelling of the  csv filenames.[/size]",
                                        markup=True),
                          size_hint=(None, None), size=(300, 150))
            popup.open()
        except ZeroDivisionError:
            popup = Popup(title='Wrong files',
                          content=Label(text="[size=12]The library id in CSV filename do not match.[/size]",
                                        markup=True),
                          size_hint=(None, None), size=(300, 150))
            popup.open()
        except TypeError:
            popup = Popup(title='Wrong files',
                          content=Label(text="[size=12]Please enter the csv filenames in the above space.[/size]",
                                        markup=True),
                          size_hint=(None, None), size=(300, 150))
            popup.open()
        except :
            popup = Popup(title='Wrong files',
                          content=Label(text="[size=12]Please enter the csv filenames in the above space.[/size]",
                                        markup=True),
                          size_hint=(None, None), size=(300, 150))
            popup.open()
            print "Unexpected error:", sys.exc_info()[0]


class Cellcount(Screen):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(Cellcount, self).__init__(**kwargs)
        self.clear_widgets()
        self.add_widget(Label(text='Percentage of cells you want to sample',size_hint=(0.74,1.15),font_size='22sp',font_name="DejaVuSans"))
        self.count = TextInput(multiline=False,pos_hint={'center_x': 0.5, 'center_y': 0.5},size_hint=(0.8,0.1),font_size=30)
        self.add_widget(self.count)
        self.count.bind(on_text_validate=self.on_enter)
        self.btnback = Button(text="Back", pos=(0, 500), size_hint=(.1, .1),markup=True)
        self.btnback.bind(on_press=lambda x:self.go_back())
        self.add_widget(self.btnback)


    def go_back(self):
        sm.current = sm.previous()


    def on_enter(self, *args):
        print "Pressed"
        print sm.screen_names
        if (str(self.count.text)):
            try:
                screens = sm.screen_names
                print len(screens)
                if len(screens)>2:
                    sm.clear_widgets(screens=sm.screens[2:])
                print sm.screen_names
                dir = os.getcwd()
                if dir.__contains__('Pdfs'):
                    os.chdir("..")
                result_csv = open('all_csv.csv', 'rb')
                df1 = pd.read_csv(result_csv)
                percent_num = str(self.count.text)
                pages = get_pages(df1, percent_num)
                for page in pages:
                    sm.add_widget(RateScreen(name=str(page),pages=pages))
                print len(sm.screen_names)
                print "In method on_enter : " + str(sm.screen_names)
                page = pages[0]
                page = str(page)
                sm.current=str(page)
                print "In method on_enter : "+ str(sm.current)
                self.count.text =" "
            except ValueError:
                print self.count.text
                print("That's not an int!")
            except IndexError:
                print "Enter correct %"


class RateScreen(Screen):
    def __init__(self, name,pages, **kwargs):
        super(RateScreen, self).__init__(**kwargs)
        self.clear_widgets()
        self.name = name
        self.pages = pages
        self.png = name
        self.wimg = Image(source=('%s.png'%self.name),pos=[self.pos[0],self.pos[1]],size=[self.width,self.height + 150])
        self.wimg.keep_ratio = False
        self.add_widget(self.wimg)
        self.l = Label(text='Press 0 for wrong ploidy',pos=[-300,-200])
        self.add_widget(self.l)
        self.wrongploidy = False

        self.btn1 = Button(text="[color=ff3333][b]1-Empty Plot[/b]",pos = (50, 5), size_hint = (.13, .1),markup=True)
        self.btn1.bind(on_press=lambda x:self.rate_cell1(name,pages))
        self.add_widget(self.btn1)

        self.btn2 = Button(text="[color=ffb733][b]2-Low Reads[/b]", pos=(190, 5), size_hint=(.13, .1),markup=True)
        self.btn2.bind(on_press=lambda x:self.rate_cell2(pages))
        self.add_widget(self.btn2)

        self.btn3 = Button(text="[color=fffd33][b]3-Poor[/b]",pos=(340,5),size_hint = (.13,.1),markup=True)
        self.btn3.bind(on_press=lambda x:self.rate_cell3(pages))
        self.add_widget(self.btn3)

        self.btn4 = Button(text="[color=3eff33][b]4-Intermediate[/b]", pos=(490, 5), size_hint=(.13, .1),markup=True)
        self.btn4.bind(on_press=lambda x: self.rate_cell4(pages))
        self.add_widget(self.btn4)

        self.btn5 = Button(text="[color=3395ff][b]5-Good[/b]",pos = (640, 5), size_hint = (.14, .1),markup=True)
        self.btn5.bind(on_press=lambda x: self.rate_cell5(pages))
        self.add_widget(self.btn5)

        self.btnback = Button(text="Back", pos=(0, 500), size_hint=(.1, .1),markup=True)
        self.btnback.bind(on_press=lambda x:self.go_back())
        self.add_widget(self.btnback)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        screens = sm.screen_names
        print len(screens)
        print sm.current_screen !=sm.screens[0]
        print "Name of current screen" + str(sm.current_screen)
        if len(screens)>2 and sm.current_screen !=sm.screens[0]:
            if keycode[1] == '0' or keycode[1] == 'numpad0':
                print "before" + str(self.wrongploidy)
                if self.wrongploidy ==False:
                    self.wrongploidy=True
                    self.popup = Popup(
                        title='Wrong Ploidy Selected',
                        size_hint=(None, None),
                        )

                else:
                    self.wrongploidy=False
                    self.popup = Popup(
                        title='Right Ploidy ',
                        size_hint=(None, None),
                        )
                print "After " + str(self.wrongploidy )
                self.popup.open()
                # call my_callback every 1 seconds
                Clock.schedule_interval(self.close_popup, 1)
            if keycode[1] == '5' or keycode[1] == 'numpad5':
                self.rate_cell5(self.pages)
            elif keycode[1] == '4' or keycode[1] == 'numpad4':
                self.rate_cell4(self.pages)
            elif keycode[1] == '3' or keycode[1] == 'numpad3':
                self.rate_cell3(self.pages)
            elif keycode[1] == '2' or keycode[1] == 'numpad2':
                self.rate_cell2(self.pages)
            elif keycode[1] == '1'or keycode[1] == 'numpad1':
                self.rate_cell1(self.pages)
            elif keycode[1] == 'backspace':
                self.go_back()

        elif keycode[1] == 'escape':
                keyboard.release()

        return True
    def close_popup(self,*args):
        self.popup.dismiss()

    def go_back(self):
        print "Back"
        if sm.previous()=='Cellcount':
            sm.clear_widgets(screens=sm.screens[2:])
        sm.current=sm.previous()
        print sm.current

    def rate_cell5(self,*args):
        print "The rating is 1"
        page = sm.current
        self.write_output_csv(5,page)
        sm.current=sm.next()
        print "Current page " + sm.current

    def rate_cell4(self, *args):
        print "The rating is 2"
        page = sm.current
        print page
        self.write_output_csv(4, page)
        sm.current = sm.next()
        print "Current page " + sm.current

    def rate_cell3(self, *args):
        page = sm.current
        print page
        self.write_output_csv(3, page)
        sm.current = sm.next()
        print "Current page " + sm.current

    def rate_cell2(self, *args):
        page = sm.current
        print page
        self.write_output_csv(2, page)
        sm.current = sm.next()
        print "Current page " + sm.current

    def rate_cell1(self, *args):
        page = sm.current
        print page
        self.write_output_csv(1, page)
        sm.current = sm.next()
        print "Current page " + sm.current

    def write_output_csv(self,rate,page):

        if self.wrongploidy == True:
            checkbox = True
            print "In method write to CSV : Wrongploidy"
        else:
            print "In method write to CSV : Rightploidy"
            checkbox = False
        print "In writetocsv"
        dir = os.getcwd()
        if dir.__contains__("Pdfs"):
            os.chdir("..")
        result_csv = open('all_csv.csv', 'rb')
        df1 = pd.read_csv(result_csv)
        if not os.path.exists("Output"):
            os.mkdir("Output")
        os.chdir("Output")
        if os.path.isfile("output.csv"):
            output = pd.read_csv("output.csv")
        else:
            output = pd.DataFrame()
        cell_id = df1.iloc[int(page)]['cell_id']
        sample_id = df1.iloc[int(page)]['sample_id']
        df2 = pd.DataFrame([[cell_id, sample_id, rate,checkbox]], columns=["Cell-ID", "Sample-ID", "Rating","Wrong Ploidy"])
        self.wrongploidy=False
        output = output.append(df2)
        if os.path.isfile("output"):
            os.remove("output.csv")
        output.drop_duplicates(subset="Cell-ID",keep='last').to_csv("output.csv",columns=["Cell-ID", "Sample-ID", "Rating","Wrong Ploidy"],index=False)
        os.chdir("..")


Builder.load_string("""
<AddCsv>:
    text_input: text_input

    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            size_hint_y: None
            height: 30
            Button:
                text: 'Load'
                on_release: root.show_load()
            Button:
                text: 'Save'
                on_release: root.show_save()

        BoxLayout:
            TextInput:
                id: text_input
                text: ''

            RstDocument:
                text: text_input.text
                show_errors: True

""")


class Root(FloatLayout):
    pass

# Create the screen manager
sm = ScreenManager(transition=SwapTransition())
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(Cellcount(name='Cellcount'))


class RateApp(App):
    def build(self):
        self.root = Body()
        return sm

if __name__ == '__main__':
        RateApp().run()
