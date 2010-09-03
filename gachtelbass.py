#!/usr/bin/env python -t
# -*- coding: utf-8 -*-

# Tutorial: http://www.pygtk.org/pygtk2tutorial/
# http://www.pygtk.org/pygtk2tutorial/sec-ToggleButtons.html
# http://www.pygtk.org/pygtk2tutorial/sec-ComboBoxAndComboboxEntry.html

#TODO Callback-Funktionen der ComboBox-Widgets, zunächst für Tonic-Auswahl
# Und natürlich die anderen Bedienelemente wie in
# ./achtelbass_gui_draft.html dargestellt implementieren
import pygtk
pygtk.require('2.0')
import gtk

class gachtelbass(object):
    def __init__(self):
        self.main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.main_window.set_title("achtelbass")
        self.main_window.connect("delete_event", self.delete_event)

# File menu
        file_submenu = gtk.Menu()

        menu_item_save_configuration = gtk.MenuItem('Save configuration')
        menu_item_save_configuration.connect("activate", self.save_configuration, 'Save configuration')
        menu_item_save_configuration.show()
        file_submenu.append(menu_item_save_configuration)

        menu_item_load_configuration = gtk.MenuItem('Load configuration')
        menu_item_load_configuration.connect("activate", self.load_configuration, 'Load configuration')
        menu_item_load_configuration.show()
        file_submenu.append(menu_item_load_configuration)

        menu_item_quit = gtk.MenuItem('Quit')
        menu_item_quit.connect("activate", self.delete_event, 'Quit')
        menu_item_quit.show()
        file_submenu.append(menu_item_quit)

        file_menu = gtk.MenuItem('File')
        file_menu.show()
        file_menu.set_submenu(file_submenu)

# Help menu
        help_submenu = gtk.Menu()

        menu_item_about = gtk.MenuItem('About')
        menu_item_about.connect("activate", self.about_window, 'about')
        menu_item_about.show()
        help_submenu.append(menu_item_about)

        help_menu = gtk.MenuItem('Help')
        help_menu.show()
        help_menu.set_submenu(help_submenu)

        main_vbox = gtk.VBox(False, 0)
        self.main_window.add(main_vbox)
        main_vbox.show()

        menu_bar = gtk.MenuBar()
        main_vbox.pack_start(menu_bar, False, False, 2)
        menu_bar.show()

        menu_bar.append(file_menu)
        menu_bar.append(help_menu)


# The actual content of achtelbass programm user interface
# Nested VBoxes are used, so that the title of the widget is displayed above
        content_hbox = gtk.HBox(False, 0)
        content_hbox.show()
        main_vbox.pack_start(content_hbox)

# Tonic is the first nestex VBox
        tonic_vbox = gtk.VBox(False, 0)
        tonic_vbox.show()
        content_hbox.pack_start(tonic_vbox)

        tonic_combo_box = gtk.combo_box_new_text()
        tonic_combo_box.show()
        tonic_combo_box.append_text('C')
        tonic_combo_box.append_text('G')
        tonic_combo_box.append_text('D')
        tonic_combo_box.append_text('A')
        tonic_combo_box.append_text('E')
        tonic_combo_box.append_text('H')
        tonic_combo_box.append_text('Fis')
        tonic_combo_box.append_text('Ges')
        tonic_combo_box.append_text('Des')
        tonic_combo_box.append_text('As')
        tonic_combo_box.append_text('Es')
        tonic_combo_box.append_text('B')
        tonic_combo_box.append_text('F')

        tonic_combo_box.connect("changed", self.select_tonic, tonic_combo_box.get_active())
        tonic_combo_box.set_active(0) # 'C' shall be the default selected
        tonic_label = gtk.Label('Tonic')
        tonic_label.show()
        tonic_label.set_alignment(0, 0)
        tonic_vbox.pack_start(tonic_label, False, False, 2)
        tonic_vbox.pack_start(tonic_combo_box, False, False, 2)

# Mode VBox 
        
        mode_vbox = gtk.VBox(False, 0)
        mode_vbox.show()
        content_hbox.pack_start(mode_vbox)

        mode_combo_box = gtk.combo_box_new_text()
        mode_combo_box.show()
        mode_combo_box.append_text('Major')
        mode_combo_box.append_text('Minor')

        mode_combo_box.set_active(0) # 'Major' shall be default value

        mode_label = gtk.Label('Mode')
        mode_label.show()
        mode_label.set_alignment(0, 0)
        mode_vbox.pack_start(mode_label, False, False, 2)
        mode_vbox.pack_start(mode_combo_box, False, False, 2)

# Intervals VBox 
# Intervals are not a dropdown combo_box, but checkboxes.

        intervals_vbox = gtk.VBox(False, 0)
        intervals_vbox.show()
        content_hbox.pack_start(intervals_vbox)

        intervals_label = gtk.Label('Intervals')
        intervals_label.show()
        intervals_label.set_alignment(0, 0)

        for interval in ('Unison', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Octave'):
            button = gtk.CheckButton(interval)
            button.connect('toggled', self.add_interval, interval)

        intervals_vbox.pack_start(intervals_label)


        self.main_window.show()

    def save_configuration(self, widget, string):
        pass

    def load_configuration(self, widget, string):
        pass

    def select_tonic(self, widget, current_tonic):
        print 'test'
        print current_tonic

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def about_window(self, widget, event):
        about_window = gtk.Window()
        about_window.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        about_window.set_transient_for(self.main_window)
#TODO here: Add a short Text about me and a button to close the window.
        about_window.show()

    def select_mode(self, widget, string):
        pass

    def add_interval(self, widget, string):
        pass


def main():
    gtk.main()
    return 0

gachtelbass()
main()
