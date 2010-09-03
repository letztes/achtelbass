#!/usr/bin/env python -t
# example base.py
# Tutorial: http://www.pygtk.org/pygtk2tutorial/
# http://www.pygtk.org/pygtk2tutorial/sec-ToggleButtons.html
# Drop-down-menu: http://www.pygtk.org/pygtk2tutorial/sec-ManualMenuExample.html
# eher: http://www.pygtk.org/docs/pygtk/class-gtkcombobox.html

# Was bisher implementiert ist, braucht man sowieso, nämlich die Menüs für
# "Datei", "Speichern", "Beenden" usw. Dafür ist die menu_bar gut.
# Aber für das normale Drop-Down-Auswählen braucht man eher die Combobox.

import pygtk
pygtk.require('2.0')
import gtk

class gachtelbass(object):
    def __init__(self):
        self.main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.main_window.set_title("achtelbass")
        self.main_window.connect("delete_event", self.delete_event)

        menu_tonic= gtk.Menu()
        for current_tonic in ('C', 'G', 'D', 'A', 'E', 'H', 'Fis', 'Des', 'As', 'Es', 'B', 'F'):
            menu_item = gtk.MenuItem(current_tonic)
            menu_tonic.append(menu_item)
            menu_item.connect("activate", self.select_tonic, current_tonic)
            menu_item.show()

        menu_item_tonic = gtk.MenuItem('Tonic')
        menu_item_tonic.set_submenu(menu_tonic)
        menu_item_tonic.show()

        menu_bar = gtk.MenuBar()
        menu_bar.append(menu_item_tonic)
        menu_bar.show()

        box = gtk.HBox()
        self.main_window.add(box)
        box.show()
        box.pack_start(menu_bar)

        self.main_window.show()
    def select_tonic(self, widget, current_tonic):
        print current_tonic

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    # Man muss sich nun ueberlegen, wie die Elemente angeordnet sein sollen.
# Das heisst, wie die vboxes und hboxes bzw. tabellen verschachtelt werden.

def main():
    gtk.main()
    return 0

gachtelbass()
main()
