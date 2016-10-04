#!/usr/bin/env python3
# -*- coding: utf8 -*-

import cairo
import TMDScanner
import re
import sys
from pathlib import Path

def main():
    if len(sys.argv)!=2:
        print("usage:\n%s InputFile.pdf\n" % sys.argv[0])
        exit()
    
    print("collectting notation info from %s... " % sys.argv[1])
    
    if Path(sys.argv[1]).is_file() != True:
        print("there is no file %s!" % sys.argv[1])
        exit()
    
    
if __name__ == '__main__':
    main()
