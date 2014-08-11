#!/usr/bin/env python3

from gi.repository import Gtk, GObject
import cairo, math

#class JingleButton(Gtk.DrawingArea):

class JingleBank(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="JingleBank")

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.width = 200
        self.height = 100

        self.button1 = Gtk.Button(label="Button1")
        self.button2 = Gtk.Button(label="Button2")
        self.button3 = Gtk.Button(label="Button3")
        self.button4 = Gtk.Button(label="Button4")
        self.button5 = Gtk.Button(label="Button5")
        self.button6 = Gtk.Button(label="Button6")
        self.button7 = Gtk.Button(label="Button7")

        self.drawarea = Gtk.DrawingArea()
        self.drawarea.set_size_request(self.width,self.height)
        self.drawarea.connect("draw", self.draw)

        self.evbox = Gtk.EventBox()
        self.evbox.add(self.drawarea)
        self.evbox.connect("button-press-event", self.on_button_clicked, "Hallo")

        self.grid.add(self.button1)
        self.grid.attach(self.button2, 1, 3, 2, 1)
        self.grid.attach_next_to(self.button3, self.button1, Gtk.PositionType.BOTTOM, 1, 2)
        self.grid.attach_next_to(self.button4, self.button3, Gtk.PositionType.RIGHT, 2, 1)
        self.grid.attach(self.button5, 1, 2, 1, 1)
        self.grid.attach_next_to(self.button6, self.button5, Gtk.PositionType.RIGHT, 1, 1)
        self.grid.add(self.button7)
        self.grid.add(self.evbox)

        self.animation = False

        #set radius depending on button size
        self.radius = math.sqrt((self.width/2)**2+(self.height/2)**2)

    def draw(self, widget, cr):

        cr.set_source_rgb(0.2, 0.7, 1)
        cr.rectangle(0,0,self.width,self.height)
        cr.fill_preserve()

        cr.set_source_rgb(0, 0, 0)
        cr.stroke()

        if self.animation == True:
            cr.translate(self.width/2, self.height/2)
            cr.rotate(-math.pi/2)
            cr.set_source_rgba(1,1,1,0.25)
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

    def on_button_clicked(self, widget, event, data):
        print(data)
        self.percentage = 0
        GObject.timeout_add(50, self.animate)
        print("Works!")

if __name__=="__main__":

    win = JingleBank()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
