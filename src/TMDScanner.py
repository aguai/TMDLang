# -*- coding: utf-8 -*-
import re
########################## Pass 1 ########################################
PartSequencePattern = r"\-\>([^\#]+)->\#"
PartContentPattern = r"(?P<partname>\S+?)?:(?P<InstrumentName>\S+?)?@\[(?P<Timing>\S+?)?\]\{\s+?(?P<PartContent>[^}]+)\}"
#PartContentPattern = r"(\S*):(\S*)@\[(\S*)\]\{([^\}]+)\}"
SongNamePattern = r"\s*\*\*\s+?(?P<SongName>[^\*]+)\s+?\*\*\s*"
TempoPattern = r"\s*?\!\s*?\=\s*?(\d\d\d?\.?\d?\d?)\s*?\n"
KeyPattern = r"\s*?\?\s*\=\s*(?P<Key>[ABCDEFGabcdefg][',]?m?)\s*?\n"
SignaturePattern = r"^\s*\<((?P<BeatsPerBar>\d\d?)\/(?P<BeatType>[12348][26]?))\>\s*"


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
    if Sig == []:
        return [4, 4]
    else:
        return [int(Sig[1]), int(Sig[2])]
########################## Pass 2 ########################################

CHORDStringPattern = r"(?P<Chord>\[[1-7][^\]]*\]\-*)"
CHORDRootAndQualityPattern = r"(?P<Root>[1-7]['|,]?)(?P<Quality>[^\]]*)"


def ChordStringGetter(PartsContainsChord):    
    CHORDPartStringPattern = r"\<(?P<Base>[12348][26]?)\*\>(?P<ChordString>[^<$]+)"   # return a tuple ('base', ''StringWithChords)
    pass
#  [["6", "♯", "m"], "7-5", ["3", "♭"],  [1, 0.5]]  # means 6♯m7-5/3♭ (bass on 3,) with 1 bar before and place at 0.5 * bar_length
#    Chord :[
#            Root        -> [ '7' ->  '1~7' ,                                 #-> full size
#            pitch       ->   '♯'|'♭'|'' ,                                       #-> 1/2 size
#            Quality    ->  'm, aug, dim, alt' ]                         #-> 1/2 size
#            Intrval      ->  'sus, sus4, 7, 11, 6, 9, 13' .etc... , #-> 1/3 size
#            Bass        ->['4','♭'] ,                                           #-> 1/2 size bold
#            Position    -> [X, W]                                            #-> X bars after and print at the W * Bar_length (1>W>0)
#            ]
#
