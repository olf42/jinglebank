#!/usr/bin/python3
from gi.repository import Gtk, GObject, Gst
import cairo, math, time
import colorsys
import os.path


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
        cr.set_font_size(18) 
 
        #get extents of text to center it 
        self.extents = cr.text_extents(self.title) 
        cr.move_to(-self.extents[2]/2,-self.extents[3]/2) 
        cr.show_text(self.title) 
 
        if self.active == True: 
            cr.rotate(-math.pi/2) 
            cr.set_source_rgba(1,1,1,0.25) 
            cr.move_to(0,0) 
            cr.line_to(self.radius,0) 
            cr.arc_negative(0,0,self.radius,0,(self.percentage*3.6)*math.pi/180) 
            cr.line_to(0,0) 
            cr.fill() 
 
    def animate(self): 
        if self.active == False: 
            return False 
        else: 
            if self.percentage > 99: 
                self.deactivate() 
                return False 
            else: 
                duration = self.player.query_duration(Gst.Format.TIME) 
                position = self.player.query_position(Gst.Format.TIME) 
                if duration[0] and position[0]: 
                    self.percentage = (position[1] / duration[1]) * 100 
                self.drawarea.queue_draw() 
                return True 
 
    # called when the button is clicked 
    def on_clicked(self, widget, event, data): 
        if not self.active: 
            #self.player.set_state(Gst.State.NULL) 
            self.activate() 
        else: 
            self.deactivate() 
 
    def activate(self): 
        self.active = True 
        self.percentage = 0 
        self.player.set_state(Gst.State.PLAYING) 
        self.id = GObject.timeout_add(50, self.animate) 
 
    def deactivate(self): 
        GObject.source_remove(self.id) 
        self.active = False 
        self.drawarea.queue_draw() 
        self.player.set_state(Gst.State.NULL) 
 
    # called by about-to-finish-event of player 
    def on_finished(self, player): 
        # time.sleep(1) is needed, since about-to-finish is triggered while 
        # file is still playing. Short Samples would then display 
        # no animation at all, and program is likely to crash :( 
        time.sleep(1) 
        self.deactivate() 
 
 
    # called when a message occurs on the bus 
    def on_message(self, bus, message): 
        t = message.type 
        if t == Gst.Message.EOS: 
            self.player.set_state(Gst.State.NULL) 
            self.active = False 
        elif t == Gst.Message.Error: 
            self.player.set_state(Gst.State.NULL) 
            err, debug = message.parse_error() 
            print("Error: %s" % err, debug) 
            self.active = False 

