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

def main():
    ARGV = sys.argv
    if FileChecker(ARGV) == False:
        sys.exit(1)
    InputFile = open(ARGV[1], 'r').read()
########################### For DEBUG ##############################
    print("collectting notation info from %s... " % ARGV[1])  
    TMDScanner.Key              =        TMDScanner.KeyGetter(InputFile)
    TMDScanner.Tempo            = float( TMDScanner.TempoGetter(InputFile) )
    TMDScanner.SongName         =        TMDScanner.SongNameGetter(InputFile)
    TMDScanner.PartsContent     =        TMDScanner.PartContentGetter(InputFile)
    print('The Contents is \n' + str(TMDScanner.AllPartsContent))
        
    print('#########################')

    print('KEY\t=\t'        +     TMDScanner.Key)
    print('Tempo\t=\t'      + str(TMDScanner.Tempo))
    print('Song Name is '+ '<<'+  TMDScanner.SongName + '>>')
    print('The Parts in the song is') 
    print(TMDScanner.PartSequenceGetter(InputFile))
    print('The Instruments in the song is') 
    print(TMDScanner.InstrumentSet)
#   print('''
#   for 
#   ''')
########################### For DEBUG ##############################
    
    
if __name__ == '__main__':
    main()
