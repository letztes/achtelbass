#!/usr/bin/env python -t
# -*- coding: utf-8 -*-

# Tutorial: http://www.pygtk.org/pygtk2tutorial/
# http://www.pygtk.org/pygtk2tutorial/sec-ToggleButtons.html
# http://www.pygtk.org/pygtk2tutorial/sec-ComboBoxAndComboboxEntry.html

#TODO 
#   *   Die Strings für die Buttons und Menüeinträge in einer Datei als
#       Liste von Paaren speichern. Damit würde die Übersetzungsarbeit
#       erleichtert werden. Die Items werden durch Zeilenumbruch getrennt,
#       die Paare durch eine Leerzeile. Etwa so:
#       Save configuration
#       Einstellungen speichern
#
#       Quit
#       Beenden
#
#       usw.
#   *   Key-Accelerations: Drückt man die Alt-Taste, soll das F in File
#       durch einen Unterstrich hervorgehoben werden. Auch soll durch die
#       F1-Taste die Hilfe geöffnet werden. Wenn es mal so eine Man-Page
#       geben wird.
#   *   Refactoring: Wiederkehrende Aufrufe wie jene beim  Menüeinträge-
#       definieren in nicht-öffentliche __Methoden auslagern.
#   *   In ./achtelbass_gui_draft.html nicht drin, muss aber auch durch
#       graphische Bedienelemente abgedeckt sein: Taktart und Taktauflösung

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
        main_vbox.pack_start(menu_bar, False, False, 0)
        menu_bar.show()

        menu_bar.append(file_menu)
        menu_bar.append(help_menu)


# The actual content of achtelbass programm user interface
# Nested VBoxes are used, so that the title of the widget is displayed above
        content_hbox = gtk.HBox(False, 0)
        content_hbox.show()
        main_vbox.pack_start(content_hbox, False, False, 5)

# Tonic is the first nested VBox
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

        tonic_combo_box.connect("changed", self.select_tonic)
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
        
        mode_combo_box.connect("changed", self.select_mode)
        mode_combo_box.set_active(0) # 'Major' shall be default value

        mode_label = gtk.Label('Mode')
        mode_label.show()
        mode_label.set_alignment(0, 0)
        mode_vbox.pack_start(mode_label, False, False, 2)
        mode_vbox.pack_start(mode_combo_box, False, False, 2)

# Intervals VBox 

        intervals_vbox = gtk.VBox(False, 0)
        intervals_vbox.show()
        content_hbox.pack_start(intervals_vbox)

        intervals_label = gtk.Label('Intervals')
        intervals_label.show()
        intervals_label.set_alignment(0, 0)

        intervals_vbox.pack_start(intervals_label)

        for interval in ('Unison', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Octave'):
            checkbutton = gtk.CheckButton(interval)
            checkbutton.show()
            intervals_vbox.pack_start(checkbutton)
            checkbutton.connect('toggled', self.add_interval, interval)
            if (interval == 'Second'):
                checkbutton.set_active(True)

        self.main_window.show()

# Min pitch VBox

        min_pitch_vbox = gtk.VBox(False, 0)
        min_pitch_vbox.show()
        content_hbox.pack_start(min_pitch_vbox)

        min_pitch_label = gtk.Label('Min pitch')
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
        content_hbox.pack_start(max_pitch_vbox)

        max_pitch_label = gtk.Label('Max pitch')
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
        print widget.get_active_text()

    def select_mode(self, widget):
        print widget.get_active_text()

    def add_interval(self, widget, interval):
        print interval

    def select_min_pitch(self, widget):
        print widget.get_active_text()
# Jedes Mal, wenn die Checkbox angeklickt wird, kommt ein toggled-Signal.
# Dabei ist es gleich, ob das Häkchen gesetzt oder entfernt wird.
# Es muss also eine Routine her, die genauso den Wert für das jeweilige
# Intervall hinzufügt und wieder entfernt.

    def select_max_pitch(self, widget):
        print widget.get_active_text()

def main():
    gtk.main()
    return 0

gachtelbass()
main()
