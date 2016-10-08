# -*- coding: utf8 -*-
import re
########################## Pass 1 ###################################################
MarkupTypePattern   = r"^\:\:(?P<MarkType>\S+)\:\:\s*?$"
PartSequencePattern = r"\-\>[^\#]+\#"
PartContentPattern  = r"(?P<partname>\S+?):(?P<InstrumentName>\S+?)@\[(?P<Timing>\S+?)\]\{\s+?(?P<PartContent>[^}]+)\}"
SongNamePattern     = r"\s*\*\*\s+?(?P<SongName>[^\*]+)\s+?\*\*\s*"
TempoPattern        = r"\s*?\!\s*?\=\s*?(\d\d\d?\.?\d?\d?)\s*?\n"
KeyPattern          = r"\s*?\?\s*\=\s*(?P<Key>[ABCDEFGabcdefg][',]?m?)\s*?\n"
ReservedInstrumet   = set({'CHORD', 'GROOVE'})
InstrumentSet       = set()
PartSet             = set()
Key                 = 'C'       # default key is C
Tempo               = 120.0     # default tempo 120
SongName            = ''        # defult no name
PartsContent        = []
PartNameList        = []
def CommitStripper(str):
    '''
    remove commits
    '''
    return re.sub(r"\/\*[^\*]+\*\/", '',str)

def FormaterStripper(str):
    ''' anything for format shall be trimed here'''
    return str.replace(' ', '').replace('\n', '').replace('|', '').replace('\t', '').replace('\r', '')
def TempoGetter(inputFile):
    return re.findall(TempoPattern, inputFile)[0]

def KeyGetter(inputFile):
    return re.findall(KeyPattern, inputFile)[0] 

def SongNameGetter(inputFile):
    return re.findall(SongNamePattern, inputFile)[0]


def PartContentGetter(inputFile):
    '''
    to collect all the part content and instrument content
    '''
    PartContentList=[]
    for Match in re.findall(PartContentPattern, inputFile):
        Match = list(Match)
        Match[3]=CommitStripper(FormaterStripper(Match[3]))       
        PartContentList.append(Match)
    return PartContentList

def PartSetGetter(PartContentList):
    TempSet=set()
    for Match in PartContentList:
        TempSet.add(Match[0])
    return TempSet

def InstrumentSetGetter(PartContentList):
    TempSet=set()
    for Match in PartContentList:
        TempSet.add(Match[1])
    return TempSet
    
def PartSequenceGetter(inputFile):
    TempList = re.findall(PartSequencePattern, inputFile)[0].split('->')[1:-1]
    for nameStrIndex in range(len(TempList)):
        TempList[nameStrIndex] = FormaterStripper(TempList[nameStrIndex])
    return TempList

########################## Pass 2 ###################################################
RawNoteSeqPattern       = r"\<(?P<Base>[0-7][0-7]?)\*\>(?P<NoteSeq>[^<$]+)"
NoteEventPattern        = r"(?P<NoteEvent>[0-7]['|,]?[\^|_]?[\^|_]?\-*)"
CHORDPartStringPattern  = r"\<(?P<Base>[12348][26]?)\*\>(?P<ChordString>[^<$]+)"
CHORDStringPattern      = r"(?P<Chord>\[[1-7][^\]]*\]\-*)"

def CodeStringGetter(PartContentList):                                                                  
    TempList=[]                                                                                         
    for ListItem in PartContentList:                                                                    
        if ListItem[1] == 'CHORD':
            MatchCHORD   =     re.findall(CHORDPartStringPattern, ListItem[3])[0]                                                            
            TheChordStr  =     MatchCHORD[1]                     
            TheBase      = int(MatchCHORD[0])              
            ChordStrList =[]                                                                            
            for C in re.findall(CHORDStringPattern, TheChordStr):                         
                ChordStrList.append((C.rstrip('-') ,C.count('-')+1 ))                                    
                TempList.append([ListItem[0],                                               
                                [int(ListItem[2].replace('|', '')),                          
                                TheBase ,                                                   
                                tuple(ChordStrList)]]) 
    return dict(TempList)# This make sure every part to be unique 
