#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO: 
#   *   Optionale n-Tolen
#       Triole mit der Gesamtdauer einer Viertel aus c4, d4 und e4 schreibt man als c44x3 d4 e4
#   *   Optionale Punktierungen 
#       ein Viertel+Achtel c4 gefolgt von einem Achtel d4 schreibt man als c44d d8
#   *   Optionale Bindebögen
#       Buchstabe t, mit Leerzeichen getrennt, jeweils hinter die Note, an der
#       der Bindebogen beginnt und noch ein t hinter der Note, wo er endet.
#       

import random

class note_values(object):
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
        pmx_note_value = ''
        while remaining_bar_length > 0.0:          
            chosen_note_value = random.choice(self.Selectable_Note_Values)
            if remaining_bar_length - chosen_note_value >= 0.0:
                if self.Selectable_Note_Values.index(chosen_note_value) > 0:
                    pmx_note_value = self.PMX_Note_Values[chosen_note_value]
                    if self.Tuplets != 0:
                        if random.uniform(0, 1) < self.Tuplets_Frequency:
                            pmx_note_value = self.Tuplets
                self.Result.append(pmx_note_value)
                remaining_bar_length -= chosen_note_value
        self.Result.append("/\n")

##############################################################################



