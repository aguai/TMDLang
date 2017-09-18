# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x
# compatibility

import re

regex = r"(\<(?P<base>1|2|4|8|16|32)\*\>)(?P<this_Contents>[^\<]+)"

test_str = ("<4*>[1]-[1sus4][1Maj7][3]-\n"
            "	[3sus4][3][4]-[4/2][4][4m]-[6,][7,]\n"
            "<1*>[1]-[1/5]-[1]-[1][1]\n"
            "<16*>[1][1'][2]")

matches = re.finditer(regex, test_str)

for matchNum, match in enumerate(matches):
    matchNum = matchNum + 1

    print("Match {matchNum} was found at {start}-{end}: {match}".format(
        matchNum=matchNum, start=match.start(), end=match.end(), match=match.group()))

    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1

        print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
                                                                        start=match.start(groupNum), end=match.end(groupNum), group=match.group(groupNum)))

# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u""
# to prefix the test string and substitution.
