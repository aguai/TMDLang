import re
from sys import exit

PartSequencePattern = re.compile("\-\>([^\#]+)->\#")
PartContentPattern = re.compile(
    "(?P<partname>\S+?)?:(?P<InstrumentName>\S+?)?@\[(?P<Timing>\S+?)?\]\{\s+?(?P<PartContent>[^\}]+)\}")
SongNamePattern = re.compile("\s*\*\*\s+?(?P<SongName>[^\*]+)\s+?\*\*\s*")
TempoPattern = re.compile("\s*?\!\s*?\=\s*?(\d\d\d?\.?\d?\d?)\s*?\n")
KeyPattern = re.compile("\s*?\?\s*\=\s*(?P<Key>[ABCDEFGabcdefg][',]?m?)\s*?\n")
SignaturePattern = re.compile(
    "\<(?P<BeatsPerBar>\d\d?)\/(?P<TickBase>\d\d?)\>\s*[\n\r]")


def CommitStripper(strn):
    '''
    remove commits
    '''
    return re.sub(r"\/\*[^\*]+\*\/", '', strn)


def FormaterStripper(strn):
    ''' anything for format shall be trimed here'''
    return strn.replace(' ', '').replace('\n', '').replace('|', '').replace('\t', '').replace('\r', '')


def TempoGetter(inputFile):
    if len(re.findall(TempoPattern, inputFile)) != 1:
        return 120
    else:
        return re.findall(TempoPattern, inputFile)[0]


def KeyGetter(inputFile):
    if len(re.findall(KeyPattern, inputFile)) != 1:
        return 'C'
    else:
        return re.findall(KeyPattern, inputFile)[0]


def SongNameGetter(inputFile):
    if len(re.findall(SongNamePattern, inputFile)) != 1:
        return ''
    else:
        return re.findall(SongNamePattern, inputFile)[0]


def PartContentGetter(inputFile):
    '''
    to collect all the part content and instrument content


    '''
#    print(inputFile, '\n\n=== input file above ===\n\n')  # debug

    def stripthis(match):
        match = list(match)
        match[3] = CommitStripper(FormaterStripper(match[3]))
        return match

    for i in [m.groupdict() for m in re.finditer(PartContentPattern, inputFile)]:
        print("%s::%s=>%s:\n%s\n" %
              (i['partname'], i['InstrumentName'],
               i['Timing'],
               re.sub(r"\/\*[^\*]+\*\/", '',
                      i['PartContent']).replace(
                   ' ', '').replace('\n', '').replace('|', '').replace('\t', '').replace('\r', '')

               ))
    return [stripthis(m) for m in re.findall(PartContentPattern, inputFile)]


def PartsContainsChord(PRTCNT):
    L = []
    for p in PRTCNT:
        if p[1] == 'CHORD':
            if p[2] not in ['|0|', '']:
                print('any CHORD part should started with |0| or none!')
                exit('syntax error')
            else:
                L.append(p)
    print('in TMDScanner:\n\tParts Contain Chord is:')  # debug
    for i in L:  # debug
        print('\t==>', i)  # debug
    return L


def PartSetGetter(PartContentList):
    return set(match[0] for match in PartContentList)


def InstrumentSetGetter(PartContentList):
    return set(match[1] for match in PartContentList)


def PartSequenceGetter(inputFile):
    if len(re.findall(PartSequencePattern, inputFile)) == 1:
        TempList = re.findall(PartSequencePattern, inputFile)[0].split('->')
        return [FormaterStripper(item) for item in TempList]
    else:
        return []


def SignatureGetter(inputFile):
    Sig = re.findall(SignaturePattern, inputFile)
    if len(Sig) == 0:
        print('signature set to default 4/4')
        return (4, 4)

    elif Sig[0][1] not in {'1', '2', '4', '8', '16', '32'}:
        print('signature should base on 1, 2, 4, 8, 16, 32.')
        exit('invalid signature')

    else:
        return (int(Sig[0][0]), int(Sig[0][1]))


def ChordListGetter(PartsContainsChord):
    CHORDPartStringPattern = re.compile(
        "\<(?P<Base>[1|2|4|8|16]?)\*\>(?P<ChordString>[^<$]+)")
    CHORDStringPattern = re.compile("(?P<Chord>\[[1-7][^\]]*\]\-*)")
    CHORDBassAndQualityPattern = re.compile(
        "(?P<Bass>[1-7]['|,]?)(?P<Quality>[^\]]*)")
    BaseAndChordStrPattern = re.compile("(\<(1|2|4|8|16|32)\*>)([^\<|$]+ )")

    pass
