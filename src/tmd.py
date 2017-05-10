#!/usr/bin/env python3
from pathlib import Path
import TMDScanner as Scan
import re
import sys
''' necessary variables '''
ReservedInstrument = set({'CHORD', 'GROOVE'})
InstrumentSet = set()
PartSet = set()
Key = 'C'            # default key is C
Tempo = 120.0       # default tempo 120
SongName = ''       # defult no name
Signature = [4, 4]  # defult to 4/4
PartsContent = []
PartNameList = []
InputFile = ''


def FileChecker(ARGV):
    MarkupTypePattern = r"^\:\:(?P<MarkType>\S+)\:\:\s*?$"
    if len(ARGV) == 1:
        print("usage:\n%s InputFile.tmd\n" % ARGV[0])
        return False

    elif not Path(ARGV[1]).is_file():
        print("there is no file named %s!" % ARGV[1])
        return False

    elif re.search(MarkupTypePattern, open(ARGV[1], 'r').readline()) is None:
        print("unknown filetype")
        return False
    else:
        return True


def main():
    ARGV = sys.argv

    if not FileChecker(ARGV):
        sys.exit('File Type Error')

    InputFile = open(ARGV[1], 'r').read()
    Key = Scan.KeyGetter(InputFile)
    Tempo = float(Scan.TempoGetter(InputFile))
    Signature = Scan.SignatureGetter(InputFile)
    SongName = Scan.SongNameGetter(InputFile)

    PartsContent = Scan.PartContentGetter(InputFile)
    PartNameList = Scan.PartSequenceGetter(InputFile)
    PartSet = Scan.PartSetGetter(PartsContent)
    InstrumentSet = Scan.InstrumentSetGetter(PartsContent)

    # debug
    for ChordsInEverPart in Scan.ChordListGetter(Scan.PartsContainsChord(PartsContent)):
        for DictItemWhichKeyIsPartName in ChordsInEverPart:
            print(DictItemWhichKeyIsPartName, ':')
            ttlist = []
            for i in ChordsInEverPart[DictItemWhichKeyIsPartName]:
                ttlist.append(
                    (i[0], 1 / int(i[1].rstrip('*>').lstrip('<')), i[2]))
            SpaceBeforeChord = 0
            WholePartLength = 0
            for i in range(len(ttlist)):
                WholePartLength += ttlist[i][1] * ttlist[i][2]
                if i == 0:
                    print('Space Before Chord %s\n\tis 0 of bar' %
                          str(ttlist[i][0]))
                else:
                    SpaceBeforeChord += ttlist[i - 1][1] * ttlist[i - 1][2]
                    print('Space Before Chord %s\n\tis %s of bar' %
                          (ttlist[i][0], SpaceBeforeChord))
            print('\nthe whole length of \"[%s]\" is %s' % (
                DictItemWhichKeyIsPartName, WholePartLength))
        print('')  # debug


if __name__ == '__main__':
    main()
