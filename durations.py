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

class durations(object):
    def __init__(self, selectable_durations, beat):
        self.Selectable_Durations = selectable_durations
        self.Beat = beat
        self.PMX_Durations = {
                             1.0    : 0,
                             1.0/2  : 2,
                             1.0/4  : 4,
                             1.0/8  : 8,
                             1.0/16 : 1,
                             1.0/32 : 3,
                             }
        self.Result = []
    
    def calculate(self):
        remaining_bar_length = self.Beat # Zum Beispiel 3.0/4 = 0.75
        while remaining_bar_length > 0.0:          
            chosen_duration = random.choice(self.Selectable_Durations)
            if remaining_bar_length - chosen_duration >= 0.0:
                self.Result.append(self.PMX_Durations[chosen_duration])
                remaining_bar_length -= chosen_duration
        self.Result.append("/\n")

##############################################################################



