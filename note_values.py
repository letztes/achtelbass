#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO: 
#   *   Optionale Punktierungen 
#       ein Viertel+Achtel c4 gefolgt von einem Achtel d4 schreibt man als c44d d8
#   *   Optionale Bindebögen
#       Buchstabe t, mit Leerzeichen getrennt, jeweils hinter die Note, an der
#       der Bindebogen beginnt und noch ein t hinter der Note, wo er endet.
#       

import random

class NoteValues(object):
    def __init__(self, selectable_note_values, time_signature, tuplets, tuplets_frequency):
        self.Selectable_Note_Values = selectable_note_values
        self.Time_Signature = time_signature
        self.Tuplets = tuplets
        self.Tuplets_Frequency = tuplets_frequency
        self.PMX_Note_Values = {
                             1.0    : 0,
                             1.0/2  : 2,
                             1.0/4  : 4,
                             1.0/8  : 8,
                             1.0/16 : 1,
                             1.0/32 : 3,
                             }
        self.Result = []
    
    def calculate(self):
        remaining_bar_length = self.Time_Signature # Zum Beispiel 3.0/4 = 0.75
        selectable_note_values_in_this_bar = self.Selectable_Note_Values
        pmx_note_value = ''
        while remaining_bar_length > 0.0:
            selectable_note_values_in_this_bar = [selectable_note_values_in_this_bar[selectable_note_values_in_this_bar.index(item)] for item in selectable_note_values_in_this_bar if item <= remaining_bar_length]
            chosen_note_value = random.choice(selectable_note_values_in_this_bar)
            print chosen_note_value, remaining_bar_length
            pmx_note_value = self.PMX_Note_Values[chosen_note_value]
            if self.Tuplets != 0:
                if random.uniform(0, 1) < float(self.Tuplets_Frequency):
                    pmx_note_value = str(pmx_note_value) + self.Tuplets
            self.Result.append(pmx_note_value)
            remaining_bar_length -= chosen_note_value
        self.Result.append("/\n")

##############################################################################



