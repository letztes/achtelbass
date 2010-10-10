#!/usr/bin/env python -t
# -*- coding: utf-8 -*-

#TODO 

import cPickle
import decimal
import gtk
import os
import pygtk
pygtk.require('2.0')

# The achtelbass file contains the actual music generator
import achtelbass

# The locales file contains a dictionary which contains all the strings
# that are displayed on buttons and so. The keys of the dictionary are
# the english terms, the values the terms in the language of choice.
from locales_de import locales
#from locales_en import locales
locales_inverse = dict([[v,k] for k,v in locales.items()])

CONFIGURATION_DIRNAME = os.environ['HOME']+"/.config/achtelbass/"
CONFIGURATION_FILENAME = CONFIGURATION_DIRNAME+"configuration"

class Gachtelbass(object):
    def __init__(self):
        self.Tonics = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F']
        self.Modes = ['Major', 'Minor']
        self.Intervals = ['Unison', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Octave']
        self.Pitches = ["c1", "d1", "e1", "f1", "g1", "a1", "b1", "c2", "d2", "e2", "f2", "g2", "a2", "b2", "c3", "d3", "e3", "f3", "g3", "a3", "b3", "c4", "d4", "e4", "f4", "g4", "a4", "b4", "c5", "d5", "e5", "f5", "g5", "a5", "b5"]
        self.Rest_Frequencies = ['no rests', '0.1', '0.2', '0.3', '0.4', '0.5']
        self.Time_Signatures = ['2/2', '3/4', '4/4']
        self.Note_Values = ["1", "1/2", "1/4", "1/8", "1/16", "1/32"]
        self.Tuplets = ['no tuplets', '2', '3', '4', '5', '6', '7']
        self.Tuplet_Frequencies = ['no tuplets', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1']
# Parameters that will be passed to the actual achtelbass script
        default_parameters = {'tonic' : 'C',
                            'changing_key' : False,
                            'mode' : 'Major',
                            'intervals' : {'Second' : True},
                            'inversion' : False,
                            'min_pitch' : 'c4',
                            'max_pitch' : 'd5',
                            'rest_frequency' : 'no rests',
                            'time_signature' : '4/4',
                            'note_values' : {'1' : True},
                            'tuplets' : 'no tuplets',
                            'tuplet_same_pitch' : False,
                            'tuplets_frequency' : 'no tuplets',
                           }
        self.Fraction_Values = {'2/2' : 1.0,
                                '3/4' : 0.75,
                                '4/4' : 1.0,
                                '1' : 1.0,
                                '1/2' : 0.5,
                                '1/4' : 0.25,
                                '1/8' : 0.125,
                                '1/16' : 0.0625,
                                '1/32' : 0.03125,
                               }  
        try:
            file_object = open(CONFIGURATION_FILENAME, 'r')
            self.parameters = cPickle.load(file_object)
            file_object.close()
        except IOError:
            self.parameters = default_parameters

        for key in default_parameters:
            if key not in self.parameters:
                self.parameters[key] = default_parameters[key]

        self.main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.main_window.set_title("achtelbass")
        self.main_window.connect("delete_event", self.delete_event)

# Create a menu and add acceleration to it
        accel_group = gtk.AccelGroup()
        self.main_window.add_accel_group(accel_group)
# File menu
        file_submenu = gtk.Menu()

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
        menu_item_about.connect("activate", self.about_dialog, 'about')
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
        for tonic in self.Tonics:
            tonic_combo_box.append_text(locales[tonic])

        tonic_combo_box.connect("changed", self.select_tonic)
        tonic_combo_box.set_active(self.Tonics.index(self.parameters['tonic']))
        tonic_label = gtk.Label(locales['Tonic'])
        tonic_label.show()
        tonic_label.set_alignment(0, 0)
        tonic_vbox.pack_start(tonic_label, False, False, 2)
        tonic_vbox.pack_start(tonic_combo_box, False, False, 2)

        # Changing key checkbox   
        checkbutton = gtk.CheckButton(locales['Changing key'])
        checkbutton.show()
        tonic_vbox.pack_start(checkbutton, False, False, 2)
        checkbutton.connect('toggled', self.set_changing_key)
        if 'changing_key' in self.parameters:
            checkbutton.set_active(True)


# Mode VBox 
        
        mode_vbox = gtk.VBox(False, 0)
        mode_vbox.show()
        parameters_hbox.pack_start(mode_vbox, False, False, 2)

        mode_combo_box = gtk.combo_box_new_text()
        mode_combo_box.show()
        for mode in self.Modes:
            mode_combo_box.append_text(locales[mode])
        
        mode_combo_box.connect("changed", self.select_mode)
        mode_combo_box.set_active(self.Modes.index(self.parameters['mode']))

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

        for interval in self.Intervals:
            checkbutton = gtk.CheckButton(locales[interval])
            checkbutton.show()
            intervals_vbox.pack_start(checkbutton, False, False, 2)
            checkbutton.connect('toggled', self.add_interval, interval)
            if (interval in self.parameters['intervals'].keys()):
                checkbutton.set_active(True)

        # Inversion
        checkbutton = gtk.CheckButton(locales['Inversion'])
        checkbutton.show()
        intervals_vbox.pack_start(checkbutton, False, False, 2)
        checkbutton.connect('toggled', self.allow_inversion)
        if self.parameters['inversion'] == True:
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
        for pitch in self.Pitches:
            min_pitch_combo_box.append_text(pitch)
        
        self.previous_min_pitch = self.parameters['min_pitch']
        min_pitch_combo_box.connect("changed", self.select_min_pitch)
        min_pitch_combo_box.set_active(self.Pitches.index(self.parameters['min_pitch']))

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
        for pitch in self.Pitches:
            max_pitch_combo_box.append_text(pitch)

        self.previous_max_pitch = self.parameters['max_pitch']
        max_pitch_combo_box.connect("changed", self.select_max_pitch)
        max_pitch_combo_box.set_active(self.Pitches.index(self.parameters['max_pitch']))

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
        for rest_frequency in self.Rest_Frequencies:
            rest_frequency_combo_box.append_text(locales[rest_frequency])

        rest_frequency_combo_box.connect("changed", self.select_rest_frequency)
        rest_frequency_combo_box.set_active(self.Rest_Frequencies.index(self.parameters['rest_frequency']))

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
        for time_signature in self.Time_Signatures:
            time_signature_combo_box.append_text(time_signature)

        time_signature_combo_box.connect("changed", self.select_time_signature)
        time_signature_combo_box.set_active(self.Time_Signatures.index(self.parameters['time_signature']))

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
        for note_value in self.Note_Values:
            checkbutton = gtk.CheckButton(note_value)
            checkbutton.show()
            note_value_vbox.pack_start(checkbutton, False, False, 2)
            checkbutton.connect("toggled", self.add_note_value, note_value)
            if note_value in self.parameters['note_values'].keys():
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
        for tuplet in self.Tuplets:
            tuplet_combo_box.append_text(locales[tuplet])

        tuplet_combo_box.connect("changed", self.select_tuplet)
        tuplet_combo_box.set_active(self.Tuplets.index(self.parameters['tuplets']))

        tuplet_vbox.pack_start(tuplet_label, False, False, 2)
        tuplet_vbox.pack_start(tuplet_combo_box, False, False, 2)
    # Tuplet same pitch in Tuplet VBox
        
        tuplet_same_pitch_checkbutton = gtk.CheckButton(locales['Same pitch in tuplet'])
        tuplet_same_pitch_checkbutton.show()
        tuplet_vbox.pack_start(tuplet_same_pitch_checkbutton, False, False,2)
        tuplet_same_pitch_checkbutton.connect("toggled", self.set_tuplet_same_pitch)
        if self.parameters['tuplet_same_pitch'] == True:
            tuplet_same_pitch_checkbutton.set_active(True)


# Tuplet frequency VBox
        
        tuplet_frequency_vbox = gtk.VBox(False, 0)
        tuplet_frequency_vbox.show()
        parameters_hbox.pack_start(tuplet_frequency_vbox, False, False, 2)

        tuplet_frequency_label = gtk.Label(locales['Tuplet frequency'])
        tuplet_frequency_label.show()
        tuplet_frequency_label.set_alignment(0, 0)

        tuplet_frequency_combo_box = gtk.combo_box_new_text()
        tuplet_frequency_combo_box.show()
        for tuplet_frequency in self.Tuplet_Frequencies:
            tuplet_frequency_combo_box.append_text(locales[tuplet_frequency])

        tuplet_frequency_combo_box.connect("changed", self.select_tuplet_frequency)
        tuplet_frequency_combo_box.set_active(self.Tuplet_Frequencies.index(self.parameters['tuplets_frequency']))

        tuplet_frequency_vbox.pack_start(tuplet_frequency_label, False, False, 2)
        tuplet_frequency_vbox.pack_start(tuplet_frequency_combo_box, False, False, 2)

# Other widgets like anacrusis checkbox VBox

        others_vbox = gtk.VBox(False, 0)
        others_vbox.show()
        parameters_hbox.pack_start(others_vbox, False, False, 2)

        others_label = gtk.Label(locales['Other parameters'])
        others_label.show()
        others_label.set_alignment(0, 0)
        others_vbox.pack_start(others_label, False, False, 2)

        accents_checkbutton = gtk.CheckButton(locales['Accents'])
        accents_checkbutton.show()
        others_vbox.pack_start(accents_checkbutton, False, False, 2)

        dots_and_ties_checkbutton = gtk.CheckButton(locales['Dots and ties'])
        dots_and_ties_checkbutton.show()
        others_vbox.pack_start(dots_and_ties_checkbutton, False, False, 2)

        anacrusis_checkbutton = gtk.CheckButton(locales['Anacrusis'])
        anacrusis_checkbutton.show()
        others_vbox.pack_start(anacrusis_checkbutton, False, False, 2)


# The submit button
        submit_box = gtk.HBox(False, 0)
        submit_box.show()
        main_vbox.pack_start(submit_box, False, False, 0)

        submit_button = gtk.Button(locales['Generate'], stock=None, use_underline=True)
        submit_button.show()
        submit_button.connect("clicked", self.execute_achtelbass)
        submit_box.pack_start(submit_button, True, False, 0)

    def warning_dialog(self, string):
        dialog = gtk.MessageDialog(self.main_window,
                                   gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_WARNING,
                                   gtk.BUTTONS_CLOSE,
                                   string)
        dialog.run()
        dialog.destroy()

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def save_configuration(self):
        file_object = open(CONFIGURATION_FILENAME, "w")
        cPickle.dump(self.parameters, file_object)
        file_object.close()

    def about_dialog(self, widget, event):
        about_dialog = gtk.AboutDialog()
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_modal(False)
        about_dialog.set_version(achtelbass.version)
        about_dialog.set_license(locales['License text'])
        about_dialog.set_wrap_license(True)
        about_dialog.set_authors([locales['Artur Spengler'] + ' <letztes@gmail.com>'])
        about_dialog.set_comments(locales['Dialog comment'])
        about_dialog.run()
        about_dialog.hide()

# http://www.pygtk.org/docs/pygtk/class-gtkaboutdialog.html

    def select_tonic(self, widget):
        self.parameters['tonic'] = locales_inverse[widget.get_active_text()]
        self.save_configuration()

    def set_changing_key(self, widget):
        if widget.get_active():
            self.parameters['changing_key'] = True
        else:
            self.parameters['changing_key'] = False

    def select_mode(self, widget):
        self.parameters['mode'] = locales_inverse[widget.get_active_text()]
        self.save_configuration()

    def add_interval(self, widget, interval):
        if widget.get_active():
            steps_in_note_span_chosen = abs(self.Pitches.index(self.parameters['max_pitch']) - self.Pitches.index(self.parameters['min_pitch']))
            if self.Intervals.index(interval) > steps_in_note_span_chosen:
                    
                warning_message = locales['Interval too big'] % (locales[interval], self.parameters['min_pitch'], self.parameters['max_pitch'])
                self.warning_dialog(warning_message)
                widget.set_active(False)
            else:
                self.parameters['intervals'][interval] = True
                widget.set_active(True)
        else:
# Checking is necessary because this method indirectly calls itself to uncheck bad interval in case interval does not fit into the span between min_pitch and max_pitch
            if interval in self.parameters['intervals'].keys():
                del self.parameters['intervals'][interval]
                if not self.parameters['intervals']:
                    warning_message = locales['All intervals unselected']
                    self.warning_dialog(warning_message)
                    self.parameters['intervals'][interval] = True
                    widget.set_active(True)

        self.save_configuration()


    def allow_inversion(self, widget):
        if widget.get_active():
            self.parameters['inversion'] = True
        else:
            self.parameters['inversion'] = False
        self.save_configuration()
      

    def select_min_pitch(self, widget):
        self.parameters['min_pitch'] = widget.get_active_text()
        steps_in_note_span_chosen = abs(self.Pitches.index(self.parameters['max_pitch']) - self.Pitches.index(self.parameters['min_pitch']))
# This list comprehension is necessary because the keys of parameters['intevals'] alone are not sorted properly
        names_of_chosen_intervals = [interval for interval in self.Intervals if interval in self.parameters['intervals'].keys()]
        greatest_interval_chosen = names_of_chosen_intervals[-1]
        steps_in_note_span_chosen = abs(self.Pitches.index(self.parameters['max_pitch']) - self.Pitches.index(self.parameters['min_pitch']))
        if steps_in_note_span_chosen >= self.Intervals.index(greatest_interval_chosen):
            self.previous_min_pitch = self.parameters['min_pitch']
        else:
            warning_message = "Interval "+greatest_interval_chosen+" does not fit between "+self.parameters['min_pitch']+" and "+self.parameters['max_pitch']+".\nPlease choose either a smaller interval or a greater span between minimum pitch and maximum pitch."
            self.warning_dialog(warning_message)
            widget.set_active(self.Pitches.index(self.previous_min_pitch))
            self.parameters['min_pitch'] = self.previous_min_pitch
        self.save_configuration()


    def select_max_pitch(self, widget):
        self.parameters['max_pitch'] = widget.get_active_text()
        steps_in_note_span_chosen = abs(self.Pitches.index(self.parameters['max_pitch']) - self.Pitches.index(self.parameters['min_pitch']))
# This list comprehension is necessary because the keys of parameters['intevals'] alone are not sorted properly
        names_of_chosen_intervals = [interval for interval in self.Intervals if interval in self.parameters['intervals'].keys()]
        greatest_interval_chosen = names_of_chosen_intervals[-1]
        steps_in_note_span_chosen = abs(self.Pitches.index(self.parameters['max_pitch']) - self.Pitches.index(self.parameters['min_pitch']))
        if steps_in_note_span_chosen >= self.Intervals.index(greatest_interval_chosen):
            self.previous_max_pitch = self.parameters['max_pitch']
        else:
            warning_message = "Interval "+greatest_interval_chosen+" does not fit between "+self.parameters['min_pitch']+" and "+self.parameters['max_pitch']+".\nPlease choose either a smaller interval or a greater span between minimum pitch and maximum pitch."
            self.warning_dialog(warning_message)
            widget.set_active(self.Pitches.index(self.previous_max_pitch))
            self.parameters['max_pitch'] = self.previous_max_pitch
        self.save_configuration()


    def select_time_signature(self, widget):
        previous_time_signature = self.parameters['time_signature']
        self.parameters['time_signature'] = widget.get_active_text()
        if not self.is_note_value_and_time_signature_ok():
            warning_message = locales['Bad time signature.']
            self.warning_dialog(warning_message)
            widget.set_active(self.Time_Signatures.index(previous_time_signature))
        self.save_configuration()

    def add_note_value(self, widget, note_value):
        if widget.get_active():
            self.parameters['note_values'][note_value] = True
            if not self.is_note_value_and_time_signature_ok():
                warning_message = locales['Bad note value.']
                self.warning_dialog(warning_message)
                widget.set_active(False)
        else:
            del self.parameters['note_values'][note_value]
            if not self.parameters['note_values']:
                warning_message = locales['All note values unselected']
                self.warning_dialog(warning_message)
                self.parameters['note_values'][note_value] = True
                widget.set_active(True)
            if not self.is_note_value_and_time_signature_ok():
# If time signature is not divisible by 1/2 and note value is 1/2
                warning_message  = locales["Bad note value."]
                self.warning_dialog(warning_message)
                widget.set_active(True)
        self.save_configuration()

    def is_note_value_and_time_signature_ok(self):
# Need to determine the critical note_values first
        good_note_values = 0
        bad_note_values = 0
        for current_note_value in self.parameters['note_values']:
            if decimal.Decimal(str(self.Fraction_Values[self.parameters['time_signature']])).remainder_near(decimal.Decimal(str(self.Fraction_Values[current_note_value]))):
                bad_note_values += 1
            else:
                good_note_values += 1

        if good_note_values:
            return True
        else:
            return False


    def select_rest_frequency(self, widget):
        self.parameters['rest_frequency'] = locales_inverse[widget.get_active_text()]
        self.save_configuration()

    def select_tuplet(self, widget):
        self.parameters['tuplets'] = locales_inverse[widget.get_active_text()]
        self.save_configuration()

    def set_tuplet_same_pitch(self, widget):
        if widget.get_active():
            self.parameters['tuplet_same_pitch'] = True
        else:
            self.parameters['tuplet_same_pitch'] = False
        self.save_configuration()

    def select_tuplet_frequency(self, widget):
        self.parameters['tuplets_frequency'] = locales_inverse[widget.get_active_text()]
        self.save_configuration()

# Some parameter values for achtelbass must be numbers, but gtk+ displays
# only strings. So the strings are converted before passed to achtelbass.
# Either here or in achtelbass.
    def execute_achtelbass(self, widget):
# Zunächst die Konfiguration in eine Datei schreiben
        if not os.path.exists(CONFIGURATION_DIRNAME):
            os.makedirs(CONFIGURATION_DIRNAME)
        new_achtelbass = achtelbass.Achtelbass(self.parameters, locales)

def main():
    gtk.main()
    return 0

Gachtelbass()
main()
