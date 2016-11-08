#!/usr/bin/env python3
# -*- coding: utf8 -*-
import TMDScanner as Scan
import re
import sys
from pathlib import Path
import TMDDrawer as Draw 
import cairocffi as cairo
''' necessery variables '''
ReservedInstrumet   = set({'CHORD', 'GROOVE'})
InstrumentSet       = set()
PartSet             = set()
Key                 = ''       # default key is C
Tempo               = 0.0     # default tempo 120
SongName            = ''        # defult no name
PartsContent        = []
PartNameList        = []
InputFile           = ''
### for debug
testChordList = [
    [('1',''), '', ('m', ''), (300, 420)], 
    [('1',''), '', ( 'aug',''), (500, 420)], 
    [('6',''), '', ( 'm','11'), (900, 420)],
    [('1',''), '', ('m',''), (300, 420)],
    [('1',''), '', ('aug','') , (500, 420)],
    [('6',''), '', ('m','11') , (900, 420)]
    ]
###


def FileChecker(ARGV):
    MarkupTypePattern   = r"^\:\:(?P<MarkType>\S+)\:\:\s*?$"
    if len(ARGV)==1:
        print("usage:\n%s InputFile.pdf\n" % ARGV[0])
        return False

    elif Path(ARGV[1]).is_file() != True:
        print("there is no file named %s!" % ARGV[1])
        return False

    elif re.search(MarkupTypePattern, open(ARGV[1], 'r').readline())==None:
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
    return cairo.Context(surface(NAME+ext, Size[0], Size[1]))

def main():
    ARGV = sys.argv
    ###########################      Checking File Head ##############
    if FileChecker(ARGV) == False:
        sys.exit('File Type Error')
    ####################### done Checking File Head ##################
    ####################### done Checking Header   ###################
    InputFile        =      open(ARGV[1], 'r').read()
    Key              =        Scan.KeyGetter(InputFile)
    Tempo            = float( Scan.TempoGetter(InputFile))
    SongName         =        Scan.SongNameGetter(InputFile)
    PartsContent     =        Scan.PartContentGetter(InputFile)
    PartNameList     =        Scan.PartSequenceGetter(InputFile)
    PartSet          =        Scan.PartSetGetter(PartsContent)
    InstrumentSet    =        Scan.InstrumentSetGetter(PartsContent)

    ########################### done Confirming Pass 1 ###################

    ###########################      Confirming Pass 2 ###################

    print('What Pass 2 has got is:')#@debug
    Scan.ChordStringGetter(PartsContent)


    '''
    Chord :[
            Root        -> ['' ->  '1~7' ,                      #-> full size
                            pitch -> '♯'|'♭'|'' ],              #-> 1/2 size
            Bass        -> '' ,                                 #-> 1/2 size bold
            Quality     -> 'm, aug, dim, alt' ,                 #-> 1/2 size
            Intrval     -> sus, sus4, 7, 11, 6, 9, 13 .etc... , #-> 1/3 size
            Position    -> [X, m, n] -> X + n/m bars before 
            ]
    '''
#    for k, v in Scan.CodeStringGetter(PartsContent).items():
#        print(k +":\t"+str(v))
#        if v[0]!=0:
#            print("\tChord MUST Begin with LEADING Bar\n\tFill \'0\' for Rhythem only Bar")
#            sys.exit('Fail To Compile %s' % ARGV[1] )
#######################################################################
###########################      Drawing Chord      ###################
#    Page = Surface(TMDScanner.SongName, 'PDF', TMDDrawer.A4)
#    TMDDrawer.ChordDrawer(Page, testChordList)
#    Page.show_page()


if __name__ == '__main__':
    main()
