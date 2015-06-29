#!/usr/bin/env python3

from jinglebutton import JingleButton		#Button
from gi.repository import Gtk, GObject, Gst, Gdk
import cairo, math, time
import colorsys
import os.path
import json					#JSON for config

#Button size

WIDTH = 200
HEIGHT = 180

class JingleBank(Gtk.Window):

    def __init__(self, width, height):
        Gtk.Window.__init__(self, title="JingleBank (Shift Q: quit)")
        self.read_config()
        self.buttons = []
        Gst.init()

        #Grid to organize the Buttons
        self.grid = Gtk.Grid()
        self.add(self.grid)

        #Set Button properties (will be replaced by configurable button dimensions)
        self.buttonwidth = width
        self.buttonheight = height

        

        for button in self.data['Jingles']:
            print(button)
            self.buttons.append(JingleButton(int(self.buttonwidth), int(self.buttonheight), button['ButtonColor'], button['ButtonName'],button['Filename']))
            self.grid.attach(self.buttons[len(self.buttons)-1],  int(button['XPosition']), int(button['YPosition']), 1, 1)

    def read_config(self, filename='jinglebank.json'):
        with open(filename) as data_file:    
            self.data = json.load(data_file)

    def on_key_press_event(self, widget, event, data=None):
       """ press Shift Q to exit """ 
       if (event.keyval == 81):
            Gtk.main_quit()

if __name__=="__main__":

    win = JingleBank(WIDTH, HEIGHT)
    win.connect("delete-event", Gtk.main_quit)
    win.connect("destroy", Gtk.main_quit)
    win.connect('key_press_event', win.on_key_press_event)
    win.show_all()
    Gtk.main()
