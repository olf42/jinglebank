#!/usr/bin/env python3

from jinglebutton import JingleButton
from gi.repository import Gtk, GObject, Gst, Gdk
import cairo, math, time
import colorsys
import os.path

#Button size

WIDTH = 200
HEIGHT = 180

JINGLE1 = os.path.join("testraffel", "Jingles", "Antenne_Gulasch_Opener.wav")
JINGLE2 = os.path.join("testraffel", "Jingles", "Antenne_Gulasch.wav") 
JINGLE3 = os.path.join("testraffel", "Jingles", "Antenne_Gulasch_1048.wav")
JINGLE4 = os.path.join("testraffel", "Jingles", "Wenn_das.wav")

JINGLE5 = os.path.join("testraffel", "Jingles", "News_Eve_Entropia.wav")
JINGLE6 = os.path.join("testraffel", "Jingles", "News_Intro.wav")
JINGLE7 = os.path.join("testraffel", "Jingles", "News_Trenner.wav")
JINGLE8 = os.path.join("testraffel", "Jingles", "Wetter_Chaos_Darmstadt.wav")

JINGLE9 = os.path.join("testraffel", "Jingles", "Sicherheitshinweis.wav")
JINGLE10 = os.path.join("testraffel", "Jingles", "Diskordianischer_Sender.wav")
JINGLE11 = os.path.join("testraffel", "Jingles", "Hallo_Bin_Ich_Jetzt_Im_Radio.wav")


JINGLE13 = os.path.join("testraffel", "news_intro.wav")
JINGLE14 = os.path.join("testraffel", "news_trenner.wav")
JINGLE15 = os.path.join("testraffel", "nur_gute_butter.wav")

class JingleBank(Gtk.Window):

    def __init__(self, width, height):
        Gtk.Window.__init__(self, title="JingleBank (Shift Q: quit)")

        Gst.init()

        #Grid to organize the Buttons
        self.grid = Gtk.Grid()
        self.add(self.grid)

        #Set Button properties (will be replaced by configurable button dimensions)
        self.buttonwidth = width
        self.buttonheight = height

        #Station Identity
        self.button1 = JingleButton(self.buttonwidth, self.buttonheight, [0.8,0.1,0.4], "AG Opener", JINGLE1)
        self.button2 = JingleButton(self.buttonwidth, self.buttonheight, [0.9,0.2,0.5], "AG SID kurz", JINGLE2)
        self.button3 = JingleButton(self.buttonwidth, self.buttonheight, [1.0,0.3,0.6], "AG SID lang", JINGLE3)


	#Jingles
        self.button4 = JingleButton(self.buttonwidth, self.buttonheight, [0.1,0.4,0.1], "Wenn das mit euch..", JINGLE4)

        
	#Infotainment
        self.button5 = JingleButton(self.buttonwidth, self.buttonheight, [0.1,0.5,0.5], "News Presenter", JINGLE5)
        self.button6 = JingleButton(self.buttonwidth, self.buttonheight, [0.1,0.5,0.6], "News Intro", JINGLE6)
        self.button7 = JingleButton(self.buttonwidth, self.buttonheight, [0.1,0.5,0.7], "News Trenner", JINGLE7)
        self.button8 = JingleButton(self.buttonwidth, self.buttonheight, [0.1,0.5,0.9], "Wetter Presenter", JINGLE8)

        self.button9 = JingleButton(self.buttonwidth, self.buttonheight, [0.1,0.4,0.2], "Sicherheitshinweis", JINGLE9)
        self.button10 = JingleButton(self.buttonwidth, self.buttonheight, [0.1,0.4,0.3], "Diskordianischer Sender", JINGLE10)
        self.button11 = JingleButton(self.buttonwidth, self.buttonheight, [0.1,0.4,0.4], "Bin ich im Radio?", JINGLE11)

	#Nachrichten
        self.button13 = JingleButton(self.buttonwidth, self.buttonheight, [0.1,0.5,0.9], "News Intro", JINGLE13)
        self.button14 = JingleButton(self.buttonwidth, self.buttonheight, [0.1,0.5,0.7], "News Trenner", JINGLE14)
        
        self.button15 = JingleButton(self.buttonwidth, self.buttonheight, [0.1,0.1,0.1], "Nur gute Butter", JINGLE15)

        #testarray of buttons
        self.grid.attach(self.button1, 1, 1, 1, 1)
        self.grid.attach(self.button2, 1, 2, 1, 1)
        self.grid.attach(self.button3, 1, 3, 1, 1)
        self.grid.attach(self.button10, 1, 4, 1, 1)
        
        self.grid.attach(self.button4, 2, 1, 1, 1)
        self.grid.attach(self.button9, 2, 2, 1, 1)
        self.grid.attach(self.button11, 2, 3, 1, 1)
        
        self.grid.attach(self.button5, 3, 1, 1, 1)
        self.grid.attach(self.button6, 3, 2, 1, 1)
        self.grid.attach(self.button7, 3, 4, 1, 1)
        self.grid.attach(self.button8, 3, 3, 1, 1)
        self.grid.attach(self.button13, 5, 1, 1, 1)
        self.grid.attach(self.button14, 5, 2, 1, 1)
        self.grid.attach(self.button15, 5, 4, 1, 1)


    def read_config(self, filename):
        pass

    def on_key_press_event(self, widget, event, data=None):
        if (event.keyval == 81):
            Gtk.main_quit()

if __name__=="__main__":

    win = JingleBank(WIDTH, HEIGHT)
    win.connect("delete-event", Gtk.main_quit)
    win.connect("destroy", Gtk.main_quit)
    win.connect('key_press_event', win.on_key_press_event)
    win.show_all()
    Gtk.main()
