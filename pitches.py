#!/usr/bin/python
# -*- coding: utf-8 -*-

#TODO Pausen einbauen 

import random

class pitches(object):
    def __init__(self, amount, min_pitch, max_pitch, key, intervals):
        self.Amount = amount
        self.Min_Pitch = min_pitch
        self.Max_Pitch = max_pitch
        self.Key = key # Tonart
        self.Intervals = intervals
        
        self.Notes = ["c1", "d1", "e1", "f1", "g1", "a1", "b1", "c2", "d2", "e2", "f2", "g2", "a2", "b2", "c3", "d3", "e3", "f3", "g3", "a3", "b3", "c4", "d4", "e4", "f4", "g4", "a4", "b4", "c5", "d5", "e5", "f5", "g5", "a5", "b5"]
        _min_index = self.Notes.index(self.Min_Pitch)
        _max_index = self.Notes.index(self.Max_Pitch)
        self.Selectable_Pitches = self.Notes[_min_index:_max_index]
        # Im nachfolgenden Dictionary wäre es nicht sinnvoll, zwischen kleinen
        # großen Intervallen zu unterscheiden, weil in den verwendeten
        # Tonleitern die Intervalle an manchen Stellen vorgegebenerweise groß
        # oder klein sind. Es ergibt sich also im Einzelfall von allein und
        # braucht nicht von vornherein definiert zu werden, es reicht wenn man
        # die Intervalle generisch benennt.
        self.Interval_Values = {
                                'Primen' : 0,
                                'Sekunden' : 1,
                                'Terzen' : 2,
                                'Quarten' : 3,
                                'Quinten' : 4,
                                'Sexten' : 5,
                                'Septimen' : 6,
                                'Oktaven' : 7,
                               }
        
        self.Result = []
    
    def fullrandom(self):
        for i in range(amount):
            _current_pitch = random.choice(self.Selectable_Pitches)
            self.Result.append(_current_pitch)
        return self.Result
    
    def easy(self):
        _current_pitch = self.Selectable_Pitches[0]
        self.Result.append(_current_pitch)
        for i in range(self.Amount-1):# -1 weil der erste Ton=Tonika feststeht
            _up_or_down = random.choice(["up", "down"])
            _current_interval = random.choice(self.Intervals)
            _step = self.Interval_Values[_current_interval]
            if _up_or_down == "up" and self.Selectable_Pitches.index(_current_pitch) + _step <= self.Selectable_Pitches.index(self.Selectable_Pitches[-1]):
                _current_pitch = self.Selectable_Pitches[self.Selectable_Pitches.index(_current_pitch)+_step]
            else:
                _up_or_down = "down"
                
            if _up_or_down == "down":
                if self.Selectable_Pitches.index(_current_pitch) - _step > 0:
                    _current_pitch = self.Selectable_Pitches[self.Selectable_Pitches.index(_current_pitch)-_step]
                else:
                    _current_pitch = self.Selectable_Pitches[self.Selectable_Pitches.index(_current_pitch)+_step]
                    
            self.Result.append(_current_pitch)
        return self.Result

