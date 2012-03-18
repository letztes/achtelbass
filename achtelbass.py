#!/usr/bin/python
# -*- coding: utf-8 -*- 

# Author:       Artur Spengler, letztes@gmail.com
# Description:  Generates music sheet semi-randomly. Especially useful for
#               learning and practicing sight-reading.
# Licence:      GPL
#
# TODO
#   Wichtiges
#
#   Großes
#   *   Klasse implementieren, die aus PMX-Dateien maschinell lernt, welche
#       Intervalle und Rhythmen häufig kombiniert werden. Wahrscheinlich in
#       neuer Datei, würde ja alternativ zu den bisher implementierten
#       Methoden in Pitches und Note_Values verwendet werden. Sie soll
#       Methoden zum Lernen andere zum Generieren enthalten.
#   *   MIDI-Input implementieren, damit die Software selbstständig
#       überprüfen kann, ob der Benutzer richtig gespielt hat. Etwa so:
#       http://www.youtube.com/watch?v=dr5_kAQ8OGg
#   *   Grand Staff implementieren, d.h.  Optional zwei Notensysteme
#       gleichzeitig
#
#   Eher kleines
#       http://www.python.org/dev/peps/pep-0008/
#

import os
import random
import re
import warnings

import note_values
import pitches
import output

# Version of the program
version = '0.1'

    
class Achtelbass(object):
    """The central class of the package

       call note_values.py, pitches.py and output.py 

    """
    def __init__(self, parameters, locales):
        self.Parameters = parameters
        self.Locales = locales
        #self.Version = version
        self.Frequency_Values = {'None' : 0,
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
        self.Tuplets_Values = {'None' : 0,
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
        self.Diatonic_Notes = 'C D E F G A B C'.split()
        self.Accidentals_For = {
                             'Major' : {
                                 'C'  : '+0',
                                 'G'  : '+1',
                                 'D'  : '+2',
                                 'A'  : '+3',
                                 'E'  : '+4',
                                 'B'  : '+5',
                                 'F#' : '+6',
                                 'C#' : '+7',
                                 'Cb' : '-7',
                                 'Gb' : '-6',
                                 'Db' : '-5',
                                 'Ab' : '-4',
                                 'Eb' : '-3',
                                 'Bb' : '-2',
                                 'F'  : '-1',
                              },
                              'Minor' : {
                                 'A'  : '+0',
                                 'E'  : '+1',
                                 'B'  : '+2',
                                 'F#' : '+3',
                                 'C#' : '+4',
                                 'G#' : '+5',
                                 'D#' : '+6',
                                 'A#' : '+7',
                                 'Ab' : '-7',
                                 'Eb' : '-6',
                                 'Bb' : '-5',
                                 'F'  : '-4',
                                 'C'  : '-3',
                                 'G'  : '-2',
                                 'D'  : '-1',
                              }
        }
        self.Tonic = parameters['tonic']
        self.Mode = parameters['mode']
        self.Changing_Key = parameters['changing_key']
        #self.Key = parameters['tonic'] + '-' + parameters['mode']
        self.Intervals = parameters['intervals'].keys()
        self.Chords = parameters['chords'] # boolean
        self.Prolongations_Frequency = parameters['prolongations_frequency']
        self.Inversion = parameters['inversion']
        self.Notes = ['c1', 'd1', 'e1', 'f1', 'g1', 'a1', 'b1',
                      'c2', 'd2', 'e2', 'f2', 'g2', 'a2', 'b2',
                      'c3', 'd3', 'e3', 'f3', 'g3', 'a3', 'b3',
                      'c4', 'd4', 'e4', 'f4', 'g4', 'a4', 'b4',
                      'c5', 'd5', 'e5', 'f5', 'g5', 'a5', 'b5']
        self.Note_Letters = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
        self.Min_Pitch = parameters['min_pitch']
        self.Max_Pitch = parameters['max_pitch']
#if max_pitch is lower than min_pitch, swap them
        if self.Notes.index(self.Min_Pitch) > self.Notes.index(self.Max_Pitch):
            self.Min_Pitch = parameters['max_pitch']
            self.Max_Pitch = parameters['min_pitch']
        
        self.Rest_Frequency = self.Frequency_Values[parameters['rest_frequency']]
        self.Selectable_Note_Values = [self.Fraction_Values[note_value] for note_value in parameters['note_values'].keys()]
        self.Selectable_Note_Values.sort()

        self.Time_Signature_Numerator = parameters['time_signature'][0]
        self.Time_Signature_Denominator = parameters['time_signature'][2]
        self.Time_Signature = self.Fraction_Values[parameters['time_signature']]
        self.Tuplets = self.Tuplets_Values[parameters['tuplets']]
        self.Tuplet_Same_Pitch = parameters['tuplet_same_pitch']
        self.Tuplets_Frequency = parameters['tuplets_frequency']
        
        self.BPM_For_Tempo = {'grave' : 40,
                            'largo' : 44,
                            'lento' : 52,
                            'adagio' : 58,
                            'andante' : 66,
                            'moderato' : 88,
                            'allegretto' : 104,
                            'allegro' : 132,
                            'vivace' : 160,
                            'presto' : 184,
        }
        self.Tempo = parameters['tempo']
        try:
            self.BPM = parameters['bpm']
        except KeyError:
            self.BPM = self.BPM_For_Tempo[self.Tempo]

        # Ausgabe immer so gestalten, dass etwa 40 bars,
        # 10 systems pro Seite stehen
        # 40 bars in 10 systems fit perfectly in 1 page.   
        self.Amount_Of_Bars = 40 
        self.Note_Values = self.get_note_values()
        self.Pitches = self.get_pitches()
        self.Note_String = self.glue_together()
        self.display()
    
    
    def get_note_values(self):
        new_note_values = note_values.NoteValues(self.Selectable_Note_Values,
                                                 self.Time_Signature,
                                                 self.Tuplets,
                                                 self.Tuplets_Frequency)
        for i in range(self.Amount_Of_Bars):
            new_note_values.calculate()
        
        return new_note_values.Result
    
    def get_pitches(self, current_tonic=''):
# current_tonic is only needed when key is changed and new tonic occurs
        amount = len(self.Note_Values)
        for note_value in self.Note_Values:
            if isinstance(note_value, str) and note_value.count('x'):
                tuplet_value = note_value[2:len(note_value)]
                amount += int(tuplet_value)

        if not current_tonic:
            current_tonic = self.Tonic

        new_pitches = pitches.Pitches(amount, self.Min_Pitch,
                                      self.Max_Pitch, current_tonic,
                                      self.Intervals, self.Inversion)
        
        return new_pitches.easy()

    def get_new_accidentals(self, old_accidentals, old_note_name):
        old_accidentals = int(old_accidentals)
        
        self.New_Tonic_For = {
                                'Major' : {
                                            '0' : {
                                                    'B' : ['B', 'Cb'],
                                            },
                                            '1' : {
                                                    'F' : ['F#', 'Gb'],
                                            },
                                            '2' : {
                                                    'C' : ['C#', 'Db'],
                                            },
                                            '3' : {
                                                    'G' : ['Ab'],
                                            },
                                            '4' : {
                                                    'D' : ['Eb'],
                                            },
                                            '5' : {
                                                    'A' : ['Bb'],
                                            },
                                            '6' : {
                                                    'E' : ['F'],
                                            },
                                            '7' : {
                                                    'B' : ['C'],
                                            },
                                            '-7' : {
                                                    'F' : ['E'],
                                            },
                                            '-6' : {
                                                    'C' : ['B'],
                                            },
                                            '-5' : {
                                                    'G' : ['F#'],
                                            },
                                            '-4' : {
                                                    'D' : ['C#'],
                                            },
                                            '-3' : {
                                                    'A' : ['Ab'],
                                            },
                                            '-2' : {
                                                    'E' : ['Eb'],
                                            },
                                            '-1' : {
                                                    'B' : ['Bb'],
                                            },
                                },
                                'Minor' : {
                                            '0' : {
                                                    'B' : ['B'],
                                            },
                                            '1' : {
                                                    'F' : ['F#'],
                                            },
                                            '2' : {
                                                    'C' : ['C#'],
                                            },
                                            '3' : {
                                                    'G' : ['G#', 'Ab'],
                                            },
                                            '4' : {
                                                    'D' : ['D#', 'Eb'],
                                            },
                                            '5' : {
                                                    'A' : ['A#', 'Bb'],
                                            },
                                            '6' : {
                                                    'E' : ['F'],
                                            },
                                            '7' : {
                                                    'B' : ['C'],
                                            },
                                            '-7' : {
                                                    'F' : ['E'],
                                            },
                                            '-6' : {
                                                    'C' : ['B'],
                                            },
                                            '-5' : {
                                                    'G' : ['F#'],
                                            },
                                            '-4' : {
                                                    'D' : ['C#'],
                                            },
                                            '-3' : {
                                                    'A' : ['Ab'],
                                            },
                                            '-2' : {
                                                    'E' : ['Eb'],
                                            },
                                            '-1' : {
                                                    'B' : ['Bb'],
                                            },
                                },
         }
         
        # new_tonic defaults to old_note_name
        new_tonic = old_note_name
        
        if old_accidentals > 0:
            old_accidentals_range = range(0, old_accidentals)
        else:
            old_accidentals_range = range(old_accidentals, -1)
        for current_accidentals_amount in old_accidentals_range:
            print 'accidentals in current loop: ' + str(current_accidentals_amount)
            # try to get new tonic from current combination
            if old_note_name in self.New_Tonic_For[ self.Mode ][ str(current_accidentals_amount) ]:
                new_tonic = random.choice( self.New_Tonic_For[ self.Mode ][ str(current_accidentals_amount) ][ old_note_name ] )
                
# Initially the algorithm was not intented to calculate the pitches
# in every bar, but whenever the key changes from # to b and vice versa,
# the names of the notes change. So it becomes necessary.
        new_pitches = pitches.Pitches(len(self.Note_Values),
                                  self.Min_Pitch,
                                  self.Max_Pitch,
                                  new_tonic[0],
                                  self.Intervals, self.Inversion)
        self.Pitches = new_pitches.easy()
        self.Pitches = self.get_pitches(new_tonic[0])
        
        return self.Accidentals_For[ self.Mode ][ new_tonic ]


    def glue_together(self):
        # PMX allows only 20 key changes, which means that it crashes
        # in  case more than 20 are set. However, with exactly  
        # 20 key changes the general key will be set incorrect, with
        # 19 key changes it works.
        remaining_key_changes = 19
        
        initial_accidentals = self.Accidentals_For[ self.Mode ][ self.Tonic ]
         
        new_accidentals = self.get_new_accidentals(initial_accidentals, self.Tonic[0].upper())
        note_string = ''

        previous_pitch = self.Pitches[0]
        previous_clef = 'c'
        _tie_pending = False
        if self.Notes.index(previous_pitch) < self.Notes.index('c4'):
            previous_clef = 'b'
        j = 0 # separate iterator for pitches. 
        
        # Metronome in the first bar
        for i in range(0, int(self.Time_Signature_Numerator)):
            note_string += self.Pitches[0][0] + str(self.Time_Signature_Denominator) + self.Pitches[0][1] + ' '
        note_string += "/\n"
        
        for i in range(len(self.Note_Values)):
            if self.Note_Values[i] == "/\n":
                note_string += "/\n"
                # If random key, insert random key signature
                # But only when its the before last iteration, because in 
                # the last iteration the key change would be set after the
                # last bar.
                if self.Changing_Key == True and remaining_key_changes > 0 and i < len(self.Note_Values)-2:
                    if random.uniform(0, 1) < (20 / float(self.Amount_Of_Bars)):
                        new_accidentals = self.get_new_accidentals(new_accidentals, self.Pitches[j][0].upper())
                        note_string += 'K+0'+new_accidentals+' '
                        remaining_key_changes -= 1
# j is reset to zero because in the method get_new_accidentals self.Pitches
# are calculated new with the current new_note as the tonic for the new
# key. It would be better if the resetting of the tonic and the enharmonic
# swapping of it were explicitly here.
                        j = 0

            else:
                # if tuplet
                if isinstance(self.Note_Values[i], str) and self.Note_Values[i].count('x'):
                    tuplet_remain = int(self.Note_Values[i][2])
                    note_string += self.Pitches[j][0] + self.Note_Values[i][0] + self.Pitches[j][1] + self.Note_Values[i][1:3] + ' '
                    while tuplet_remain > 1:
# PMX cannot end an xtuplet with a rest.
                        if self.Tuplet_Same_Pitch == False:
                            j += 1
                    
                        if random.uniform(0, 1) < self.Rest_Frequency and tuplet_remain > 2:
                            note_string += 'r '
                        else:
                            note_string += self.Pitches[j] + ' '
                        tuplet_remain -= 1
                    j += 1

                else:
                    if _tie_pending == True or random.uniform(0, 1) < float(self.Frequency_Values[self.Prolongations_Frequency]):
                    
                        # if current note value measures half the previous skip
                        # the current pitch but prolongate the previous with a dot
                        # But only if it is not the first note in the bar
                        if _tie_pending == False and self.Note_Values[i-1] != "/\n" and note_string[-2] != ")" and self.PMX_Note_Values[self.Note_Values[i-1]] == (2 * self.PMX_Note_Values[self.Note_Values[i]]):
                            note_string = re.sub(r" $", 'd ', note_string)
                        # else tie the previous note to current note
                        else:
                            if _tie_pending == False:
                                note_string += '( ' + self.Pitches[j][0] + str(self.Note_Values[i]) + self.Pitches[j][1] + ' '
                                _tie_pending = True
                            else:
                                note_string += self.Pitches[j][0] + str(self.Note_Values[i]) + self.Pitches[j][1] + ' ) '
                                _tie_pending = False
                    else:
                        # a rest or a note?
                        if random.uniform(0, 1) < self.Rest_Frequency:
                            note_string += 'r'+str(self.Note_Values[i]) + ' '
                        else:
                            note_string += self.Pitches[j][0] + str(self.Note_Values[i]) + self.Pitches[j][1] + ' '
                            if self.Chords == True:
                                note_string += ' ? ' + 'z' + self.Note_Letters[ self.Note_Letters.index(self.Pitches[j][0]) - 5] + ' ' + 'z' + self.Note_Letters[ self.Note_Letters.index(self.Pitches[j][0]) - 3] + ' ' + '? '
                            j += 1
                        
                
                # Clef change
                if previous_clef == 'b' and self.Notes.index(self.Pitches[j]) > self.Notes.index('e4'):
                    note_string += 'Ct '
                    previous_clef = 't'
                    
                if previous_clef == 't' and self.Notes.index(self.Pitches[j]) < self.Notes.index('a3'):
                    note_string += 'Cb '
                    previous_clef = 'b'
                    
                previous_pitch = self.Pitches[j]
        note_string = re.sub(r"(C[bt] )(/\n)", r"\g<2>\g<1>", note_string)
        note_string = re.sub(r"\n/$", r"", note_string)
        #print note_string; exit()
        return note_string
    
    def display(self):
        
        new_output = output.Output(self.Tonic, self.Mode,
                self.Accidentals_For['Major'], self.Accidentals_For['Minor'],
                self.Min_Pitch, self.Max_Pitch, self.Intervals,
                self.Pitches, self.Note_String, self.Amount_Of_Bars,
                self.Time_Signature_Numerator,
                self.Time_Signature_Denominator, self.Locales, self.BPM)
        pmx_string = new_output.print_out()
        os.chdir('/tmp/')
        file_object = open('out.pmx', 'w')
        file_object.write(pmx_string)
        file_object.close()
        os.system('pmx out.pmx')
        os.system('dvipdf out.dvi')
        os.system('evince out.pdf')
       

if __name__ == '__main__':
    import getopt, sys

    def usage():
        print sys.argv[0], """is a semi random generator for sheet music."
Usage: , sys.argv[0], [OPTIONS]
None of the options are mandatory, any omitted options
are set to default values listed below.
    
Options are:
    -t, --tonic=TONIC
      default=C
    
    -m, --mode=MODE
      default=Major

    -k, --changing_key
    
    -c, --chords
    
    -l, --prolongations
    
    -q, --prolongations_frequency=FREQUENCY
      default=0.5
    
    -m, --tempo=TEMPO
      default=andante
    
    -b, --bpm=BPM
      default=60
      bpm overrides tempo if set both
    
    -i, --interval=INTERVAL1 [--interval=INTERVAL2...]
      default=Second
    
    -e, --inversion
    
    -n, --min_pitch=MIN_PITCH
      default=c4
    
    -x, --max_pitch=MAX_PITCH
      default=d5
    
    -r, --rest_frequency=REST_FREQUENCY
      default='no rests'
    
    -s, --time_signature=TIME_SIGNATURE
      default='4/4' (note the quotation marks)
    
    -v, --note_values=NOTE_VALUE1 [--note_values=NOTE_VALUE2...]
      default=1 (1 means whole notes)
    
    -u, --tuplets=TUPLETS
      default='no tuplets'
    
    -p, --tuplet_same_pitch
    
    -f, --tuplets_frequency=TUPLETS_FREQUENCY
      default='no tuplets'
    
     --help  print this message and exit
     --version print version information and exit"""
   
    # Definition of default parameters
    parameters = {'tonic' : 'C',
                  'mode' : 'Major',
                  'changing_key' : False,
                  'chords' : False,
                  'intervals' : {},
                  'inversion' : False,
                  'min_pitch' : 'c3',
                  'max_pitch' : 'd5',
                  'rest_frequency' : 'no rests',
                  'time_signature' : '4/4',
                  'note_values' : {},
                  'tuplets' : 'no tuplets',
                  'tuplet_same_pitch' : False,
                  'tuplets_frequency' : 'no tuplets',
                  'prolongations' : False,
                  'prolongations_frequency' : 0.5,
                  'bpm' : 60,
                  'tempo' : 'andante',
                 }
    pitches_opt = ['c1', 'd1', 'e1', 'f1', 'g1', 'a1', 'b1',
                   'c2', 'd2', 'e2', 'f2', 'g2', 'a2', 'b2',
                   'c3', 'd3', 'e3', 'f3', 'g3', 'a3', 'b3',
                   'c4', 'd4', 'e4', 'f4', 'g4', 'a4', 'b4',
                   'c5', 'd5', 'e5', 'f5', 'g5', 'a5', 'b5']
    intervals_opt = ['Unison', 'Second', 'Third', 'Fourth',
                     'Fifth', 'Sixth', 'Seventh', 'Octave']
    tempo_opt = ['grave', 'largo', 'lento', 'adagio',
                     'andante', 'moderato', 'allegretto', 'allegro',
                     'vivace', 'presto']

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:],
                     't:m:kci:en:x:r:s:l:v:u:pf:bm',
                     ['tonic=', 'mode=', 'changing_key', 'chords', 'interval=',
                      'inversion', 'min_pitch=', 'max_pitch=', 'rest_frequency=', 
                      'time_signature=', 'prolongations_frequency=',
                      'note_values=', 'tuplets=', 'tuplet_same_pitch',
                      'tuplets_frequency=', 'bpm', 'tempo', 'help', 'version'])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        exit()

    for opt, arg in opts:
        if opt in ('-t', '--tonic'):
            if arg in ('C', 'G', 'D', 'A', 'E', 'B', 'F#',
                       'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F'):
                parameters['tonic'] = arg
            else:
                print arg, 'is not a valid value for tonic.'
                print 'Tonic must be one of', 'C', 'G', 'D', 'A', 'E',\
                        'B', 'F#', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F'
                exit()

    for opt, arg in opts:
        if opt in ('-m', '--tempo'):
            if arg in ():
                parameters['tempo'] = arg
            else:
                print arg, 'is not a valid value for tempo.'
                print 'Tempo must be one of', str(tempo_opt[1:-1])
                exit()

    for opt, arg in opts:
        if opt in ('-b', '--bpm'):
            if arg > 40 and arg < 200:
                parameters['bpm'] = arg
            else:
                print arg, 'is not a valid value for bpm.'
                print 'Beats per minute must be an integer between 40 and 200'
                exit()

        if opt in ('-m', '--mode'):
            if arg in ('Major', 'Minor', 'Changing key'):
                parameters['mode'] = arg
            else:
                print arg, 'is not a valid value for mode.'
                print "mode must be one of Minor, Major, 'Changing key'"
                exit()

        if opt in ('-k', '--changing_key'):
            parameters['changing_key'] = True

        if opt in ('-c', '--chords'):
            parameters['chords'] = True
            
        if opt in ('-q', '--prolongations_frequency'):
            if float(arg) >= 0 and float(arg) <= 1:
                parameters['prolongations_frequency'] = arg
            else:
                print arg, 'is not a valid value for prolongations_frequency.'
                print 'prolongations_frequency must be an integer between 0 and 1'
                print 'For example 0.5'
                exit()
            

        if opt in ('-i', '--interval'):
            if arg in (intervals_opt):
                parameters['intervals'][arg] = True
            else:
                print arg, 'is not a valid value for interval.'
                print 'interval must be one of', str(intervals_opt[1:-1])
                exit()

        if opt in ('-e', '--inversion'):
            parameters['inversion'] = True

        if opt in ('-n', '--min_pitch'):
            if arg in (pitches_opt):
                parameters['min_pitch'] = arg
            else:
                print arg, 'is not a valid value for min_pitch.'
                print 'min_pitch must be one of', str(pitches_opt)[1:-1]
                exit()

        if opt in ('-x', '--max_pitch'):
            if arg in (pitches_opt):
                parameters['max_pitch'] = arg
            else:
                print arg, 'is not a valid value for max_pitch.'
                print 'max_pitch must be one of', str(pitches_opt)[1:-1]
                exit()

        if opt in ('-r', '--rest_frequency'):
            if arg in ('no rests', '0.1', '0.2', '0.3', '0.4', '0.5'):
                parameters['rest_frequency'] = arg
            else:
                print arg, 'is not a valid value for rest_frequency.'
                print 'rest_frequency must be one of', 'no rests',\
                      '0.1', '0.2', '0.3', '0.4', '0.5'
                exit()

        if opt in ('-s', '--time_signature'):
            if arg in ('2/2', '3/4', '4/4'):
                parameters['time_signature'] = arg
            else:
                print arg, 'is not a valid value for time_signature.'
                print 'max_pitch must be one of', 'no rests', '2/2',\
                      '3/4', '4/4'
                exit()


        if opt in ('-o', '--note_values'):
            if arg in ('1', '1/2', '1/4', '1/8', '1/16', '1/32'):
                parameters['note_values'][arg] = True
            else:
                print arg, 'is not a valid value for note_values.'
                print 'note_values must be one of',\
                        "'1',", "'1/2',", "'1/4',", "'1/8',", "'1/16',", "'1/32',"
                exit()

        if opt in ('-u', '--tuplets'):
            if arg in ('no tuplets', '2', '3', '4', '5', '6', '7'):
                parameters['tuplets'] = arg
            else:
                print arg, 'is not a valid value for tuplets.'
                print 'tuplets must be one of', "'no tuplets'",\
                        '2', '3', '4', '5', '6', '7'
                exit()

        if opt in ('-p', '--tuplet_same_pitch'):
            parameters['tuplet_same_pitch'] = True

        if opt in ('-f', '--tuplets_frequency'):
            if arg in ('no tuplets', '0.1', '0.2', '0.3', '0.4', '0.5',
                       '0.6', '0.7', '0.8', '0.9', '1'):
                parameters['tuplets_frequency'] = arg
            else:
                print arg, 'is not a valid value for tuplets_frequency.'
                print 'tuplets_frequency must be one of', 'no tuplets',\
                        '0.1', '0.2', '0.3', '0.4', '0.5', '0.6',\
                        '0.7', '0.8', '0.9', '1'
                exit()

        if opt == '--help':
            usage()
            exit()

        if opt in ('--version'):
            print sys.argv[0], 'version', version
            print ""
            exit()

# These two are stored in a dict of dict, so their defaults must 
# be set here separately
    if not dict(parameters['note_values']):
        parameters['note_values']['1'] = True # set default
    if not dict(parameters['intervals']):
        parameters['intervals']['Second'] = True # set default
    print ''
    #print parameters
    print ''
    #exit()
# If time singature and note values don't fit together
    opt_fraction_values = {'2/2' : 1.0,
                            '3/4' : 0.75,
                            '4/4' : 1.0,
                            '1' : 1.0,
                            '1/2' : 0.5,
                            '1/4' : 0.25,
                            '1/8' : 0.125,
                            '1/16' : 0.0625,
                            '1/32' : 0.03125,
                           }
# When time signature is 3/4 and the only note value is 1 or 1/2, exit
    if opt_fraction_values[parameters['time_signature']] < 1:
        if '1' in parameters['note_values']:
            print 'Cannot put whole notes into '+parameters['time_signature']+' bar.'
            exit()
        if opt_fraction_values[parameters['time_signature']] != 0.5 and \
                parameters['note_values']['1/2']:
            print 'Cannot put half notes into '+parameters['time_signature']+' bar.'
            exit()

# If the span between min_pitch and max_pitch is smaller than the greatest
# interval chosen, raise an error and exit.
    names_of_chosen_intervals = parameters['intervals'].keys()
    names_of_chosen_intervals.sort()
    greatest_interval_chosen = names_of_chosen_intervals[-1]
    steps_in_note_span_chosen = abs(pitches_opt.index(parameters['max_pitch']) - pitches_opt.index(parameters['min_pitch']))
    if steps_in_note_span_chosen < intervals_opt.index(greatest_interval_chosen):
        #print steps_in_note_span_chosen; exit()
        print 'You have chosen', greatest_interval_chosen, 'as the'
        print 'greatest interval, but the span between the minimum'
        print 'pitch', parameters['min_pitch'], 'and the maximum pitch', parameters['max_pitch'], ' is only a ', intervals_opt[steps_in_note_span_chosen]+'.'
        print 'That will not fit.'
        print 'Please choose either a smaller interval or a greater'
        print "span between minimum pitch and maximum pitch.\n"
        exit()

    from locales_en import locales
    Achtelbass(parameters, locales)

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
