# -*- coding: utf8 -*-
import re
PartSequencePattern = r"\-\>[^\#]+\#"
ChordContentPattern = r"\<\s?(?P<TickBase>\d\d?)\s?\*\>(?P<ChordString>[^$\<]+)"
PartContentPattern  = r"(?P<partname>\S+?):(?P<InstrumentName>\S+?)@\[(?P<Timing>\S+?)\]\{\s+?(?P<PartContent>[^}]+)\}"
SongNamePattern     = r"\s*\*\*\s+?(?P<SongName>[^\*]+)\s+?\*\*\s*"
ReservedInstrumet   = set({'__CHORD__', '__GROOVE__'})
InstrumentSet       = set()
PartSet             = set()



def CommitStripper(str):
    return re.sub(r'#.+(\n|\r|\r\n|\n\r|$)', '',str)

def FormaterStripper(str):
    ''' anything for format shall be trimed here'''
    return str.replace(' ', '').replace('\n', '').replace('|', '').replace('\t', '').replace('\r', '')

def PartContentGetter(inputFile):
    TempList=[]
    ReturnList=[]
    for Match in re.findall(PartContentPattern, inputFile):
        TempList.append(list(Match))
    for everyMatch in TempList:
        everyMatch[3]=CommitStripper(FormaterStripper(everyMatch[3]))
    for Item in TempList:
        ReturnList.append(tuple(Item ))
        InstrumentSet.add(ReturnList[1])
        PartSet.add(ReturnList[0])
    return ReturnList
def PartSequenceGetter(inputFile):
    PartNameList = re.findall(PartSequencePattern, inputFile)[0].split('->')[1:-1]
    for nameStrIndex in range(len(PartNameList)):
        PartNameList[nameStrIndex] = FormaterStripper(PartNameList[nameStrIndex])
    return tuple(PartNameList)

