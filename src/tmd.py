#!/usr/bin/env python3
# -*- coding: utf8 -*-
import TMDScanner as Scan
import re
import sys
from pathlib import Path
import TMDDrawer as Draw
import cairocffi as cairo
''' necessery variables '''
ReservedInstrumet = set({'CHORD', 'GROOVE'})
InstrumentSet = set()
PartSet = set()
Key = ''            # default key is C
Tempo = 120.0         # default tempo 120
SongName = ''       # defult no name
Signature = [4, 4]  # defult to 4/4
PartsContent = []
PartNameList = []
InputFile = ''

# for debug
# means 6♯m7-5/1 (bass on 1) with 1 bar before and place at 0.5 *
# bar_length
testChordList = [
    [
        ["6", "''", "m"],
        "7-5",
        ["1", ""],
        [1, 0.5]
    ],
    [
        ["3", "','", "m"],
        "7-5",
        ["1", "''"],
        [1, 0.5]
    ]
]
###


def FileChecker(ARGV):
    MarkupTypePattern = r"^\:\:(?P<MarkType>\S+)\:\:\s*?$"
    if len(ARGV) == 1:
        print("usage:\n%s InputFile.pdf\n" % ARGV[0])
        return False

    elif Path(ARGV[1]).is_file() != True:
        print("there is no file named %s!" % ARGV[1])
        return False

    elif re.search(MarkupTypePattern, open(ARGV[1], 'r').readline()) == None:
        print("unknown filetype")
        return False
    else:
        return True


def Surface(NAME, TYPE, Size):
    # NAME: Song Name (with page#?)
    # TYPE: {PDF, SVG}
    # Size: {A3, A4, B4, B3}
    if TYPE == 'PDF':
        surface, ext = cairo.PDFSurface, '.pdf'
    elif TYPE == 'SVG':
        surface, ext = cairo.SVGSurface, '.svg'
    return cairo.Context(surface(NAME + ext, Size[0], Size[1]))


def main():
    ARGV = sys.argv
    ###########################      Checking File Head ##############
    if FileChecker(ARGV) == False:
        sys.exit('File Type Error')
    ####################### done Checking File Head ##################
    ####################### done Checking Header   ###################
    InputFile = open(ARGV[1], 'r').read()
    Key = Scan.KeyGetter(InputFile)
    Tempo = float(Scan.TempoGetter(InputFile))
    Signature = Scan.SignatureGetter(InputFile)
    SongName = Scan.SongNameGetter(InputFile)
    PartsContent = Scan.PartContentGetter(InputFile)
    PartNameList = Scan.PartSequenceGetter(InputFile)
    PartSet = Scan.PartSetGetter(PartsContent)
    InstrumentSet = Scan.InstrumentSetGetter(PartsContent)

    ########################### done Confirming Pass 1 ###################

    ###########################      Confirming Pass 2 ###################
    # for Chord First
    def PartsContainsChord(PRTCNT):
        L=[]
        for p in PRTCNT:
            if p[1] == 'CHORD' :
                if p[2] != '|0|':
                    print('any CHORD part should started with |0|!')
                    sys.exit('syntax error')
                else:
                    L.append(p)
        return L                

    Scan.ChordListGetter(PartsContainsChord(PartsContent))

#  [["6", "♯", "m"], "7-5", ["3", "♭"],  [1, 0.5]]  # means 6♯m7-5/3♭ (bass on 3,) with 1 bar before and place at 0.5 * bar_length
#    Chord :[
#            Root        -> [ '7' ->  '1~7' ,                                 #-> full size
#            pitch       ->   '♯'|'♭'|'' ,                                       #-> 1/2 size
#            Quality    ->  'm, aug, dim, alt' ]                         #-> 1/2 size
#            Intrval      ->  'sus, sus4, 7, 11, 6, 9, 13' .etc... , #-> 1/3 size
#            Bass        ->['4','♭'] ,                                           #-> 1/2 size bold
#            Position    -> [X, W]                                            #-> X bars after and print at the W * Bar_length (1>W>0)
#            ]
#

if __name__ == '__main__':
    main()
