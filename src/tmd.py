#!/usr/local/bin/python3
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
    PreDrawChordMsg = Scan.PerChordSymbolAndPosition(PartsContent, Signature)
    # print(PreDrawChordMsg)
    for i in PreDrawChordMsg:
        print('This Part Length: ', i[1])
        for j in i[0]:
            print(j, ':')
            for k in i[0][j]:
                # print(k[1],  k[0], 'bar behind\n-> \trow:', int(k[0] // 6), '\tcol:', k[0] % 6,
                #       '\n==>', k[0] - (k[0] // 6) * 6)
                print(k[0], '\n', k[1],  'bar behind->', 'at bar ', str(int(k[0])),
                      '\trow:', int(k[0] // 6), '\tcol:', int(k[0]) % 6)
    print('\nthe sequence: ', PartNameList)


if __name__ == '__main__':
    main()
