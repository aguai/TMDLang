#!/usr/local/bin/python
# -*- coding: utf8 -*-

import TMDParser
import re
import sys
def main():
    if len(sys.argv)!=2:
        print("usage:\n%s InputFile.pdf\n", sys.argv[0])
    print(sys.argv[1])
    
if __name__ == '__main__':
    main()
