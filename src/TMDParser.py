import re
PartContentRegex = r'(?P<partname>\\S+?):(?P<InstrumentName>\\S+?)@(\\||\\[)(?P<Timing>\\S+?)(\\||\\])\\{(\\s+?)(?P<PartContent>[^}]+)\\}'
SongNameRegex = r'\\s*\\*\\*\\s+?(?P<SongName>[^\\*]+)\\s+?\\*\\*\\s*'
InstrumentSet=set()
PartSet=set()

def CommitStripper(str):
    return re.sub(r'#.+(\n|\r|\r\n|\n\r|$)', '',str)

def FormaterStripper(str):
    ''' anything for format shall be trimed here'''
    return str.replace(' ', '').replace('\n', '').replace('|', '').replace('\t', '').replace('\r', '')

