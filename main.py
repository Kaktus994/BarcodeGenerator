import barcode
import os
import sys
from barcode.writer import ImageWriter
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.logger import LoggerHistory

sys.stderr = open("output.txt", "w")
sys.stdout = sys.stderr

print("\n".join([str(l) for l in LoggerHistory.history]))


class Manager(ScreenManager):
    def __init__(self):
        super(Manager, self).__init__()

        self.add_widget(MainScreen('main'))
        self.add_widget(Galerija("galerija"))


class MainScreen(Screen):
    def __init__(self, name):
        super(MainScreen, self).__init__()

        self.name = name

        self.lay = GridLayout()
        self.lay.cols = 1

        self.lay.inside = GridLayout()
        self.lay.inside.cols = 2
        self.lay.rows = 2

        self.lay.inside.add_widget(Label(text="Unesi BarCode: "))
        self.lay.bc = TextInput(hint_text="UNESI KOD OD 12 KARAKTERA", multiline=False)
        self.lay.inside.add_widget(self.lay.bc)

        self.lay.add_widget(Button(text="UNESI", on_press=self.unesi))

        self.lay.add_widget(self.lay.inside)
        self.add_widget(self.lay)

        self.bc_39 = 12

    def unesi(self, instance):
        code = self.lay.bc.text

        if len(code) != self.bc_39:
            Pp.popup_pogresan(self)
            print(len(self.lay.bc.text))
        else:
            c128 = barcode.get("code128", code, writer=ImageWriter())
            path = os.path.dirname(os.path.abspath(__file__))
            c128.save(os.path.join(path, "128"))
            self.lay.bc.text = ""

    def broj_karaktera(self):
        c_number = len(self.lay.bc.text)
        return c_number


class Galerija(Screen):
    def __init__(self, name):
        super(Galerija, self).__init__()

        self.name = name
# DISPLAY
        path = os.path.dirname(os.path.abspath(__file__))
        img = Image(source=os.path.join(path, "128.png"), nocache=True)
        img.allow_stretch = False
        Clock.schedule_interval(lambda dt: img.reload(), 0.2)
        self.add_widget(img)


class Pp(FloatLayout):

    def popup_pogresan(self):
        show = Pp()
        popup_window = Popup(title="POGRESAN UNOS", auto_dismiss=False, content=show, size_hint=(None, None), size=(350, 200))
        popup_window.open()
        lbl1 = Label(text="Kod ima manje od 12 karaktera", pos_hint={"x":0, "y":0.3})
        btn1 = Button(text="ZATVORI", size_hint=(None, None), size=(100, 50), pos_hint={"x":0.34, "top":0.5})
        btn1.bind(on_press=popup_window.dismiss)
        show.add_widget(lbl1)
        show.add_widget(btn1)


class MyGrid(GridLayout):
    def __init__(self, sm=None):
        super(MyGrid, self).__init__()

        self.sm = sm
        self.cols = 2
        self.size_hint = (1, 0.1)
        self.add_widget(Button(text="Unos Barkoda", on_release=self.go_screen))

    def go_screen(self, ins):
        self.sm.current = "main"


class MyGrid2(GridLayout):
    def __init__(self, sm=None):
        super(MyGrid2, self).__init__()

        self.sm = sm
        self.cols = 3
        self.size_hint = (1, 0.1)
        self.add_widget(Button(text="Galerija", on_release=self.go_screen))

    def go_screen(self, ins):
        self.sm.current = "galerija"


class Root(BoxLayout):

    def __init__(self):
        super(Root, self).__init__()
        self.orientation = "vertical"
        sm = Manager()

        self.add_widget(MyGrid(sm=sm))
        self.add_widget(MyGrid2(sm=sm))
        self.add_widget(sm)


class MyApp(App):
    def build(self):
        return Root()


if __name__ == "__main__":
    MyApp().run()
