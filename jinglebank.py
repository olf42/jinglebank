#!/usr/bin/env python3

from gi.repository import Gtk, GObject
import cairo, math

class JingleButton(Gtk.EventBox):

    #"""This Class describes a single jingle button"""

    def __init__(self, width, height, color, title, jingle):
        Gtk.EventBox.__init__(self)

        self.width = width      # width of the jingle button
        self.height = height    # height of the jingle button
        self.color = color      # color, list with rgb floats 0<=r,g,b<=1
        self.title = title      # title to be displayed
        self.jingle = jingle    # filename of the jingle to be player

        # The DrawingArea is used to display the title and animation
        self.drawarea = Gtk.DrawingArea()
        self.drawarea.set_size_request(self.width,self.height)
        self.drawarea.connect("draw", self.draw)
        self.add(self.drawarea)

        #Connect the EventBox to the click event
        self.connect("button-press-event", self.on_clicked, "Hallo")

        #Only play the animation, when the button is pressed
        self.animation = False

        #set radius depending on button size
        self.radius = math.sqrt((self.width/2)**2+(self.height/2)**2)


    def draw(self, widget, cr):

        cr.set_source_rgb(self.color[0], self.color[1], self.color[2])
        cr.rectangle(0,0,self.width,self.height)
        cr.fill_preserve()

        cr.set_source_rgb(0, 0, 0)
        cr.stroke()

        cr.set_source_rgb(1,1,1)
        cr.select_font_face("Sans")
        cr.set_font_size(20)
        cr.show_text(self.title)

        if self.animation == True:
            cr.translate(self.width/2, self.height/2)
            cr.rotate(-math.pi/2)
            cr.set_source_rgba(1,1,1,0.25)
            cr.move_to(0,0)
            cr.line_to(self.radius,0)
            cr.arc_negative(0,0,self.radius,0,(self.percentage*3.6)*math.pi/180)
            cr.line_to(0,0)
            cr.fill()


    def animate(self):
        self.animation = True
        self.drawarea.queue_draw()
        if self.percentage == 100:
            self.animation = False
            return False
        else:
            self.percentage +=1
            return True

    def on_clicked(self, widget, event, data):
        print(data)
        self.percentage = 0
        GObject.timeout_add(50, self.animate)
        print("Works!")


class JingleBank(Gtk.Window):

    def __init__(self, width, height):
        Gtk.Window.__init__(self, title="JingleBank")

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.buttonwidth = width
        self.buttonheight = height

        self.button1 = JingleButton(self.buttonwidth, self.buttonheight, [0.3,0.7,0.9], "Track 1", "Filename")
        self.button2 = JingleButton(self.buttonwidth, self.buttonheight, [0.4,0.6,0.4], "Track 2", "Filename")
        self.button3 = JingleButton(self.buttonwidth, self.buttonheight, [0.5,0.5,0.3], "Track 3", "Filename")
        self.button4 = JingleButton(self.buttonwidth, self.buttonheight, [0.6,0.4,0.2], "Track 4", "Filename")
        self.button5 = JingleButton(self.buttonwidth, self.buttonheight, [0.7,0.3,0.4], "Track 5", "Filename")
        self.button6 = JingleButton(self.buttonwidth, self.buttonheight, [0.8,0.2,0.3], "Track 6", "Filename")
        self.button7 = JingleButton(self.buttonwidth, self.buttonheight, [0.9,0.1,0.8], "Track 7", "Filename")

        self.grid.attach(self.button1, 1, 1, 1, 1)
        self.grid.attach(self.button2, 1, 2, 1, 1)
        self.grid.attach(self.button3, 2, 1, 1, 1)
        self.grid.attach(self.button4, 2, 2, 1, 1)
        self.grid.attach(self.button5, 3, 1, 1, 1)
        self.grid.attach(self.button6, 3, 2, 1, 1)
        self.grid.attach(self.button7, 3, 3, 1, 1)


if __name__=="__main__":

    win = JingleBank(200, 100)
    win.connect("delete-event", Gtk.main_quit)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
