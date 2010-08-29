#!/usr/bin/python
# -*- coding: utf-8 -*- 

#TODO
#   *   Attribut- und Methodennamen auf Englisch übersetzen.
#
#


import re

class output(object):
    def __init__(self, key, min_pitch, max_pitch, intervals, pitches, note_string, amount_of_bars):
        self.Key = key
        self.Min_Pitch = min_pitch
        self.Max_Pitch = max_pitch
        self.Intervals = intervals
        self.Note_String = note_string
        
        ## Hier faengt die Definition der Praeambelelemente an.
        ## Zwoelf Zahlen stehen als erstes in der Praeambel, durch whitespace
        ## getrennt.
        ## Die ersten acht beschreiben musikalische Daten.
        
        # Anzahl der Notensysteme (relativ zu der Anzahl der Instrumente)
        self.Anzahl_Notensysteme = 1
        
        self.Anzahl_Instrumente = 1	# Anzahl der Instrumente
        self.Logischer_Metrumzaehler = 4
        self.Logischer_Metrumnenner = 4
        self.Gedruckter_Metrumzaehler = 4
        self.Gedruckter_Metrumnenner = 4
        
        # Anzahl logischer Schlaege im ersten Auftakt. Dezimalbrueche moeglich.
        self.Auftaktschlaege = 0
        
        # Vorzeichen entsprechend dem Quintenzirkel. Positive Zahlen sind Kreuze, negative sind bs.
        self.Amount_Of_Accidentals = self.get_amount_of_accidentals()
        
        ## Die naechsten vier Zeilen beschreiben drucktechnische Details.
        
        # Anzahl der Seiten, die das Dokument haben soll.
        # 30 bis 60 Noten pro System, 10 bis 20 Systeme pro Seite.
#        self.Anzahl_Seiten = amount_of_bars / 40
        if amount_of_bars % 40 < 20:
            self.Anzahl_Seiten = amount_of_bars / 40
        else:
            self.Anzahl_Seiten = (amount_of_bars / 40) + 1
        
        # Anzahl der Notensysteme, d.h. gedruckter Partiturzeilen
        self.Anzahl_Systeme = amount_of_bars / 4
        self.Groesse_System = 16 # Groesse eines Notensystems in pt
        
        # Einrueckung in Prozent. 8.5 % schreibt man als .085
        self.Einrueckung = .1
        
        ## Namen der Instrumente, von unten nach oben.
        # Wird vor das jeweilige Notensystem geschrieben.
        # Kann leergelassen werden.
        self.Instrumentenbezeichnung = 'Blockfloete'
        
        ## Notenschluessel, von unten nach oben.
        # b heisst Bassschluessel, t heisst Violinschluessel.
        # Wird in notenschluessel() berechnet.
        self.Notenschluessel = self.notenschluessel(pitches[0])
        self.Notenschluessel_Vormals = self.Notenschluessel

        ## Das Verzeichnis, in das die Tex-Datei geschrieben werden soll.
        self.Verzeichnis = "./"
        
        ## Titel des Stuecks.
        #Wird zusammengestellt aus den Intervalsn und dem Notenumfang.
        intervals_string = ""
        for i in self.Intervals:
            intervals_string += i + ", "
        intervals_string = re.sub(r', $', r' in ', intervals_string)
        intervals_string = re.sub(r'(.+),(.+?)$', r'\g<1> und \g<2>', intervals_string)
        self.Titel = "Tt\n" + intervals_string + self.Min_Pitch + " - " + self.Max_Pitch # usw.
        
    def get_amount_of_accidentals(self):
        self.Key = self.Key.lower();
        self.Key = re.sub(r'[ \-]', '', self.Key)
        amount_of_accidentals = {
                             "cdur" : 0,
                             "gdur" : 1,
                             "ddur" : 2,
                             "adur" : 3,
                             "edur" : 4,
                             "hdur" : 5,
                             "fisdur" : 6,
                             "gesdur" : -6,
                             "desdur" : -5,
                             "asdur" : -4,
                             "esdur" : -3,
                             "bdur" : -2,
                             "fdur" : -1,
                            }
        return amount_of_accidentals[self.Key]
    
    def schreiben(self):
        
        # Zunaechst die Praeambel
        print "% PRAEAMBEL\n"
        praeambel = str(self.Anzahl_Notensysteme) + ' '
        praeambel += str(self.Anzahl_Instrumente) + ' '
        praeambel += str(self.Logischer_Metrumzaehler) + ' '
        praeambel += str(self.Logischer_Metrumnenner) + ' '
        praeambel += str(self.Gedruckter_Metrumzaehler) + ' '
        praeambel += str(self.Gedruckter_Metrumnenner) + ' '
        praeambel += str(self.Auftaktschlaege) + ' '
        praeambel += str(self.Amount_Of_Accidentals) + ' '
        print praeambel + ' '
        praeambel = str(self.Anzahl_Seiten) + ' '
        praeambel += str(self.Anzahl_Systeme) + ' '
        praeambel += str(self.Groesse_System) + ' '
        praeambel += str(self.Einrueckung) + ' '
        print praeambel
        print self.Instrumentenbezeichnung
        print self.Notenschluessel
        print self.Verzeichnis
        print self.Titel
        
        # Der Corpus
        # Gibt die Seitennummer (P = Pagenumber) aus. r = Right. c = Text.
        # I ist Anweisung fuer midi. i ist Instrument
        # K-8-0 ist die Anweisung zum herunteroktavieren.
        # Dabei werden die Noten um eine Oktave tiefer ausgegeben.
        # T-12 ist die Anweisung zum Transponieren um 12 Halbtoene nach unten
        # beim Schreiben der Midi-Datei.
        print "% CORPUS"
        print "Prc Ii34"
        
        # An dieser Stelle werden die eigentlichen Noten gesetzt.
        print self.Note_String
        
        
        
        
        
        
    
    def notenschluessel(self, notenhoehe):
        if re.search(r"[4567]$", notenhoehe):
            return 't'
        if re.search(r"[123]$", notenhoehe):
            return 'b'
        
        
#neu = ausgabe(['e4', 'g1'])
#neu.schreiben()
