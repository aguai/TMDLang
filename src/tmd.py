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

    elif Path(ARGV[1]).is_file() != True:
        print("there is no file named %s!" % ARGV[1])
        return False

    elif re.search(MarkupTypePattern, open(ARGV[1], 'r').readline()) == None:
        print("unknown filetype")
        return False
    else:
        return True


# def Surface(NAME, Size):
    # NAME: Song Name (with page#?)
    # TYPE: {PDF}
    # Size: {A3, A4, B4, B3}
#    if Size == '':
#        Size = 'A4'
#    return cairo.Context(surface(NAME + '.pdf', Size))


def main():
    ARGV = sys.argv

    # Checking File Head #

    if not FileChecker(ARGV):
        sys.exit('File Type Error')

    # done Checking Header
    InputFile = open(ARGV[1], 'r').read()
    Key = Scan.KeyGetter(InputFile)
    Tempo = float(Scan.TempoGetter(InputFile))
    Signature = Scan.SignatureGetter(InputFile)
    SongName = Scan.SongNameGetter(InputFile)

    PartsContent = Scan.PartContentGetter(InputFile)
    PartNameList = Scan.PartSequenceGetter(InputFile)
    PartSet = Scan.PartSetGetter(PartsContent)
    InstrumentSet = Scan.InstrumentSetGetter(PartsContent)

    for jjj in Scan.ChordListGetter(Scan.PartsContainsChord(PartsContent)):  # debug
        for itit in jjj:  # debug
            print(itit, ':')  # debug
            for i in jjj[itit]:  # debug
                print(i)  # debug
        print('')  # debug

if __name__ == '__main__':
    main()
