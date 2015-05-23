#!/usr/bin/env python3

from gi.repository import Gtk, GObject, Gst
import sys, time
import cairo, math, time
import colorsys
import os.path

Gst.init()

#Button size

WIDTH = 200
HEIGHT = 200

TESTFILE = os.path.join("testraffel", "hauptuhr.mp3")

class JingleButton(Gtk.EventBox):

    #"""This Class describes a single jingle button"""

    def __init__(self, width, height, color, title, jingle):
        Gtk.EventBox.__init__(self)


        self.width = width      # width of the jingle button
        self.height = height    # height of the jingle button
        self.color = color      # color, list with rgb floats 0<=r,g,b<=1
        self.title = title      # title to be displayed
        self.jingle = "file://" + os.path.join(os.path.dirname(os.path.abspath(__file__)), jingle)    # filename of the jingle to be player

        # The DrawingArea is used to display the title and animation
        self.drawarea = Gtk.DrawingArea()
        self.drawarea.set_size_request(self.width,self.height)
        self.drawarea.connect("draw", self.draw)
        self.add(self.drawarea)

        #Connect the EventBox to the click event
        self.connect("button-press-event", self.on_clicked, "Hallo")

        #Only play the animation, when the button is pressed
        self.active = False
        self.position = 0

        #set radius depending on button size
        self.radius = math.sqrt((self.width/2)**2+(self.height/2)**2)

        #initialize the player
        self.player = Gst.ElementFactory.make("playbin", "player")
        self.player.set_property('uri', self.jingle)
        #self.player.connect("about_to_finish", self.on_finished)
        #bus = self.player.get_bus()

    def draw(self, widget, cr):
        cr.set_source_rgb(self.color[0], self.color[1], self.color[2])
        cr.rectangle(0,0,self.width,self.height)
        cr.fill_preserve()

        cr.set_source_rgb(0, 0, 0)
        cr.stroke()

        #move origin to center of Drawingarea
        cr.translate(self.width/2, self.height/2)

        cr.set_source_rgb(1,1,1)
        cr.select_font_face("Sans")
        cr.set_font_size(20)

        #get extents of text to center it
        self.extents = cr.text_extents(self.title)
        cr.move_to(-self.extents[2]/2,-self.extents[3]/2)
        cr.show_text(self.title)

    # called when the button is clicked
    def on_clicked(self, widget, event, data):
        if not self.active:
            self.activate()
        else:
            self.deactivate()

    def activate(self):
        self.active = True
        self.percentage = 0
        self.player.set_state(Gst.State.PLAYING)

    def deactivate(self):
        self.active = False
        self.drawarea.queue_draw()
        self.player.set_state(Gst.State.NULL)

class JingleBank(Gtk.Window):

    def __init__(self, width, height):
        Gtk.Window.__init__(self, title="JingleBank")

        #Grid to organize the Buttons
        self.grid = Gtk.Grid()
        self.add(self.grid)

        #Set Button properties (will be replaced by configurable button dimensions)
        self.buttonwidth = width
        self.buttonheight = height
    
        #create buttons (will be read from configfile in the future)
        self.button1 = JingleButton(self.buttonwidth, self.buttonheight, [0.3,0.7,0.9], "Track 1", TESTFILE)
        self.button2 = JingleButton(self.buttonwidth, self.buttonheight, [0.4,0.6,0.4], "Track 2", TESTFILE)
        self.button3 = JingleButton(self.buttonwidth, self.buttonheight, [0.5,0.5,0.3], "Track 3", TESTFILE)
        self.button4 = JingleButton(self.buttonwidth, self.buttonheight, [0.6,0.4,0.2], "Track 4", TESTFILE)
        self.button5 = JingleButton(self.buttonwidth, self.buttonheight, [0.7,0.3,0.4], "Track 5", TESTFILE)
        self.button6 = JingleButton(self.buttonwidth, self.buttonheight, [0.8,0.2,0.3], "Track 6", TESTFILE)
        self.button7 = JingleButton(self.buttonwidth, self.buttonheight, [0.9,0.1,0.8], "Track 7", TESTFILE)

        #testarray of buttons
        self.grid.attach(self.button1, 1, 1, 1, 1)
        self.grid.attach(self.button2, 1, 2, 1, 1)
        self.grid.attach(self.button3, 2, 1, 1, 1)
        self.grid.attach(self.button4, 2, 2, 1, 1)
        self.grid.attach(self.button5, 3, 1, 1, 1)
        self.grid.attach(self.button6, 3, 2, 1, 1)
        self.grid.attach(self.button7, 3, 3, 1, 1)

    def read_config(self, filename):
        pass

#our stream to play

def on_finished(player):
  print("Das ist das Ende")
  #sys.exit(0)
  i=30
i = 0

music_stream_uri = 'file:///home/olf/Code/jinglebank/testraffel/hauptuhr.mp3'
#creates a playbin (plays media form an uri)
#start playing

if __name__=="__main__":

    win = JingleBank(WIDTH, HEIGHT)
    win.connect("delete-event", Gtk.main_quit)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
