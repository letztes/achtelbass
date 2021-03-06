#!/usr/bin/python
# -*- coding: utf-8 -*-

#TODO 

import random

class Pitches(object):
    def __init__(self, amount, min_pitch, max_pitch, tonic, intervals, inversion):
        self.Amount = amount
        self.Min_Pitch = min_pitch
        self.Max_Pitch = max_pitch
# Because the accidentals will be set according to the actual tonic name,
# we don't need the sharp or b in the tonic name here.
        self.Tonic = tonic[0] # Tonart
        self.Intervals = intervals
        self.Inversion = inversion
        
        self.Notes = ['c1', 'd1', 'e1', 'f1', 'g1', 'a1', 'b1', 'c2', 'd2', 'e2', 'f2', 'g2', 'a2', 'b2', 'c3', 'd3', 'e3', 'f3', 'g3', 'a3', 'b3', 'c4', 'd4', 'e4', 'f4', 'g4', 'a4', 'b4', 'c5', 'd5', 'e5', 'f5', 'g5', 'a5', 'b5']
        _min_index = self.Notes.index(self.Min_Pitch)
        _max_index = self.Notes.index(self.Max_Pitch)
# Plus one because the slice does not include the element with the _max_index
        self.Selectable_Pitches = self.Notes[_min_index:_max_index+1]
# Find all the notes within selectable span that are a tonic of the key
        tonics = [note for note in self.Selectable_Pitches if note[0] == self.Tonic.lower()]
# If no actual tonic found, take the lowest note in the selectable span
        self.First_Note = self.Selectable_Pitches[0]
# The first found tonic in the selectable span is the first note to print
        if tonics:
            self.First_Note = tonics[0]
        # Im nachfolgenden Dictionary wäre es nicht sinnvoll, zwischen kleinen
        # großen Intervallen zu unterscheiden, weil in den verwendeten
        # Tonleitern die Intervalle an manchen Stellen vorgegebenerweise groß
        # oder klein sind. Es ergibt sich also im Einzelfall von allein und
        # braucht nicht von vornherein definiert zu werden, es reicht wenn man
        # die Intervalle generisch benennt.
        self.Interval_Values = {
                                'Unison' : 0,
                                'Second' : 1,
                                'Third' : 2,
                                'Fourth' : 3,
                                'Fifth' : 4,
                                'Sixth' : 5,
                                'Seventh' : 6,
                                'Octave' : 7,
                               }
        
        self.Result = []
    
    def easy(self):
        _current_pitch = self.First_Note
        _pre_previous_pitch = ''
        self.Result.append(_current_pitch)
        for i in range(self.Amount-1):# -1 weil der erste Ton=Tonika feststeht
            _up_or_down = random.choice(['up', 'down'])
            _current_interval = random.choice(self.Intervals)
            _step = self.Interval_Values[_current_interval]
            if self.Inversion == True:
                if (_up_or_down == 'up' and self.Selectable_Pitches.index(_current_pitch) + _step >= self.Selectable_Pitches.index(self.Selectable_Pitches[-1])) or (_up_or_down == 'down' and self.Selectable_Pitches.index(_current_pitch) - _step < 0):
                    _step = _step - 7

            if _up_or_down == 'up' and self.Selectable_Pitches.index(_current_pitch) + _step <= self.Selectable_Pitches.index(self.Selectable_Pitches[-1]) and _pre_previous_pitch != self.Selectable_Pitches[self.Selectable_Pitches.index(_current_pitch)+_step]:
                _current_pitch = self.Selectable_Pitches[self.Selectable_Pitches.index(_current_pitch)+_step]
            else:
                _up_or_down = 'down'
                
            if _up_or_down == 'down' and _pre_previous_pitch != self.Selectable_Pitches[self.Selectable_Pitches.index(_current_pitch)-_step]:
                if self.Selectable_Pitches.index(_current_pitch) - _step >= 0:
                    _current_pitch = self.Selectable_Pitches[self.Selectable_Pitches.index(_current_pitch)-_step]
                else:
                    _current_pitch = self.Selectable_Pitches[self.Selectable_Pitches.index(_current_pitch)+_step]
            _pre_previous_pitch = _current_pitch
            self.Result.append(_current_pitch)
        return self.Result

