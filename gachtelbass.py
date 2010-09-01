#!/usr/bin/env python -t
# example base.py
# Tutorial: http://www.pygtk.org/pygtk2tutorial/
# http://www.pygtk.org/pygtk2tutorial/sec-ToggleButtons.html


import pygtk
pygtk.require('2.0')
import gtk

class gachtelbass(object):
    def __init__(self):
       self.window1 = gtk.Window(gtk.WINDOW_TOPLEVEL)
       self.window1.set_title("achtelbass")
       self.window1.connect("delete_event", self.delete_event)

       self.window1.show()

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

def main():
    gtk.main()
    return 0

gachtelbass()
main()
