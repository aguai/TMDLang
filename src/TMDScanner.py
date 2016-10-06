# -*- coding: utf8 -*-
import re
########################## Pass 1 ###################################################
MarkupTypePattern   = r"^\:\:(?P<MarkType>\S+)\:\:\s*?$"
PartSequencePattern = r"\-\>[^\#]+\#"
ChordContentPattern = r"\<\s?(?P<TickBase>\d\d?)\s?\*\>(?P<ChordString>[^$\<]+)"
PartContentPattern  = r"(?P<partname>\S+?):(?P<InstrumentName>\S+?)@\[(?P<Timing>\S+?)\]\{\s+?(?P<PartContent>[^}]+)\}"
SongNamePattern     = r"\s*\*\*\s+?(?P<SongName>[^\*]+)\s+?\*\*\s*"
TempoPattern        = r"\s*?\!\s*?\=\s*?(\d\d\d?\.?\d?\d?)\s*?\n"
KeyPattern          = r"\s*?\?\s*\=\s*(?P<Key>[ABCDEFGabcdefg][',]?m?)\s*?\n"
ReservedInstrumet   = set({'__CHORD__', '__GROOVE__'})
InstrumentSet       = set()
PartSet             = set()
Key                 = 'C'       # default key is C
Tempo               = 120.0     # default tempo 120


def CommitStripper(str):
    '''
    remove commits
    '''
    return re.sub(r'#.+(\n|\r|\r\n|\n\r|$)', '',str)

def FormaterStripper(str):
    ''' anything for format shall be trimed here'''
    return str.replace(' ', '').replace('\n', '').replace('|', '').replace('\t', '').replace('\r', '')

def PartContentGetter(inputFile):
    '''
    to collect all the part content and instrument content
    '''
    TempList = re.findall(TempoPattern, inputFile)
    if TempList != []: 
        Tempo = float(TempList[0])

    TempList = re.findall(KeyPattern, inputFile)
    if TempList !=[]:
        Key = TempList[0]
    
    TempList=[]
    for Match in re.findall(PartContentPattern, inputFile):
        Match = list(Match)
        Match[3]=CommitStripper(FormaterStripper(Match[3]))
        InstrumentSet.add(Match[1])
        PartSet.add(Match[0])
        TempList.append(Match)
    return TempList

def PartSequenceGetter(inputFile):
    PartNameList = re.findall(PartSequencePattern, inputFile)[0].split('->')[1:-1]
    for nameStrIndex in range(len(PartNameList)):
        PartNameList[nameStrIndex] = FormaterStripper(PartNameList[nameStrIndex])
    return tuple(PartNameList)

########################## Pass 2 ###################################################
RawNoteSeqPattern   = r"\<(?P<Base>[0-7][0-7]?)\*\>(?P<NoteSeq>[^<$]+)"
NoteEventPattern    = r"(?P<NoteEvent>[0-7]['|,]?[\^|_]?[\^|_]?\-*)"
