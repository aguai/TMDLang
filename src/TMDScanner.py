import re
from sys import exit
from fractions import Fraction as frac

PartSequencePattern = re.compile("\-\>([^\#]+)->\#")
PartContentPattern = re.compile(
    r"(?P<partname>\S*)?:(?P<InstrumentName>\S*)@(?P<Timing>[^\{]*)\{(?P<PartContent>[^}]+)\}")
SongNamePattern = re.compile("\s*\*\*\s+?(?P<SongName>[^\*]+)\s+?\*\*\s*")
TempoPattern = re.compile("\s*?\!\s*?\=\s*?(\d\d\d?\.?\d?\d?)\s*?\n")
KeyPattern = re.compile("\s*?\?\s*\=\s*(?P<Key>[ABCDEFGabcdefg][',]?m?)\s*?\n")
PerChordPattern = re.compile(
    "\[(?P<Root>[1-7])(?P<RootAccidental>['|,])?(?P<Tonic>maj|Maj|aug|dim|m|M)?(P<Ext>[sus|alt])?(?P<TensionNote>[^\]|^\/]*)?[\/]?(?P<Bass>[1-7])?(?P<BassAccidental>['|,])?\]")

SignaturePattern = re.compile(
    "\<(?P<BeatsPerBar>\d\d?)\/(?P<TickBase>\d\d?)\>\s*[\n\r]")


def TempoGetter(inputFile):
    if len(re.findall(TempoPattern, inputFile)) != 1:
        return 120
    else:
        return re.findall(TempoPattern, inputFile)[0]


def KeyGetter(inputFile):
    if len(re.findall(KeyPattern, inputFile)) != 1:
        return ''
    else:
        return re.findall(KeyPattern, inputFile)[0]


def SongNameGetter(inputFile):
    if len(re.findall(SongNamePattern, inputFile)) != 1:
        return ''
    else:
        return re.findall(SongNamePattern, inputFile)[0]


def PartContentGetter(inputFile):
    LL = [m.groupdict() for m in re.finditer(PartContentPattern, inputFile)]

    for i in LL:
        i['PartContent'] = re.sub(r"\/\*[^\*]+\*\/", '', i['PartContent'].replace(
            ' ', '').replace('\n', '').replace('|', '').replace('\t', '').replace('\r', ''))

    return LL


def PartsContainsChord(PRTCNT):
    L = []
    for p in PRTCNT:
        if p['InstrumentName'] == 'CHORD':
            if p['Timing'] != '' and p['Timing'] != '|0|':
                print('any CHORD part should started with |0| or none!')
                exit('syntax error')
            else:
                L.append(p)
    return L


def PartSetGetter(PartContentDict):
    SetOfPartname = set()
    # print('PartSetGetter:')
    for i in PartContentDict:
        # print(i['partname'])
        SetOfPartname.add(i['partname'])
    # print(SetOfPartname)
    return SetOfPartname


def InstrumentSetGetter(PartContentList):
    SetOfInstument = set()
    for i in PartContentList:
        SetOfInstument.add(i['InstrumentName'])
    # print(SetOfInstument)
    return SetOfInstument


def PartSequenceGetter(inputFile):
    if len(re.findall(PartSequencePattern, inputFile)) == 1:
        TempList = re.findall(PartSequencePattern, inputFile)[0].split('->')
        return [re.sub(r"\/\*[^\*]+\*\/", '', item.replace(
            ' ', '').replace('\n', '').replace('|', '').replace('\t', '').replace('\r', '')) for item in TempList]
    else:
        return []


def SignatureGetter(inputFile):
    Sig = re.findall(SignaturePattern, inputFile)
    if len(Sig) == 0:
        # print('signature set to default 4/4')
        return (4, 4)

    elif Sig[0][1] not in {'1', '2', '4', '8', '16', '32'}:
        print('signature should base on 1, 2, 4, 8, 16, 32.')
        exit('invalid signature')

    else:
        return (int(Sig[0][0]), int(Sig[0][1]))


def ChordListGetter(PartsContainsChord):
    # print(PartsContainsChord)#debug
    XX = []
    re4Content = re.compile(
        r"(?P<TimeBase>\<[1|2|4|8|16|32]\*\>)(?P<ChordString>[^<$]+)")
    re4ChordLengh = re.compile(r"(?P<FullChord>\[[^\]]+\])(?P<dash>\-*)")
    for i in PartsContainsChord:
        # print('\n=== === ===  ', i['partname'] + '\t=== === ===\n')
        TT = {i['partname']: []}
        for j in re4Content.findall(i['PartContent']):
            for k in re4ChordLengh.findall(j[1]):
                TT[i['partname']].append((k[0], j[0], len(k[1]) + 1))
        XX.append(TT)

    return XX


def PerChordSymbolAndPosition(PCTX, SIGTRE):
    print((frac('1/' + str(SIGTRE[0])),
           SIGTRE[1],  frac(str(SIGTRE[1]) + '/' + str(SIGTRE[0]))))
    Y = []
    for ChordsInEveryPart in ChordListGetter(PartsContainsChord(PCTX)):
        X = []
        for DictItemWhichKeyIsPartName in ChordsInEveryPart:
            # print(DictItemWhichKeyIsPartName, ':')
            ListOfChordWithEveryPartContent = []
            for i in ChordsInEveryPart[DictItemWhichKeyIsPartName]:
                ListOfChordWithEveryPartContent.append(
                    (i[0], 1 / int(i[1].rstrip('*>').lstrip('<')), i[2]))
                print(i[0], frac('1/' + i[1].rstrip('*>').lstrip('<')), i[2])
            SpaceBeforeChord = 0
            WholePartLength = 0
            for i in range(len(ListOfChordWithEveryPartContent)):
                WholePartLength += ListOfChordWithEveryPartContent[i][1] * \
                    ListOfChordWithEveryPartContent[i][2] * \
                    frac(str(SIGTRE[1]) + '/' + str(SIGTRE[0]))
                if i == 0:
                    X.append((0.0, [m.groupdict() for m in re.finditer(
                        PerChordPattern, ListOfChordWithEveryPartContent[i][0])][0]))
                else:
                    SpaceBeforeChord += frac(ListOfChordWithEveryPartContent[i - 1][1]) * \
                        frac(ListOfChordWithEveryPartContent[i - 1][2]) * \
                        frac(str(SIGTRE[1]) + '/' + str(SIGTRE[0]))
                    X.append((SpaceBeforeChord, [m.groupdict() for m in re.finditer(
                        PerChordPattern, ListOfChordWithEveryPartContent[i][0])][0]))
            Y.append(({DictItemWhichKeyIsPartName: X}, WholePartLength))
    return Y
