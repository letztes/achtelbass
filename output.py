#!/usr/bin/python
# -*- coding: utf-8 -*- 

#TODO
#
#


import re

class Output(object):
    def __init__(self, tonic, mode, major_accidentals, minor_accidentals, min_pitch, max_pitch, intervals, pitches, note_string, amount_of_bars, time_signature_numerator, time_signature_denominator, locales):
        self.Locales = locales
        self.Tonic = tonic
        self.Mode = mode
        self.Major_Accidentals = major_accidentals
        self.Minor_Accidentals = minor_accidentals
        self.Min_Pitch = min_pitch
        self.Max_Pitch = max_pitch
        self.Intervals = intervals
        self.Note_String = note_string
        self.Time_Signature_Numerator = time_signature_numerator
        self.Time_Signature_Denominator = time_signature_denominator
        
        ## Hier faengt die Definition der Praeambelelemente an.
        ## Zwoelf Zahlen stehen als erstes in der Praeambel, durch whitespace
        ## getrennt.
        ## Die ersten acht beprint_out musikalische Daten.
        
        # Anzahl der Notensysteme (relativ zu der Anzahl der Instrumente)
        self.Amount_Of_Note_Systems = 1
        
        self.Amount_Of_Instruments = 1	# Anzahl der Instrumente
        self.Logical_Meter_Numerator = self.Time_Signature_Numerator 
        self.Logical_Meter_Denominator = self.Time_Signature_Denominator 
        self.Printed_Meter_Numerator = self.Time_Signature_Numerator 
        self.Printed_Meter_Denominator = self.Time_Signature_Denominator 
        
        # Anzahl logischer Schlaege im ersten Auftakt. Dezimalbrueche moeglich.
        self.Auftaktschlaege = 0
        
        # Vorzeichen entsprechend dem Quintenzirkel. Positive Zahlen sind Kreuze, negative sind bs.
        self.Amount_Of_Accidentals = self.get_amount_of_accidentals()
        
        ## Die naechsten vier Zeilen beprint_out drucktechnische Details.
        
        # Anzahl der Seiten, die das Dokument haben soll.
        # 30 bis 60 Noten pro System, 10 bis 20 Systeme pro Seite.
#        self.Amount_Of_Pages = amount_of_bars / 40
        if amount_of_bars % 40 < 20:
            self.Amount_Of_Pages = amount_of_bars / 40
        else:
            self.Amount_Of_Pages = (amount_of_bars / 40) + 1
        
        # Anzahl der Notensysteme, d.h. gedruckter Partiturzeilen
        self.Amount_Of_Systems = amount_of_bars / 4
        self.Size_Of_System = 16 # Groesse eines Notensystems in pt
        
        # Indentation in Prozent. 8.5 % schreibt man als .085
        self.Indentation = .1
        
        ## Namen der Instrumente, von unten nach oben.
        # Wird vor das jeweilige Notensystem geschrieben.
        # Kann leergelassen werden.
        #self.Instrument_Name = 'Blockfloete'
        self.Instrument_Name = ''
        
        ## Clef, von unten nach oben.
        # b heisst Bassschluessel, t heisst Violinschluessel.
        # Wird in get_clef() berechnet.
        self.Clef = self.get_clef(pitches[0])
        self.Clef_Vormals = self.Clef

        ## Das Directory, in das die Tex-Datei geschrieben werden soll.
        self.Directory = "./"
        
        ## Titel des Stuecks.
        #Wird zusammengestellt aus den Intervalsn und dem Notenumfang.
        intervals_string = ""
        for interval in self.Intervals:
            intervals_string += self.Locales[interval] + ", "
        intervals_string = re.sub(r', $', r' in ', intervals_string)
        intervals_string = re.sub(r'(.+),(.+?)$', r'\g<1> '+locales['and']+' \g<2>', intervals_string)
        self.Titel = "Tt\n" + intervals_string + self.Min_Pitch + " - " + self.Max_Pitch # usw.
        
    def get_amount_of_accidentals(self):
        if self.Mode == 'Major':
            return self.Major_Accidentals[self.Tonic]
        elif self.Mode == 'Minor':
            return self.Minor_Accidentals[self.Tonic]
    
    def print_out(self):
       
        output_string = ''
        # Zunaechst die Praeambel
        praeambel = "% PRAEAMBEL\n\n"
        praeambel += str(self.Amount_Of_Note_Systems) + ' '
        praeambel += str(self.Amount_Of_Instruments) + ' '
        praeambel += str(self.Logical_Meter_Numerator) + ' '
        praeambel += str(self.Logical_Meter_Denominator) + ' '
        praeambel += str(self.Printed_Meter_Numerator) + ' '
        praeambel += str(self.Printed_Meter_Denominator) + ' '
        praeambel += str(self.Auftaktschlaege) + ' '
        praeambel += str(self.Amount_Of_Accidentals) + ' '
        praeambel += " \n"
        praeambel += str(self.Amount_Of_Pages) + ' '
        praeambel += str(self.Amount_Of_Systems) + ' '
        praeambel += str(self.Size_Of_System) + ' '
        praeambel += str(self.Indentation) + ' '
        output_string += praeambel + "\n"
        output_string += self.Instrument_Name + "\n"
        output_string += self.Clef + "\n"
        output_string += self.Directory + "\n"
        output_string += self.Titel + "\n"
        
        # Der Corpus
        # Gibt die Seitennummer (P = Pagenumber) aus. r = Right. c = Text.
        # I ist Anweisung fuer midi. i ist Instrument
        # K-8-0 ist die Anweisung zum herunteroktavieren.
        # Dabei werden die Noten um eine Oktave tiefer ausgegeben.
        # T-12 ist die Anweisung zum Transponieren um 12 Halbtoene nach unten
        # beim Schreiben der Midi-Datei.
        output_string += "% CORPUS" + "\n"
        output_string += "Prc Ii34" + "\n"
        
        # An dieser Stelle werden die eigentlichen Noten gesetzt.
        output_string += self.Note_String + "\n"
        
        return output_string
        
    
    def get_clef(self, notenhoehe):
        if re.search(r"[4567]$", notenhoehe):
            return 't'
        if re.search(r"[123]$", notenhoehe):
            return 'b'
        
        
#neu = ausgabe(['e4', 'g1'])
#neu.print_out()
