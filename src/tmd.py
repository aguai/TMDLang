#!/usr/bin/env python3
# -*- coding: utf8 -*-
import TMDScanner
import re
import sys
from pathlib import Path
import TMDDrawer
import cairocffi as cairo
### for debug
testChordList = [
<<<<<<< HEAD
    [('1',''), '', ('m', ''), (300, 420)], 
    [('1',''), '',( 'aug',''), (500, 420)], 
    [('6',''), '',( 'm','11') , (900, 420)]
=======
    ['1','', '', 'm','', (300, 420)],
    ['1','', '', 'aug','', (500, 420)],
    ['6','', '', 'm','11' , (900, 420)]
>>>>>>> pyx/patch-1-pythonic
    ]
###
def Surface(NAME, TYPE, Size):
    # NAME: Song Name (with page#?)
    # TYPE: {PDF, SVG}
    # Size: {A3, A4, B4, B3}

    if TYPE == 'PDF':
        surface, ext = cairo.PDFSurface, '.pdf'
    elif TYPE == 'SVG':
        surface, ext = cairo.SVGSurface, '.svg'

    return cairo.Context(surface(NAME+ext, Size[0], Size[1]))


def FileChecker(ARGV):
    if len(ARGV)==1:
        print("usage:\n%s InputFile.pdf\n" % ARGV[0])
        return False

    elif Path(ARGV[1]).is_file() != True:
        print("there is no file named %s!" % ARGV[1])
        return False

    elif re.search(TMDScanner.MarkupTypePattern,open(ARGV[1], 'r').readline())==None:
        # or re.search(r"\.[tT][mM][dD]", ARGV[1][-4:]) ==None:
        print("unknown filetype")
        return False
    else:
        return True

def Pass1(InputFile):
    TMDScanner.Key              =        TMDScanner.KeyGetter(InputFile)
    TMDScanner.Tempo            = float( TMDScanner.TempoGetter(InputFile) )
    TMDScanner.SongName         =        TMDScanner.SongNameGetter(InputFile)
    TMDScanner.PartsContent     =        TMDScanner.PartContentGetter(InputFile)
    TMDScanner.PartNameList     =        TMDScanner.PartSequenceGetter(InputFile)
    TMDScanner.PartSet          =        TMDScanner.PartSetGetter(TMDScanner.PartsContent)
    TMDScanner.InstrumentSet    =        TMDScanner.InstrumentSetGetter(TMDScanner.PartsContent)

def main():
    ARGV = sys.argv
    ###########################      Checking File Head ##############
    if FileChecker(ARGV) == False:
        sys.exit('File Type Error')
    ####################### done Checking File Head ##################
    ####################### done Checking Header   ###################
    InputFile = open(ARGV[1], 'r').read()
    Pass1(InputFile)
    #######################      Confirming Pass 1 ###################
    print('Given File is:\n'    +       InputFile               )
    print('')
    print('The Contents is')
    for item in TMDScanner.PartsContent:
        print('part:**' + str(item[0]) + '**\t:'
            + ' whith instrument:**'+ str(item[1]) + '**\t when bar number ['
            + str(item[2]).replace('|','') +']\n'
            + str(item[3]) )
    print('')
    print('KEY\t=\t'            +     TMDScanner.Key             )
    print('Tempo\t=\t'          + str(TMDScanner.Tempo          ))
    print('Song Name is '+ '<<' +     TMDScanner.SongName  + '>>')
    print('')
    print('The Sequnece in the song is:\n\t'           + str(TMDScanner.PartNameList ))
    print('The Parts includes:\n\t'                    + str(TMDScanner.PartSet      ))
    print('The Instruments in the song is:\n\t'        + str(TMDScanner.InstrumentSet))
    ########################### done Confirming Pass 1 ###################
    ###########################      Confirming Pass 2 ###################
    print('What Pass 2 has got is\nCHORD:\n')
    for k, v in TMDScanner.CodeStringGetter(TMDScanner.PartsContent).items():
        print(k +":\t"+str(v))
        if v[0]!=0:
            print("\tChord MUST Begin with LEADING Bar\n\tFill \'0\' for Rhythem only Bar")
            sys.exit('Fail To Compile %s' % ARGV[1] )
    ###########################      Drawing Chord      ###################
    # Chord :[Root-> {'chr'/[1-7]/,['#'|'b'|''] }, Bass -> '1-7', Quality -> 'm, aug, dim, alt', Intrval -> 7, 11, 6, 9, 13,Position -> {x, y}]

    Page = Surface(TMDScanner.SongName, 'PDF', TMDDrawer.A4)
    TMDDrawer.ChordDrawer(Page, testChordList)
    Page.show_page()

if __name__ == '__main__':
    main()
