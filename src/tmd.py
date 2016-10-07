#!/usr/bin/env python3
# -*- coding: utf8 -*-

import cairo
import TMDScanner
import re
import sys
from pathlib import Path
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
###########################      Checking File Head ################## 
    if FileChecker(ARGV) == False:
        sys.exit('File Type Error')
########################### done Checking File Head ################## 
########################### done Checking Header   ################### 
    InputFile = open(ARGV[1], 'r').read()
    Pass1(InputFile)
###########################      Confirming Pass 1 ###################
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

    
if __name__ == '__main__':
    main()
