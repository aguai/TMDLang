PartContentRegex = '(?P<partname>\\S+?):(?P<InstrumentName>\\S+?)@(\\||\\[)(?P<Timing>\\S+?)(\\||\\])\\{(\\s+?)(?P<PartContent>[^}]+)\\}'
SongNameRegex = '\\s*\\*\\*\\s+?(?P<SongName>[^\\*]+)\\s+?\\*\\*\\s*'
InstrumentSet=set()
PartSet=set()

def FormaterStripper(str):
    ''' anything for format shall be trimed here'''
    return str.replace(' ', '').replace('\n', '').replace('|', '').replace('\t', '')

