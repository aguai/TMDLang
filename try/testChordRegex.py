# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x
# compatibility

import re

regex = re.compile(
    "\[(?P<Root>[1-7]['|,]?)(?P<Tonic>maj|Maj|aug|dim|m)?(P<Ext>[sus|alt])?(?P<TensionNote>[^\]|^\/]*)?[\/]?(?P<Bass>[1-7][',])?\]")

test_str = "[1sus4][1Maj7][1maj7][1mMaj7][3m][4m][7m7-5][6,7][7,7][7m7][1aug9+13][27/4']"

matches = re.finditer(regex, test_str)

for matchNum, match in enumerate(matches):
    matchNum = matchNum + 1

    print ("Match {matchNum} was found at {start}-{end}: {match}".format(
        matchNum=matchNum, start=match.start(), end=match.end(), match=match.group()))

    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1

        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
                                                                         start=match.start(groupNum), end=match.end(groupNum), group=match.group(groupNum)))

# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u""
# to prefix the test string and substitution.
