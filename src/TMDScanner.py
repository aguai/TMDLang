# -*- coding: utf8 -*-
import re
########################## Pass 1 ########################################
PartSequencePattern = r"\-\>([^\#]+)->\#"
PartContentPattern = r"(?P<partname>\S+?):(?P<InstrumentName>\S+?)@\[(?P<Timing>\S+?)\]\{\s+?(?P<PartContent>[^}]+)\}"
SongNamePattern = r"\s*\*\*\s+?(?P<SongName>[^\*]+)\s+?\*\*\s*"
TempoPattern = r"\s*?\!\s*?\=\s*?(\d\d\d?\.?\d?\d?)\s*?\n"
KeyPattern = r"\s*?\?\s*\=\s*(?P<Key>[ABCDEFGabcdefg][',]?m?)\s*?\n"
SignaturePattern = r"^\s*\<((?P<BeatsPerBar>\d\d?)\/(?P<BeatType>[12348][26]?))\>\s*"


def CommitStripper(str):
    '''
    remove commits
    '''
    return re.sub(r"\/\*[^\*]+\*\/", '', str)


def FormaterStripper(str):
    ''' anything for format shall be trimed here'''
    return str.replace(' ', '').replace('\n', '').replace('|', '').replace('\t', '').replace('\r', '')


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
RawNoteSeqPattern = r"\<(?P<Base>[0-7][0-7]?)\*\>(?P<NoteSeq>[^<$]+)"
NoteEventPattern = r"(?P<NoteEvent>[0-7]['|,]?[\^|_]?[\^|_]?\-*)"
CHORDPartStringPattern = r"\<(?P<Base>[12348][26]?)\*\>(?P<ChordString>[^<$]+)"
CHORDStringPattern = r"(?P<Chord>\[[1-7][^\]]*\]\-*)"
CHORDRootAndQualityPattern = r"(?P<Root>[1-7]['|,]?)(?P<Quality>[^\]]*)"


def ChordStringGetter(PartsContent):
    # print('in Scanning Pass 2:\nCodeStringGetter:') #@debug
    # print(PartsContent) #@debug
    for i in PartsContent:
        # print(i[3])
        print(re.findall(CHORDStringPattern, i[3]))

''' #@debug:note
# so that different base notes/chord/events can be written in a same Part Block
In [1]: pat=r"(\<\d\d?\*\>)([^\<]+)"
In [2]: tstr = "<4*>[1]-[1sus4][1maj7][3]-[3sus4][3][4]-[4/2][4][4m]-[6,][7,]<1*>[1]-[1/5]-[1]-[1][1]"
In [3]: re.findall(pat , tstr)
Out[3]:
        [
        ('<4*>', '[1]-[1sus4][1maj7][3]-[3sus4][3][4]-[4/2][4][4m]-[6,][7,]'), 
        ('<1*>', '[1]-[1/5]-[1]-[1][1]')
        ]
'''
# TempList=[]
'''
    for ListItem in PartsContent:
        MatchCHORD   =     re.findall(CHORDPartStringPattern, ListItem[3])[0]
        TheChordStr  =     MatchCHORD[1]
        TheBase      = int(MatchCHORD[0])
        ChordStrList =[]
        for C in re.findall(CHORDStringPattern, TheChordStr):
            ChordStrList.append((re.findall(CHORDRootAndQualityPattern, C.rstrip('-')) ,len(C)- len(C.rstrip('-'))+1))
            TempList.append([ListItem[0],
                            [int(ListItem[2].replace('|', '')),
                            TheBase ,
                            tuple(ChordStrList)]])
    return dict(TempList)# This make sure every part to be unique
'''
