#!/usr/bin/python
# -*- coding: utf-8 -*- 

# Author:       Artur Spengler, letztes@gmail.com
# Description:  Generates music sheet semi-randomly. Especially useful for
#               learning and practicing sight-reading.
# Licence:      GPL
#
# TODO
#   Wichtiges
#   *   In note_values.py wird Unsinn berechnet: ['', '', 2, '/\n', '', '', '', '', '/\n', '', 2, 2, '/\n', 2, 2, 2, '/\n' usw. Ausprobiert mit Halben
#       und Vierteln.
#   Großes
#   *   Klasse implementieren, die aus PMX-Dateien maschinell lernt, welche
#       Intervalle und Rhythmen häufig kombiniert werden. Wahrscheinlich in
#       neuer Datei, würde ja alternativ zu den bisher implementierten
#       Methoden in Pitches und Note_Values verwendet werden. Sie soll
#       Methoden zum Lernen andere zum Generieren enthalten.
#   *   MIDI-Input implementieren, damit die Software selbstständig
#       überprüfen kann, ob der Benutzer richtig gespielt hat. Etwa so:
#       http://www.youtube.com/watch?v=dr5_kAQ8OGg
#   *   Grand Staff implementieren: Optional zwei Notensysteme gleichzeitig
#   *   n-Tolen implementieren
#
#   Eher kleines
#   *   In allen Modulen den Klassennamen in CapWords schreiben.
#       http://www.python.org/dev/peps/pep-0008/
#   *   Wenn direkt auf Kommandozeile aufgerufen, soll mit getopts params
#       geholt werden
#

import os
import random
import re
import warnings

import note_values
import pitches
import output


# Die Reihenfolge ist:
#   * dauern
#   * hoehen (Erwartet Anzahl der Notendauern aus dauern.py)
#   * ausgabe (Erwartet Werte für die Noten aus hoehen.py)
#
# Zuerst werden die Noten-Dauern (Viertelnote usw.) berechnet.
# dauern erwartet 2 Parameter: selectable_note_values, time_signature
#                              [1/2, 1/8]            4/4
#
    
    
class achtelbass(object):
    def __init__(self, parameters):
        self.Parameters = parameters
        self.Frequency_Values = {'no tuplets' : 0,
                                 'no rests' : 0,
                                 '0.1' : 0.1,
                                 '0.2' : 0.2,
                                 '0.3' : 0.3,
                                 '0.4' : 0.4,
                                 '0.5' : 0.5,
                                 '0.6' : 0.6,
                                 '0.7' : 0.7,
                                 '0.8' : 0.8,
                                 '0.9' : 0.9,
                                 '1' : 1,
                                 '2' : 2,
                                 '3' : 3,
                                 '4' : 4,
                                 '5' : 5,
                                 '6' : 6,
                                 '7' : 7,
                                 '8' : 8,
                                 '9' : 9,
                                }
        self.Tuplets_Values = {'no tuplets' : 0,
                                '2' : 'x2',
                                '3' : 'x3',
                                '4' : 'x4',
                                '5' : 'x5',
                                '6' : 'x6',
                                '7' : 'x7',
                                '8' : 'x8',
                                '9' : 'x9',
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
        self.PMX_Note_Values = {
                                 0 : 1.0,
                                 2 : 1.0/2,
                                 4 : 1.0/4,
                                 8 : 1.0/8,
                                 1 : 1.0/16,
                                 3 : 1.0/32,
                                }
    
        self.Key = parameters['tonic'] + '-' + parameters['mode']
        self.Intervals = parameters['intervals'].keys()
        self.Min_Pitch = parameters['min_pitch']
        self.Max_Pitch = parameters['max_pitch']
        self.Rest_Frequency = self.Frequency_Values[parameters['rest_frequency']]
        self.Selectable_Note_Values = [self.Fraction_Values[note_value] for note_value in parameters['note_values'].keys()]
        self.Selectable_Note_Values.sort()

        match = re.search('(\d)/(\d)', parameters['time_signature'])
        self.Time_Signature_Numerator = match.group(1)
        self.Time_Signature_Denominator = match.group(2)
        self.Time_Signature = self.Fraction_Values[parameters['time_signature']]
        self.Tuplets = self.Tuplets_Values[parameters['tuplets']]
        self.Tuplets_Frequency = parameters['tuplets_frequency']

        # Ausgabe immer so gestalten, dass etwa 40 bars, 10 systems pro Seite stehen
        self.Amount_Of_Bars = 81 # 40 bars in 10 systems fit perfectly in 1 page.   
        self.Notes = ["c1", "d1", "e1", "f1", "g1", "a1", "b1", "c2", "d2", "e2", "f2", "g2", "a2", "b2", "c3", "d3", "e3", "f3", "g3", "a3", "b3", "c4", "d4", "e4", "f4", "g4", "a4", "b4", "c5", "d5", "e5", "f5", "g5", "a5", "b5"]
        self.Note_Values = self.get_note_values()
        self.Pitches = self.get_pitches()
        self.Note_String = self.glue_together()
        self.display()
    
    
    def get_note_values(self):
        new_note_values = note_values.note_values(self.Selectable_Note_Values, self.Time_Signature, self.Tuplets, self.Tuplets_Frequency)
        for i in range(self.Amount_Of_Bars):
            new_note_values.calculate()
        
        return new_note_values.Result
    
    def get_pitches(self):
#TODO Berechnen, wie viele pitches berechnet werden müssen: Anzahl der Elemente
# in der Note_Values Liste plus Summe der Multiolen.
        amount = len(self.Note_Values)
        for note_value in self.Note_Values:
            if isinstance(note_value, str) and note_value.count('x'):
                tuplet_value = note_value[2:len(note_value)]
                amount += int(tuplet_value)

        new_pitches = pitches.pitches(amount, self.Min_Pitch, self.Max_Pitch, self.Key, self.Intervals)
        
        return new_pitches.easy()
    
    
    def glue_together(self):
        
        note_string = ''

        previous_pitch = self.Pitches[0]
        previous_clef = "b"
        j = 0 # separate iterator for pitches. 
        for i in range(len(self.Note_Values)):
            if self.Note_Values[i] == "/\n":
                note_string += "/\n"
            else:
                if isinstance(self.Note_Values[i], str) and self.Note_Values[i].count('x'): # Falls Multiole
#An dieser Stelle, das heißt als erste Note in der Multiolengruppe, kommt
# bisweilen keine Pause vor. Muss man ändern. Überhaupt ist in den
# Multiolen noch keine Pause möglich.
                    match = re.search('(\d)x(\d)', self.Note_Values[i])
                    j += 1
                    note_value_for_tuplet = int(match.group(1))
                    tuplet_remain = int(self.Note_Values[i][2])
                    note_string += self.Pitches[j][0] + self.Note_Values[i][0] + self.Pitches[j][1] + self.Note_Values[i][1:3] + ' '
                    while tuplet_remain > 1:
                        if random.uniform(0, 1) < self.Rest_Frequency:
                            note_string += 'r '
                        else:
                            note_string += self.Pitches[j] + ' '
                            j += 1
                        tuplet_remain -= 1

                else:
                    # a rest or a note?
                    if random.uniform(0, 1) < self.Rest_Frequency:
                        note_string += 'r'+str(self.Note_Values[i]) + ' '
                    else:
#                        note_string += re.sub(r'^(.)(.)$', r"\g<1>"+str(self.Note_Values[i])+"\g<2>", self.Pitches[j]) + ' '# not efficient.
                        note_string += self.Pitches[j][0] + str(self.Note_Values[i]) + self.Pitches[j][1] + ' '
                        j += 1
                
              # nachfolgender Fall für Vorzeichenwechsel im Fließtext
                if previous_clef == 'b' and self.Notes.index(self.Pitches[j]) > self.Notes.index('d4'):
                    note_string += 'Ct '
                    previous_clef = 't'
                    
                if previous_clef == 't' and self.Notes.index(self.Pitches[j]) < self.Notes.index('b3'):
                    note_string += 'Cb '
                    previous_clef = 'b'
                    
                previous_pitch = self.Pitches[j]
        note_string = re.sub(r"(C[bt] )(/\n)", r"\g<2>\g<1>", note_string)
        note_string = re.sub(r"\n/$", r"", note_string)
        
        return note_string
    
    def display(self):
        
        new_output = output.output(self.Key, self.Min_Pitch, self.Max_Pitch, self.Intervals, self.Pitches, self.Note_String, self.Amount_Of_Bars, self.Time_Signature_Numerator, self.Time_Signature_Denominator)
        pmx_string = new_output.print_out()
        file_object = open('out.pmx', "w")
        file_object.write(pmx_string)
        file_object.close()
        os.system('pmx out.pmx')
        os.system('dvipdf out.dvi')
        os.system('evince out.pdf')
       







