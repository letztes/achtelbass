#!/usr/bin/env python -t
# -*- coding: utf-8 -*-

# Tutorial: http://www.pygtk.org/pygtk2tutorial/
# http://www.pygtk.org/pygtk2tutorial/sec-ToggleButtons.html
# http://www.pygtk.org/pygtk2tutorial/sec-ComboBoxAndComboboxEntry.html

#TODO 
#   *   Key-Accelerations: Drückt man die Alt-Taste, soll das F in File
#       durch einen Unterstrich hervorgehoben werden. Auch soll durch die
#       F1-Taste die Hilfe geöffnet werden. Wenn es mal so eine Man-Page
#       geben wird.
#   *   Refactoring: Wiederkehrende Aufrufe wie jene beim  Menüeinträge-
#       definieren in nicht-öffentliche __Methoden auslagern.
#   *   Anzahl der Seiten soll in einem Menü (Bearbeiten) einstellbar sein.
#   *   

import pygtk
pygtk.require('2.0')
import gtk

# The achtelbass file contains the actual music generator
import achtelbass

# The locales file contains a dictionary which contains all the strings
# that are displayed on buttons and so. The keys of the dictionary are
# the english terms, the values the terms in the language of choice.
#from locales_de import locales
from locales_en import locales
locales_inverse = dict([[v,k] for k,v in locales.items()])

class gachtelbass(object):
    def __init__(self):
# Parameters that will be passed to the actual achtelbass script
        self.parameters = {'tonic' : '',
                            'mode' : '',
                            'intervals' : {},
                            'min_pitch' : '',
                            'max_pitch' : '',
                            'rest_frequency' : '',
                            'time_signature' : '',
                            'note_values' : {},
                            'tuplets' : '',
                            'tuplets_frequency' : '',
                           }
        self.main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.main_window.set_title("achtelbass")
        self.main_window.connect("delete_event", self.delete_event)

# File menu
        file_submenu = gtk.Menu()

        menu_item_save_configuration = gtk.MenuItem(locales['Save configuration'])
        menu_item_save_configuration.connect("activate", self.save_configuration, locales['Save configuration'])
        menu_item_save_configuration.show()
        file_submenu.append(menu_item_save_configuration)

        menu_item_load_configuration = gtk.MenuItem(locales['Load configuration'])
        menu_item_load_configuration.connect("activate", self.load_configuration, locales['Load configuration'])
        menu_item_load_configuration.show()
        file_submenu.append(menu_item_load_configuration)

        menu_item_quit = gtk.MenuItem(locales['Quit'])
        menu_item_quit.connect("activate", self.delete_event, locales['Quit'])
        menu_item_quit.show()
        file_submenu.append(menu_item_quit)

        file_menu = gtk.MenuItem(locales['File'])
        file_menu.show()
        file_menu.set_submenu(file_submenu)

# Help menu
        help_submenu = gtk.Menu()

        menu_item_about = gtk.MenuItem(locales['About'])
        menu_item_about.connect("activate", self.about_window, 'about')
        menu_item_about.show()
        help_submenu.append(menu_item_about)

        help_menu = gtk.MenuItem(locales['Help'])
        help_menu.show()
        help_menu.set_submenu(help_submenu)

        main_vbox = gtk.VBox(False, 0)
        self.main_window.add(main_vbox)
        main_vbox.show()

        menu_bar = gtk.MenuBar()
        main_vbox.pack_start(menu_bar, False, False, 0)
        menu_bar.show()

        menu_bar.append(file_menu)
        menu_bar.append(help_menu)


# The actual content of achtelbass programm user interface
# Nested VBoxes are used, so that the title of the widget is displayed above
        parameters_hbox = gtk.HBox(False, 0)
        parameters_hbox.show()
        main_vbox.pack_start(parameters_hbox, False, False, 5)

# Tonic is the first nested VBox
        tonic_vbox = gtk.VBox(False, 0)
        tonic_vbox.show()
        parameters_hbox.pack_start(tonic_vbox, False, False, 2)

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

        tonic_combo_box.connect("changed", self.select_tonic)
        tonic_combo_box.set_active(0) # 'C' shall be the default selected
        tonic_label = gtk.Label(locales['Tonic'])
        tonic_label.show()
        tonic_label.set_alignment(0, 0)
        tonic_vbox.pack_start(tonic_label, False, False, 2)
        tonic_vbox.pack_start(tonic_combo_box, False, False, 2)

# Mode VBox 
        
        mode_vbox = gtk.VBox(False, 0)
        mode_vbox.show()
        parameters_hbox.pack_start(mode_vbox, False, False, 2)

        mode_combo_box = gtk.combo_box_new_text()
        mode_combo_box.show()
        mode_combo_box.append_text(locales['Major'])
        mode_combo_box.append_text(locales['Minor'])
        
        mode_combo_box.connect("changed", self.select_mode)
        mode_combo_box.set_active(0) # 'Major' shall be default value

        mode_label = gtk.Label(locales['Mode'])
        mode_label.show()
        mode_label.set_alignment(0, 0)
        mode_vbox.pack_start(mode_label, False, False, 2)
        mode_vbox.pack_start(mode_combo_box, False, False, 2)

# Intervals VBox 

        intervals_vbox = gtk.VBox(False, 0)
        intervals_vbox.show()
        parameters_hbox.pack_start(intervals_vbox, False, False, 2)

        intervals_label = gtk.Label(locales['Intervals'])
        intervals_label.show()
        intervals_label.set_alignment(0, 0)

        intervals_vbox.pack_start(intervals_label, False, False, 2)

#        for interval in ('Unison', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Octave'):
        for interval in (locales['Unison'], locales['Second'], locales['Third'], locales['Fourth'], locales['Fifth'], locales['Sixth'], locales['Seventh'], locales['Octave']):
            checkbutton = gtk.CheckButton(interval)
            checkbutton.show()
            intervals_vbox.pack_start(checkbutton, False, False, 2)
            checkbutton.connect('toggled', self.add_interval, interval)
            if (interval == locales['Second']):
                checkbutton.set_active(True)

        self.main_window.show()

# Min pitch VBox

        min_pitch_vbox = gtk.VBox(False, 0)
        min_pitch_vbox.show()
        parameters_hbox.pack_start(min_pitch_vbox, False, False, 2)

        min_pitch_label = gtk.Label(locales['Min pitch'])
        min_pitch_label.show()
        min_pitch_label.set_alignment(0, 0)

        min_pitch_combo_box = gtk.combo_box_new_text()
        min_pitch_combo_box.show()
        for pitch in ("c1", "d1", "e1", "f1", "g1", "a1", "b1", "c2", "d2", "e2", "f2", "g2", "a2", "b2", "c3", "d3", "e3", "f3", "g3", "a3", "b3", "c4", "d4", "e4", "f4", "g4", "a4", "b4", "c5", "d5", "e5", "f5", "g5", "a5", "b5"):
            min_pitch_combo_box.append_text(pitch)

        min_pitch_combo_box.connect("changed", self.select_min_pitch)
        min_pitch_combo_box.set_active(7)

        min_pitch_vbox.pack_start(min_pitch_label, False, False, 2)
        min_pitch_vbox.pack_start(min_pitch_combo_box, False, False, 2)

# Max pitch VBox

        max_pitch_vbox = gtk.VBox(False, 0)
        max_pitch_vbox.show()
        parameters_hbox.pack_start(max_pitch_vbox, False, False, 2)

        max_pitch_label = gtk.Label(locales['Max pitch'])
        max_pitch_label.show()
        max_pitch_label.set_alignment(0, 0)

        max_pitch_combo_box = gtk.combo_box_new_text()
        max_pitch_combo_box.show()
        for pitch in ("c1", "d1", "e1", "f1", "g1", "a1", "b1", "c2", "d2", "e2", "f2", "g2", "a2", "b2", "c3", "d3", "e3", "f3", "g3", "a3", "b3", "c4", "d4", "e4", "f4", "g4", "a4", "b4", "c5", "d5", "e5", "f5", "g5", "a5", "b5"):
            max_pitch_combo_box.append_text(pitch)

        max_pitch_combo_box.connect("changed", self.select_max_pitch)
        max_pitch_combo_box.set_active(15)

        max_pitch_vbox.pack_start(max_pitch_label, False, False, 2)
        max_pitch_vbox.pack_start(max_pitch_combo_box, False, False, 2)

# Rest frequency VBox
        
        rest_frequency_vbox = gtk.VBox(False, 0)
        rest_frequency_vbox.show()
        parameters_hbox.pack_start(rest_frequency_vbox, False, False, 2)

        rest_frequency_label = gtk.Label(locales['Rest frequency'])
        rest_frequency_label.show()
        rest_frequency_label.set_alignment(0, 0)

        rest_frequency_combo_box = gtk.combo_box_new_text()
        rest_frequency_combo_box.show()
        rest_frequency_combo_box.append_text(locales['no rests'])
        rest_frequency_combo_box.append_text(locales["0.1"])
        rest_frequency_combo_box.append_text(locales["0.2"])
        rest_frequency_combo_box.append_text(locales["0.3"])
        rest_frequency_combo_box.append_text(locales["0.4"])
        rest_frequency_combo_box.append_text(locales["0.5"])

        rest_frequency_combo_box.connect("changed", self.select_rest_frequency)
        rest_frequency_combo_box.set_active(0)

        rest_frequency_vbox.pack_start(rest_frequency_label, False, False, 2)
        rest_frequency_vbox.pack_start(rest_frequency_combo_box, False, False, 2)

# Time signature VBox
        
        time_signature_vbox = gtk.VBox(False, 0)
        time_signature_vbox.show()
        parameters_hbox.pack_start(time_signature_vbox, False, False, 2)

        time_signature_label = gtk.Label(locales['Time signature'])
        time_signature_label.show()
        time_signature_label.set_alignment(0, 0)

        time_signature_combo_box = gtk.combo_box_new_text()
        time_signature_combo_box.show()
        time_signature_combo_box.append_text("2/2")
        time_signature_combo_box.append_text("3/4")
        time_signature_combo_box.append_text("4/4")

        time_signature_combo_box.connect("changed", self.select_time_signature)
        time_signature_combo_box.set_active(2)

        time_signature_vbox.pack_start(time_signature_label, False, False, 2)
        time_signature_vbox.pack_start(time_signature_combo_box, False, False, 2)

# Note value VBox
        
        note_value_vbox = gtk.VBox(False, 0)
        note_value_vbox.show()
        parameters_hbox.pack_start(note_value_vbox, False, False, 2)

        note_value_label = gtk.Label(locales['Note values'])
        note_value_label.show()
        note_value_label.set_alignment(0, 0)

        note_value_vbox.pack_start(note_value_label, False, False, 2)
        
#TODO here: display (vector graphic) images instead of fraction of digits
# for note values
        for note_value in ("1", "1/2", "1/4", "1/8", "1/16", "1/32"):
            checkbutton = gtk.CheckButton(note_value)
            checkbutton.show()
            note_value_vbox.pack_start(checkbutton, False, False, 2)
            checkbutton.connect("toggled", self.add_note_value, note_value)
            if (note_value == "1"):
                checkbutton.set_active(True)


# Tuplet VBox
        
        tuplet_vbox = gtk.VBox(False, 0)
        tuplet_vbox.show()
        parameters_hbox.pack_start(tuplet_vbox, False, False, 2)

        tuplet_label = gtk.Label(locales['Tuplets'])
        tuplet_label.show()
        tuplet_label.set_alignment(0, 0)

        tuplet_combo_box = gtk.combo_box_new_text()
        tuplet_combo_box.show()
        tuplet_combo_box.append_text(locales['no tuplets'])
        tuplet_combo_box.append_text("3")
        tuplet_combo_box.append_text("4")
        tuplet_combo_box.append_text("5")
        tuplet_combo_box.append_text("6")
        tuplet_combo_box.append_text("7")

        tuplet_combo_box.connect("changed", self.select_tuplet)
        tuplet_combo_box.set_active(0)

        tuplet_vbox.pack_start(tuplet_label, False, False, 2)
        tuplet_vbox.pack_start(tuplet_combo_box, False, False, 2)


# Tuplet frequency VBox
        
        tuplet_frequency_vbox = gtk.VBox(False, 0)
        tuplet_frequency_vbox.show()
        parameters_hbox.pack_start(tuplet_frequency_vbox, False, False, 2)

        tuplet_frequency_label = gtk.Label(locales['Tuplet frequency'])
        tuplet_frequency_label.show()
        tuplet_frequency_label.set_alignment(0, 0)

        tuplet_frequency_combo_box = gtk.combo_box_new_text()
        tuplet_frequency_combo_box.show()
        tuplet_frequency_combo_box.append_text(locales['no tuplets'])
        tuplet_frequency_combo_box.append_text("0.1")
        tuplet_frequency_combo_box.append_text("0.2")
        tuplet_frequency_combo_box.append_text("0.3")
        tuplet_frequency_combo_box.append_text("0.4")
        tuplet_frequency_combo_box.append_text("0.5")
        tuplet_frequency_combo_box.append_text("0.6")
        tuplet_frequency_combo_box.append_text("0.7")
        tuplet_frequency_combo_box.append_text("0.8")
        tuplet_frequency_combo_box.append_text("0.9")
        tuplet_frequency_combo_box.append_text("1")

        tuplet_frequency_combo_box.connect("changed", self.select_tuplet_frequency)
        tuplet_frequency_combo_box.set_active(0)

        tuplet_frequency_vbox.pack_start(tuplet_frequency_label, False, False, 2)
        tuplet_frequency_vbox.pack_start(tuplet_frequency_combo_box, False, False, 2)

# The submit button
        submit_box = gtk.HBox(False, 0)
        submit_box.show()
        main_vbox.pack_start(submit_box, False, False, 0)

        submit_button = gtk.Button(locales['Generate'])
        submit_button.show()
        submit_button.connect("clicked", self.execute_achtelbass)
        submit_box.pack_start(submit_button, True, False, 0)

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def save_configuration(self, widget, string):
        pass

    def load_configuration(self, widget, string):
        pass

    def about_window(self, widget, event):
        about_window = gtk.Window()
        about_window.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        about_window.set_transient_for(self.main_window)
#TODO here: Add a short Text about me and a button to close the window.
        about_window.show()

    def select_tonic(self, widget):
        self.parameters['tonic'] = widget.get_active_text()
        print self.parameters['tonic']

    def select_mode(self, widget):
        self.parameters['mode'] = locales_inverse[widget.get_active_text()]
        print self.parameters['mode']

    def add_interval(self, widget, interval):
        if widget.get_active():
            self.parameters['intervals'][locales_inverse[interval]] = True
        else:
            del self.parameters['intervals'][locales_inverse[interval]]
        print self.parameters['intervals']

    def select_min_pitch(self, widget):
        self.parameters['min_pitch'] = widget.get_active_text()
        print self.parameters['min_pitch']

    def select_max_pitch(self, widget):
        self.parameters['max_pitch'] = widget.get_active_text()
        print self.parameters['max_pitch']

    def select_time_signature(self, widget):
        self.parameters['time_signature'] = widget.get_active_text()
        print self.parameters['time_signature']

    def add_note_value(self, widget, note_value):
        if widget.get_active():
            self.parameters['note_values'][note_value] = True
        else:
            del self.parameters['note_values'][note_value]
        print self.parameters['note_values']

    def select_rest_frequency(self, widget):
        self.parameters['rest_frequency'] = locales_inverse[widget.get_active_text()]
        print self.parameters['rest_frequency']

    def select_tuplet(self, widget):
        self.parameters['tuplet'] = locales_inverse[widget.get_active_text()]
        print self.parameters['tuplet']

    def select_tuplet_frequency(self, widget):
        self.parameters['tuplets_frequency'] = locales_inverse[widget.get_active_text()]
        print self.parameters['tuplets_frequency']

# Some parameter values for achtelbass must be numbers, but gtk+ displays
# only strings. So the strings are converted before passed to achtelbass.
# Either here or in achtelbass.
    def execute_achtelbass(self, widget):
        new_achtelbass = achtelbass.achtelbass(self.parameters)

def main():
    gtk.main()
    return 0

gachtelbass()
main()
