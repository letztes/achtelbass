#!/usr/bin/python
# -*- coding: utf-8 -*- 

# Author:       Artur Spengler, letztes@gmail.com
# Description:  Generates music sheet semi-randomly. Especially useful for
#               learning and practicing sight-reading.
# Licence:      GPL
#
# TODO
#   *   In allen Modulen den Klassennamen in CapWords schreiben.
#       http://www.python.org/dev/peps/pep-0008/
#   *   GTK+ Frontend implementieren. Wahrscheinlich in einer neuen Datei,
#       gachtelbass oder so. Diese Datei hier würde dann dort aufgerufen
#       werden und die Werte von gachtelbass übernehmen. Diese Datei hier
#       sollte wohl Werte von außen erwarten, so kann man sie nicht nur mit
#       GTK+, sondern auch als CGI verwenden.
#   *   Klasse implementieren, die aus PMX-Dateien maschinell lernt, welche
#       Intervalle und Rhythmen häufig kombiniert werden. Wahrscheinlich in
#       neuer Datei, würde ja alternativ zu den bisher implementierten
#       Methoden in Pitches und Note_Values verwendet werden. Sie soll
#       Methoden zum Lernen andere zum Generieren enthalten.
#   *   Primen als wählbares Intervall hinzufügen
#   *   MIDI-Input implementieren, damit die Software selbstständig
#       überprüfen kann, ob der Benutzer richtig gespielt hat. Etwa so:
#       http://www.youtube.com/watch?v=dr5_kAQ8OGg
#   *   Grand Staff implementieren: Optional zwei Notensysteme gleichzeitig
#

import note_values
import pitches
import output

import random
import re
import warnings


# Die Reihenfolge ist:
#   * dauern
#   * hoehen (Erwartet Anzahl der Notendauern aus dauern.py)
#   * ausgabe (Erwartet Werte für die Noten aus hoehen.py)
#
# Zuerst werden die Noten-Dauern (Viertelnote usw.) berechnet.
# dauern erwartet 2 Parameter: selectable_note_values, time_signature
#                              [1/2, 1/8]            4/4
#
# TODO Für die Bruchzahlen in note_values und time_signature müssen die
# ints nach floats mit regulären Ausdrücken umgewandelt werden.
# Und nach floats konvertieren! Mit der Methode float().
    
    
class achtelbass(object):
    def __init__(self, parameters):
#        print parameters
        self.Parameters = parameters
        self.Key = parameters['tonic'] + '-' + parameters['mode'] #'f-Dur', f-Major
        self.Intervals = parameters['intervals'].keys() #['Sekunden', 'Terzen']
        self.Min_Pitch = parameters['min_pitch'] #'c3'
        self.Max_Pitch = parameters['max_pitch'] # 'd5'
        self.Rest_Frequency = parameters['rest_frequency'] # 0.25 # 0.01 (very few) till 1 (very every, bad) or 0 (none)
        self.Selectable_Note_Values = parameters['note_values'].keys() # [1.0/4, 1.0/8] # [1.0, 1.0/2, 1.0/4, 1.0/8, 1.0/16, 1.0/32]
        self.Time_Signature = parameters['time_signature'] # 4.0/4
        self.Tuplets = parameters['tuplets'] # 3 # 0 wenn n-Tolen nicht gewünscht sind. besser hier als bei freq.
        self.Tuplets_Frequency = parameters['tuplets_frequency'] # 1 # 0 wenn n-Tolen unerwünscht.

        # Ausgabe immer so gestalten, dass etwa 40 bars, 10 systems pro Seite stehen
        self.Amount_Of_Bars = 81 # 40 bars in 10 systems fit perfectly in 1 page.   
        self.Notes = ["c1", "d1", "e1", "f1", "g1", "a1", "b1", "c2", "d2", "e2", "f2", "g2", "a2", "b2", "c3", "d3", "e3", "f3", "g3", "a3", "b3", "c4", "d4", "e4", "f4", "g4", "a4", "b4", "c5", "d5", "e5", "f5", "g5", "a5", "b5"]
        self.PMX_Note_Values = {
                 0 : 1.0,
                 2 : 1.0/2,
                 4 : 1.0/4,
                 8 : 1.0/8,
                 1 : 1.0/16,
                 3 : 1.0/32,
                }
    
        self.Note_Values = self.get_note_values()
        self.Pitches = self.get_pitches()
        self.Note_String = self.glue_together()
        self.print_out()
    
    
    def get_note_values(self):
        new_note_values = note_values.note_values(self.Selectable_Note_Values, self.Time_Signature)
        for i in range(self.Amount_Of_Bars):
            new_note_values.calculate()
        
        return new_note_values.Result
    
    def get_pitches(self):
        new_pitches = pitches.pitches(len(self.Note_Values), self.Min_Pitch, self.Max_Pitch, self.Key, self.Intervals)
        
        return new_pitches.easy()
    
    
    def glue_together(self):
        
        note_string = ''

        previous_pitch = self.Pitches[0]
        previous_clef = "b"
        for i in range(len(self.Note_Values)):
            if self.Note_Values[i] == "/\n":
                note_string += "/\n"
            else:
                # a rest or a note?
                if random.uniform(0, 1) < self.Rest_Frequency:
                    note_string += 'r'+str(self.Note_Values[i]) + ' '
                else:
                    note_string += re.sub(r'^(.)(.)$', r"\g<1>"+str(self.Note_Values[i])+"\g<2>", self.Pitches[i]) + ' '
                
              # nachfolgender Fall für Vorzeichenwechsel im Fließtext
                if previous_clef == 'b' and self.Notes.index(self.Pitches[i]) > self.Notes.index('d4'):
                    note_string += 'Ct '
                    previous_clef = 't'
                    
                if previous_clef == 't' and self.Notes.index(self.Pitches[i]) < self.Notes.index('b3'):
                    note_string += 'Cb '
                    previous_clef = 'b'
                    
                previous_pitch = self.Pitches[i]
        note_string = re.sub(r"(C[bt] )(/\n)", r"\g<2>\g<1>", note_string)
        note_string = re.sub(r"\n/$", r"", note_string)
        
        return note_string
    
    def print_out(self):
        
        new_output = output.output(self.Key, self.Min_Pitch, self.Max_Pitch, self.Intervals, self.Pitches, self.Note_String, self.Amount_Of_Bars)
        new_output.schreiben()
        
# Ausführen nicht vergessen!
#achtelbass()
