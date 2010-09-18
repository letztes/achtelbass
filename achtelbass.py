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

version=0.1

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
        self.Notes = ["c1", "d1", "e1", "f1", "g1", "a1", "b1", "c2", "d2", "e2", "f2", "g2", "a2", "b2", "c3", "d3", "e3", "f3", "g3", "a3", "b3", "c4", "d4", "e4", "f4", "g4", "a4", "b4", "c5", "d5", "e5", "f5", "g5", "a5", "b5"]
        self.Min_Pitch = parameters['min_pitch']
        self.Max_Pitch = parameters['max_pitch']
#if max_pitch is lower than min_pitch, swap them
        if self.Notes.index(self.Min_Pitch) > self.Notes.index(self.Max_Pitch):
            self.Min_Pitch = parameters['max_pitch']
            self.Max_Pitch = parameters['min_pitch']
        
        self.Rest_Frequency = self.Frequency_Values[parameters['rest_frequency']]
        self.Selectable_Note_Values = [self.Fraction_Values[note_value] for note_value in parameters['note_values'].keys()]
        self.Selectable_Note_Values.sort()

       # match = re.search('(\d)/(\d)', parameters['time_signature'])
        #self.Time_Signature_Numerator = match.group(1)
        self.Time_Signature_Numerator = parameters['time_signature'][0]
        #self.Time_Signature_Denominator = match.group(2)
        self.Time_Signature_Denominator = parameters['time_signature'][2]
        self.Time_Signature = self.Fraction_Values[parameters['time_signature']]
        self.Tuplets = self.Tuplets_Values[parameters['tuplets']]
        self.Tuplets_Frequency = parameters['tuplets_frequency']

        # Ausgabe immer so gestalten, dass etwa 40 bars, 10 systems pro Seite stehen
        self.Amount_Of_Bars = 81 # 40 bars in 10 systems fit perfectly in 1 page.   
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
        previous_clef = "c"
        if self.Notes.index(previous_pitch) < self.Notes.index("c4"):
            previous_clef = "b"
        j = 0 # separate iterator for pitches. 
        for i in range(len(self.Note_Values)):
            if self.Note_Values[i] == "/\n":
                note_string += "/\n"
            else:
                if isinstance(self.Note_Values[i], str) and self.Note_Values[i].count('x'): # Falls Multiole
                    #match = re.search('(\d)x(\d)', self.Note_Values[i])
                    #note_value_for_tuplet = int(match.group(1))
                    #tuplet_remain = int(self.Note_Values[i][2])
                    note_value_for_tuplet = int(self.Note_Values[i][0])
                    tuplet_remain = int(self.Note_Values[i][2])
                    note_string += self.Pitches[j][0] + self.Note_Values[i][0] + self.Pitches[j][1] + self.Note_Values[i][1:3] + ' '
                    j += 1
                    while tuplet_remain > 1:
# PMX cannot end an xtuplet with a rest. But why "> 2" and not "> 1"?
                        if random.uniform(0, 1) < self.Rest_Frequency and tuplet_remain > 2:
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
        os.chdir('/tmp/')
        file_object = open('out.pmx', "w")
        file_object.write(pmx_string)
        file_object.close()
        os.system('pmx out.pmx')
        os.system('dvipdf out.dvi')
        os.system('evince out.pdf')
       

if __name__ == "__main__":
    import getopt, sys

    def usage():
        print ""
        print sys.argv[0], "is a semi random generator for sheet music."
        print "Usage: ", sys.argv[0], "[OPTIONS]"
        print "None of the options are mandatory, any omitted options"
        print "are set to default values listed below."
        print ""
        print "Options are:"
        print " -t, --tonic=TONIC"
        print "         default=C"
        print ""
        print " -m, --mode=MODE"
        print "         default=Major"
        print ""
        print " -i, --intervals=INTERVAL1 [--intervals=INTERVAL2...]"
        print "         default=Second"
        print ""
        print " -n, --min_pitch=MIN_PITCH"
        print "         default=c4"
        print ""
        print " -x, --max_pitch=MAX_PITCH"
        print "         default=d5"
        print ""
        print " -r, --rest_frequency=REST_FREQUENCY"
        print "         default='no rests'"
        print ""
        print " -s, --time_signature=TIME_SIGNATURE"
        print "         default='4/4' (note the quotation marks)"
        print ""
        print " -o, --note_values=NOTE_VALUE1 [--note_values=NOTE_VALUE2...]"
        print "         default=1 (1 means whole notes)"
        print ""
        print " -u, --tuplets=TUPLETS"
        print "         default='no tuplets'"
        print ""
        print " -f, --tuplets_frequency=TUPLETS_FREQUENCY"
        print "         default='no tuplets'"
        print ""
        print "     --help      print these message and exit"
        print "     --version   print version information and exit"
        print ""
        


    parameters = {'tonic' : 'C',
                  'mode' : 'Major',
                  'intervals' : {},
                  'min_pitch' : 'c4',
                  'max_pitch' : 'd5',
                  'rest_frequency' : 'no rests',
                  'time_signature' : '4/4',
                  'note_values' : {},
                  'tuplets' : 'no tuplets',
                  'tuplets_frequency' : 'no tuplets',
                 }
    pitches_opt = ["c1", "d1", "e1", "f1", "g1", "a1", "b1", "c2", "d2", "e2", "f2", "g2", "a2", "b2", "c3", "d3", "e3", "f3", "g3", "a3", "b3", "c4", "d4", "e4", "f4", "g4", "a4", "b4", "c5", "d5", "e5", "f5", "g5", "a5", "b5"]
    intervals_opt = ['Unison', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Octave']

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 't:m:i:n:x:r:s:o:u:f:', ['tonic=', 'mode=', 'intervals=', 'min_pitch=', 'max_pitch=', 'rest_frequency=', 'time_signature=', 'note_values=', 'tuplets=', 'tuplets_frequency=', '--help', '--version'])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        exit()

    for opt, arg in opts:
        if opt in ('-t', '--tonic'):
            if arg in ('C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F'):
                parameters['tonic'] = arg
                print parameters
            else:
                print arg, 'is not a valid value for tonic.'
                print 'Tonic must be one of', 'C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F'

        if opt in ('-m', '--mode'):
            if arg in ('Major', 'Minor'):
                parameters['mode'] = arg
            else:
                print arg, 'is not a valid value for mode.'
                print 'mode must be one of', 'Minor', 'Major'

        if opt in ('-i', '--intervals'):
            if arg in (intervals_opt):
                parameters['intervals'][arg] = True
            else:
                print arg, 'is not a valid value for intervals.'
                print 'interval must be one of', str(intervals_opt[1:-1])
        
        if opt in ('-n', '--min_pitch'):
            if arg in (pitches_opt):
                parameters['min_pitch'] = arg
            else:
                print arg, 'is not a valid value for min_pitch.'
                print 'min_pitch must be one of', str(pitches_opt)[1:-1]

        if opt in ('-x', '--max_pitch'):
            if arg in (pitches_opt):
                parameters['max_pitch'] = arg
            else:
                print arg, 'is not a valid value for max_pitch.'
                print 'max_pitch must be one of', str(pitches_opt)[1 : -1]

        if opt in ('-r', '--rest_frequency'):
            if arg in ('no rests', '0.1', '0.2', '0.3', '0.4', '0.5'):
                parameters['rest_frequency'] = arg
            else:
                print arg, 'is not a valid value for rest_frequency.'
                print 'rest_frequency must be one of', 'no rests', '0.1', '0.2', '0.3', '0.4', '0.5'

        if opt in ('-s', '--time_signature'):
            if arg in ('2/2', '3/4', '4/4'):
                parameters['time_signature'] = arg
            else:
                print arg, 'is not a valid value for time_signature.'
                print 'max_pitch must be one of', 'no rests', '2/2', '3/4', '4/4'


        if opt in ('-o', '--note_values'):
            if arg in ("1", "1/2", "1/4", "1/8", "1/16", "1/32"):
                parameters['note_values'][arg] = True
            else:
                print arg, 'is not a valid value for note_values.'
                print 'note_values must be one of', "'no rests'", '0.1', '0.2', '0.3', '0.4', '0.5'

        if opt in ('-u', '--tuplets'):
            if arg in ('no tuplets', '2', '3', '4', '5', '6', '7'):
                parameters['tuplets'] = arg
            else:
                print arg, 'is not a valid value for tuplets.'
                print 'tuplets must be one of', "'no tuplets'", '2', '3', '4', '5', '6', '7'

        if opt in ('-f', '--tuplets_frequency'):
            if arg in ('no tuplets', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1'):
                parameters['tuplets_frequency'] = arg
            else:
                print arg, 'is not a valid value for tuplets_frequency.'
                print 'tuplets_frequency must be one of', 'no tuplets', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1'

        if opt == '--help':
            usage()

        if opt in ('--version'):
            print sys.argv[0], "version", version
            print ""
            exit()

    if not dict(parameters['note_values']):
        parameters['note_values']['1'] = True # set default
    if not dict(parameters['intervals']):
        parameters['intervals']['Second'] = True # set default
    print ''
    print parameters
    print ''
    #exit()


# If the span between min_pitch and max_pitch is smaller than the greatest
# interval chosen, raise an error and exit.
    names_of_chosen_intervals = parameters['intervals'].keys()
    names_of_chosen_intervals.sort()
    greatest_interval_chosen = names_of_chosen_intervals[-1]
    steps_in_note_span_chosen = abs(pitches_opt.index(parameters['max_pitch']) - pitches_opt.index(parameters['min_pitch']))
    if steps_in_note_span_chosen < intervals_opt.index(greatest_interval_chosen):
        #print steps_in_note_span_chosen; exit()
        print "You have chosen", greatest_interval_chosen, "as the"
        print "greatest interval, but the span between the minimum"
        print "pitch", parameters['min_pitch'], "and the maximum pitch", parameters['max_pitch'], "is only a", intervals_opt[steps_in_note_span_chosen]+"."
        print "That will not fit."
        print "Please choose either a smaller interval or a greater"
        print "span between minimum pitch and maximum pitch.\n"
        exit()
    achtelbass(parameters)

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
