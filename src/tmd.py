#!/usr/bin/env python3
# -*- coding: utf8 -*-

import cairo
import TMDScanner
import re
import sys
from pathlib import Path
def FileChecker(ARGV):
    if len(ARGV)!=2:
        print("usage:\n%s InputFile.pdf\n" % ARGV[0])
        return False
    
    elif Path(ARGV[1]).is_file() != True:
        print("there is no file named %s!" % ARGV[1])
        return False

    elif re.search(TMDScanner.MarkupTypePattern,open(ARGV[1], 'r').readline())==None or re.search(r"\.[tT][mM][dD]", ARGV[1][-4:]) ==None:
        print("unknown filetype")
        return False
    else:
        return True

def main():
    ARGV = sys.argv
    if FileChecker(ARGV) != True:
        exit()
    InputFile = open(ARGV[1], 'r').read()
    print("collectting notation info from %s... " % ARGV[1])  

    print('\n'+'#'*100+'\n')
    for i in TMDScanner.PartContentGetter(InputFile):
        print(i)
    print('\n'+'#'*100+'\n')
    print(TMDScanner.PartSequenceGetter(InputFile))
    
    
if __name__ == '__main__':
    main()
