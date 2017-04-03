# -*- coding: utf-8 -*-
import re
from sys import exit
from fractions import Fraction as frac
########################## Pass 1 ########################################
PartSequencePattern = r"\-\>([^\#]+)->\#"
PartContentPattern = r"(?P<partname>\S+?)?:(?P<InstrumentName>\S+?)?@\[(?P<Timing>\S+?)?\]\{\s+?(?P<PartContent>[^\}]+)\}"
SongNamePattern = r"\s*\*\*\s+?(?P<SongName>[^\*]+)\s+?\*\*\s*"
TempoPattern = r"\s*?\!\s*?\=\s*?(\d\d\d?\.?\d?\d?)\s*?\n"
KeyPattern = r"\s*?\?\s*\=\s*(?P<Key>[ABCDEFGabcdefg][',]?m?)\s*?\n"
SignaturePattern = r"\<(?P<BeatsPerBar>\d\d?)\/(?P<TickBase>\d\d?)\>\s*[\n\r]"

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
    def strip(match):
        match = list(match)
        match[3] = CommitStripper(FormaterStripper(match[3]))
        return match

    return [strip(m) for m in re.findall(PartContentPattern, inputFile)]

def PartsContainsChord(PRTCNT):
    L = []
    for p in PRTCNT:
        if p[1] == 'CHORD':
            if p[2] not in ['|0|', '']:
                print('any CHORD part should started with |0| or none!')
                exit('syntax error')
            else:
                L.append(p)
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

    for i in PartsContainsChord:    # debug    
        print(i)                    # debug

    # return a tuple ('base', ''StringWithChords)
    CHORDPartStringPattern = r"\<(?P<Base>[012348][26]?)\*\>(?P<ChordString>[^<$]+)"
    CHORDStringPattern = r"(?P<Chord>\[[1-7][^\]]*\]\-*)"
    CHORDBassAndQualityPattern = r"(?P<Bass>[1-7]['|,]?)(?P<Quality>[^\]]*)"
    # put a "<4*>[1][6m][4][5][1][5][1]-" to split tickBase and chord string
    BaseAndChordStrPattern = r"(\<(1|2|4|8|16|32)\*>)([^\<|$]+ )"

    pass
    # return [{'PartName':[ CHORD, CHORD, CHORD, CHORD, CHORD, CHORD, CHORD]}, {}'PartName':[CHORD, CHORD, CHORD, CHORD, CHORD, CHORD, CHORD],... ]
    # which PartName is PartsContainsChord[i][0] and Chord is combine with signature and 'string'
    #  [["6", "♯", "m"], "7-5", ["3", "♭"],  [1, 0.5]]  # means 6♯m7-5/3♭ (bass on 3,) with 1 bar before and place at 0.5 * bar_length
    #    Chord :[
    #            Root        -> [ '7' ->  '1~7' ,                                 #-> full size
    #            pitch       ->   '♯'|'♭'|'' ,                                       #-> 1/2 size
    #            Quality    ->  'm, aug, dim, alt' ]                         #-> 1/2 size
    #            Intrval      ->  'sus, sus4, 7, 11, 6, 9, 13' .etc... , #-> 1/3 size
    #            Bass        ->['4','♭'] ,                                           #-> 1/2 size bold
    #            Lengh    -> frac(x,y)                                            #-> confuse now
    #            ]
    #
    # In [10]: [int(re.findall(r"(\<(1|2|4|8|16|32)\*>)([^\<|$]+)" , opc[3])[0][1]), re.findall(r"(\<(1|2|4|8|16|32)\*>)([^\<|$]+ )" , opc[3])[0][2]]
    # Out[10]: [4, '[1]-[1sus4][1maj7][3]-[3sus4][3][4]-[4/2][4][4m]-[6,][7,]']
    # In [11]: opc
    # Out[11]: ['Ending', 'CHORD', '|0|', '<4*>[1]-[1sus4][1maj7][3]-[3sus4][3][4]-[4/2][4][4m]-[6,][7,]<1*>[1]-[1/5]-[1]-[1][1]']
    # =========================================================================================
    # find Partname
    #@ pseudo code
    #   def makeCHORDList('<4*>[1]-[1sus4][1maj7][3]-[3sus4][3][4]-[4/2][4][4m]-[6,][7,]<1*>[1]-[1/5]-[1]-[1][1]' -> strContains Chords):
    #       blah blah blah
    #       return CHORDList
    #       
    #   for item in PartsContainsChord:
    #       return {item[0]:makeCHORDList(item[3])}